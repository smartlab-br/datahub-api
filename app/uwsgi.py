''' WSGI Initializer '''
import logging
from main import application
from service.request_handler import FLPORequestHandler

if __name__ == "__main__":
    logging.basicConfig(filename='werkzeug.log', level=logging.INFO)
    LOGGER = logging.getLogger('werkzeug')
    LOGGER.setLevel(logging.INFO)
    application.run(request_handler=FLPORequestHandler)
