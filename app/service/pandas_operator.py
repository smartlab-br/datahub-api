''' Module for sequence of pandas datasets manipulations '''
import pandas as pd
import requests
import yaml

from flask import current_app as app

class PandasOperator():
    ''' Class for sequence of pandas datasets manipulations '''
    @classmethod
    def get_cut_pattern(cls, pattern_id):
        ''' Gets patterns from GIT '''
        return yaml.load(requests.get(
            app.config['GIT_VIEWCONF_BASE_URL'].format('options', 'cut', pattern_id),
            verify=False
        ).content)

    @classmethod
    def operate(cls, dataset, operation, categories):
        ''' Runs an aoperation, that functions as a macro for building additional columns in
            a dataset '''
        if operation == 'rerank':
            return cls.rerank(dataset)
        if 'cut' in operation: # Verifica se a operação é de CUT
            # Segrega a identificação do padrão de CUT
            pattern = operation.split('-')
            if len(pattern) < 2:
                return dataset
            target = pattern[1]
            pattern_id = 'default'
            if len(pattern) > 2:
                pattern_id = pattern[2]
            # Gets patterns from GIT
            return cls.cut(
                dataset,
                target,
                cls.get_cut_pattern(pattern_id),
                categories
            )
        return dataset

    @staticmethod
    def rerank(dataset):
        ''' Gets rankings '''
        # Architecture step: [1] 2 N
        # (1) Funciona apenas para atender a uma demanda de indicadores temáticos do
        # trabalho escravo
        rules = {
            'br': 'cd_indicador',
            'uf': ['cd_uf', 'cd_indicador']
        }

        for key, value in rules.items():
            rank_key = f'rerank_rank_{key}'
            dataset[rank_key] = dataset.groupby(value)['agr_sum_vl_indicador'].rank(
                method='min', ascending=False
            )
            sum_key = f'agr_sum_vl_indicador_{key}'
            dataset[sum_key] = dataset.groupby(value)['agr_sum_vl_indicador'].transform('sum')
            perc_key = f'rerank_perc_{key}'
            dataset[perc_key] = dataset['agr_sum_vl_indicador'] / dataset[sum_key]

        return dataset

    @staticmethod
    def cut(dataset, target, options, categories):
        ''' Cuts the dataset, placing items on bins, based on config '''
        # Gets the array of binned-data
        cut_vals = pd.cut(
            dataset[target],
            options['bins'],
            right=options.get('right', True),
            labels=options.get('labels')
        )
        # Adds resulting vector to dataset
        dataset['cut'] = cut_vals

        # Reaggregates the dataset
        local_cats = categories.copy()
        local_cats.remove(target)
        local_cats.append('cut')
        dataset = dataset.groupby(local_cats).sum()
        dataset = dataset.drop([target], axis=1)
        dataset.reset_index(level=0, inplace=True)

        # Adds a row number to the final result
        dataset['row_id'] = dataset.reset_index().index

        return dataset
