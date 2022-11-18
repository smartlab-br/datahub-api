""" Repository para recuperar informações de uma empresa """
import json
from pandas.api.types import is_string_dtype
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
            'empresa',
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
                persp_col = self.PERSP_COLUMNS[ds_key]
                table_cols = self.get_column_defs(ds_key)
                for nu_persp_key, nu_persp_val in self.PERSP_VALUES[ds_key].items(): 
                    persp_option = options.get('perspective', nu_persp_key)
                    if persp_option == nu_persp_key: 
                        nu_key = ds_key + "_" + nu_persp_key 
                        if persp_col in table_cols:
                            table_persp_cols = table_cols[persp_col][persp_option]
                            result[nu_key] = dataframe[ds_key][
                                (dataframe[ds_key][table_persp_cols['column']] == options.get(persp_col)) &
                                (dataframe[ds_key][table_persp_cols['flag']] == '1')
                            ]
                        else:
                            result[nu_key] = dataframe[ds_key][ 
                                dataframe[ds_key][persp_col] == nu_persp_val 
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
            if is_string_dtype(result[col_cnpj_name]):
                result = result[result[col_cnpj_name].str.lstrip("0") == cnpj.lstrip("0")]
            else:
                result = result[result[col_cnpj_name] == cnpj]

        # Filtrar apenas id_pf nos datasets pandas
        id_pf = options.get('id_pf')
        if id_pf is not None and col_pf_name is not None:
            if result[col_pf_name].dtype == 'int64':
                id_pf = int(id_pf)
            if is_string_dtype(result[col_pf_name]):
                result = result[result[col_pf_name].str.lstrip("0") == id_pf.lstrip("0")]
            else:
                result = result[result[col_pf_name] == id_pf]
        return result
