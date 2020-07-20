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
