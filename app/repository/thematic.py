""" Repository para recuperar informações da CEE """
from repository.base import ImpalaRepository
from flask import current_app

#pylint: disable=R0903
class ThematicRepository(ImpalaRepository):
    """ Definição do repo """

    def __init__(self):
        """ Constructor """
        super().__init__()  # Invokes the parent constructor, bringing default config values
        self.load_repo_configs()

    def load_repo_configs(self):
        """ Load repository definitions """
        self.TABLE_NAMES = current_app.config["CONF_REPO_THEMATIC"].get("TABLE_NAMES")
        self.DEFAULT_PARTITIONING = current_app.config["CONF_REPO_THEMATIC"].get("DEFAULT_PARTITIONING")
        self.ON_JOIN = current_app.config["CONF_REPO_THEMATIC"].get("ON_JOIN")
        self.JOIN_SUFFIXES = current_app.config["CONF_REPO_THEMATIC"].get("JOIN_SUFFIXES")

    def get_default_partitioning(self, options):
        """ Gets default partitioning from thematic datasets' definition """
        if options is None:
            return getattr(self, 'DEFAULT_PARTITIONING', {}).get('MAIN')
        if 'theme' not in options:
            return getattr(self, 'DEFAULT_PARTITIONING', {}).get('MAIN')
        if options.get('theme') in getattr(self, 'DEFAULT_PARTITIONING', {}):
            return getattr(self, 'DEFAULT_PARTITIONING', {}).get(options.get('theme'))
        if options.get('theme') in getattr(self, 'DEFAULT_PARTITIONING', {}).get('NONE'):
            return ''
        return getattr(self, 'DEFAULT_PARTITIONING', {}).get('MAIN')
