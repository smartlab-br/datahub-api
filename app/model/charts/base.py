''' Basic chart classes and methods '''
import pandas as pd

class BaseChart():
    ''' Base Chart class '''

class BaseCartesianChart(BaseChart):
    ''' Base Cartesian Chart class '''
    @staticmethod
    def pivot_dataframe(dataframe, options):
        ''' Pivot dataframe to create series in charts '''
        if options is None:
            return None
        if dataframe is None:
            return {}
        src = dataframe.copy()
        src = pd.pivot_table(
            src,
            values=[options.get('chart_options').get('y')],
            columns=options.get('chart_options').get('id'),
            index=options.get('chart_options').get('x'),
            aggfunc="sum",
            fill_value=0
        )
        src.columns = src.columns.droplevel()
        src = src.reset_index()
        src[options.get('chart_options').get('x')] = src[options.get('chart_options').get('x')].astype(str)
        return {col:list(src[col]) for col in src.columns}
