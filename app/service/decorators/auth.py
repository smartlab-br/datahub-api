from functools import wraps
from flask import abort, request
from flask import current_app as app
import requests


def authenticate(**kwargs):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kws):
            if 'Authorization' not in request.headers:
                abort(401)

            user = None
            token = request.headers['Authorization'].replace('Bearer ', '')
            domain = kwargs.get('domain')
            auth_config = app.config['AUTH_GATEWAYS'].get(domain)
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
            introspect = introspect_resp.json()
            if introspect.get('active', False):
                user = introspect.get('username')

            def track_event(tracker_config, event_user, tracker_options=None):
                if tracker_options is None:  # No tracker
                    return
                if 'GA_ID' in tracker_config:  # Uses GA to track events
                    additional_parameters = {}
                    for param_key, param_value in tracker_options.get('additional_parameters', {}).items():
                        if param_value == "query":
                            additional_parameters[param_key] = request.args.copy().to_dict(flat=False).get(param_key)
                        elif param_value == "path":
                            additional_parameters[param_key] = request.view_args[param_key]
                    data = {
                        **{
                            'v': '1',  # API Version.
                            'tid': tracker_config.get('AU_ID'),  # Tracking ID / Property ID.
                            # Anonymous Client Identifier. Ideally, this should be a UUID that
                            # is associated with particular user, device, or browser instance.
                            'cid': 555,
                            't': 'event',  # Event hit type.
                            'ec': tracker_options.get('category'),  # Event category.
                            'ea': tracker_options.get('action'),  # Event action.
                            'el': tracker_options.get('label'),  # Event label.
                            'uid': event_user
                        },
                        **additional_parameters
                    }

                    tracking_resp = requests.post('https://www.google-analytics.com/collect', data=data, verify=False)
                    tracking_resp.raise_for_status()

            try:
                track_event(
                    app.config['EVENT_TRACKERS'].get(kwargs.get('domain')),
                    user,
                    kwargs.get('event_tracker_options')
                )
            except:
                abort(500)  # Failed to track event

            if user is None:
                abort(401)

            return f(*args, **kws)
        return decorated_function
    return decorator
