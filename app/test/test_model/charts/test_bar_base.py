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

class BarChartConfigTest(unittest.TestCase):
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
