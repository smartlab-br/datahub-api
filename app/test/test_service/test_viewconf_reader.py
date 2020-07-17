'''Main tests in API'''
import unittest
from service.viewconf_reader import ViewConfReader

class ViewConfGetApiUrlTest(unittest.TestCase):
    ''' Test behaviours linked to YAML API call transformations '''
    def test_no_call(self):
        ''' Tests if returns None when no api call is passed '''
        self.assertEqual(
            ViewConfReader.get_api_url(None, None),
            None
        )
    
    def test_fixed_no_template(self):
        ''' Tests if returns the YAML fixed value with no transformation '''
        dict_from_yaml = {
            "fixed": "this_is_a_fixed_value"
        }
        self.assertEqual(
            ViewConfReader.get_api_url(dict_from_yaml, None),
            "this_is_a_fixed_value"
        )
    
    def test_template(self):
        ''' Tests if returns the YAML fixed value with no transformation '''
        dict_from_yaml = {
            "template": "{0}, {1}, {2}, {3}.",
            "args": [
                {"fixed": "fixed"},
                {"named_prop": "existing_named_prop"},
                {"named_prop": "idLocalidade"},
                {"named_prop": "missing_named_prop"},
            ]
        }
        custom_args = {
            "existing_named_prop": "existing_named_prop",
            "au": "analysis_unit"
        }
        self.assertEqual(
            ViewConfReader.get_api_url(dict_from_yaml, custom_args),
            "fixed, existing_named_prop, analysis_unit, analysis_unit."
        )
    
    def test_template_missing_args(self):
        ''' Tests if returns template as fixed, AS-IS, when no custom args are passed '''
        dict_from_yaml = {
            "template": "{0}, {1}, {2}, {3}.",
            "args": [
                {"fixed": "fixed"},
                {"named_prop": "existing_named_prop"},
                {"named_prop": "idLocalidade"},
                {"named_prop": "missing_named_prop"},
            ]
        }
        self.assertEqual(
            ViewConfReader.get_api_url(dict_from_yaml, None),
             "{0}, {1}, {2}, {3}."
        )
    
    def test_fixed_with_spurious_template(self):
        ''' Tests if returns the YAML fixed value with no transformation,
            even when a template is wrongly informed '''
        dict_from_yaml = {
            "fixed": "this_is_a_fixed_value",
            "template": "{0}, {1}, {2}, {3}.",
            "args": [
                {"fixed": "fixed"},
                {"named_prop": "existing_named_prop"},
                {"named_prop": "idLocalidade"},
                {"named_prop": "missing_named_prop"},
            ]
        }
        custom_args = {
            "existing_named_prop": "existing_named_prop",
            "au": "analysis_unit"
        }
        self.assertEqual(
            ViewConfReader.get_api_url(dict_from_yaml, custom_args),
            "this_is_a_fixed_value"
        )

class ViewConfGetChartTitleTest(unittest.TestCase):
    ''' Test behaviours linked to getting the correct chart title '''
    def test_fetch_chart_title_no_options(self):
        ''' Tests if title falls back to None when no YAML options are
            actually passed to the method '''
        self.assertEqual(ViewConfReader.get_chart_title(None), None)
    
    def test_fetch_chart_title(self):
        ''' Tests if the title for a single chart is properly acquired '''
        options_from_yaml = {"title": {"fixed": "simple_title"}}
        self.assertEqual(
            ViewConfReader.get_chart_title(options_from_yaml),
            "simple_title"
        )

    def test_fetch_chart_title_no_fixed(self):
        ''' Tests if the title for a single chart falls back to "background"
            property when no fixed value is passed '''
        options_from_yaml = {"title": {}}
        self.assertEqual(
            ViewConfReader.get_chart_title(options_from_yaml),
            "background"
        )
    
    def test_fetch_chart_title_among_multiple(self):
        ''' Tests if the title is properly acquired when the card contains multiple instances '''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [
                {"id": "wrong", "title": "wrong_title"},
                {"id": "right", "title": "right_title"}
            ],
            "chart_id": "right"
        }
        self.assertEqual(
            ViewConfReader.get_chart_title(options_from_yaml),
            "right_title"
        )

    def test_fetch_chart_title_among_multiple_no_title(self):
        ''' Tests if the title falls back to "background" property when chart has
            no title property '''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [{"id": "wrong"}, {"id": "right"}],
            "chart_id": "right"
        }
        self.assertEqual(
            ViewConfReader.get_chart_title(options_from_yaml),
            "background"
        )

    def test_fetch_chart_title_among_multiple_no_id(self):
        ''' Tests if the title from the first chart is properly acquired when 
            no id is requested from the options '''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [
                {"id": "first", "title": "first_title"},
                {"id": "wrong", "title": "wrong_title"},
                {"id": "right", "title": "right_title"}
            ]
        }
        self.assertEqual(
            ViewConfReader.get_chart_title(options_from_yaml),
            "first_title"
        )

    def test_fetch_chart_title_among_multiple_no_valid_chart_collection(self):
        ''' Tests if the title falls back to None when there's no card in the
            multiple-charts collection '''
        options_from_yaml = {"type": "multiple-charts"}
        self.assertEqual(
            ViewConfReader.get_chart_title(options_from_yaml),
            None
        )

class ViewConfGetMarkerColorTest(unittest.TestCase):
    ''' Test behaviours linked to getting the correct chart title '''
    def test_default_color_single_chart_no_options(self):    
        ''' Tests if "red" is returned when no options is sent '''
        self.assertEqual(ViewConfReader.get_marker_color(None), "red")

    def test_fetch_marker_color(self):
        ''' Tests if the marker color for a single chart is properly acquired '''
        options_from_yaml = {"marker_color": "blue"}
        self.assertEqual(
            ViewConfReader.get_marker_color(options_from_yaml),
            "blue"
        )

    def test_fetch_marker_color_no_fixed(self):
        ''' Tests if the marker color for a single chart falls back to "red"
            property when no marker_color attribute value is passed '''
        self.assertEqual(
            ViewConfReader.get_marker_color({}),
            "red"
        )
    
    def test_fetch_marker_color_among_multiple(self):
        ''' Tests if the marker color is properly acquired when the card contains multiple instances '''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [
                {"id": "wrong", "marker_color": "green"},
                {"id": "right", "marker_color": "blue"}
            ],
            "chart_id": "right"
        }
        self.assertEqual(
            ViewConfReader.get_marker_color(options_from_yaml),
            "blue"
        )

    def test_fetch_marker_color_among_multiple_no_title(self):
        ''' Tests if the marker color falls back to "background" property when chart has
            no marker_color property '''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [{"id": "wrong"}, {"id": "right"}],
            "chart_id": "right"
        }
        self.assertEqual(
            ViewConfReader.get_marker_color(options_from_yaml),
            "red"
        )

    def test_fetch_marker_color_among_multiple_no_id(self):
        ''' Tests if the title from the first chart is properly acquired when 
            no id is requested from the options '''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [
                {"id": "first", "marker_color": "blue"},
                {"id": "wrong", "marker_color": "purple"},
                {"id": "right", "marker_color": "green"}
            ]
        }
        self.assertEqual(
            ViewConfReader.get_marker_color(options_from_yaml),
            "blue"
        )

    def test_fetch_marker_color_among_multiple_no_valid_chart_collection(self):
        ''' Tests if the marker color falls back to None when there's no card in the
            multiple-charts collection '''
        options_from_yaml = {"type": "multiple-charts"}
        self.assertEqual(
            ViewConfReader.get_marker_color(options_from_yaml),
            None
        )

class ViewConfSetCustomOptionsTest(unittest.TestCase):
    ''' Test behaviours linked to creating custom attributes to YAML options '''
    def test_default_generated_options(self):
        ''' Tests resulting options when none were passed '''
        self.assertEqual(
            ViewConfReader.set_custom_options(None), {})

    def test_uf_from_municipality_id(self):
        ''' Tests resulting options when the analysis unit is a municipality
            and no scope (visao) is passed '''
        self.assertEqual(
            ViewConfReader.set_custom_options({'au': '1234567'}),
            {'cd_uf': '12'}
        )

    def test_uf_from_municipality_id_visao(self):
        ''' Tests resulting options when the analysis unit is a municipality
            and visao is not 'uf' '''
        self.assertEqual(
            ViewConfReader.set_custom_options({'au': '1234567', 'visao': 'mun'}),
            {'cd_uf': '12'}
        )

    def test_uf_from_municipality_id_visao_uf(self):
        ''' Tests resulting options when the analysis unit is a municipality
            and visao is 'uf' '''
        self.assertEqual(
            ViewConfReader.set_custom_options({'au': '1234567', 'visao': 'uf'}),
            {'cd_uf': '12'}
        )

    def test_uf_from_visao_uf(self):
        ''' Tests resulting options when none were passed '''
        self.assertEqual(
            ViewConfReader.set_custom_options({'au': '12', 'visao': 'uf'}),
            {'cd_uf': '12'}
        )

    def test_uf_from_visao(self):
        ''' Tests resulting options when none were passed '''
        self.assertEqual(
            ViewConfReader.set_custom_options({'au': '12', 'visao': 'mun'}),
            {}
        )

class ViewConfGetHeadersFromDescriptorTest(unittest.TestCase):
    ''' Test behaviours linked to getting headers from descriptos in the card from YAML '''
    BASE_INITIAL = [{
        'text': 'Analysis Unit',
        'value': 'nm_municipio'
    }]

    def test_no_descriptor(self):
        ''' Tests resulting headers when no descriptor is sent '''
        self.assertEqual(
            ViewConfReader.get_headers_from_options_descriptor(None, self.BASE_INITIAL),
            self.BASE_INITIAL
        )

    def test_empty_descriptor(self):
        ''' Tests resulting headers when no descriptor is sent '''
        self.assertEqual(
            ViewConfReader.get_headers_from_options_descriptor([], self.BASE_INITIAL),
            self.BASE_INITIAL
        )

    def test_descriptor(self):
        ''' Tests resulting headers when a descriptor is sent '''
        description = [
            {"id": "ignore", "items": [
                {"label": "lbl_ign1_1", "value": "val_ign1_1", "id": "id_ign1_1"},
                {"label": "lbl_ign1_2", "value": "val_ign1_2", "id": "id_ign1_2"}
            ]},
            {"id": "selectlayer", "items": [
                {"label": "lbl_ok_1", "value": "val_ok_1", "id": "id_ok_1"},
                {"label": "lbl_ok_2", "value": "val_ok_2", "id": "id_ok_2"}
            ]},
            {"id": "ignore2", "items": [
                {"label": "lbl_ign2_1", "value": "val_ign2_1", "id": "id_ign2_1"},
                {"label": "lbl_ign2_2", "value": "val_ign2_2", "id": "id_ign2_2"}
            ]}
        ]
        expected = self.BASE_INITIAL.copy()
        expected.extend([
            {"text": "lbl_ok_1", "layer_id": "val_ok_1", "value": "id_ok_1"},
            {"text": "lbl_ok_2", "layer_id": "val_ok_2", "value": "id_ok_2"}
        ])
        self.assertEqual(
            ViewConfReader.get_headers_from_options_descriptor(description, self.BASE_INITIAL),
            expected
        )

    def test_descriptor_no_match(self):
        ''' Tests resulting headers when a descriptor with no layer control is sent '''
        description = [
            {"id": "ignore", "items": [
                {"label": "lbl_ign1_1", "value": "val_ign1_1", "id": "id_ign1_1"},
                {"label": "lbl_ign1_2", "value": "val_ign1_2", "id": "id_ign1_2"}
            ]},
            {"id": "ignore2", "items": [
                {"label": "lbl_ign2_1", "value": "val_ign2_1", "id": "id_ign2_1"},
                {"label": "lbl_ign2_2", "value": "val_ign2_2", "id": "id_ign2_2"}
            ]}
        ]
        self.assertEqual(
            ViewConfReader.get_headers_from_options_descriptor(description, self.BASE_INITIAL),
            self.BASE_INITIAL
        )

class ViewConfApiToOptionsTest(unittest.TestCase):
    ''' Test behaviours linked to transforming a URL from YAML config to a disctionary '''
    def test_conversion_thematic(self):
        ''' Tests resulting dictionary '''
        dict_from_yaml = {"fixed": "/thematic/mytheme?categorias=mycat1,mycat2&valor=myval"}
        self.assertEqual(
            ViewConfReader.api_to_options(dict_from_yaml, None),
            {
                "theme": "mytheme",
                "categorias": ["mycat1","mycat2"],
                "valor": ["myval"]
            }
        )

    def test_conversion_thematic_operation(self):
        ''' Tests if no direct operation is allowed in thematic url '''
        dict_from_yaml = {"fixed": "/thematic/mytheme-myop?categorias=mycat1,mycat2&valor=myval"}
        self.assertEqual(
            ViewConfReader.api_to_options(dict_from_yaml, None),
            {
                "theme": "mytheme-myop",
                "categorias": ["mycat1","mycat2"],
                "valor": ["myval"]
            }
        )

    def test_conversion(self):
        ''' Tests resulting dictionary '''
        dict_from_yaml = {"fixed": "/my/theme?categorias=mycat1,mycat2&valor=myval"}
        self.assertEqual(
            ViewConfReader.api_to_options(dict_from_yaml, None),
            {
                "theme": "mytheme",
                "categorias": ["mycat1","mycat2"],
                "valor": ["myval"]
            }
        )

    def test_conversion_operation(self):
        ''' Tests if the theme is located before operation segment '''
        dict_from_yaml = {"fixed": "/my/theme/det-myop?categorias=mycat1,mycat2&valor=myval"}
        self.assertEqual(
            ViewConfReader.api_to_options(dict_from_yaml, None),
            {
                "theme": "mytheme",
                "operation": "det-myop",
                "categorias": ["mycat1","mycat2"],
                "valor": ["myval"]
            }
        )
    






    # @classmethod
    # def generate_columns(cls, dataframe, options):
    #     ''' Create new columns by applying calcs and formatters '''
    #     # Applying calcs
    #     calcs = options.get('api', {}).get('options', {}).get('calcs', [])
    #     for calc in calcs:
    #         try:
    #             dataframe['calc_' + calc.get('id')] = dataframe.apply(
    #                 getattr(cls, calc.get('function')),
    #                 axis=1,
    #                 **calc
    #             )
    #         except AttributeError:
    #             # Ignores non-existing functions
    #             continue

    #     # Applying formatters
    #     formatters = options.get('api', {}).get('options', {}).get('formatters', [])
    #     for fmtr in formatters:
    #         dataframe['fmt_' + fmtr.get('id')] = dataframe[fmtr.get('id')].apply(
    #             NumberFormatter.format,
    #             options=fmtr
    #         )

    #     return dataframe

    # @staticmethod
    # def get_proportional_indicator_uf(row, **kwargs):
    #     ''' Custom function to get the data as a positive number based on moved log curve '''
    #     return np.log(((row.get(kwargs.get('campo', 'vl_indicador')) - row.get(kwargs.get('media', 'media_uf'))) / row.get(kwargs.get('media', 'media_uf'))) + 1.01)

    
    # @staticmethod
    # def get_color_scale(options, vmin=None, vmax=None):
    #     ''' Gets a color array as given by options or builds a linear scale '''
    #     # Check if color list is given, escaping if true
    #     if options.get('chart_options', {}).get('colorArray'):
    #         return options.get('chart_options', {}).get('colorArray')
    #     scale_def = options.get('chart_options', {}).get('colorScale', {'name': 'Blues'})
    #     if options.get('type') == 'multiple-charts':
    #         for chart in options.get('charts'):
    #             if chart.get('id') == options.get('chart_id'):
    #                 if chart.get('options', {}).get('colorArray'):
    #                     return chart.get('options', {}).get('colorArray')
    #                 scale_def = chart.get('options', {}).get('colorScale', {'name': 'Blues'})

    #     plt = brewer2mpl.get_map(
    #         scale_def.get("name"),
    #         scale_def.get('nature', 'sequential'),
    #         scale_def.get("levels", 5),
    #         reverse=scale_def.get("order", "asc") == 'desc'
    #     )

    #     return LinearColormap(
    #         plt.mpl_colors,
    #         vmin=vmin,
    #         vmax=vmax
    #     )






    # @staticmethod
    # def get_dimension_descriptor(language, observatory, scope, dimension):
    #     ''' Gets the dimension YAML descriptor as dictionary '''
    #     location = app.config['GIT_VIEWCONF_BASE_URL'].format(
    #         f'{language}/observatorio/{observatory}/localidade/',
    #         scope,
    #         dimension
    #     )
    #     return yaml.load(requests.get(location, verify=False).content)

    # @classmethod
    # def get_card_descriptor(cls, language, observatory, scope, dimension, card_id):
    #     ''' Gets a single card from a viewconf yaml as a dictionary '''
    #     dim = cls.get_dimension_descriptor(language, observatory, scope, dimension)
    #     if dim.get('secoes'):
    #         for secao in dim.get('secoes'):
    #             if secao.get('cards'):
    #                 for card in secao.get('cards'):
    #                     if card.get('id') == card_id:
    #                         return card
    #     return None
