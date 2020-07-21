'''Main tests in API'''
import unittest
import pandas as pd
from model.charts.base import BaseCartesianChart

class BaseCartesianChartPivotTest(unittest.TestCase):
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

    def test_get_fill_color(self):
        ''' Tests if an element from collor array is correctly fetched '''
        options_from_yaml = {'chart_options': {'colorArray': ['red', 'yellow', 'green']}}
        self.assertEqual(
            BaseCartesianChart.get_fill_color(1, options_from_yaml),
            'yellow'
        )

class BarLegendNamesTest(unittest.TestCase):
    ''' Test behaviours linked to fetching legend names for series '''
    def test_legend_names_no_options(self):
        ''' Tests if no legend names are returned when there's no option '''
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            BaseCartesianChart.get_legend_names(dataframe, None),
            {}
        )
    
    def test_legend_names_no_chart_options(self):
        ''' Tests if no legend names are returned when there's no chart_options '''
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            BaseCartesianChart.get_legend_names(dataframe, {}),
            {}
        )

    def test_legend_names_no_dataframe(self):
        ''' Tests if no legend names are returned when there's no dataframe '''
        options_from_yaml = {'chart_options': {'id': 'idx'}}
        self.assertEqual(
            BaseCartesianChart.get_legend_names(None, options_from_yaml),
            {}
        )
    
    def test_legend_names_empty_dataframe(self):
        ''' Tests if no legend names are returned when the dataframe is empty '''
        options_from_yaml = {'chart_options': {'id': 'idx'}}
        self.assertEqual(
            BaseCartesianChart.get_legend_names(pd.DataFrame([]), options_from_yaml),
            {}
        )

    def test_legend_names_no_id_field(self):
        ''' Tests if no legend names are returned when no ID field is given '''
        options_from_yaml = {'chart_options': {'legend_field': 'lgnd'}}
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            BaseCartesianChart.get_legend_names(dataframe, options_from_yaml),
            {}
        )

    def test_legend_names_no_label_field(self):
        ''' Tests if legend names are built from series ID in the dataframe '''
        options_from_yaml = {'chart_options': {'id': 'idx'}}
        dataframe = pd.DataFrame([{'idx': 'A'}, {'idx': 'B'}])
        self.assertEqual(
            BaseCartesianChart.get_legend_names(dataframe, options_from_yaml),
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
            BaseCartesianChart.get_legend_names(dataframe, options_from_yaml),
            {'A': 'A_lbl', 'B': 'B_lbl'}
        )

class BarTooltipTest(unittest.TestCase):
    ''' Test behaviours linked to creating tooltip structure '''
    def test_tooltip_no_option(self):
        ''' Tests if default tooltip is returned when no option is given '''
        self.assertEqual(
            BaseCartesianChart.build_tooltip(None),
            'Tooltip!'
        )
    
    def test_tooltip_no_headers(self):
        ''' Tests if default tooltip is returned when no headers are given '''
        self.assertEqual(
            BaseCartesianChart.build_tooltip({}),
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
            BaseCartesianChart.build_tooltip(options_from_yaml),
            '<table>'
                '<tr style="text-align: left;"><th style="padding: 4px; padding-right: 10px;">Value A:</th><td style="padding: 4px;">@field_a</td></tr>'
                '<tr style="text-align: left;"><th style="padding: 4px; padding-right: 10px;">Value B:</th><td style="padding: 4px;">@field_b</td></tr>'
            '</table>'
        )