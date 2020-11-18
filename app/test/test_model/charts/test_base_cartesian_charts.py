'''Main tests in API'''
import unittest
import pandas as pd
from bokeh.plotting import figure
from model.charts.base import BaseCartesianChart

class BaseCartesianChartPivotTest():
# class BaseCartesianChartPivotTest(unittest.TestCase):
    ''' Test behaviours linked to pivoting a dataframe to build the chart's
        series as a dictionary '''
    def test_pivoting_no_options(self):
        ''' Test if None is returned when no option is given '''
        self.assertEqual(
            BaseCartesianChart.pivot_dataframe(pd.DataFrame([]), None),
            None
        )

    def test_pivoting_no_dataframe(self):
        ''' Test if an empty dictionary is returned when no dataframe is given '''
        self.assertEqual(
            BaseCartesianChart.pivot_dataframe(None, {}),
            {}
        )

    def test_pivoting(self):
        ''' Test if pivoting works '''
        dataframe = pd.DataFrame([
            {'idx': 'a', 'x': 2000, 'y': 0},
            {'idx': 'a', 'x': 2001, 'y': 1},
            {'idx': 'a', 'x': 2002, 'y': 2},
            {'idx': 'b', 'x': 2000, 'y': 3},
            {'idx': 'b', 'x': 2001, 'y': 4},
            {'idx': 'b', 'x': 2002, 'y': 5},
        ])
        options = {'chart_options': {'x': 'x', 'y': 'y', 'id': 'idx'}}
        self.assertEqual(
            BaseCartesianChart.pivot_dataframe(dataframe, options),
            {'x': ['2000', '2001', '2002'], 'a': [0, 1, 2], 'b': [3, 4, 5]}
        )

class BaseCartesianChartConfigTest():
# class BaseCartesianChartConfigTest(unittest.TestCase):
    ''' Test behaviours linked to foundational bar charts capabilities '''
    def test_cartesian_chart_config_no_option(self):
        ''' Tests if default config is set when no option is given '''
        chart = BaseCartesianChart().chart_config(figure(), None)

        self.assertEqual(chart.axis.major_label_text_font, ['Palanquin', 'Palanquin'])
        self.assertEqual(chart.axis.major_tick_line_color, [None, None])
        self.assertEqual(chart.axis.minor_tick_line_color, [None, None])

        self.assertEqual(chart.xgrid.grid_line_color, None)
        self.assertEqual(chart.ygrid.grid_line_color, None)

        # self.assertEqual(chart.legend.label_text_font, 'Palanquin')
        # self.assertEqual(chart.legend.location, 'top_right')
        # self.assertEqual(chart.legend.orientation, 'vertical')

    def test_bar_chart_config_no_chart_option(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = BaseCartesianChart().chart_config(figure(), {})

        self.assertEqual(chart.axis.major_label_text_font, ['Palanquin', 'Palanquin'])
        self.assertEqual(chart.axis.major_tick_line_color, [None, None])
        self.assertEqual(chart.axis.minor_tick_line_color, [None, None])

        self.assertEqual(chart.xgrid.grid_line_color, None)
        self.assertEqual(chart.ygrid.grid_line_color, None)

        # self.assertEqual(chart.legend.label_text_font, 'Palanquin')
        # self.assertEqual(chart.legend.location, 'top_right')
        # self.assertEqual(chart.legend.orientation, 'vertical')

    def test_bar_chart_config(self):
        ''' Tests if default config is set when no chart_option is given '''
        chart = BaseCartesianChart().chart_config(
            figure(),
            {'chart_options': {'show_x_axis': False, 'show_y_axis': True}})

        self.assertEqual(chart.axis.major_label_text_font, ['Palanquin', 'Palanquin'])
        self.assertEqual(chart.axis.major_tick_line_color, [None, None])
        self.assertEqual(chart.axis.minor_tick_line_color, [None, None])

        self.assertEqual(chart.xgrid.grid_line_color, None)
        self.assertEqual(chart.ygrid.grid_line_color, None)

        # self.assertEqual(chart.legend.label_text_font, 'Palanquin')
        # self.assertEqual(chart.legend.location, 'top_right')
        # self.assertEqual(chart.legend.orientation, 'vertical')
