''' WSGI Initializer '''
import logging
from main import application
from service.request_handler import FLPORequestHandler

if __name__ == "__main__":
    logging.basicConfig(filename='werkzeug.log', level=logging.INFO)
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.INFO)
    application.run(request_handler=FLPORequestHandler)
