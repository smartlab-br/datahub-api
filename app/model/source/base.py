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
                "and", f"eq-cast({local_cols.get('cnpj')} as BIGINT)-{options.get('cnpj')}"
            ])
            if 'cnpj_flag' in local_cols:
                subset_rules.extend([
                    "and", f"eq-{local_cols.get('cnpj_flag')}-'1'"
                ])

        # Add pf filter
        if options.get('id_pf'):
            subset_rules.extend([
                "and", f"eq-cast({local_cols.get('pf')} as INT)-{options.get('id_pf')}"
            ])
        return subset_rules

    def get_options_rules_empresa(self, options, local_cols, df, persp):
        subset_rules = []
        if (local_cols.get('filter_rules')):
            subset_rules = ["and"] + local_cols.get('filter_rules').split(',')
        subset_rules.extend(
            self.get_context_options_empresa(options, local_cols, persp)
        )
        return subset_rules

    def get_options_empresa(self, options, local_cols, df, persp):
        ''' Create options according to tables and query conditions '''
        subset_rules = []
        cat = ['\'1\'-pos']
        if local_cols.get('cnpj_raiz'):
            subset_rules = [f"eq-cast({local_cols.get('cnpj_raiz')} as INT)-{options.get('cnpj_raiz')}"]
            cat = [local_cols.get('cnpj_raiz')]
        elif local_cols.get('cnpj'):
            subset_rules = [f"eqlponstr-{local_cols.get('cnpj')}-{options.get('cnpj_raiz')}-14-0-1-8"]
        else: 
            raise ValueError('"cnpj_raiz" or "cnpj" column not set for this theme')

        if options.get('column') and local_cols.get('compet'):
            subset_rules.extend([
                "and", f"eq-cast({local_cols.get('compet')} as INT)-{options.get('column')}"
            ])    
        subset_rules.extend(
            self.get_options_rules_empresa(options, local_cols, df, persp)
        )

        # themes catweb and sisben for public data
        # themes catweb_c and sisben_c for private data (empresa)
        if df in ['catweb', 'sisben']: 
            theme = f"{df}_c" 
        else:
            theme = df

        return {
            "categorias": cat,
            "agregacao": ['count'],
            "where": subset_rules,
            "theme": theme
        }
