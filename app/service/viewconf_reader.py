''' Module for reading viewconf yaml files '''
import urllib
import requests
import yaml
import numpy as np
from branca.colormap import LinearColormap
import brewer2mpl
from flask import current_app as app
from service.number_formatter import NumberFormatter
from service.qry_options_builder import QueryOptionsBuilder

class ViewConfReader():
    ''' Service that formats a number into a HTML snippet '''
    @staticmethod
    def get_api_url(api_call_obj, custom_args):
        ''' Read API url formation '''
        if api_call_obj is None:
            return None
        if 'fixed' in api_call_obj:
            return api_call_obj.get('fixed')
        if 'template' in api_call_obj:
            api_url = api_call_obj.get('template')
            if custom_args is None:
                return api_url
            for arg_i, arg in enumerate(api_call_obj.get('args')):
                rplc = arg.get('fixed')
                if arg.get('named_prop'):
                    if arg.get('named_prop') in ['idLocalidade']: # Analysis Unit ID mnemonics
                        rplc = custom_args.get('au')
                    else:
                        rplc = custom_args.get(arg.get('named_prop'), custom_args.get('au'))
                api_url = api_url.replace(f'{{{arg_i}}}', rplc)
            return api_url

    @staticmethod
    def get_dimension_descriptor(language, observatory, scope, dimension):
        ''' Gets the dimension YAML descriptor as dictionary '''
        location = app.config['GIT_VIEWCONF_BASE_URL'].format(
            f'{language}/observatorio/{observatory}/localidade/',
            scope,
            dimension
        )
        return yaml.load(requests.get(location, verify=False).content)

    @classmethod
    def api_to_options(cls, api_call_obj, custom_args):
        ''' Transforms API string into datahub options '''
        url = cls.get_api_url(api_call_obj, custom_args)
        url_parts = urllib.parse.urlparse(url)

        args_dict = {arg.split('=')[0]: arg.split('=')[1] for arg in url_parts.query.split('&')}
        options = QueryOptionsBuilder.build_options(args_dict)

        path_parts = url_parts.path.split('/')
        if path_parts[0] == '':
            path_parts.pop(0)

        if path_parts[0] == 'thematic':
            options['theme'] = path_parts[1]
        elif '-' in path_parts[-1]:
            options['theme'] = ''.join(path_parts[:-1])
            options['operation'] = path_parts[-1]
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
        if options is None:
            return {}
        nu_options = {}
        analysis_unit = options.get('au')
        visao = options.get('visao', 'uf')

        if len(str(analysis_unit)) > 2 or (len(str(analysis_unit)) == 2 and visao == 'uf'):
            nu_options['cd_uf'] = str(analysis_unit)[:2]

        return nu_options

    @classmethod
    def generate_columns(cls, dataframe, options):
        ''' Create new columns by applying calcs and formatters '''
        # Applying calcs
        calcs = options.get('api', {}).get('options', {}).get('calcs', [])
        for calc in calcs:
            try:
                dataframe['calc_' + calc.get('id')] = dataframe.apply(
                    getattr(cls, calc.get('function')),
                    axis=1,
                    **calc
                )
            except AttributeError:
                # Ignores non-existing functions
                continue

        # Applying formatters
        formatters = options.get('api', {}).get('options', {}).get('formatters', [])
        for fmtr in formatters:
            dataframe['fmt_' + fmtr.get('id')] = dataframe[fmtr.get('id')].apply(
                NumberFormatter.format,
                options=fmtr
            )

        return dataframe

    @staticmethod
    def get_proportional_indicator_uf(row, **kwargs):
        ''' Custom function to get the data as a positive number based on moved log curve '''
        return np.log(((row.get(kwargs.get('campo', 'vl_indicador')) - row.get(kwargs.get('media', 'media_uf'))) / row.get(kwargs.get('media', 'media_uf'))) + 1.01)

    @staticmethod
    def get_chart_title(options):
        ''' Gets the chart title based on given options '''
        if options is None:
            return None
        if options.get('type') == 'multiple-charts':
            if len(options.get('charts', [])) == 0:
                return None
            for chart in options.get('charts'):
                if chart.get('id') == options.get('chart_id'):
                    return chart.get('title', 'background')
            return options.get('charts')[0].get('title', 'background')
        return options.get('title', {}).get('fixed', 'background')

    @staticmethod
    def get_color_scale(options, vmin=0, vmax=1):
        ''' Gets a color array as given by options or builds a linear scale '''
        # Check if color list is given, escaping if true
        if options and options.get('chart_options', {}).get('colorArray'):
            return options.get('chart_options', {}).get('colorArray')
        scale_def = {'name': 'Blues'}    
        if options is not None:
            scale_def = options.get('chart_options', {}).get('colorScale', {'name': 'Blues'})
            if options.get('type') == 'multiple-charts':
                for chart in options.get('charts'):
                    if chart.get('id') == options.get('chart_id'):
                        if chart.get('options', {}).get('colorArray'):
                            return chart.get('options', {}).get('colorArray')
                        scale_def = chart.get('options', {}).get('colorScale', {'name': 'Blues'})

        plt = brewer2mpl.get_map(
            scale_def.get("name"),
            scale_def.get('nature', 'sequential'),
            scale_def.get("levels", 5),
            reverse=scale_def.get("order", "asc") == 'desc'
        )

        return LinearColormap(
            plt.mpl_colors,
            vmin=vmin,
            vmax=vmax
        )

    @staticmethod
    def get_marker_color(options):
        ''' Gets the marker color to use in a map '''
        if options is None:
            return 'red'
        if options.get('type') == 'multiple-charts':
            if len(options.get('charts', [])) == 0:
                return None
            for chart in options.get('charts'):
                if chart.get('id') == options.get('chart_id'):
                    return chart.get('marker_color', 'red')
            return options.get('charts')[0].get('marker_color', 'red')
        return options.get('marker_color', 'red')

    @staticmethod
    def get_headers_from_options_descriptor(description, initial):
        ''' Constructs the headers options based on basic rules '''
        if description is None:
            return initial
        for descriptor in description:
            if descriptor.get('id') in ['selectlayer']:
                for layer in descriptor.get('items', []):
                    initial.append({
                        'text': layer.get('label'),
                        'layer_id': layer.get('value'),
                        'value': layer.get('id')
                    })
        return initial
