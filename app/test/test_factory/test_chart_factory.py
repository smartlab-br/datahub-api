'''Main tests in API'''
import unittest
from factory.chart import ChartFactory
from model.charts.maps.choropleth import Choropleth
from model.charts.maps.heat import Heat
from model.charts.maps.cluster import Cluster
from model.charts.maps.bubbles import Bubbles
from model.charts.bar import BarHorizontal, BarVertical, \
    BarHorizontalStacked, BarVerticalStacked, \
    BarHorizontalPyramid, BarVerticalPyramid
from model.charts.line import Line, LineArea

class ChartFactoryCreateTest(unittest.TestCase):
    ''' Test behaviours linked to chart instantiation '''
    def test_instantiation_choropleth(self):
        ''' Tests if create returns a Choropleth '''
        chart = ChartFactory().create({"chart_type": "MAP_TOPOJSON"},[])
        self.assertTrue(isinstance(chart, Choropleth))

    def test_instantiation_heat(self):
        ''' Tests if create returns a Heat '''
        chart = ChartFactory().create({"chart_type": "MAP_HEAT"},[])
        self.assertTrue(isinstance(chart, Heat))

    def test_instantiation_cluster(self):
        ''' Tests if create returns a Cluster '''
        chart = ChartFactory().create({"chart_type": "MAP_CLUSTER"},[])
        self.assertTrue(isinstance(chart, Cluster))

    def test_instantiation_bubbles(self):
        ''' Tests if create returns a Bubbles '''
        chart = ChartFactory().create({"chart_type": "MAP_BUBBLES"},[])
        self.assertTrue(isinstance(chart, Bubbles))

    def test_instantiation_line(self):
        ''' Tests if create returns a line chart '''
        chart = ChartFactory().create({"chart_type": "LINE"},[])
        self.assertTrue(isinstance(chart, Line))

    def test_instantiation_bar_horizontal(self):
        ''' Tests if create returns a bar chart '''
        chart = ChartFactory().create({"chart_type": "BAR"},[])
        self.assertTrue(isinstance(chart, BarHorizontal))

class ChartFactorySelectBarTest(unittest.TestCase):
    ''' Test behaviours linked to bar chart instantiation '''
    def test_instantiation_bar_horizontal_as_default(self):
        ''' Tests if create returns a horizontal bar if no orientation is given '''
        chart = ChartFactory().create({"chart_type": "BAR"},[])
        self.assertTrue(isinstance(chart, BarHorizontal))

    def test_instantiation_bar_horizontal(self):
        ''' Tests if create returns a horizontal bar '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "horizontal"}
        },[])
        self.assertTrue(isinstance(chart, BarHorizontal))

    def test_instantiation_bar_vertical(self):
        ''' Tests if create returns a vertical bar '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "vertical"}
        },[])
        self.assertTrue(isinstance(chart, BarVertical))

    def test_instantiation_bar_horizontal_stacked_as_default(self):
        ''' Tests if create returns a stacked horizontal bar if no orientation is given '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"stacked": True}
        },[])
        self.assertTrue(isinstance(chart, BarHorizontalStacked))

    def test_instantiation_bar_horizontal_stacked(self):
        ''' Tests if create returns a stacked horizontal bar '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "horizontal", "stacked": True}
        },[])
        self.assertTrue(isinstance(chart, BarHorizontalStacked))

    def test_instantiation_bar_vertical_stacked(self):
        ''' Tests if create returns a stacked vertical stacked bar '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "vertical", "stacked": True}
        },[])
        self.assertTrue(isinstance(chart, BarVerticalStacked))

    def test_instantiation_bar_horizontal_pyramid_as_default(self):
        ''' Tests if create returns a horizontal pyramid if no orientation is given '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"left": "neg_series"}
        },[])
        self.assertTrue(isinstance(chart, BarHorizontalPyramid))

    def test_instantiation_bar_horizontal_pyramid(self):
        ''' Tests if create returns a horizontal pyramid '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "horizontal", "left": "neg_series"}
        },[])
        self.assertTrue(isinstance(chart, BarHorizontalPyramid))

    def test_instantiation_bar_vertical_pyramid(self):
        ''' Tests if create returns a vertical pyramid '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "vertical", "left": "neg_series"}
        },[])
        self.assertTrue(isinstance(chart, BarVerticalPyramid))

    def test_instantiation_bar_horizontal_pyramid_precedence_as_default(self):
        ''' Tests if create returns a horizontal pyramid if no orientation is given '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"left": "neg_series", "stacked": True}
        },[])
        self.assertTrue(isinstance(chart, BarHorizontalPyramid))

    def test_instantiation_bar_horizontal_pyramid_precedence(self):
        ''' Tests if create returns a horizontal pyramid '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "horizontal", "left": "neg_series", "stacked": True}
        },[])
        self.assertTrue(isinstance(chart, BarHorizontalPyramid))

    def test_instantiation_bar_vertical_pyramid_precedence(self):
        ''' Tests if create returns a vertical pyramid '''
        chart = ChartFactory().create({
            "chart_type": "BAR",
            "chart_options": {"orientation": "vertical", "left": "neg_series", "stacked": True}
        },[])
        self.assertTrue(isinstance(chart, BarVerticalPyramid))

class ChartFactorySelectLineTest(unittest.TestCase):
    ''' Test behaviours linked to line chart instantiation '''
    def test_instantiation_line_as_default(self):
        ''' Tests if create returns a line if no stacked flag is given '''
        chart = ChartFactory().create({"chart_type": "LINE"},[])
        self.assertTrue(isinstance(chart, Line))

    def test_instantiation_line(self):
        ''' Tests if create returns a line chart '''
        chart = ChartFactory().create({
            "chart_type": "LINE",
            "chart_options": {"stacked": False}
        },[])
        self.assertTrue(isinstance(chart, Line))

    def test_instantiation_area(self):
        ''' Tests if create returns a area chart '''
        chart = ChartFactory().create({
            "chart_type": "LINE",
            "chart_options": {"stacked": True}
        },[])
        self.assertTrue(isinstance(chart, LineArea))
