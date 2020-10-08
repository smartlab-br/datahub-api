'''Main tests in API'''
import unittest
from bokeh.plotting import figure
from model.charts.line import Line

class LineChartConfigTest(unittest.TestCase):
    ''' Test behaviours linked to foundational bar charts capabilities '''
    def test_bar_chart_config_no_option(self):
        ''' Tests if default config is set when no option is given '''
        chart = Line().chart_config(figure(), None)
        self.assertEqual(chart.xaxis.visible, True)
        self.assertEqual(chart.yaxis.visible, True)

    def test_bar_chart_config_no_chart_option(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Line().chart_config(figure(), {})
        self.assertEqual(chart.xaxis.visible, True)
        self.assertEqual(chart.yaxis.visible, True)

    def test_bar_chart_config(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Line().chart_config(
            figure(),
            {'chart_options': {'show_x_axis': False, 'show_y_axis': True}})
        self.assertEqual(chart.xaxis.visible, False)
        self.assertEqual(chart.yaxis.visible, True)

    def test_bar_chart_config_reverse_visibility(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Line().chart_config(
            figure(),
            {'chart_options': {'show_x_axis': True, 'show_y_axis': False}})
        self.assertEqual(chart.xaxis.visible, True)
        self.assertEqual(chart.yaxis.visible, False)
