"""API Base """
import os
from flask import Flask
from flask import g
from flask_cors import CORS
from flask_restful_swagger_2 import Api

from service.request_handler import FLPORequestHandler

from resources.v1.municipio import MunicipiosResource, MunicipioResource

from resources.v1.indicadores.indicadores_municipais \
    import IndicadoresMunicipaisResource, IndicadoresMunicipaisChartResource
from resources.v1.indicadores.indicadores_estaduais \
    import IndicadoresEstaduaisResource
from resources.v1.indicadores.indicadores_microrregionais \
    import IndicadoresMicrorregionaisResource
from resources.v1.indicadores.indicadores_mesorregionais \
    import IndicadoresMesorregionaisResource
from resources.v1.indicadores.indicadores_regionais \
    import IndicadoresRegionaisResource
from resources.v1.indicadores.indicadores_nacionais \
    import IndicadoresNacionaisResource
from resources.v1.indicadores.indicadores_mpt_unidades \
    import IndicadoresMptUnidadesResource

# Endpoints genéricos de temáticos
from resources.v1.thematic import ThematicResource

# Endpoints temáticos de Saúde e Segurança
from resources.v1.sst.beneficio import BeneficiosResource
from resources.v1.sst.cat import CatsResource, CatsOpResource
from resources.v1.sst.indicadores_br import IndicadoresSSTBrasilResource
from resources.v1.sst.indicadores_mun import IndicadoresSSTMunicipiosResource
from resources.v1.sst.indicadores_uf import IndicadoresSSTEstadosResource
from resources.v1.sst.indicadores_mpt_unidades import IndicadoresSSTMptUnidadesResource

# Endpoints temáticos de Trabalho Escravo
from resources.v1.te.incidencia import IncidenciaEscravoResource
from resources.v1.te.operacoes import OperacoesEscravoResource
from resources.v1.te.migracoes import MigracoesEscravoResource
from resources.v1.te.migracoes_sankey import MigracoesSankeyEscravoResource
from resources.v1.te.indicadores_br import IndicadoresEscravoBrasilResource
from resources.v1.te.indicadores_mun import IndicadoresEscravoMunicipiosResource, IndicadoresEscravoMunicipiosOpResource
from resources.v1.te.indicadores_uf import IndicadoresEscravoEstadosResource
from resources.v1.te.indicadores_mpt_unidades import IndicadoresEscravoMptUnidadesResource
# MAchine Learning do Trabalho Escravo
from resources.v1.te.ml.exposicao_rgt import MLExposicaoResgateResource
from resources.v1.te.ml.exposicao_rgt_feat_importance \
    import MLExposicaoResgateFeatureImportanceResource
from resources.v1.te.ml.exposicao_nat import MLExposicaoNaturalidadeResource
from resources.v1.te.ml.exposicao_nat_feat_importance \
    import MLExposicaoNaturalidadeFeatureImportanceResource

# Endpoints de EstadicMunic
from resources.v1.estadic_munic.estadic_munic import EstadicMunicResource
from resources.v1.estadic_munic.estadic_munic_uf import EstadicMunicUfResource
from resources.v1.estadic_munic.estadic_munic_mpt_unidades import EstadicMunicMptUnidadesResource

# Endpoints temáticos do Trabalho Infantil
from resources.v1.ti.indicadores_br import IndicadoresTIBrasilResource
from resources.v1.ti.indicadores_mun import IndicadoresTIMunicipiosResource
from resources.v1.ti.indicadores_uf import IndicadoresTIEstadosResource
from resources.v1.ti.indicadores_mpt_unidades import IndicadoresTIMptUnidadesResource
# Endpoints do Mapear - Trabalho Infantil
from resources.v1.ti.mapear import MapearInfantilResource
# Endpoints da Prova Brasil - Trabalho Infantil
from resources.v1.ti.prova_brasil import ProvaBrasilInfantilResource
# Endpoints do Censo Agro
from resources.v1.ti.censo_agro import CensoAgroMunicipiosResource
from resources.v1.ti.censo_agro_uf import CensoAgroEstadosResource
from resources.v1.ti.censo_agro_br import CensoAgroBrasilResource
# Endpoints das organizações assistência social
from resources.v1.orgs.orgs_assistencia_social import OrgsAssistenciaSocialResource

# Endpoint para obter a estrutura de dados de um template de card
from resources.v1.card_template import CardTemplateResource

from resources.v1.healthchecks import HCAlive

config = {
    "dev": "config.dev.DevelopmentConfig",
    "prod": "config.prod.ProductionConfig",
    "staging": "config.staging.StagingConfig",
}

application = Flask(__name__, static_folder='static', static_url_path='') #pylint: disable=C0103
config_name = os.getenv('FLASK_CONFIGURATION', 'dev')
application.config.from_object(config[config_name])

@application.teardown_appcontext
def close_db_connection(error):
    ''' Cleanup on application crash '''
    # Encerra a conexão com o hive
    if hasattr(g, 'hive_connection'):
        g.hive_connection.close()
        g.hive_connection = None
    # Encerra a conexão com o impala
    if hasattr(g, 'impala_connection'):
        g.impala_connection.close()
        g.impala_connection = None

CORS = CORS(application, resources={r"/*": {"origins": "*"}})
api = Api(application, api_version='0.1', api_spec_url='/api/swagger') #pylint: disable=C0103

api.add_resource(HCAlive, '/hcalive')

api.add_resource(MunicipiosResource, '/municipios')
api.add_resource(MunicipioResource, '/municipio/<int:cd_municipio_ibge>')

# Endpoints de buscas por datasets de indicadores
api.add_resource(IndicadoresMunicipaisResource, '/indicadoresmunicipais')
api.add_resource(IndicadoresEstaduaisResource, '/indicadoresestaduais')
api.add_resource(IndicadoresMicrorregionaisResource, '/indicadoresmicrorregionais')
api.add_resource(IndicadoresMesorregionaisResource, '/indicadoresmesorregionais')
api.add_resource(IndicadoresRegionaisResource, '/indicadoresregionais')
api.add_resource(IndicadoresNacionaisResource, '/indicadoresnacionais')
api.add_resource(IndicadoresMptUnidadesResource, '/indicadoresmptunidades')

# Endpoints de estadic-munic
api.add_resource(EstadicMunicResource, '/estadicmunic')
api.add_resource(EstadicMunicUfResource, '/estadicuf')
api.add_resource(EstadicMunicMptUnidadesResource, '/estadicunidadempt')

## Endpoints temáticos
# Endpoint temático genérico
api.add_resource(ThematicResource, '/thematic/<string:theme>')

# Saúde e Segurança no Trabalho
api.add_resource(CatsResource, '/sst/cats')
api.add_resource(CatsOpResource, '/sst/cats/<string:operation>')
api.add_resource(BeneficiosResource, '/sst/beneficios')
api.add_resource(IndicadoresSSTBrasilResource, '/sst/indicadoresnacionais')
api.add_resource(IndicadoresSSTMunicipiosResource, '/sst/indicadoresmunicipais')
api.add_resource(IndicadoresSSTEstadosResource, '/sst/indicadoresestaduais')
api.add_resource(IndicadoresSSTMptUnidadesResource, '/sst/indicadoresunidadempt')

# Trabalho Escravo
api.add_resource(IncidenciaEscravoResource, '/te/incidencia')
api.add_resource(IndicadoresEscravoBrasilResource, '/te/indicadoresnacionais')
api.add_resource(IndicadoresEscravoMunicipiosResource, '/te/indicadoresmunicipais')
api.add_resource(IndicadoresEscravoMunicipiosOpResource, '/te/indicadoresmunicipais/<string:operation>')
api.add_resource(IndicadoresEscravoEstadosResource, '/te/indicadoresestaduais')
api.add_resource(IndicadoresEscravoMptUnidadesResource, '/te/indicadoresunidadempt')
api.add_resource(MigracoesEscravoResource, '/te/migracoes')
api.add_resource(MigracoesSankeyEscravoResource, '/te/migracoes/sankey')
api.add_resource(OperacoesEscravoResource, '/te/operacoes')
# Machine Learning no Trabalho Escravo
api.add_resource(MLExposicaoResgateResource, '/te/ml/exposicaoresgate')
api.add_resource(MLExposicaoResgateFeatureImportanceResource, '/te/ml/exposicaoresgate/features')
api.add_resource(MLExposicaoNaturalidadeResource, '/te/ml/exposicaonaturais')
api.add_resource(
    MLExposicaoNaturalidadeFeatureImportanceResource,
    '/te/ml/exposicaonaturais/features'
)

# Trabalho Infantil
api.add_resource(MapearInfantilResource, '/ti/mapear')
api.add_resource(ProvaBrasilInfantilResource, '/ti/provabrasil')
api.add_resource(IndicadoresTIBrasilResource, '/ti/indicadoresnacionais')
api.add_resource(IndicadoresTIMunicipiosResource, '/ti/indicadoresmunicipais')
api.add_resource(IndicadoresTIEstadosResource, '/ti/indicadoresestaduais')
api.add_resource(IndicadoresTIMptUnidadesResource, '/ti/indicadoresunidadempt')
api.add_resource(CensoAgroMunicipiosResource, '/ti/censoagromunicipal')
api.add_resource(CensoAgroEstadosResource, '/ti/censoagroestadual')
api.add_resource(CensoAgroBrasilResource, '/ti/censoagronacional')

# Organizações de Assistência social
api.add_resource(OrgsAssistenciaSocialResource, '/orgs/assistenciasocial')

# Endpoint para obter a estrutura de dados de um template de card
api.add_resource(CardTemplateResource, '/cardtemplate/<string:cd_template>')

# Endpoint de obtenção de gráficos de indicadores
api.add_resource(IndicadoresMunicipaisChartResource, '/charts/indicadoresmunicipais')

if __name__ == '__main__':
    application.run(request_handler=FLPORequestHandler)
