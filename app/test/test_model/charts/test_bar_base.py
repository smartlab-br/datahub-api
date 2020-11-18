'''Main tests in API'''
import unittest
from bokeh.plotting import figure
from model.charts.bar import Bar, BarPyramid

class BarBaseTest():
# class BarBaseTest(unittest.TestCase):
    ''' Test behaviours linked to foundational bar charts capabilities '''
    def test_mandatory_implementation(self):
        ''' Tests if an exception is raised when no implementation is found
            for draw method '''
        self.assertRaises(NotImplementedError, Bar().draw, {}, {})

    def test_mandatory_implementation_pyramid(self):
        ''' Tests if an exception is raised when no implementation is found
            for create_bar method '''
        self.assertRaises(NotImplementedError, BarPyramid().create_bar, {}, {})

class BarChartConfigTest():
# class BarChartConfigTest(unittest.TestCase):
    ''' Test behaviours linked to foundational bar charts capabilities '''
    def test_bar_chart_config_no_option(self):
        ''' Tests if default config is set when no option is given '''
        chart = Bar().chart_config(figure(), None)
        self.assertEqual(chart.xaxis.visible, False)
        self.assertEqual(chart.yaxis.visible, False)

    def test_bar_chart_config_no_chart_option(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Bar().chart_config(figure(), {})
        self.assertEqual(chart.xaxis.visible, False)
        self.assertEqual(chart.yaxis.visible, False)

    def test_bar_chart_config(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Bar().chart_config(
            figure(),
            {'chart_options': {'show_x_axis': False, 'show_y_axis': True}})
        self.assertEqual(chart.xaxis.visible, False)
        self.assertEqual(chart.yaxis.visible, True)

    def test_bar_chart_config_reverse_visibility(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = Bar().chart_config(
            figure(),
            {'chart_options': {'show_x_axis': True, 'show_y_axis': False}})
        self.assertEqual(chart.xaxis.visible, True)
        self.assertEqual(chart.yaxis.visible, False)
