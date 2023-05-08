''' Repository para recuperar informações da CEE '''
from datetime import datetime
import json
import re
import requests
from flask import current_app
from datasources import send_rabbit_message
from model.thematic import Thematic
from model.base import BaseModel
from model.empresa.datasets import DatasetsRepository
from repository.empresa.empresa import EmpresaRepository
from repository.empresa.pessoadatasets import PessoaDatasetsRepository
from factory.source import SourceFactory

#pylint: disable=R0903
class Empresa(BaseModel):
    ''' Definição do repo '''
    TOPICS = [
        'rais', 'rfb', 'sisben', 'catweb', 'auto', 'caged', 'rfbsocios',
        'rfbparticipacaosocietaria', 'aeronaves', 'renavam', 'cagedsaldo',
        'cagedtrabalhador', 'cagedtrabalhadorano', 'embarcacoes'
    ]

    def __init__(self):
        ''' Construtor '''
        self.repo = None
        self.dataset_repo = None
        self.pessoa_dataset_repo = None
        self.thematic_handler = None
        self.__set_repo()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = EmpresaRepository()
        return self.repo

    def get_dataset_repo(self):
        if self.dataset_repo is None:
            self.dataset_repo = DatasetsRepository()
        return self.dataset_repo

    def get_pessoa_dataset_repo(self):
        if self.pessoa_dataset_repo is None:
            self.pessoa_dataset_repo = PessoaDatasetsRepository()
        return self.pessoa_dataset_repo

    def get_thematic_handler(self):
        ''' Gets single instance of Thematic model to delegate query execution '''
        if self.thematic_handler is None:
            self.thematic_handler = Thematic()
        return self.thematic_handler

    def __set_repo(self):
        ''' Setter invoked in Construtor '''
        self.repo = EmpresaRepository()

    def find_datasets(self, options):
        ''' Localiza um todos os datasets de uma empresa pelo CNPJ Raiz '''
        dict_datasets = self.get_dataset_repo().retrieve()
        loading_entry_is_valid = self.is_valid_loading_entry(options['cnpj_raiz'], options, dict_datasets)
        (loading_entry, column_status) = self.get_loading_entry(options['cnpj_raiz'], options, dict_datasets)
        result = {}
        try:
            metadata = self.get_statistics(options)
            result['metadata'] = metadata
            if 'only_meta' in options and options['only_meta']:
                result['dataset'] = []
            else:
                dataset = self.get_repo().find_datasets(options)
                result['dataset'] = dataset
        except requests.exceptions.HTTPError:
            loading_entry_is_valid = False
        if not loading_entry_is_valid:
            result['invalid'] = True
            self.produce(
                options['cnpj_raiz'],
                options.get('column_family'),
                options.get('column'),
                dict_datasets
            )
            if 'INGESTING' in column_status:
                (loading_entry, column_status) = self.get_loading_entry(options['cnpj_raiz'], options, dict_datasets)
        if 'column' in options:
            result['status_competencia'] = column_status
        result['status'] = loading_entry
        return result

    def produce(self, cnpj_raiz, column_family, column, dict_datasets):
        redis_dao = PessoaDatasetsRepository()
        ds_dict = dict_datasets

        if column_family is None:
            for topic in self.TOPICS:
                # First, updates status on REDIS
                redis_dao.store_status(cnpj_raiz, topic, ds_dict[topic].split(','))
                # Then build RabbitMQ message
                for comp in ds_dict[topic].split(','):
                    msg = bytes(f'{cnpj_raiz}:{comp}', 'utf-8')
                    send_rabbit_message('suetonio',topic, msg)
        else:
            if column is None:
                # First, updates status on REDIS
                redis_dao.store_status(cnpj_raiz, column_family, ds_dict[column_family].split(','))
                # Then build RabbitMQ message
                for comp in ds_dict[column_family].split(','):
                    msg = bytes(f'{cnpj_raiz}:{comp}', 'utf-8')
                    send_rabbit_message('suetonio',column_family, msg)
            else:
                # First, updates status on REDIS
                redis_dao.store_status(cnpj_raiz, column_family, [column])
                # Then build RabbitMQ message
                msg = bytes(f'{cnpj_raiz}:{column}', 'utf-8')
                send_rabbit_message('suetonio',column_family, msg)

    def get_loading_entry(self, cnpj_raiz, options=None, dict_datasets=None):
        ''' Verifica se há uma entrada ainda válida para ingestão de dados da empresa '''
        loading_entry = {}
        column_status = None
        column_status_specific = None
        for dataframe, slot_list in dict_datasets.items():
            rev_theme = dataframe
            if rev_theme in ["catweb_c", "sisben_c"]:
                rev_theme = rev_theme[:-2]
            columns_available = self.get_pessoa_dataset_repo().retrieve(cnpj_raiz, rev_theme)
            if options is not None:
                theme = options.get('column_family', dataframe)
                if theme in ["catweb", "sisben"]:
                    theme = f"{theme}_c"
            if (options is not None and 'column_family' in options and
                    theme == dataframe and
                    'column' in options):
                column_status = self.assess_column_status(
                    slot_list.split(','),
                    columns_available,
                    options.get('column')
                )
                column_status_specific = column_status
            if columns_available:
                loading_entry[dataframe] = columns_available

        # Overrides if there's a specific column status
        if column_status_specific is not None:
            column_status = column_status_specific

        return (loading_entry, column_status)

    def is_valid_loading_entry(self, cnpj_raiz, options=None, dict_datasets=None):
        ''' Checks if a loading entry is valid '''
        rules = dict_datasets
        if options is None:
            raise ValueError('Dataset inválido')
        cf = options.get('column_family')
        if cf in ['catweb', 'sisben']:
            cf = f"{cf}_c"
        if not cf or not rules.get(cf):
            raise ValueError('Dataset inválido')
        if options.get('column') and options.get('column') not in rules.get((cf)).split(','):
            raise ValueError('Competência inválida para o dataset informado')
        for dataframe, slot_list in rules.items():
            columns_available = self.get_pessoa_dataset_repo().retrieve(cnpj_raiz, dataframe)
            if options.get('column_family', dataframe) == dataframe:
                # Aquela entrada já existe no REDIS (foi carregada)?
                # A entrada é compatível com o rol de datasources?
                # A entrada tem menos de 1 mês?
                # A entrada tem menos de 2 min que está em processo de ingestão?
                if (columns_available is None or
                        options.get('column') not in columns_available):
                    return False
                if any(
                    [
                        options.get('column', col_key) == col_key and
                            'INGESTED' in col_val and len(col_val.split('|')) > 1 and
                            (datetime.now() - 
                                datetime.strptime(col_val.split('|')[1], "%Y-%m-%d")
                            ).days > 30
                        for
                        col_key, col_val
                        in
                        columns_available.items()
                    ]):
                    return False
                if any(
                    [
                        options.get('column', col_key) == col_key and
                            'INGESTING' in col_val and len(col_val.split('|')) > 1 and
                            (datetime.now() - 
                                datetime.strptime(col_val.split('|')[1], "%Y-%m-%d %H:%M:%S")
                            ).seconds > 120
                        for
                        col_key, col_val
                        in
                        columns_available.items()
                    ]):
                    return False
        return True

    @staticmethod
    def assess_column_status(slot_list, columns_available, column):
        ''' Checks the status of a defined column '''
        if columns_available is None:
            columns_available = {}
        if column in slot_list:
            if column in columns_available.keys():
                return columns_available[column]
            return 'MISSING'
        if (column in columns_available.keys() and
                'INGESTED' in columns_available[column]):
            return 'DEPRECATED'
        return 'UNAVAILABLE'

    def get_statistics(self, options):
        ''' Gets statistics for a company using impala '''
        if options.get('column_family'):
            dataframes = [options.get('column_family')]
        else:
            dataframes = self.TOPICS

        # Autos and Catweb need a timeframe to filter
        if ('column' not in options and 
                any([dataframe in ['auto', 'catweb'] for dataframe in dataframes])):
            raise AttributeError(f'Fontes de dados demandam uma competência')

        result = {}
        for dataframe in dataframes:
            # Get statistics for dataset
            cols = self.get_thematic_handler().get_column_defs(dataframe)

            # If the dataset doesn't have a unique column to identify a company
            perspectives = self.get_thematic_handler().get_persp_values(
                dataframe, options.get('perspective')
            )
            
            if perspectives: # If the source demands a perspective or one is provided in options
                local_result = {}

                for each_persp_key in perspectives:
                    local_cols = self.get_thematic_handler().decode_column_defs(
                        cols, each_persp_key
                    )
                    local_result[each_persp_key] = self.get_statistics_from_perspective(
                        dataframe,
                        each_persp_key,
                        local_cols,
                        self.get_stats_local_options(
                            options,
                            local_cols,
                            dataframe,
                            each_persp_key
                        ),
                        options
                    )

                result[dataframe] = {'stats_persp': local_result}
            else:
                result[dataframe] = self.get_statistics_from_perspective(
                    dataframe,
                    None,
                    cols,
                    self.get_stats_local_options(options, cols, dataframe, None),
                    options
                )
        return result

    def get_statistics_from_perspective(self, dataframe, each_persp_value, local_cols, local_options, options):
        ''' Gets statistics from a specific given persoective, when a datasource
            has multiple column lookup rules '''
        if dataframe not in ['catweb', 'catweb_c'] and each_persp_value is not None:
            local_options["where"].extend([
                f"and",
                f"eq-{self.get_thematic_handler().get_persp_columns(dataframe)}-{each_persp_value}"
            ])

        base_stats = self.get_thematic_handler().find_dataset({
            **local_options,
            **{'as_pandas': False, 'no_wrap': False}
        })

        result = {}
        if each_persp_value is None:
            result = base_stats.get('metadata')
        if base_stats.get('dataset', []):
            result["stats"] = base_stats.get('dataset')[0]
        else:
            result["stats"] = self.build_empty_stats(
                local_options,
                local_cols,
                options
            )

        return {
            **result,
            **self.get_grouped_stats(options, local_options, local_cols)
        }

    @staticmethod
    def get_stats_local_options(options, local_cols, dataframe, persp):
        ''' Create options according to tables and queriy conditions '''
        return SourceFactory.create(dataframe).get_options_empresa(
            options, local_cols, dataframe, persp
        )

    def get_grouped_stats(self, original_options, options, cols):
        ''' Get stats for dataframe partitions '''
        result = {}

        options['as_pandas'] = True
        options['no_wrap'] = True

        # Get statistics partitioning by unit
        stats_unit = self.get_thematic_handler().find_dataset({
            **options,
            **{
                "categorias": [cols.get('cnpj', 'cnpj')],
                "ordenacao": [cols.get('cnpj', 'cnpj')]
            }
        })

        if cols.get('cnpj', 'cnpj') in stats_unit.columns:
            result["stats_estab"] = stats_unit.set_index(
                cols.get('cnpj', 'cnpj')).to_dict(orient="index")

        # Get statistics partitioning by timeframe
        ds_no_compet = [
            'sisben', 'sisben_c', 'auto', 'rfb', 'rfbsocios',
            'rfbparticipacaosocietaria', 'aeronaves', 'renavam', 'embarcacoes'
        ]
        ds_displaced_compet = ['catweb', 'catweb_c']

        # Ignores datasources with no timeframe definition
        if options.get('theme') not in ds_no_compet:
            # Get statistics partitioning by timeframe
            compet_attrib = 'compet' # Single timeframe, no need to group
            if 'compet' in cols and options.get('theme') not in ds_displaced_compet:
                # Changes lookup for tables with timeframe values
                compet_attrib = cols.get('compet')
                current_df = self.get_thematic_handler().find_dataset({
                    **options,
                    **{
                        "categorias": [compet_attrib],
                        "ordenacao":[f"-{compet_attrib}"]
                    }
                })
            else:
                current_df = self.get_thematic_handler().find_dataset({
                    **options,
                    **{
                        "categorias": [f"\'{original_options.get('column')}\'-compet"],
                        "ordenacao": ["-compet"]
                    }
                })

            current_df[compet_attrib] = current_df[compet_attrib].apply(str).replace(
                {'\.0': ''}, regex=True
            )
            result["stats_compet"] = current_df.set_index(compet_attrib).to_dict(orient="index")

            # Get statistics partitioning by timeframe and units
            if 'compet' in cols and options.get('theme') not in ds_displaced_compet:
                # Changes lookup for tables with timeframe values
                df_local_result = self.get_thematic_handler().find_dataset({
                    **options,
                    **{"categorias": [cols.get('cnpj'), compet_attrib]}
                })
            else:
                df_local_result = self.get_thematic_handler().find_dataset({
                    **options,
                    **{
                        "categorias": [cols.get('cnpj'),
                        f"\'{original_options.get('column')}\'-compet"]
                    }
                })

            df_local_result['idx'] = df_local_result[compet_attrib].apply(str).replace(
                {'\.0': ''}, regex=True) + '_' + \
                df_local_result[cols.get('cnpj', 'cnpj')].apply(str).replace({'\.0': ''}, regex=True)
            result["stats_estab_compet"] = df_local_result.set_index('idx').to_dict(orient="index")

        ## RETIRADO pois a granularidade torna imviável a performance
        # metadata['stats_pf'] = dataframe[
        #     [col_pf_name, 'col_compet']
        # ].groupby(col_pf_name).describe(include='all')

        ## RETIRADO pois a granularidade torna inviável a performance
        # metadata['stats_pf_compet'] = dataframe[
        #     [col_pf_name, 'col_compet']
        # ].groupby(
        #     ['col_compet', col_cnpj_name]
        # ).describe(include='all')

        return result

    @staticmethod
    def build_empty_stats(options, cols, original_options):
        ''' Builds a structure to denote no aggregate data
            found in the datalake '''
        result = {f"{cols.get('cnpj_raiz')}": f"{original_options.get('cnpj_raiz')}"}
        if 'valor' in options:
            for val in options.get('valor', []):
                for agr in options.get('agregacao', []):
                    result[f"agr_{agr}_{val}"] = 0
        else:
            for agr in options.get('agregacao', []):
                result[f"agr_{agr}"] = 0
        return result
