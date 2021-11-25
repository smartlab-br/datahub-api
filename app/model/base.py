''' Base Model '''
import json
import requests
import yaml
import numpy as np
import pandas as pd

from flask import current_app as app
from service.qry_options_builder import QueryOptionsBuilder
from service.pandas_operator import PandasOperator
from service.template_helper import TemplateHelper

#pylint: disable=R0903
class BaseModel():
    ''' Definição do repo '''
    METADATA = {}

    def find_dataset(self, options=None):
        ''' Obtém todos, sem tratamento '''
        result = self.get_repo().find_dataset(options)
        if options.get('pivot') is not None:
            if options.get('calcs'):
                nu_val = 'api_calc_' + options['calcs'][0]
            elif options.get('valor') is None:
                nu_val = self.get_repo().get_agr_string(
                    options.get('agregacao')[0], '*'
                ).split()[-1]
            else:
                nu_val = self.get_repo().get_agr_string(
                    options.get('agregacao')[0], options.get('valor')[0]
                ).split()[-1]
            nu_val = nu_val.lower()
            result = pd.DataFrame(result)
            result = pd.pivot_table(
                result, values=[nu_val],
                columns=options.get('pivot'),
                index=options.get('categorias'),
                aggfunc=self.convert_aggr_to_np(
                    options.get('agregacao'),
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
            if options.get('as_pandas', False):
                return {
                    "metadata": self.fetch_metadata(options),
                    "dataset": dataset
                }
            if options.get('as_string', False):
                return f'{{ \
                    "metadata": {json.dumps(self.fetch_metadata(options))}, \
                    "dataset": {dataset.to_json(orient="records")} \
                }}'
        return {
            "metadata": self.fetch_metadata(options),
            "dataset": dataset.replace({np.nan: None}).to_dict('records')
        }

    def get_repo(self):
        ''' Método abstrato para carregamento do repositório '''
        raise NotImplementedError("Models precisam implementar get_repo")

    def fetch_metadata(self, _options=None):
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
        if aggr.upper() == 'GROUP_CONCAT':
            return (lambda x: ' '.join(x))
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

        # Adding theme by datasource
        options["theme"] = options.get('datasource', 'indicadores')

        # Fetches data collection from impala
        if 'api_obj_collection' in struct:
            (data_collection, any_nodata) = self.get_template_data_collection(
                struct['api_obj_collection'],
                options
            )
        # Adds query params as fixed data in the collection
        if 'coefficient' in options:
            data_collection = {**data_collection, **TemplateHelper.get_coefficients(
                options['coefficient']
            )}
        if 'term' in options:
            data_collection = {**data_collection, **TemplateHelper.get_terms(options['term'])}
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
            if each_options.get('theme') is None:
                each_options["theme"] = options.get("theme")

            # Adds complimentary options
            each_options = QueryOptionsBuilder.build_options(each_options)
            each_options["as_pandas"] = True

            # Builds the options to query impala
            each_obj = self.find_dataset(each_options)

            # Transforms the dataset with coefficient
            if 'coefficient' in options:
                each_obj = TemplateHelper.apply_coefficient(options['coefficient'], each_obj)

            # Runs formatters from config
            if 'formatters' in each_obj_struct:
                each_obj = TemplateHelper.run_formatters(each_obj_struct['formatters'], each_obj)

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
                        "fixed": struct.get('msgNoData', {}).get('desc', 'no data')
                    }
                }]
            elif isinstance(each_arg, list):
                struct[each_arg_key] = [
                    self.templates_to_fixed(each_item, data_collection) for each_item in each_arg
                ]
            elif isinstance(each_arg, dict):
                if 'template' in each_arg:
                    each_arg = self.replace_template_arg(each_arg, data_collection)
                elif 'named_prop' in each_arg:
                    # Replaces the named_prop
                    each_arg = self.replace_named_prop(each_arg, data_collection)
                else:
                    struct[each_arg_key] = self.templates_to_fixed(each_arg, data_collection)
        return struct

    @classmethod
    def build_derivatives(cls, each_obj_struct, options, each_obj, data_collection):
        ''' Gets derivetive attributes from configs '''
        any_nodata = False
        for each_inst in each_obj_struct.get('instances'):
            try:
                data_collection[each_inst.get('name')] = cls.get_collection_from_type(
                    each_obj.get('dataset'),
                    each_inst.get('type'),
                    each_inst.get('named_prop'),
                    options.get('cd_analysis_unit')
                )
            except (ValueError, KeyError, TypeError, IndexError):
                data_collection[each_inst.get('name')] = None
                any_nodata = True
            if each_inst.get('name') not in data_collection:
                data_collection[each_inst.get('name')] = None
                any_nodata = True
        return (data_collection, any_nodata)

    @staticmethod
    def get_collection_from_type(dataset, inst_type, named_prop=None, id_au=None):
        ''' Use pandas filter to set a collection '''
        functions = {
            'from_id': (
                lambda named_prop, id_au:
                dataset.loc[dataset[named_prop] == int(id_au)].iloc[0]
            ),
            'first_occurence': lambda named_prop, id_au: dataset.reset_index().loc[0],
            'min': (
                lambda named_prop, id_au:
                dataset.loc[dataset[named_prop] == dataset[named_prop].min()].iloc[0]
                if dataset[named_prop].dtype == 'object'
                else dataset.loc[dataset[named_prop].idxmin()]
            ),
            'max': (
                lambda named_prop, id_au:
                dataset.loc[dataset[named_prop] == dataset[named_prop].max()].iloc[0]
                if dataset[named_prop].dtype == 'object'
                else dataset.loc[dataset[named_prop].idxmax()]
            )
        }
        if inst_type is not None and inst_type in functions:
            return functions[inst_type](named_prop, id_au)
        return None

    @staticmethod
    def replace_named_prop(struct, data_collection):
        ''' Replaces the named_prop according to confs '''
        struct['fixed'] = TemplateHelper.get_formatted_value(struct, data_collection)
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

    @staticmethod
    def replace_template_arg(struct, data_collection):
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
                base_args.append(TemplateHelper.get_formatted_value(each_rep, data_collection))
            elif 'prop' in each_rep:
                # In this case, data_collection is a single object
                base_fn_object = data_collection[each_rep['prop']]
                if 'function' in each_rep:
                    base_fn_object = TemplateHelper.run_named_function(each_rep, base_fn_object)
                base_args.append(base_fn_object)
        # Replaces the template
        if not 'keep_template' in struct or not struct['keep_template']:
            struct['fixed'] = str(struct['template']).format(*tuple(base_args))
            del struct['template']
            del struct['args']
        else:
            struct['template'] = str(struct['template']).format(*tuple(base_args))
            del struct['keep_template']
            struct['args'] = [
                TemplateHelper.del_keywords(i)
                for
                i
                in
                struct['args']
                if 'as_is' in i and i['as_is']
            ]
        # Returns cleaned arg
        return struct

    def find_and_operate(self, operation, options=None):
        ''' Obtém um conjunto de dados e opera em cima deles '''
        if options is None:
            return self.find_dataset(options)
        local_options = options.copy()
        ejected_filters = []
        if 'where' in local_options:
            ejected_filters = local_options.pop('where')

        # Convert filter strings to actionable list
        (reinserted_filters, ejected_filters) = self.reform_filters_for_pandas(ejected_filters)

        local_options['as_pandas'] = True
        local_options['no_wrap'] = True
        local_options['where'] = reinserted_filters

        # Gets base dataset
        base_dataset = self.find_dataset(local_options)

        # Operates the dataset
        base_dataset = PandasOperator.operate(
            base_dataset,
            operation,
            local_options.get('categorias')
        )

        # Apply ejected filters
        result = self.filter_pandas_dataset(base_dataset, ejected_filters)

        # Reapply sorting
        if 'ordenacao' in local_options:
            result = self.resort_dataset(result, options['ordenacao'])

        if options.get('no_wrap'):
            return result
        return self.wrap_result(result, options)

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
                base_dataset = base_dataset[
                    base_dataset[each_filter[1]].astype(str) == each_filter[2]
                ]
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
