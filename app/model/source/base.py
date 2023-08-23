''' Classes to create options dictionary for datasources '''
class BaseSource():
    ''' Base Option builder class for Caged datasources '''
    def get_context_options_empresa(self, options, local_cols, persp):
        ''' Get additional filters, common to all datasources '''
        subset_rules = []
        if 'cnpj_raiz_flag' in local_cols:
            subset_rules.extend([
                "and", f"eq-{local_cols.get('cnpj_raiz_flag')}-'1'"
            ])

        # Add cnpj filter
        if options.get('cnpj'):
            subset_rules.extend([
                "and", f"eq-{local_cols.get('cnpj')}-{options.get('cnpj')}"
            ])
            if 'cnpj_flag' in local_cols:
                subset_rules.extend([
                    "and", f"eq-{local_cols.get('cnpj_flag')}-'1'"
                ])

        # Add pf filter
        if options.get('id_pf'):
            subset_rules.extend([
                "and", f"eq-{local_cols.get('pf')}-{options.get('id_pf')}"
            ])
        return subset_rules

    def get_options_rules_empresa(self, options, local_cols, df, persp):
        return self.get_context_options_empresa(options, local_cols, persp)

    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = [f"eq-cast({local_cols.get('cnpj_raiz')} as INT)-{options.get('cnpj_raiz')}"]
        if options.get('column') and local_cols.get('compet'):
            subset_rules.extend([
                "and", f"eq-cast({local_cols.get('compet')} as INT)-{options.get('column')}"
            ])    
        subset_rules.extend(
            self.get_options_rules_empresa(options, local_cols, df, persp)
        )
        return {
            "categorias": [local_cols.get('cnpj_raiz')],
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": df
        }
