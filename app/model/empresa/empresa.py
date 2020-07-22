''' Repository para recuperar informações da CEE '''
from datetime import datetime
import requests
import json
import re
from kafka import KafkaProducer
from flask import current_app
from model.thematic import Thematic
from model.base import BaseModel
from model.empresa.datasets import DatasetsRepository
from repository.empresa.empresa import EmpresaRepository
from repository.empresa.pessoadatasets import PessoaDatasetsRepository

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
            if isinstance(cols.get('cnpj_raiz'), dict) and options.get('perspective') is None and thematic_handler.get_persp_values(df):
                local_result = {}
                for each_persp_key, each_persp_value in thematic_handler.get_persp_values(df).items():
                    local_cols = thematic_handler.decode_column_defs(cols, df, each_persp_key)
                    local_options = self.get_stats_local_options(options, local_cols, df, each_persp_key)
                    if df != 'catweb':
                        local_options["where"].append(f"and")
                        local_options["where"].append(f"eq-{thematic_handler.get_persp_columns(df)}-{each_persp_value}")
                    base_stats = json.loads(thematic_handler.find_dataset(local_options))
                    if df not in result:
                        result[df] = base_stats.get('metadata')
                    if base_stats.get('dataset',[]):
                        local_result[each_persp_key] = base_stats.get('dataset')[0]
                    else: # TODO - How to express no value??
                        print(base_stats.get('dataset'))
                        local_result[each_persp_key] = {'agr_count': 0}
                    local_result[each_persp_key] = {
                        **local_result[each_persp_key],
                        **self.get_grouped_stats(thematic_handler, local_options, cols)
                    }
                result[df]['stats_persp'] = local_result
            else:
                if isinstance(cols.get('cnpj_raiz'), dict):
                    local_cols = thematic_handler.decode_column_defs(local_cols, df, options.get('perspective'))
                local_options = self.get_stats_local_options(options, local_cols, df, options.get('perspective'))
                print(local_options)
                base_stats = json.loads(thematic_handler.find_dataset(local_options))
                result[df] = base_stats.get('metadata')
                
                if base_stats.get('dataset',[]):
                    result[df]["stats"] = base_stats.get('dataset')[0]
                else: # TODO - How to express no value??
                    print(base_stats.get('dataset'))
                    result[df]["stats"] = {'agr_count': 0}

                result[df] = {**result[df], **self.get_grouped_stats(thematic_handler, local_options, cols)}
        return result

    def get_stats_local_options(self, options, local_cols, df, persp):
        ''' Create options according to tables and queriy conditions '''
        subset_rules = [f"eq-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}"]
        # Change initial subset_rules for renavam and aeronaves
        if df == 'cagedsaldo':
            subset_rules = [f"eqlpint-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}-14-0-1-8"]
        elif df == 'rfbsocios': # Some columns are varchar
            subset_rules = [f"eqlponstr-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}-8-0-1-8"]
        elif df == 'rfbparticipacaosocietaria': # Some columns are varchar
            subset_rules = [f"eqlponstr-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}-14-0-1-8"]
        elif df in ['catweb', 'auto']: # Some columns are varchar
            subset_rules = [f"eq-{local_cols.get('cnpj_raiz')}-'{options.get('cnpj_raiz')}'"]
        elif df == 'aeronaves':
            subset_rules = [
                f"eqon-{local_cols.get('cnpj_raiz')}-{options.get('cnpj_raiz')}-1-8",
                "and",
                f"neon-{local_cols.get('cnpj_raiz')}-00000000000000"
            ]
        elif df == 'renavam':
            subset_rules = [
                f"eq-{local_cols.get('cnpj_raiz')}-'{options.get('cnpj_raiz')}'-1-8",
                "and",
                f"eqsz-{local_cols.get('cnpj_raiz')}-14"
            ]
        elif df == 'sisben':        
            subset_rules = [
                f"eq-{local_cols.get('cnpj_raiz')}-'{options.get('cnpj_raiz')}'",
                "and",
                f"ne-{local_cols.get('cnpj')}-'00000000000000'"
            ]
        
        if 'cnpj_raiz_flag' in local_cols:
            subset_rules.append("and")
            subset_rules.append(f"eq-{local_cols.get('cnpj_raiz_flag')}-'1'")

        # Add cnpj filter
        if options.get('cnpj'): 
            subset_rules.append("and")
            subset_rules.append(f"eq-{local_cols.get('cnpj')}-{options.get('cnpj')}")
            if 'cnpj_flag' in local_cols:
                subset_rules.append("and")
                subset_rules.append(f"eq-{local_cols.get('cnpj_flag')}-'1'")

        # Add pf filter
        if options.get('id_pf'): 
            subset_rules.append("and")
            subset_rules.append(f"eq-{local_cols.get('pf')}-{options.get('id_pf')}")

        # Add timeframe filter
        ds_no_compet = ['catweb', 'sisben', 'auto', 'rfb', 'rfbsocios', 'rfbparticipacaosocietaria', 'aeronaves', 'renavam']
        if options.get('column') and df not in ds_no_compet: 
            subset_rules.append("and")
            subset_rules.append(f"eq-{local_cols.get('compet')}-{options.get('column')}")

        if df == 'rais':
            subset_rules.append("and")
            subset_rules.append(f"eq-tp_estab-1")
        elif df == 'auto':
            subset_rules.append("and")
            subset_rules.append(f"eq-tpinscricao-'1'")
            subset_rules.append("and")
            subset_rules.append(f"nl-dtcancelamento")
            subset_rules.append("and")
            subset_rules.append(f"gestr-{local_cols.get('compet')}-\'{options.get('column')}\-01\-01\'-1-10")
            subset_rules.append("and")
            subset_rules.append(f"lestr-{local_cols.get('compet')}-\'{options.get('column')}\-12\-31\'-1-10")
        elif df == 'catweb':
            subset_rules.append("and")
            subset_rules.append(f"ge-{local_cols.get('compet')}-\'{options.get('column')}0101\'")
            subset_rules.append("and")
            subset_rules.append(f"le-{local_cols.get('compet')}-\'{options.get('column')}1231\'")
        elif df in ['caged', 'cagedsaldo', 'cagedtrabalhador', 'cagedtrabalhadorano']:
            subset_rules.append("and")
            subset_rules.append(f"eq-tipo_estab-1")
        
        if df == 'cagedsaldo':
            return {
                "categorias": ['\'1\'-pos'],
                "valor": ['qtd_admissoes','qtd_desligamentos','saldo_mov'],
                "agregacao": ['count'],
                "where": subset_rules,
                "theme": df
            }
        elif df in ['rfb','rfbsocios','rfbparticipacaosocietaria']:
            return {
                "categorias": ['\'1\'-pos'],
                "agregacao": ['count'],
                "where": subset_rules,
                "theme": df
            }

        return {
            "categorias": [local_cols.get('cnpj_raiz')],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": df
        }    

    @staticmethod
    def get_grouped_stats(thematic_handler, options, cols):
        ''' Get stats for dataframe partitions '''
        # TODO 2 - Remove .0 from compet grouping
        result = {}        

        options['as_pandas'] = True
        options['no_wrap'] = True

        # Get statistics partitioning by unit
        if 'cnpj' not in cols: # Ignores datasources with no cnpj definition
            options["categorias"] = [cols.get('cnpj')]
            options["ordenacao"] = [cols.get('cnpj')]
            result["stats_estab"] = json.loads(
                thematic_handler.find_dataset(options).set_index(cols.get('cnpj')).to_json(orient="index")
            )

        # Get statistics partitioning by timeframe
        ds_no_compet = ['catweb', 'sisben', 'auto', 'rfb', 'rfbsocios', 'rfbparticipacaosocietaria', 'aeronaves', 'renavam']
        if 'compet' in cols and options.get('theme') not in ds_no_compet: # Ignores datasources with no timeframe definition
            options["categorias"] = [cols.get('compet')]
            options["ordenacao"] = [f"-{cols.get('compet')}"]
            result["stats_compet"] = json.loads(
                thematic_handler.find_dataset(options).set_index(cols.get('compet')).to_json(orient="index")
            )
        
            # Get statistics partitioning by unit and timeframe
            options["categorias"] = [cols.get('cnpj'), cols.get('compet')]
            options["ordenacao"] = [f"-{cols.get('compet')}"]
            df_local_result = thematic_handler.find_dataset(options)
            df_local_result['idx'] = df_local_result[cols.get('compet')].apply(str) + \
                '_' + df_local_result[cols.get('cnpj')].apply(str)
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