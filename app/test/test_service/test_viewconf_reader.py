'''Main tests in API'''
import unittest
from test.stubs.viewconf import StubViewConfReader
import numpy as np
import pandas as pd
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
        ''' Tests if the marker color is properly acquired when the card contains
            multiple instances '''
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

class ViewConfGetColorScaleTest(unittest.TestCase):
    ''' Test behaviours linked to getting the color scale '''
    def test_fetch_color_array_single_chart(self):
        ''' Tests if a color array apssed as chart_option is returned AS-IS '''
        options_from_yaml = {'chart_options': {'colorArray': ['red', 'yellow', 'green']}}
        self.assertEqual(
            ViewConfReader.get_color_scale(options_from_yaml),
            ['red', 'yellow', 'green']
        )

    def test_fetch_color_array_among_multiple(self):
        ''' Tests if the color array property is properly acquired when the card
            contains multiple instances '''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [
                {"id": "wrong", "options": {'colorArray': ['blue', 'purple', 'orange']}},
                {"id": "right", "options": {'colorArray': ['red', 'yellow', 'green']}}
            ],
            "chart_id": "right"
        }
        self.assertEqual(
            ViewConfReader.get_color_scale(options_from_yaml),
            ['red', 'yellow', 'green']
        )

    def test_fetch_default_color_scale_no_option(self):
        ''' Tests if the default color scale is returned when YAML option is None '''
        color_scale = ViewConfReader.get_color_scale(None)
        self.assertEqual(color_scale(0), "#eff3ffff")
        self.assertEqual(color_scale(0.5), "#6baed6ff")
        self.assertEqual(color_scale(1), "#08519cff")

    def test_fetch_default_color_scale(self):
        ''' Tests if the default color scale is returned when no definition is given '''
        color_scale = ViewConfReader.get_color_scale({})
        self.assertEqual(color_scale(0), "#eff3ffff")
        self.assertEqual(color_scale(0.5), "#6baed6ff")
        self.assertEqual(color_scale(1), "#08519cff")

    def test_fetch_default_color_scale_min_max(self):
        ''' Tests if the default color scale is returned when no definition is given '''
        min_val = 10
        max_val = 20
        color_scale = ViewConfReader.get_color_scale({}, min_val, max_val)
        self.assertEqual(color_scale(min_val), "#eff3ffff")
        self.assertEqual(color_scale((max_val + min_val) / 2), "#6baed6ff")
        self.assertEqual(color_scale(max_val), "#08519cff")

    def test_fetch_color_scale_single_chart(self):
        ''' Tests if a color scale is fetched apropriately from single chart YAML options '''
        color_scale = ViewConfReader.get_color_scale({
            'chart_options': {'colorScale': {"name": "Reds"}}
        })
        self.assertEqual(color_scale(0), "#fee5d9ff")
        self.assertEqual(color_scale(0.5), "#fb6a4aff")
        self.assertEqual(color_scale(1), "#a50f15ff")

    def test_fetch_color_scale_among_multiple(self):
        ''' Tests if the color scale property is properly acquired when the card
            contains multiple instances '''
        color_scale = ViewConfReader.get_color_scale({
            "type": "multiple-charts",
            "charts": [
                {"id": "wrong", "options": {'colorScale': {"name": "invalid"}}},
                {"id": "right", "options": {'colorScale': {"name": "Reds"}}}
            ],
            "chart_id": "right"
        })
        self.assertEqual(color_scale(0), "#fee5d9ff")
        self.assertEqual(color_scale(0.5), "#fb6a4aff")
        self.assertEqual(color_scale(1), "#a50f15ff")

    def test_fetch_reversed_color_scale_single_chart(self):
        ''' Tests if a color scale in reverse order is fetched apropriately
            from single chart YAML options '''
        color_scale = ViewConfReader.get_color_scale({
            'chart_options': {'colorScale': {"name": "Reds", "order": "desc"}}
        })
        self.assertEqual(color_scale(0), "#a50f15ff")
        self.assertEqual(color_scale(0.5), "#fb6a4aff")
        self.assertEqual(color_scale(1), "#fee5d9ff")

    def test_fetch_qualitative_paired_color_scale_single_chart(self):
        ''' Tests if a paired qualitative color scale is fetched apropriately
            from single chart YAML options '''
        color_scale = ViewConfReader.get_color_scale({
            'chart_options': {'colorScale': {
                "name": "Paired",
                "nature": "Qualitative"
            }}
        })
        self.assertEqual(color_scale(0), "#a6cee3ff")
        self.assertEqual(color_scale(0.5), "#b2df8aff")
        self.assertEqual(color_scale(1), "#fb9a99ff")

    def test_fetch_qualitative_paired_color_scale_single_chart_color_list(self):
        ''' Tests if a paired qualitative color scale with defined # of colors
            is fetched apropriately from single chart YAML options '''
        color_scale = ViewConfReader.get_color_scale({
            'chart_options': {'colorScale': {
                "name": "Paired",
                "nature": "Qualitative",
                "levels": 5
            }}
        })
        self.assertEqual(
            color_scale,
            ['#a6cee3ff', '#1f78b4ff', '#b2df8aff', '#33a02cff', '#fb9a99ff']
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
    BASE_INITIAL = [{'text': '', 'value': 'nm_municipio'}]

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
                "categorias": ["mycat1", "mycat2"],
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
                "categorias": ["mycat1", "mycat2"],
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
                "categorias": ["mycat1", "mycat2"],
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
                "categorias": ["mycat1", "mycat2"],
                "valor": ["myval"]
            }
        )

class ViewConfCustomCalcTest(unittest.TestCase):
    ''' Test behaviours linked to custom calc functions '''
    def test_proportional_default_fields(self):
        ''' Tests custom calc proportion function using default fields
            when no options are sent '''
        self.assertEqual(
            ViewConfReader.get_proportional_indicator_uf({
                "vl_indicador": 110,
                "media_uf": 100
            }),
            np.log(1.11)
        )

    def test_proportional(self):
        ''' Tests custom calc proportion function with custom fields '''
        self.assertEqual(
            ViewConfReader.get_proportional_indicator_uf(
                {"myfield": 110, "mymeanfield": 100},
                campo="myfield",
                media="mymeanfield"
            ),
            np.log(1.11)
        )

class ViewConfGenerateColumnsTest(unittest.TestCase):
    ''' Test behaviours linked to adding columns do dataframes as
        defined by calc and format attributes in YAML '''
    SAMPLE_DATAFRAME = [
        {"vl_indicador": 110, "media_uf": 100, "to_format": "1", "to_format_2": "1.1"},
        {"vl_indicador": 220, "media_uf": 200, "to_format": "2", "to_format_2": "2.2"}
    ]
    def test_proportional_default_fields(self):
        ''' Tests custom calc and formatting column generators '''
        options = {
            "api": {
                "options": {
                    "formatters": [
                        {"id": "to_format", "format": 'inteiro'},
                        {"id": "to_format_2", "format": 'real', "precision": 2},
                    ],
                    "calcs": [
                        {
                            "id": "deviation",
                            "function": "get_proportional_indicator_uf",
                            "fn_args": [
                                {"fixed": 'vl_indicador'},
                                {"fixed": 'media_br'}
                            ]
                        },
                        {
                            "id": "deviation_again",
                            "function": "get_proportional_indicator_uf",
                            "fn_args": [
                                {"fixed": 'vl_indicador'},
                                {"fixed": 'media_br'}
                            ]
                        }
                    ]
                }
            }
        }
        result = ViewConfReader.generate_columns(
            pd.DataFrame(self.SAMPLE_DATAFRAME),
            options
        )
        expected = [
            {
                "vl_indicador": 110, "media_uf": 100, "to_format": "1", "to_format_2": "1.1",
                "calc_deviation": 0.10436001532424286,
                "calc_deviation_again": 0.10436001532424286,
                "fmt_to_format": "1",
                "fmt_to_format_2": "1,1"
            },
            {
                "vl_indicador": 220, "media_uf": 200, "to_format": "2", "to_format_2": "2.2",
                "calc_deviation": 0.10436001532424286,
                "calc_deviation_again": 0.10436001532424286,
                "fmt_to_format": "2",
                "fmt_to_format_2": "2,2"
            }
        ]
        self.assertEqual(result.to_dict(orient="records"), expected)

    def test_invalid_calc(self):
        ''' Tests if custom calc function is ignored if it doesn't exist '''
        options = {"api": {"options": {"calcs": [{
            "id": "deviation",
            "function": "mynonexistingfunction",
            "fn_args": [
                {"fixed": 'vl_indicador'},
                {"fixed": 'media_br'}
            ]
        }]}}}
        result = ViewConfReader.generate_columns(
            pd.DataFrame(self.SAMPLE_DATAFRAME),
            options
        )
        self.assertEqual(result.to_dict(orient="records"), self.SAMPLE_DATAFRAME)

class ViewConfGetCardDescriptorTest(unittest.TestCase):
    ''' Test behaviours linked to getting the card descriptor from YAML '''
    def test_empty_yaml(self):
        ''' Tests if an empty yaml results in None descriptor '''
        self.assertEqual(
            StubViewConfReader.get_card_descriptor(
                'br', None, None, 'empty', 'right'
            ),
            None
        )

    def test_no_sections_yaml(self):
        ''' Tests if a yaml with no sections results in None descriptor '''
        self.assertEqual(
            StubViewConfReader.get_card_descriptor(
                'br', None, None, 'no_sections', 'right'
            ),
            None
        )

    def test_no_cards_yaml(self):
        ''' Tests if a yaml with no cards results in None descriptor '''
        self.assertEqual(
            StubViewConfReader.get_card_descriptor(
                'br', None, None, 'no_cards', 'right'
            ),
            None
        )

    def test_empty_cards_yaml(self):
        ''' Tests if a yaml with empty cards attribute results in None descriptor '''
        self.assertEqual(
            StubViewConfReader.get_card_descriptor(
                'br', None, None, 'empty_cards', 'right'
            ),
            None
        )

    def test_card_not_found_yaml(self):
        ''' Tests if a yaml with no cards with the given id results in None descriptor '''
        self.assertEqual(
            StubViewConfReader.get_card_descriptor(
                'br', None, None, 'card_not_found', 'right'
            ),
            None
        )

    def test_card_yaml(self):
        ''' Tests if descriptor is returned correctly '''
        self.assertEqual(
            StubViewConfReader.get_card_descriptor(
                'br', None, None, 'card_exists', 'right'
            ),
            {"id": "right"}
        )

class ViewConfGetLayersNamesTest(unittest.TestCase):
    ''' Test behaviours linked to getting layer names from headers '''
    def test_layer_names_no_headers(self):
        ''' Tests if an empty dictionary is returned when no header is sent '''
        self.assertEqual(
            ViewConfReader.get_layers_names(None),
            {}
        )

    def test_layer_names_empty_headers(self):
        ''' Tests if an empty dictionary is returned when an empty header is sent '''
        self.assertEqual(
            ViewConfReader.get_layers_names([]),
            {}
        )

    def test_layer_names_no_valid_layer_in_header(self):
        ''' Tests if an empty list is returned when no item in header
            has an identifier '''
        self.assertEqual(
            ViewConfReader.get_layers_names([
                {'value': 'layer_1', 'text': 'layer 1'},
                {'value': 'layer_2', 'text': 'layer 2'}
            ]),
            {}
        )

    def test_layer_names(self):
        ''' Tests if headers are decoded to layer names adequately '''
        self.assertEqual(
            ViewConfReader.get_layers_names([
                {'layer_id': 'layer_1', 'text': 'layer 1'},
                {'text': 'invalid layer', 'value': 'value_field'},
                {'layer_id': 'layer_2', 'text': 'layer 2'}
            ]),
            {'layer_1': 'layer 1', 'layer_2': 'layer 2'}
        )

class ViewConfGetAttributeFromCharttSpecTest(unittest.TestCase):
    ''' Test behaviours linked to getting an atttribute from chart options '''
    def test_no_options(self):
        ''' Tests if no attribute is returned if no options and no default are
            given '''
        self.assertEqual(
            ViewConfReader.get_attribute_from_chart_spec(None, 'colorArray'),
            None
        )

    def test_no_attribute(self):
        ''' Tests if no attribute is returned if no attribute is given '''
        self.assertEqual(
            ViewConfReader.get_attribute_from_chart_spec({}, None, 'default'),
            None
        )

    def test_no_options_with_default(self):
        ''' Tests if default value is returned if no options are given '''
        self.assertEqual(
            ViewConfReader.get_attribute_from_chart_spec(None, 'colorArray', 'default'),
            'default'
        )

    def test_fetch_existing_attribute_among_multiple(self):
        ''' Tests if existing attribute is returned from multiple charts'''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [
                {"id": "wrong", "options": {'colorArray': ['blue', 'purple', 'orange']}},
                {"id": "right", "options": {'colorArray': ['red', 'yellow', 'green']}}
            ],
            "chart_id": "right"
        }
        self.assertEqual(
            ViewConfReader.get_attribute_from_chart_spec(
                options_from_yaml,
                'colorArray',
                'default'
            ),
            ['red', 'yellow', 'green']
        )

    def test_fetch_existing_attribute_from_single(self):
        ''' Tests if existing attribute is returned from simple card '''
        options_from_yaml = {
            "chart_options": {'colorArray': ['blue', 'purple', 'orange']}
        }
        self.assertEqual(
            ViewConfReader.get_attribute_from_chart_spec(
                options_from_yaml,
                'colorArray',
                'default'
            ),
            ['blue', 'purple', 'orange']
        )

    def test_fetch_existing_attribute_among_multiple_dafault(self):
        ''' Tests if existing attribute is returned from multiple charts'''
        options_from_yaml = {
            "type": "multiple-charts",
            "charts": [
                {"id": "wrong", "options": {'colorArray': ['blue', 'purple', 'orange']}},
                {"id": "right", "options": {'colorArray': ['red', 'yellow', 'green']}}
            ],
            "chart_id": "missing"
        }
        self.assertEqual(
            ViewConfReader.get_attribute_from_chart_spec(
                options_from_yaml,
                'colorArray',
                'default'
            ),
            'default'
        )
