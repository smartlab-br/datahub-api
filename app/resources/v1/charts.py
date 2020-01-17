''' Controller para fornecer dados da CEE '''
from flask import request, Response
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.thematic import Thematic

import matplotlib.pyplot as plt
import io
from flask import send_file

class ChartsResource(BaseResource):
    ''' Classe de múltiplos Indicadores Municipais '''
    def __init__(self):
        ''' Construtor'''
        self.domain = Thematic()

    def get(self):
        ''' Obtém os registros do dataset temático, conforme parâmetros informados '''
        # options = self.build_options(request.args)
        # options['theme'] = theme
        # return self.__get_domain().find_dataset(options)
        f, ax = plt.subplots(figsize=(11, 9))

        circle1 = plt.Circle((0, 0), 0.2, color='r')
        circle2 = plt.Circle((0.5, 0.5), 0.2, color='blue')
        circle3 = plt.Circle((1, 1), 0.2, color='g', clip_on=False)
        
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        ax.add_artist(circle3)
        
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)

        return send_file(bytes_image, attachment_filename="chart.png", mimetype="image/png")

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = Thematic()
        return self.domain
