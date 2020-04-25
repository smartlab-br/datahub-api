''' Template helper classes '''
from service.number_formatter import NumberFormatter

class TemplateHelper():
    ''' Helper class for template parsing '''
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
            each_obj['dataset'][each_fmt['prop']] = [
                NumberFormatter.format(row[each_fmt['named_prop']], args)
                for
                index, row
                in
                each_obj['dataset'].iterrows()
            ]
        return each_obj

    @staticmethod
    def apply_coefficient(str_coefficients, each_obj):
        ''' Applies the given coefficients to the values in the dataset '''
        coefficients = str_coefficients.split(',')
        for coefficient in coefficients:
            coefficient_parts = coefficient.split("-")
            if coefficient_parts[0] in each_obj['dataset']:
                each_obj['dataset'][coefficient_parts[0]] = each_obj['dataset'][
                    coefficient_parts[0]
                ] * float(coefficient_parts[1])
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

    @staticmethod
    def del_keywords(struct):
        ''' Removes datahub-only keywords from an object and returns it clean '''
        keywords = ['as_is', 'keep_template']
        for keyword in keywords:
            if keyword in struct:
                del struct[keyword]
        return struct

    @staticmethod
    def run_named_function(struct, base_object):
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
