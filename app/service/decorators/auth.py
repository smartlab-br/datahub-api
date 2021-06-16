from functools import wraps
from flask import abort, request
from flask import current_app as app
import requests
import json


def authenticate(**kwargs):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kws):
            if 'Authorization' not in request.headers:
                abort(401)

            user = None
            error_message = None

            token = request.headers['Authorization'].replace('Bearer ', '')
            domain = kwargs.get('domain')
            auth_config = app.config['AUTH_GATEWAYS'].get(domain)


            try:
                introspect_resp = requests.post(
                    f"{auth_config.get('BASE_URL')}/oauth/introspect",
                    data=f"token={token}",
                    verify=False,
                    headers={
                        'Cache-Control': 'no-cache',
                        'Accept': 'application/json',
                        'Authorization': f"Basic {auth_config.get('CLIENT_SECRET')}",
                        'Content-Type': 'application/x-www-form-urlencoded',
                        "Host": auth_config.get('LOCAL')
                    }
                )
                introspect_resp.raise_for_status()

                introspect = introspect_resp.json()
                if introspect.get('active', False):
                    user = introspect.get('username')
            except:
                error_message = "Falha ao validar token no gerenciador de identidades"

            def track_event(domain, tracker_config, event_user, tracker_options=None, error_message=None):
                if tracker_options is None:  # No tracker
                    return
                if 'GA_ID' in tracker_config:  # Uses GA to track events
                    additional_parameters = {}
                    if error_message is not None:
                        additional_parameters['error_message'] = error_message
                    for param_key, param_value in tracker_options.get('additional_parameters', {}).items():
                        if param_value == "query":
                            param = request.args.copy().to_dict(flat=False).get(param_key)
                            if isinstance(param, list):
                                additional_parameters[param_key] = ", ".join(param)
                            else:
                                additional_parameters[param_key] = param
                        elif param_value == "path":
                            additional_parameters[param_key] = str(request.view_args[param_key])
                    username = event_user
                    if event_user is None:
                        username = '@anonymous'
                    data = {
                        "client_id": domain,
                        "non_personalized_ads": False,
                        "events": [
                            {
                                "name": tracker_config.get("EV_NAME"),
                                "params": {
                                    **{
                                        'category': tracker_options.get('category'),
                                        'action': tracker_options.get('action'),
                                        'item': tracker_options.get('item'),
                                        "username": username
                                    },
                                    **additional_parameters
                                }
                            }
                        ],
                        "user_properties": {"username": {"value": username}}
                    }
                    url = f"https://www.google-analytics.com/mp/collect?measurement_id={tracker_config.get('EV_ID')}&api_secret={tracker_config.get('EV_SECRET')}"

                    tracking_resp = requests.post(
                        url, data=json.dumps(data), verify=False,
                        headers={"Host": "www.google-analytics.com"}
                    )
                    tracking_resp.raise_for_status()

            try:
                track_event(
                    kwargs.get('domain'),
                    app.config['EVENT_TRACKERS'].get(kwargs.get('domain')),
                    user,
                    kwargs.get('event_tracker_options'),
                    error_message
                )
            except:
                abort(500, {"origin": "Analytics", "message": "Falha ao registrar evento"})  # Failed to track event

            if user is None:
                abort(401, {"origin": "Access Manager", "message": error_message})

            return f(*args, **kws)
        return decorated_function
    return decorator
