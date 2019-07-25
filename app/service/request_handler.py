''' Request handlers and related utilities '''
from werkzeug.serving import WSGIRequestHandler, _log
import colors # pip3 install ansicolors
from collections.abc import Iterable

class FLPORequestHandler(WSGIRequestHandler):
    ''' Request Handler to override WSGI's '''
    # Just like WSGIRequestHandler, but without "- -"
    def log(self, _type, message, *args):
        ''' Silences some endpoints '''
        silent_endpoints = ["/hcalive", "/static", "/favicon.ico"]
        if (type(args[1]) is str or not isinstance(args[1], Iterable) or (
                not any(slnt in args[1] for slnt in silent_endpoints) and
                args[1] != '/')):
            if len(args) >= 5:
                log_params = [
                    ('host', self.address_string(), 'red'),
                    ('time', self.log_date_time_string(), 'magenta'),
                    ('method', args[0], 'blue'),
                    ('path', args[1], 'blue'),
                    ('protocol', args[2], 'blue'),
                    ('status', args[3], 'yellow'),
                    ('size', args[4], 'blue')
                ]

                # Standard log layout
                # 127.0.0.1 - - [15/Mar/2019 12:02:23] "POST /mail HTTP/1.1" 504 -
                template = '%s - - [%s] ' + message + '\n'
            else:
                log_params = [
                    ('host', self.address_string(), 'red'),
                    ('time', self.log_date_time_string(), 'magenta'),
                    ('status', args[0], 'yellow'),
                    ('msg', args[1], 'blue')
                ]

                # Standard log layout
                # 127.0.0.1 - - [15/Mar/2019 12:02:23] Mensagem de erro
                template = '%s - - [%s] "%s" %s\n'

            parts = []
            for _name, value, color in log_params:
                part = colors.color(str(value), fg=color)
                parts.append(part)

            content = template % tuple(parts)
            _log(_type, content)

    # Just like WSGIRequestHandler, but without "code"
    def log_request(self, code='-', size='-'):
        # Standard log message
        # "POST /mail HTTP/1.1" 504 -
        l_args = self.requestline.split(" ")
        l_args.append(code)
        l_args.append(size)
        self.log('info', '"%s %s %s" %s %s', *l_args)
