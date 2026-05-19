"""
Standalone script to measure connection time for each datasource:
impala, redis, hbase, and rabbit.

Reads the same environment variables used by the app.
Run with: python probe_connections.py
"""

import os
import subprocess
import time
import ssl
from datetime import datetime


def check_klist():
    """Parse and display the current Kerberos TGT status from the ticket cache."""
    cache = os.environ.get("KRB5CCNAME", "")
    cmd = ["klist"] + (["-c", cache] if cache else [])
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        lines = out.stdout.strip().splitlines()
    except Exception as exc:
        print(f"[klist] ERROR: {exc}\n")
        return

    principal, valid_from, expires, renew_until = "-", "-", "-", "-"
    for line in lines:
        if line.startswith("Default principal:"):
            principal = line.split(":", 1)[1].strip()
        # ticket lines: "MM/DD/YY HH:MM:SS  MM/DD/YY HH:MM:SS  service"
        if "krbtgt/" in line:
            parts = line.split()
            if len(parts) >= 5:
                valid_from = f"{parts[0]} {parts[1]}"
                expires = f"{parts[2]} {parts[3]}"
        if "renew until" in line:
            parts = line.split()
            if len(parts) >= 3:
                renew_until = f"{parts[2]} {parts[3]}"

    now = datetime.now()
    try:
        exp_dt = datetime.strptime(expires, "%m/%d/%y %H:%M:%S")
        time_left = exp_dt - now
        hours, rem = divmod(int(time_left.total_seconds()), 3600)
        minutes = rem // 60
        ttl_str = f"{hours}h {minutes}m" if time_left.total_seconds() > 0 else "EXPIRED"
    except ValueError:
        ttl_str = "unknown"

    print("[Kerberos TGT]")
    print(f"  Principal  : {principal}")
    print(f"  Valid from : {valid_from}")
    print(f"  Expires    : {expires}  (TTL: {ttl_str})")
    print(f"  Renew until: {renew_until}")
    print()


def probe_impala():
    from impala.dbapi import connect
    import kerberos

    host = os.environ["IMPALA_HOST"]
    port = int(os.environ["IMPALA_PORT"])

    # Pre-fetch the Kerberos service ticket so we can time the KDC round-trip
    # separately from the actual TCP/SSL connection.
    # After authGSSClientStep the ticket is cached, so connect() reuses it.
    impala_service = f"impala/{host}@MPT.INTRA"
    t0 = time.perf_counter()
    __, krb_context = kerberos.authGSSClientInit(impala_service)
    kerberos.authGSSClientStep(krb_context, "")
    t1 = time.perf_counter()
    krb_elapsed = t1 - t0

    conn = connect(
        host=host,
        database="spai",
        port=port,
        kerberos_service_name="impala",
        auth_mechanism="GSSAPI",
        use_ssl=True,
    )
    conn_elapsed = time.perf_counter() - t1
    conn.close()
    return {"impala (krb)": krb_elapsed, "impala (conn)": conn_elapsed - krb_elapsed}


def probe_redis():
    import redis

    host = os.environ["REDIS_HOST"]
    port = int(os.environ["REDIS_PORT"])
    db = int(os.environ["REDIS_DB"])

    start = time.perf_counter()
    r = redis.Redis(host=host, port=port, db=db)
    r.ping()
    elapsed = time.perf_counter() - start
    return elapsed


def probe_hbase():
    import kerberos
    from thrift.transport import THttpClient
    from thrift.protocol import TBinaryProtocol
    from hbase import Hbase

    host = os.environ["HBASE_HOST"]
    port = os.environ["HBASE_PORT"]

    hbase_service = f"HTTP/{host}@MPT.INTRA"
    ssl._create_default_https_context = ssl._create_unverified_context

    t0 = time.perf_counter()
    __, krb_context = kerberos.authGSSClientInit(hbase_service)
    kerberos.authGSSClientStep(krb_context, "")
    negotiate_details = kerberos.authGSSClientResponse(krb_context)
    t1 = time.perf_counter()
    krb_elapsed = t1 - t0

    headers = {
        "Authorization": "Negotiate " + negotiate_details,
        "Content-Type": "application/binary",
    }
    http_client = THttpClient.THttpClient(f"https://{host}:{port}/")
    http_client.setCustomHeaders(headers=headers)
    protocol = TBinaryProtocol.TBinaryProtocol(http_client)
    http_client.open()
    Hbase.Client(protocol)
    http_client.close()
    conn_elapsed = time.perf_counter() - t1

    return {"hbase (krb)": krb_elapsed, "hbase (conn)": conn_elapsed}


def probe_rabbit():
    import pika

    host = os.environ["RABBIT_HOST"]
    port = int(os.environ["RABBIT_PORT"])
    user = os.environ["RABBIT_USER"]
    password = os.environ["RABBIT_PASSWORD"]
    env = os.environ.get("RABBIT_ENV", "stg")
    vhost = f"/suetonio/{env}"

    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, port, vhost, credentials)

    start = time.perf_counter()
    conn = pika.BlockingConnection(parameters)
    conn.close()
    elapsed = time.perf_counter() - start
    return elapsed


PROBES = {
    "impala": probe_impala,
    "redis": probe_redis,
    "hbase": probe_hbase,
    "rabbit": probe_rabbit,
}

if __name__ == "__main__":
    check_klist()
    print(f"{'Service':<14}  {'Status':<8}  {'Time (s)':>10}  {'Error'}")
    print("-" * 70)

    for name, fn in PROBES.items():
        try:
            result = fn()
            if isinstance(result, dict):
                for sub_name, elapsed in result.items():
                    print(f"{sub_name:<14}  {'OK':<8}  {elapsed:>10.3f}")
            else:
                print(f"{name:<14}  {'OK':<8}  {result:>10.3f}")
        except Exception as exc:
            print(f"{name:<14}  {'FAILED':<8}  {'N/A':>10}  {exc}")
