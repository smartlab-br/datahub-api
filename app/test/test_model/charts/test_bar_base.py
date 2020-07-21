'''Main tests in API'''
import unittest
import pandas as pd
from bokeh.plotting import figure
from model.charts.bar import Bar

class BarBaseTest(unittest.TestCase):
    ''' Test behaviours linked to foundational bar charts capabilities '''
    def test_mandatory_implementation(self):
        ''' Tests if an exception is raised when no implementation is found
            for draw method '''
        self.assertRaises(NotImplementedError, Bar().draw, {}, {})

    def test_get_fill_color(self):
        ''' Tests if an element from collor array is correctly fetched '''
        options_from_yaml = {'chart_options': {'colorArray': ['red', 'yellow', 'green']}}
        self.assertEqual(
            Bar().get_fill_color(1, options_from_yaml),
            'yellow'
        )

class BarLegendNamesTest(unittest.TestCase):
    ''' Test behaviours linked to fetching legend names for series '''
    def test_legend_names_no_options(self):
        ''' Tests if no legend names are returned when there's no option '''
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            Bar().get_legend_names(dataframe, None),
            {}
        )
    
    def test_legend_names_no_chart_options(self):
        ''' Tests if no legend names are returned when there's no chart_options '''
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            Bar().get_legend_names(dataframe, {}),
            {}
        )

    def test_legend_names_no_dataframe(self):
        ''' Tests if no legend names are returned when there's no dataframe '''
        options_from_yaml = {'chart_options': {'id': 'idx'}}
        self.assertEqual(
            Bar().get_legend_names(None, options_from_yaml),
            {}
        )
    
    def test_legend_names_empty_dataframe(self):
        ''' Tests if no legend names are returned when the dataframe is empty '''
        options_from_yaml = {'chart_options': {'id': 'idx'}}
        self.assertEqual(
            Bar().get_legend_names(pd.DataFrame([]), options_from_yaml),
            {}
        )

    def test_legend_names_no_id_field(self):
        ''' Tests if no legend names are returned when no ID field is given '''
        options_from_yaml = {'chart_options': {'legend_field': 'lgnd'}}
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            Bar().get_legend_names(dataframe, options_from_yaml),
            {}
        )

    def test_legend_names_no_label_field(self):
        ''' Tests if legend names are built from series ID in the dataframe '''
        options_from_yaml = {'chart_options': {'id': 'idx'}}
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            Bar().get_legend_names(dataframe, options_from_yaml),
            {'A': 'A', 'B': 'B'}
        )

    def test_legend_names(self):
        ''' Tests if legend names are built from series ID in the dataframe, with
            a mirror legend name specified '''
        options_from_yaml = {'chart_options': {'legend_field': 'lgnd', 'id': 'idx'}}
        dataframe = pd.DataFrame([
            {'idx': 'A', 'lgnd': 'A_lbl'},
            {'idx': 'B', 'lgnd': 'B_lbl'}
        ])
        self.assertEqual(
            Bar().get_legend_names(dataframe, options_from_yaml),
            {'A': 'A_lbl', 'B': 'B_lbl'}
        )

class BarTooltipTest(unittest.TestCase):
    ''' Test behaviours linked to creating tooltip structure '''
    def test_tooltip_no_option(self):
        ''' Tests if default tooltip is returned when no option is given '''
        self.assertEqual(
            Bar().build_tooltip(None),
            'Tooltip!'
        )
    
    def test_tooltip_no_headers(self):
        ''' Tests if default tooltip is returned when no headers are given '''
        self.assertEqual(
            Bar().build_tooltip({}),
            'Tooltip!'
        )
        
    def test_tooltip(self):
        ''' Tests if tooltips are built correctly '''
        options_from_yaml = {'headers': [
            {'text': 'Value A:', 'value': 'field_a'},
            {'text': 'Value B:', 'value': 'field_b'}
        ]}
        self.maxDiff = None
        self.assertEqual(
            Bar().build_tooltip(options_from_yaml),
            '<table>'
                '<tr style="text-align: left;"><th style="padding: 4px; padding-right: 10px;">Value A:</th><td style="padding: 4px;">@field_a</td></tr>'
                '<tr style="text-align: left;"><th style="padding: 4px; padding-right: 10px;">Value B:</th><td style="padding: 4px;">@field_b</td></tr>'
            '</table>'
        )

class BarChartConfigTest(unittest.TestCase):
    ''' Test behaviours linked to foundational bar charts capabilities '''
    def test_bar_chart_config_no_option(self):
        ''' Tests if default config is set when no option is given '''
        chart = Bar().chart_config(figure(), None)
        
        self.assertEqual(chart.axis.major_label_text_font, ['Palanquin','Palanquin'])
        self.assertEqual(chart.axis.major_tick_line_color, [None, None])
        self.assertEqual(chart.axis.minor_tick_line_color, [None, None])
    
        self.assertEqual(chart.xgrid.grid_line_color, None)
        self.assertEqual(chart.ygrid.grid_line_color, None)
    
        # self.assertEqual(chart.legend.label_text_font, 'Palanquin')
        # self.assertEqual(chart.legend.location, 'top_right')
        # self.assertEqual(chart.legend.orientation, 'vertical')
    
        self.assertEqual(chart.xaxis.visible, False)
        self.assertEqual(chart.yaxis.visible, False)
    
    def test_bar_chart_config_no_chart_option(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Bar().chart_config(figure(), {})
        
        self.assertEqual(chart.axis.major_label_text_font, ['Palanquin','Palanquin'])
        self.assertEqual(chart.axis.major_tick_line_color, [None, None])
        self.assertEqual(chart.axis.minor_tick_line_color, [None, None])
    
        self.assertEqual(chart.xgrid.grid_line_color, None)
        self.assertEqual(chart.ygrid.grid_line_color, None)
    
        # self.assertEqual(chart.legend.label_text_font, 'Palanquin')
        # self.assertEqual(chart.legend.location, 'top_right')
        # self.assertEqual(chart.legend.orientation, 'vertical')
    
        self.assertEqual(chart.xaxis.visible, False)
        self.assertEqual(chart.yaxis.visible, False)
        
    def test_bar_chart_config(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Bar().chart_config(
            figure(),
            {'chart_options': {'show_x_axis': False, 'show_y_axis': True}})
        
        self.assertEqual(chart.axis.major_label_text_font, ['Palanquin','Palanquin'])
        self.assertEqual(chart.axis.major_tick_line_color, [None, None])
        self.assertEqual(chart.axis.minor_tick_line_color, [None, None])
    
        self.assertEqual(chart.xgrid.grid_line_color, None)
        self.assertEqual(chart.ygrid.grid_line_color, None)
    
        # self.assertEqual(chart.legend.label_text_font, 'Palanquin')
        # self.assertEqual(chart.legend.location, 'top_right')
        # self.assertEqual(chart.legend.orientation, 'vertical')
    
        self.assertEqual(chart.xaxis.visible, False)
        self.assertEqual(chart.yaxis.visible, True)
