''' Module for formatting numbers '''
from math import floor, isnan
from babel.numbers import format_number, format_decimal

class NumberFormatter():
    ''' Service that formats a number into a HTML snippet '''
    @classmethod
    def format(cls, valor, options):
        ''' Method that formats a number into a HTML snippet '''
        # Escapes with default, when there's no value
        try:
            valor = cls.validate(valor)
        except ValueError:
            if 'default' in options and options['default'] is not None:
                return options['default']
            return '-'

        if 'format' not in options:
            return valor

        # Sets default values
        (
            precision, multiplier, collapse, str_locale, n_format, ui_tags
        ) = cls.load_defaults(options)

        # Applies multiplier and sets precision
        valor = cls.apply_multiplier(valor, multiplier)
        precision = cls.precision_override(n_format, collapse, precision)

        # Adjusts collapsed value
        (valor_c, suffix, magnitude) = cls.get_value_suffix(valor, n_format, collapse, ui_tags)

        # Changes format according to actual collapsing
        if collapse is not None and magnitude is not None and magnitude > 0:
            if 'precision' in collapse:
                precision = collapse['precision']
            if 'format' in collapse:
                n_format = collapse['format']
            if 'uiTags' in collapse:
                ui_tags = collapse['uiTags']

        if cls.is_integer_after_collapse(n_format, valor, valor_c, precision, collapse):
            # Se o número for efetivamente um inteiro e não tiver
            # collapse, retira a casa decimal
            precision = 0

        valor_c = round(valor_c, precision)
        vlr_fmt = cls.format_with_locale(n_format, valor_c, str_locale)

        return cls.get_unit_prefix(n_format, ui_tags) + vlr_fmt + suffix

    @staticmethod
    def validate(valor):
        ''' Returns converted, valid, number '''
        if isinstance(valor, str):
            return float(valor)
        if valor is None or isnan(valor):
            raise ValueError
        return valor

    @staticmethod
    def is_integer_after_collapse(n_format, valor, valor_c, precision, collapse):
        ''' Checks if after collapsing the number is actually an integer '''
        if n_format == 'inteiro':
            return True
        if n_format in ['real', 'porcentagem', 'monetario']:
            if (valor - floor(valor))*(10 ** precision) == 0.0 and not collapse:
                return True
            if (valor_c - floor(valor_c))*(10 ** precision) == 0.0 and collapse:
                return True
        return False

    @staticmethod
    def load_defaults(options):
        ''' Loads default values for options '''
        precision = None
        if 'precision' in options:
            precision = options['precision']

        multiplier = 1
        if 'multiplier' in options:
            multiplier = int(options['multiplier'])

        collapse = None
        if 'collapse' in options:
            collapse = options['collapse']

        str_locale = "pt_br"
        if 'str_locale' in options:
            str_locale = options['str_locale']

        ui_tags = True
        if 'uiTags' in options:
            ui_tags = options['uiTags']

        n_format = options['format']

        return (precision, multiplier, collapse, str_locale, n_format, ui_tags)

    @staticmethod
    def get_unit_prefix(n_format, ui_tags=True):
        ''' Define um prefixo de unidade '''
        if n_format == 'monetario':
            if ui_tags:
                return "<span>R$</span>"
            return "R$"
        return ''

    @staticmethod
    def get_value_suffix(valor, n_format, collapse, ui_tags=True):
        ''' Verifica a ordem de grandeza do número, para poder reduzir o tamanho da string '''
        if n_format == 'porcentagem':
            if ui_tags:
                return (valor, "<span>%</span>", None)
            return (valor, "%", None)
        if collapse is not None:
            magnitude = floor((len(str(floor(abs(valor)))) - 1)/3)

            if magnitude > 0 and 'uiTags' in collapse:
                ui_tags = collapse['uiTags']

            if ui_tags:
                magnitudes = [
                    '',
                    '<span>mil</span>',
                    '<span>mi</span>',
                    '<span>bi</span>',
                    '<span>tri</span>'
                ]
            else:
                magnitudes = ['', 'mil', 'mi', 'bi', 'tri']

            if magnitude > 0:
                valor = valor / (10 ** (magnitude * 3))
            return (valor, magnitudes[magnitude], magnitude)
        return (valor, '', None)

    @staticmethod
    def apply_multiplier(valor, multiplier):
        ''' Applies multiplier to value '''
        if isinstance(valor, int):
            return valor * multiplier
        if isinstance(valor, float):
            return valor * float(multiplier)
        return float(valor) * float(multiplier)

    @staticmethod
    def precision_override(n_format, collapse, precision):
        ''' Precision overriding '''
        if ((n_format in ['porcentagem'] and precision is None) or
                (n_format in ['real'] and collapse)):
            return 1
        if precision is None:
            return 0
        return precision

    @staticmethod
    def format_with_locale(n_format, valor_c, str_locale):
        ''' Formatting value according to locale '''
        if n_format in ['monetario', 'porcentagem', 'real']:
            return format_decimal(valor_c, locale=str_locale)
        return format_number(valor_c, locale=str_locale)
