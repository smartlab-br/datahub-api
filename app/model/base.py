''' Base Model '''
import json
import requests
import yaml
import numpy as np
import pandas as pd

from flask import current_app as app
from service.number_formatter import NumberFormatter
from service.qry_options_builder import QueryOptionsBuilder
from service.pandas_operator import PandasOperator

#pylint: disable=R0903
class BaseModel():
    ''' Definição do repo '''
    METADATA = {}

    def find_dataset(self, options=None):
        ''' Obtém todos, sem tratamento '''
        result = self.get_repo().find_dataset(options)
        if options['pivot'] is not None:
            if options['calcs'] is not None and options['calcs']:
                nu_val = 'api_calc_' + options['calcs'][0]
            elif options['valor'] is None:
                nu_val = self.get_repo().get_agr_string(options['agregacao'][0], '*').split()[-1]
            else:
                nu_val = self.get_repo().get_agr_string(
                    options['agregacao'][0], options['valor'][0]
                ).split()[-1]
            result = pd.DataFrame(result)
            result = pd.pivot_table(
                result, values=[nu_val],
                columns=options['pivot'],
                index=options['categorias'],
                aggfunc=self.convert_aggr_to_np(
                    options['agregacao'],
                    [nu_val]
                )
            )

            if not result.empty:
                result.columns = result.columns.droplevel()
                result.reset_index(level=result.index.names, inplace=True)

        if options is not None and 'no_wrap' in options.keys() and options['no_wrap']:
            return result
        return self.wrap_result(result, options)

    def find_joined_dataset(self, options=None):
        ''' Obtém todos, sem tratamento '''
        return self.wrap_result(self.get_repo().find_joined_dataset(options))

    def wrap_result(self, dataset=None, options=None):
        ''' Adiciona metadados à resposta '''
        if dataset is None:
            return None
        if options is not None:
            if 'as_pandas' in options and options['as_pandas']:
                return {
                    "metadata": self.fetch_metadata(options),
                    "dataset": dataset
                }
            if 'as_dict' in options and options['as_dict']:
                return {
                    "metadata": self.fetch_metadata(options),
                    "dataset": dataset.to_dict('records')
                }
        return f'{{ \
            "metadata": {json.dumps(self.fetch_metadata(options))}, \
            "dataset": {dataset.to_json(orient="records")} \
            }}'

    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        raise NotImplementedError("Models precisam implementar get_repo")

    def fetch_metadata(self, options=None):
        ''' Método abstrato para carregamento do dataset '''
        return self.METADATA

    def convert_aggr_to_np(self, aggrs, vals):
        ''' Método que converte um conjunto de agregações em um dictionary
            para usar no pandas para pivotar '''
        if isinstance(aggrs, list):
            result = {}
            for indx, aggr in enumerate(aggrs):
                result[vals[indx]] = self.aggr_to_np(aggr)
            return result
        return self.aggr_to_np(aggrs)

    @staticmethod
    def aggr_to_np(aggr):
        ''' Método que obtém a função de agregação correspondente para
            aplicar no pandas para pivotar '''
        if aggr is None:
            return np.mean
        if aggr.upper() == 'SUM' or aggr.upper() == 'COUNT':
            return np.sum
        return np.mean

    def get_template(self, cd_template, options):
        ''' Gets and fills a template '''
        # Gets a template from git
        location = app.config['GIT_VIEWCONF_BASE_URL'].format(
            'br/cards', options['datasource'], cd_template
        )
        struct = yaml.load(requests.get(location, verify=False).content)

        data_collection = {}
        any_nodata = False
        # Fetches data collection from impala
        if 'api_obj_collection' in struct:
            (data_collection, any_nodata) = self.get_template_data_collection(
                struct['api_obj_collection'],
                options
            )
        # Adds query params as fixed data in the collection
        if 'coefficient' in options:
            data_collection = {**data_collection, **self.get_coefficients(options['coefficient'])}
        if 'term' in options:
            data_collection = {**data_collection, **self.get_terms(options['term'])}
        # Removes data_collection definition from yaml
        del struct['api_obj_collection']

        # Interpolate the structure with data
        final_struct = self.templates_to_fixed(struct, data_collection, any_nodata)

        # Adds chart datasets
        if 'chart_data' in struct:
            if isinstance(struct['chart_data'], list):
                final_struct['chart_data'] = []
                for each_dataset in struct['chart_data']:
                    final_struct['chart_data'].append(data_collection[each_dataset])
            else:
                final_struct['chart_data'] = data_collection[struct['chart_data']]

        # Returns the filled structure
        return final_struct

    def get_template_data_collection(self, structure, options):
        ''' Fetches data from impala '''
        data_collection = {}
        any_nodata = False
        for each_obj_struct in structure:
            each_options = self.remove_templates(each_obj_struct['endpoint'], options)

            # Adds complimentary options
            each_options = QueryOptionsBuilder.build_options(each_options)
            each_options["as_pandas"] = True

            # Builds the options to query impala
            each_obj = self.find_dataset(each_options)

            # Transforms the dataset with coefficient
            if 'coefficient' in options:
                each_obj = self.apply_coefficient(options['coefficient'], each_obj)

            # Runs formatters from config
            if 'formatters' in each_obj_struct:
                each_obj = self.run_formatters(each_obj_struct['formatters'], each_obj)

            # Gets derived attributes
            any_blank = False
            if 'instances' in each_obj_struct:
                (data_collection, any_blank) = self.build_derivatives(
                    each_obj_struct,
                    options,
                    each_obj,
                    data_collection
                )
            if any_blank:
                any_nodata = True

            # Converts pandas dataframe to conventional dict, to add to response
            each_obj['dataset'] = each_obj['dataset'].to_dict('records')
            data_collection[each_obj_struct['name']] = each_obj
        return (data_collection, any_nodata)

    def remove_templates(self, struct, base_object):
        ''' Transforms templates into simple string '''
        for each_arg_key, each_arg in struct.items():
            if isinstance(each_arg, list):
                nu_list = []
                for each_item in each_arg:
                    nu_list.append(self.remove_templates(each_item, base_object))
                struct[each_arg_key] = nu_list
            elif isinstance(each_arg, dict):
                if 'template' in each_arg:
                    # Gets only the fixed value of the resulting template substitution
                    struct[each_arg_key] = self.replace_template_arg(each_arg, base_object)['fixed']
                else:
                    struct[each_arg_key] = self.remove_templates(each_arg, base_object)

        return struct

    def templates_to_fixed(self, struct, data_collection, any_nodata=False):
        ''' Transforms templates into fixed attribute '''
        if isinstance(struct, dict) and 'named_prop' in struct:
            return self.replace_named_prop(struct, data_collection)
        for each_arg_key, each_arg in struct.items():
            if any_nodata and each_arg_key == 'description':
                struct[each_arg_key] = [{
                    "type": "text",
                    "title": "",
                    "content": {
                        "fixed": struct['msgNoData']['desc']
                    }
                }]
            elif isinstance(each_arg, list):
                struct[each_arg_key] = [self.templates_to_fixed(each_item, data_collection) for each_item in each_arg]
            elif isinstance(each_arg, dict):
                if 'template' in each_arg:
                    each_arg = self.replace_template_arg(each_arg, data_collection)
                elif 'named_prop' in each_arg:
                    # Replaces the named_prop
                    each_arg = self.replace_named_prop(each_arg, data_collection)
                else:
                    struct[each_arg_key] = self.templates_to_fixed(each_arg, data_collection)
        return struct

    @staticmethod
    def get_formatted_value(structure, data_collection):
        ''' Gets the formatted value '''
        if (structure['base_object'] in data_collection and
                data_collection[structure['base_object']] is not None):
            fmt_arg = data_collection[structure['base_object']][structure['named_prop']]
            if 'format' in structure:
                fmt_arg = NumberFormatter.format(fmt_arg, structure)
            return fmt_arg
        return "N/D"

    @staticmethod
    def run_formatters(each_obj_struct, each_obj):
        ''' Runs formatters from config '''
        for each_fmt in each_obj_struct:
            args = {'format': each_fmt['format']}
            if 'precision' in each_fmt:
                args['precision'] = each_fmt['precision']
            if 'multiplier' in each_fmt:
                args['multiplier'] = int(each_fmt['multiplier'])
            else:
                args['multiplier'] = 1
            if 'collapse' in each_fmt:
                args['collapse'] = each_fmt['collapse']
            else:
                args['collapse'] = None
            if 'default' in each_fmt:
                args['default'] = each_fmt['default']

            # Creates formatted column by applying number format method
            # in the declared named_prop
            each_obj['dataset'][each_fmt['prop']] = [NumberFormatter.format(row[each_fmt['named_prop']], args) for index, row in each_obj['dataset'].iterrows()]
        return each_obj

    @staticmethod
    def apply_coefficient(str_coefficients, each_obj):
        ''' Applies the given coefficients to the values in the dataset '''
        coefficients = str_coefficients.split(',')
        for coefficient in coefficients:
            coefficient_parts = coefficient.split("-")
            if coefficient_parts[0] in each_obj['dataset']:
                each_obj['dataset'][coefficient_parts[0]] = each_obj['dataset'][coefficient_parts[0]] * float(coefficient_parts[1])
        return each_obj

    @staticmethod
    def get_coefficients(str_coefficients):
        ''' Adds coefficients passed in the request to the structure '''
        coefficients = str_coefficients.split(',')
        coefficient_values = {}
        for coefficient in coefficients:
            coefficient_parts = coefficient.split("-")
            coefficient_id = 'coef_' + coefficient_parts[0]
            coefficient_values[coefficient_id] = {
                "value": float(coefficient_parts[1]),
                "label": coefficient_parts[2]
            }
        return coefficient_values

    @staticmethod
    def get_terms(str_terms):
        ''' Adds terms passed in the request to the structure '''
        terms = str_terms.split(',')
        term_values = {}
        for term in terms:
            term_parts = term.split("-")
            term_id = 'term_' + term_parts[0]
            term_values[term_id] = {
                "value": term_parts[1]
            }
        return term_values

    @classmethod
    def build_derivatives(cls, each_obj_struct, options, each_obj, data_collection):
        ''' Gets derivetive attributes from configs '''
        any_nodata = False
        for each_inst in each_obj_struct['instances']:
            try:
                data_collection[each_inst['name']] = cls.get_collection_from_type(each_obj['dataset'], each_inst['type'], each_inst['named_prop'], options['cd_analysis_unit'])
            except:
                data_collection[each_inst['name']] = None
                any_nodata = True
            if each_inst['name'] not in data_collection:
                data_collection[each_inst['name']] = None
                any_nodata = True
        return (data_collection, any_nodata)

    @staticmethod
    def get_collection_from_type(dataset, inst_type, named_prop=None, id_au=None):
        ''' Use pandas filter to set a collection '''
        if inst_type == 'from_id':
            return dataset.loc[dataset[named_prop] == int(id_au)].iloc[0]
        if inst_type == 'first_occurence':
            return dataset.reset_index().loc[0]
        if inst_type == 'min':
            if dataset[named_prop].dtype == 'object':
                return dataset.loc[dataset[named_prop] == dataset[named_prop].min()].iloc[0]
            return dataset.loc[dataset[named_prop].idxmin()]
        if inst_type == 'max':
            if dataset[named_prop].dtype == 'object':
                return dataset.loc[dataset[named_prop] == dataset[named_prop].max()].iloc[0]
            return dataset.loc[dataset[named_prop].idxmax()]
        return None

    def replace_named_prop(self, struct, data_collection):
        ''' Replaces the named_prop according to confs '''
        struct['fixed'] = self.get_formatted_value(struct, data_collection)
        # Cleans the structure
        del struct['base_object']
        del struct['named_prop']
        if 'format' in struct:
            del struct['format']
        if 'precision' in struct:
            del struct['precision']
        if 'multiplier' in struct:
            del struct['multiplier']
        if 'collapse' in struct:
            del struct['collapse']
        if 'uiTags' in struct:
            del struct['uiTags']
        # Returns the cleaned and formatted structure
        return struct

    def replace_template_arg(self, struct, data_collection):
        ''' Replaces the template for a fixed structure or just replaces
            its arguments, according to attribute keep_template '''
        # Gets base arguments from base object
        base_args = []
        kept_args = 0
        for each_rep in struct['args']:
            if 'as_is' in each_rep and each_rep['as_is']:
                base_args.append('{{{}}}'.format(kept_args))
                kept_args = kept_args + 1
            elif 'fixed' in each_rep:
                base_args.append(each_rep['fixed'])
            elif 'named_prop' in each_rep:
                base_args.append(self.get_formatted_value(each_rep, data_collection))
            elif 'prop' in each_rep:
                # In this case, data_collection is a single object
                base_fn_object = data_collection[each_rep['prop']]
                if 'function' in each_rep:
                    base_fn_object = self.run_named_function(each_rep, base_fn_object)
                base_args.append(base_fn_object)
        # Replaces the template
        if not 'keep_template' in struct or not struct['keep_template']:
            struct['fixed'] = str(struct['template']).format(*tuple(base_args))
            del struct['template']
            del struct['args']
        else:
            struct['template'] = str(struct['template']).format(*tuple(base_args))
            del struct['keep_template']
            struct['args'] = [self.del_keywords(i) for i in struct['args'] if 'as_is' in i and i['as_is']]
        # Returns cleaned arg
        return struct

    @staticmethod
    def del_keywords(struct):
        ''' Removes datahub-only keywords from an object and returns it clean '''
        keywords = ['as_is', 'keep_template']
        for keyword in keywords:
            if keyword in struct:
                del struct[keyword]
        return struct

    def run_named_function(self, struct, base_object):
        ''' Gets value from function set in config '''
        fn_args = []

        # Gets function args
        if 'args' in struct:
            for each_fn_arg in struct['args']:
                if 'fixed' in each_fn_arg:
                    fn_args.append(each_fn_arg['fixed'])

        # Runs function
        if struct['function'] == 'slice':
            return base_object[fn_args[0]:fn_args[1]]
        return getattr(base_object, struct['function'])(*tuple(fn_args))

    def find_and_operate(self, operation, options=None):
        ''' Obtém um conjunto de dados e opera em cima deles '''
        ejected_filters = options.pop('where')

        # Convert filter strings to actionable list
        (reinserted_filters, ejected_filters) = self.reform_filters_for_pandas(ejected_filters)

        options['as_pandas'] = True
        options['no_wrap'] = True
        options['where'] = reinserted_filters

        # Gets base dataset
        base_dataset = self.find_dataset(options)

        # Operates the dataset
        base_dataset = PandasOperator.operate(base_dataset, operation)

        # Apply ejected filters
        result = self.filter_pandas_dataset(base_dataset, ejected_filters)

        # Reapply sorting
        if 'ordenacao' in options:
            result = self.resort_dataset(result, options['ordenacao'])

        return self.wrap_result(result)

    @staticmethod
    def reform_filters_for_pandas(filters):
        ''' Changes string filters to actionable filters '''
        if filters is None:
            return (None, None)
        filters = list(filter(lambda a: a not in ['and', 'or'], filters))
        ejected_filters = []
        reinserted_filters = []
        for each_filter in filters:
            if each_filter.split('-')[0] == 'post':
                if len(ejected_filters) > 0:
                    ejected_filters.append('and')
                ejected_filters.append(each_filter.split('-'))
            else:
                if len(reinserted_filters) > 0:
                    reinserted_filters.append('and')
                reinserted_filters.append(each_filter)
        return (reinserted_filters, ejected_filters)

    @staticmethod
    def filter_pandas_dataset(base_dataset, ejected_filters):
        ''' Apply filters on operated pandas '''
        if ejected_filters is None:
            return base_dataset
        for each_filter in ejected_filters:
            each_filter.remove('post')
            # Remove NOT NULL
            if each_filter[0] == 'nn':
                base_dataset = base_dataset.dropna(subset=each_filter[1:])
            if each_filter[0] == 'eq':
                base_dataset = base_dataset[base_dataset[each_filter[1]].astype(str) == each_filter[2]]
            if each_filter[0] == 'in':
                base_dataset = base_dataset[base_dataset[each_filter[1]].isin(each_filter[2:])]
        return base_dataset

    @staticmethod
    def resort_dataset(base_dataset, rules):
        ''' Re-execute sorting on the dataset '''
        # Checks descending
        if rules is None:
            return base_dataset

        ascending = not all(['-' in x for x in rules])

        clean_rules = [x.replace('-', '') for x in rules]

        return base_dataset.sort_values(by=clean_rules, ascending=ascending)
