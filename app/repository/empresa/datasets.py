''' Repository para recuperar informações de uma empresa '''
from repository.base import RedisRepository


#pylint: disable=R0903
class DatasetsRepository(RedisRepository):
    ''' Definição do repo '''
    REDIS_KEY = 'rx:ds'

    # TODO Na migração para configmap no k8s essa conf deve ser adicionada no configmap
    # DATASETS_COMPETENCIA = current_app.config["CONF_REPO_DATASETS_COMPETENCIA"]
    # DATASETS_COMPETENCIA = {
    #     "auto": "DISTINCT ano",
    #     "caged": "DISTINCT competencia_declarada",
    #     "cagedano": "DISTINCT ano",
    #     "cagedsaldo": "DISTINCT competencia_mov",
    #     "cagedtrabalhador": "DISTINCT competencia_mov",
    #     "cagedtrabalhadorano": "DISTINCT ano_declarado",
    #     "rais": "DISTINCT nu_ano_rais",
    #     "catweb_c": "DISTINCT ano",
    #     "catweb": "DISTINCT ano_cat",
    #     "rfb": "MAX dt_carga",
    #     "sisben_c": "DISTINCT nu_ano_compet",
    #     "sisben": "DISTINCT ano_beneficio",
    #     "rfbsocios": "MAX dt_carga",
    #     "rfbparticipacaosocietaria": "MAX dt_carga",
    #     "renavam": "MAX dt_carga",
    #     "aeronaves": "MAX dt_carga",
    #     "embarcacoes": "MAX dt_carga"
    # }

    def retrieve(self):
        ''' Localiza o dicionário de datasources no REDIS '''
        return self.retrieve_hashset(self.REDIS_KEY)

    def store(self, datasets):
        ''' Inclui/atualiza dicionário de competências e datasources no REDIS '''
        self.get_dao().hmset(self.REDIS_KEY, datasets)
        return datasets
