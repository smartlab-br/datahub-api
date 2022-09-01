""" Repository para recuperar informações de uma empresa """
import json
from flask import current_app
from repository.base import HBaseRepository

#pylint: disable=R0903
class EmpresaRepository(HBaseRepository):
    """ Definição do repo """
    TABLE = 'sue'
    SIMPLE_COLUMNS = {}

    def load_repo_configs(self):
        """ Load repository definitions """

    def find_datasets(self, options):
        """ Localiza um município pelo código do IBGE """
        if options is None or options.get('cnpj_raiz') is None:
            return None

        result = self.find_row(
            f'{current_app.config["HBASE_DATABASE"]}:empresa',
            options['cnpj_raiz'],
            options.get('column_family'),
            options.get('column')
        )

        # Result splitting according to perspectives
        result = {**result, **self.split_dataframe_by_perspective(result, options)}

        for ds_key in result:
            col_cnpj_name = self.CNPJ_COLUMNS.get(ds_key, 'cnpj')
            col_pf_name = self.PF_COLUMNS.get(ds_key)

            if not result[ds_key].empty:
                result[ds_key] = self.filter_by_person(
                    result[ds_key], options, col_cnpj_name, col_pf_name
                )

            # Redução de dimensionalidade (simplified)
            if not result[ds_key].empty and options.get('simplified'):
                list_dimred = self.SIMPLE_COLUMNS.get(
                    ds_key, ['nu_cnpj_cei', 'nu_cpf', 'col_compet']
                )
                # Garantir que col_compet sempre estará na lista
                if 'col_compet' not in list_dimred:
                    list_dimred.append('col_compet')
                result[ds_key] = result[ds_key][list_dimred]

            # Conversão dos datasets em json
            result[ds_key] = result[ds_key].to_dict(orient="records")
        return result

    def split_dataframe_by_perspective(self, dataframe, options):
        """ Splits a dataframe by perpectives """
        result = {}
        if dataframe is None:
            return result    
        for ds_key in dataframe:
            if not dataframe[ds_key].empty and ds_key in self.PERSP_COLUMNS:
                for nu_persp_key, nu_persp_val in self.PERSP_VALUES[ds_key].items():
                    if options.get('perspective', nu_persp_key) == nu_persp_key:
                        nu_key = ds_key + "_" + nu_persp_key
                        result[nu_key] = dataframe[ds_key][
                            dataframe[ds_key][self.PERSP_COLUMNS[ds_key]] == nu_persp_val
                        ]
        return result

    @staticmethod
    def filter_by_person(dataframe, options, col_cnpj_name, col_pf_name):
        """ Filter dataframe by person identification, according to options data """
        if dataframe is None or options is None:
            return None
        result = dataframe.copy()

        # Filtrar apenas cnpj nos datasets pandas
        cnpj = options.get('cnpj')
        if col_cnpj_name is None:
            col_cnpj_name = 'cnpj'
        if cnpj is not None and col_cnpj_name is not None:
            if result[col_cnpj_name].dtype == 'int64':
                cnpj = int(cnpj)
            result = result[result[col_cnpj_name] == cnpj]

        # Filtrar apenas id_pf nos datasets pandas
        id_pf = options.get('id_pf')
        if id_pf is not None and col_pf_name is not None:
            if result[col_pf_name].dtype == 'int64':
                id_pf = int(id_pf)
            result = result[result[col_pf_name] == id_pf]
        return result
