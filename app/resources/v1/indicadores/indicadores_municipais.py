''' Controller para fornecer dados da CEE '''
from flask import request, Response
from flask_restful_swagger_2 import swagger
from resources.base import BaseResource
from model.indicadores.indicadores_municipais import IndicadoresMunicipais

class IndicadoresMunicipaisResource(BaseResource):
    ''' Classe de múltiplos Indicadores Municipais '''
    CUSTOM_SWAGGER_PARAMS = [
        {"name": "categorias", "required": True, "type": 'string', "in": "query",
         "description": "Informações que devem ser trazidas no dataset. \
            Campos disponíveis: cd_mun_ibge, cd_dimensao, \
            cd_divisao_territorial, cd_indicador, nm_indicador, \
            ds_indicador, ds_indicador_completo, ds_indicador_radical, \
            ds_indicador_prefixo, ds_indicador_curto, ds_agreg_primaria, \
            ds_agreg_secundaria, nu_competencia, nu_competencia_min, \
            nu_competencia_max, tp_competencia, ds_fonte, vl_indicador, \
            vl_indicador_uf, vl_indicador_br, rank_br, rank_br_total, \
            pct_br, rank_uf, rank_uf_total, media_uf, pct_uf, \
            vl_indicador_min_br, vl_indicador_max_br, \
            vl_indicador_min_uf, vl_indicador_max_uf, \
            cd_municipio_ibge_dv, cd_municipio_ibge, nm_municipio, \
            nm_municipio_sem_acento, cd_uf, latitude, longitude, \
            nm_uf, sg_uf, nm_municipio_uf, cd_unidade, cd_prt, nm_prt, \
            nm_unidade, tp_unidade, sg_unidade, cd_mesorregiao, \
            nm_mesorregiao, cd_microrregiao, nm_microrregiao, \
            cd_regiao e nm_regiao. \
            Para renomear campos do dataset de retorno, após o campo de \
            consulta, adicionar o novo nome, separado por '-' (ex: \
            campo-campo_novo)."}
    ]

    def __init__(self):
        ''' Construtor'''
        self.domain = IndicadoresMunicipais()

    @swagger.doc({
        'tags':['indicadores_municipais'],
        'description':'Obtém todos os indicadores municipais, de acordo com os \
        parâmetros informados',
        'parameters': CUSTOM_SWAGGER_PARAMS + BaseResource.DEFAULT_SWAGGER_PARAMS,
        'responses': {
            '200': {'description': 'Indicadores Municipais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores municipais, conforme parâmetros informados '''
        options = self.build_options(request.args)
        return self.__get_domain().find_dataset(options)

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = IndicadoresMunicipais()
        return self.domain

class IndicadoresMunicipaisChartResource(BaseResource):
    ''' Classe de múltiplos Indicadores Municipais '''
    def __init__(self):
        ''' Construtor'''
        self.domain = IndicadoresMunicipais()

    @swagger.doc({
        'tags':['indicadores_municipais'],
        'description':'Obtém todos os indicadores municipais, de acordo com os \
        parâmetros informados',
        'parameters':[
        ],
        'responses': {
            '200': {'description': 'Indicadores Municipais'}
        }
    })
    def get(self):
        ''' Obtém os registros de indicadores municipais, conforme parâmetros informados '''
        # TODO Após testes, remover fake_options, retornadno a construção do options
        #      usando request.args
        fake_options = {
            "categorias": 'cd_mun_ibge,nu_competencia',
            "valor": 'vl_indicador',
            "filtros": "eq-nu_competencia-'2010',and,eq-cd_indicador-'06_02_03_03'"
        }
        options = self.build_options(fake_options)
        return Response(self.__get_domain().load_chart(options), mimetype='text/html')

    def __get_domain(self):
        ''' Carrega o modelo de domínio, se não o encontrar '''
        if self.domain is None:
            self.domain = IndicadoresMunicipais()
        return self.domain
