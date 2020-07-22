''' Repository para recuperar informações de uma empresa '''
import json
from repository.base import HBaseRepository

#pylint: disable=R0903
class EmpresaRepository(HBaseRepository):
    ''' Definição do repo '''
    TABLE = 'sue'
    SIMPLE_COLUMNS = {}

    def find_datasets(self, options):
        ''' Localiza um município pelo código do IBGE '''
        if 'cnpj_raiz' in options and options['cnpj_raiz'] is not None:
            result = self.find_row(
                'empresa',
                options['cnpj_raiz'],
                options.get('column_family'),
                options.get('column')
            )
            
            # Result splitting according to perspectives
            nu_results = {}
            for ds_key in result:
                if not result[ds_key].empty and ds_key in self.PERSP_COLUMNS:
                    for nu_persp_key, nu_persp_val in self.PERSP_VALUES[ds_key].items():
                        if options.get('perspective', nu_persp_key) == nu_persp_key:
                            nu_key = ds_key + "_" + nu_persp_key
                            nu_results[nu_key] = result[ds_key][
                                result[ds_key][self.PERSP_COLUMNS[ds_key]] == nu_persp_val
                            ]
            result = {**result, **nu_results}

            for ds_key in result:
                col_cnpj_name = 'cnpj'
                if ds_key in self.CNPJ_COLUMNS:
                    col_cnpj_name = self.CNPJ_COLUMNS[ds_key]
                col_pf_name = None
                if ds_key in self.PF_COLUMNS:
                    col_pf_name = self.PF_COLUMNS[ds_key]

                if not result[ds_key].empty:
                    result[ds_key] = self.filter_by_person(
                        result[ds_key], options, col_cnpj_name, col_pf_name
                    )

                # Redução de dimensionalidade (simplified)
                if not result[ds_key].empty and options.get('simplified'):
                    list_dimred = ['nu_cnpj_cei', 'nu_cpf', 'col_compet']
                    if ds_key in self.SIMPLE_COLUMNS:
                        list_dimred = self.SIMPLE_COLUMNS[ds_key]
                        # Garantir que col_compet sempre estará na lista
                        if 'col_compet' not in list_dimred:
                            list_dimred.append('col_compet')
                    result[ds_key] = result[ds_key][list_dimred]

                # Captura de metadados
                
                # Conversão dos datasets em json
                result[ds_key] = json.loads(result[ds_key].to_json(orient="records"))

            return result

    @staticmethod
    def filter_by_person(dataframe, options, col_cnpj_name, col_pf_name):
        ''' Filter dataframe by person identification, according to options data '''
        cnpj = options.get('cnpj')
        id_pf = options.get('id_pf')
        # Filtrar cnpj e id_pf nos datasets pandas
        if cnpj is not None and id_pf is not None and col_pf_name is not None:
            if dataframe[col_cnpj_name].dtype == 'int64':
                cnpj = int(cnpj)
            if dataframe[col_pf_name].dtype == 'int64':
                id_pf = int(id_pf)
            dataframe = dataframe[
                (dataframe[col_cnpj_name] == cnpj) & (dataframe[col_pf_name] == id_pf)
            ]
        # Filtrar apenas cnpj nos datasets pandas
        elif cnpj is not None:
            if dataframe[col_cnpj_name].dtype == 'int64':
                cnpj = int(cnpj)
            dataframe = dataframe[dataframe[col_cnpj_name] == cnpj]
        # Filtrar apenas id_pf nos datasets pandas
        elif (id_pf is not None and col_pf_name is not None):
            if dataframe[col_pf_name].dtype == 'int64':
                id_pf = int(id_pf)
            dataframe = dataframe[dataframe[col_pf_name] == id_pf]
        return dataframe
