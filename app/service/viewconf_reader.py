''' Module for reading viewconf yaml files '''
import requests
import urllib
import yaml
from flask import current_app as app
from service.number_formatter import NumberFormatter
from service.qry_options_builder import QueryOptionsBuilder
import numpy as np

class ViewConfReader():
    ''' Service that formats a number into a HTML snippet '''
    @staticmethod
    def get_api_url(api_call_obj, custom_args):
        ''' Read API url formation '''
        if api_call_obj is None:
            return None

        api_url = api_call_obj.get('fixed')
        if api_call_obj.get('template'):
            api_url = api_call_obj.get('template')
            for arg_i, arg in enumerate(api_call_obj.get('args')):
                rplc = arg.get('fixed')
                if arg.get('named_prop'):
                    rplc = custom_args[arg.get('named_prop')]
                api_url = api_url.replace(f'{{{arg_i}}}', rplc)

        return api_url

    @staticmethod
    def get_dimension_descriptor(language, observatory, scope, dimension):
        ''' Gets the dimension YAML descriptor as dictionary '''
        location = app.config['GIT_VIEWCONF_BASE_URL'].format(language, observatory, scope, dimension)
        return yaml.load(requests.get(location, verify=False).content)

    @classmethod
    def api_to_options(cls, api_call_obj, custom_args):
        ''' Transforms API string into datahub options '''
        url = cls.get_api_url(api_call_obj, custom_args)
        url_parts = urllib.parse.urlparse(url)

        args = [x for x in url_parts.query.split('&')]
        args_dict = {arg.split('=')[0]: arg.split('=')[1] for arg in args}
        options = QueryOptionsBuilder.build_options(args_dict)

        path_parts = url_parts.path.split('/')
        if path_parts[0] == '':
            path_parts.pop(0)

        if path_parts[0] == 'thematic':
            options['theme'] = path_parts[1]
        else:
            options['theme'] = ''.join(path_parts)

        return options
        
    @classmethod
    def get_card_descriptor(cls, language, observatory, scope, dimension, card_id):
        ''' Gets a single card from a viewconf yaml as a dictionary '''
        dim = cls.get_dimension_descriptor(language, observatory, scope, dimension)
        if dim.get('secoes'):
            for secao in dim.get('secoes'):
                if secao.get('cards'):
                    for card in secao.get('cards'):
                        if card.get('id') == card_id:
                            return card
        return None

    @staticmethod
    def set_custom_options(options):
        ''' Creates new options from predefined rules '''
        nu_options = {}
        au = options.get('au')
        visao = options.get('visao', 'uf')

        if len(str(au)) > 2 or (len(str(au)) == 2 and visao == 'uf'):
            nu_options['cd_uf']=str(au)[:2]

        return nu_options
    
    @classmethod
    def generate_columns(cls, dataframe, options):
        ''' Create new columns by applying calcs and formatters '''
        # Applying calcs
        calcs = options.get('api',{}).get('options',{}).get('calcs')
        for calc in calcs:
            dataframe['calc_' + calc.get('id')] = dataframe.apply(
                getattr(cls, calc.get('function')),
                axis=1,
                **calc
            )
        
        # Applying formatters
        formatters = options.get('api',{}).get('options',{}).get('formatters')
        for fmtr in formatters:
            dataframe['fmt_' + fmtr.get('id')] = dataframe[fmtr.get('id')].apply(
                NumberFormatter.format,
                options = fmtr
            )
        
        return dataframe

    @staticmethod
    def get_proportional_indicator_uf(row, **kwargs):
        ''' Custom function to get the data as a positive number based on moved log curve '''
        return np.log(((row.get(kwargs.get('campo', 'vl_indicador')) - row.get(kwargs.get('media', 'media_uf'))) / row.get(kwargs.get('media', 'media_uf'))) + 1.01)