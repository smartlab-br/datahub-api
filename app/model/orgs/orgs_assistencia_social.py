''' Repository para recuperar informações das organizações de assistência social '''
from model.base import BaseModel
from repository.orgs.orgs_assistencia_social import OrgsAssistenciaSocialRepository

#pylint: disable=R0903
class OrgsAssistenciaSocial(BaseModel):
    ''' Definição do repo '''
    METADATA = {
        'fonte': 'Censo SUAS(Sistema Único de Assistência social)', 'link': ''
    }

    def __init__(self):
        ''' Construtor '''
        self.repo = OrgsAssistenciaSocialRepository()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = OrgsAssistenciaSocialRepository()
        return self.repo
