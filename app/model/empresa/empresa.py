''' Repository para recuperar informações da CEE '''
from datetime import datetime
import json
import re
import requests
from kafka import KafkaProducer
from flask import current_app
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
        'cagedtrabalhador', 'cagedtrabalhadorano'
    ]

    def __init__(self):
        ''' Construtor '''
        self.repo = None
        self.__set_repo()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = EmpresaRepository()
        return self.repo

    def __set_repo(self):
        ''' Setter invoked in Construtor '''
        self.repo = EmpresaRepository()

    def find_datasets(self, options):
        ''' Localiza um todos os datasets de uma empresa pelo CNPJ Raiz '''
        (loading_entry, loading_entry_is_valid, column_status) = self.get_loading_entry(
            options['cnpj_raiz'],
            options
        )
        result = {'status': loading_entry}
        try:
            dataset = self.get_repo().find_datasets(options)
            metadata = self.get_statistics(options)
            result['metadata'] = metadata
            if 'only_meta' in options and options['only_meta']:
                result['dataset'] = []
            else:
                result['dataset'] = dataset
        except requests.exceptions.HTTPError:
            loading_entry_is_valid = False
            self.produce(
                options['cnpj_raiz'],
                options.get('column_family'),
                options.get('column')
            )
        if not loading_entry_is_valid:
            result['invalid'] = True
        if 'column' in options:
            result['status_competencia'] = column_status
        return result

    def produce(self, cnpj_raiz, column_family, column):
        ''' Gera uma entrada na fila para ingestão de dados da empresa '''
        kafka_server = f'{current_app.config["KAFKA_HOST"]}:{current_app.config["KAFKA_PORT"]}'
        producer = KafkaProducer(bootstrap_servers=[kafka_server])
        redis_dao = PessoaDatasetsRepository()
        ds_dict = DatasetsRepository().DATASETS

        if column_family is None:
            for topic in self.TOPICS:
                # First, updates status on REDIS
                redis_dao.store_status(cnpj_raiz, topic, ds_dict[topic].split(','))
                # Then publishes to Kafka
                for comp in ds_dict[topic].split(','):
                    t_name = f'{current_app.config["KAFKA_TOPIC_PREFIX"]}-{topic}'
                    msg = bytes(f'{cnpj_raiz}:{comp}', 'utf-8')
                    producer.send(t_name, msg)
        else:
            if column is None:
                # First, updates status on REDIS
                redis_dao.store_status(cnpj_raiz, column_family, ds_dict[column_family].split(','))
                # Then publishes to Kafka
                for comp in ds_dict[column_family].split(','):
                    t_name = f'{current_app.config["KAFKA_TOPIC_PREFIX"]}-{column_family}'
                    msg = bytes(f'{cnpj_raiz}:{comp}', 'utf-8')
                    producer.send(t_name, msg)
            else:
                # First, updates status on REDIS
                redis_dao.store_status(cnpj_raiz, column_family, [column])
                t_name = f'{current_app.config["KAFKA_TOPIC_PREFIX"]}-{column_family}'
                msg = bytes(f'{cnpj_raiz}:{column}', 'utf-8')
                producer.send(t_name, msg)
        producer.close()

    def get_loading_entry(self, cnpj_raiz, options=None):
        ''' Verifica se há uma entrada ainda válida para ingestão de dados da empresa '''
        rules_dao = DatasetsRepository()
        if (not options.get('column_family') or
                not rules_dao.DATASETS.get((options.get('column_family')))):
            raise ValueError('Dataset inválido')
        if (options.get('column') and
                options.get('column') not in rules_dao.DATASETS.get((options.get('column_family'))).split(',')):
            raise ValueError('Competência inválida para o dataset informado')
        loading_status_dao = PessoaDatasetsRepository()
        is_valid = True
        loading_entry = {}
        column_status = 'INGESTED'
        column_status_specific = None
        for dataframe, slot_list in rules_dao.DATASETS.items():
            columns_available = loading_status_dao.retrieve(cnpj_raiz, dataframe)
            if options.get('column_family', dataframe) == dataframe:
                # Aquela entrada já existe no REDIS (foi carregada)?
                # A entrada é compatível com o rol de datasources?
                # A entrada tem menos de 1 mês?
                if (columns_available is None or
                        any([slot not in columns_available.keys() for slot in slot_list.split(',')])):
                    is_valid = False
                else:
                    for col_key, col_val in columns_available.items():
                        if (options.get('column', col_key) == col_key and
                                'INGESTED' in col_val and
                                len(col_val.split('|')) > 1 and
                                (datetime.strptime(col_val.split('|')[1], "%Y-%m-%d") - datetime.now()).days > 30):
                            is_valid = False

                if 'column' in options:
                    column_status = self.assess_column_status(
                        slot_list.split(','),
                        columns_available,
                        options.get('column')
                    )
                    if options.get('column_family') == dataframe:
                        column_status_specific = column_status
            if columns_available:
                loading_entry[dataframe] = columns_available

        # Overrides if there's a specific column status
        if column_status_specific is not None:
            column_status = column_status_specific

        return (loading_entry, is_valid, column_status)

    @staticmethod
    def assess_column_status(slot_list, columns_available, column):
        ''' Checks the status of a defined column '''
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
            dataframes = self.TOPICS # TODO 1 - Check if tables and topics names match

        # TODO 99 - Add threads to run impala queries
        result = {}
        thematic_handler = Thematic()
        for df in dataframes:
            # Get statistics for dataset
            cols = thematic_handler.get_column_defs(df)
            local_cols = cols.copy()

            # Autos and Catweb need a timeframe to filter
            if df in ['auto', 'catweb'] and 'column' not in options:
                raise AttributeError(f'{df} demanda uma competência')

            # If the dataset doesn't have a unique column to identify a company
            if isinstance(cols.get('cnpj_raiz'), dict) and thematic_handler.get_persp_values(df):    
                local_result = {}

                perspectives = thematic_handler.get_persp_values(df)
                if options.get('perspective'):
                    perspectives = {k: v for k, v in perspectives.items() if k == options.get('perspective')}

                for each_persp_key, each_persp_value in perspectives.items():
                    local_cols = thematic_handler.decode_column_defs(cols, df, each_persp_key)
                    local_options = self.get_stats_local_options(
                        options,
                        local_cols,
                        df,
                        each_persp_key
                    )
                    print(local_options)
                    if df != 'catweb':
                        local_options["where"].extend([
                            f"and",
                            f"eq-{thematic_handler.get_persp_columns(df)}-{each_persp_value}"
                        ])
                    base_stats = thematic_handler.find_dataset(local_options)

                    if df not in result:
                        result[df] = base_stats.get('metadata')
                    if base_stats.get('dataset', []):
                        local_result[each_persp_key] = base_stats.get('dataset')[0]
                    else:
                        local_result[each_persp_key] = self.build_empty_stats(
                            local_options,
                            local_cols,
                            options
                        )

                    local_result[each_persp_key] = {
                        **local_result[each_persp_key],
                        **self.get_grouped_stats(thematic_handler, options, local_options, local_cols)
                    }
            else:
                if isinstance(cols.get('cnpj_raiz'), dict):
                    local_cols = thematic_handler.decode_column_defs(
                        local_cols,
                        df,
                        options.get('perspective')
                    )
                local_options = self.get_stats_local_options(
                    options,
                    local_cols,
                    df,
                    options.get('perspective')
                )
                print(local_options)
                base_stats = thematic_handler.find_dataset(local_options)
                result[df] = base_stats.get('metadata')
                
                if base_stats.get('dataset',[]):
                    result[df]["stats"] = base_stats.get('dataset')[0]
                else:
                    result[df]["stats"] = self.build_empty_stats(local_options, local_cols, options)

                result[df] = {
                    **result[df],
                    **self.get_grouped_stats(thematic_handler, options, local_options, cols)
                }

        return result

    def get_stats_local_options(self, options, local_cols, df, persp):
        ''' Create options according to tables and queriy conditions '''
        return SourceFactory.create(df).get_options_empresa(
            options, local_cols, df, persp
        )

    @staticmethod
    def get_grouped_stats(thematic_handler, original_options, options, cols):
        ''' Get stats for dataframe partitions '''
        result = {}

        options['as_pandas'] = True
        options['no_wrap'] = True

        # Get statistics partitioning by unit
        if 'cnpj' not in cols: # Ignores datasources with no cnpj definition
            result["stats_estab"] = json.loads(
                thematic_handler.find_dataset({
                    **options,
                    **{
                        "categorias": [cols.get('cnpj')],
                        "ordenacao": [cols.get('cnpj')]
                    }
                }).set_index(cols.get('cnpj')).to_json(orient="index")
            )

        # Get statistics partitioning by timeframe
        ds_no_compet = [
            'sisben', 'sisben_c', 'auto', 'rfb', 'rfbsocios',
            'rfbparticipacaosocietaria', 'aeronaves', 'renavam'
        ]
        ds_displaced_compet = ['catweb', 'catweb_c']

        # Ignores datasources with no timeframe definition
        if options.get('theme') not in ds_no_compet:
            # Get statistics partitioning by timeframe
            compet_attrib = 'compet' # Single timeframe, no need to group
            if 'compet' in cols and options.get('theme') not in ds_displaced_compet: # Changes lookup for tables with timeframe values
                compet_attrib = cols.get('compet')
                current_df = thematic_handler.find_dataset({
                    **options,
                    **{
                        "categorias": [compet_attrib],
                        "ordenacao":[f"-{compet_attrib}"]
                    }
                })
            else:
                current_df = thematic_handler.find_dataset({
                    **options,
                    **{
                        "categorias": [f"\'{original_options.get('column')}\'-compet"],
                        "ordenacao": ["-compet"]
                    }
                })
                
            current_df[compet_attrib] = current_df[compet_attrib].apply(str).replace(
                {'\.0': ''}, regex=True
            )
            result["stats_compet"] = json.loads(
                current_df.set_index(compet_attrib).to_json(orient="index")
            )

            # Get statistics partitioning by timeframe and units
            if 'compet' in cols and options.get('theme') not in ds_displaced_compet: # Changes lookup for tables with timeframe values
                df_local_result = thematic_handler.find_dataset({
                    **options,
                    **{"categorias": [cols.get('cnpj'), compet_attrib]}
                })
            else:
                df_local_result = thematic_handler.find_dataset({
                    **options,
                    **{"categorias": [cols.get('cnpj'), f"\'{original_options.get('column')}\'-compet"]}
                })
            
            df_local_result['idx'] = df_local_result[compet_attrib].apply(str).replace(
                {'\.0': ''}, regex=True) + '_' + \
                df_local_result[cols.get('cnpj')].apply(str).replace({'\.0': ''}, regex=True)
            result["stats_estab_compet"] = json.loads(
                df_local_result.set_index('idx').to_json(orient="index")
            )
            
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
        result = {f"{cols.get('cnpj_raiz')}": f"{original_options.get('cnpj_raiz')}"}
        if 'valor' in options:
            for val in options.get('valor', []):
                for agr in options.get('agregacao', []):
                    result[f"agr_{agr}_{val}"] = 0
        else:
            for agr in options.get('agregacao', []):
                result[f"agr_{agr}"] = 0
        return result
