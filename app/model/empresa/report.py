''' Repository para recuperar informações da CEE '''
from datetime import datetime
from model.empresa.empresa import Empresa
from repository.empresa.report import ReportRepository

#pylint: disable=R0903
class Report(Empresa):
    ''' Definição do model '''
    REDIS_KEY = 'rmd:{}'
    REDIS_STATUS_KEY = 'rmd:st:{}:{}'
    STATUS = ['FAILED', 'PROCESSING', 'SUCCESS']

    def __init__(self):
        ''' Construtor '''
        self.repo = None
        self.__set_repo()

    def get_repo(self):
        ''' Garantia de que o repo estará carregado '''
        if self.repo is None:
            self.repo = ReportRepository()
        return self.repo

    def __set_repo(self):
        ''' Setter invoked in Construtor '''
        self.repo = ReportRepository()

    def find_report(self, cnpj_raiz):
        ''' Localiza report pelo CNPJ Raiz '''
        redis_report_status = self.check_status(cnpj_raiz)
        if redis_report_status is not None and redis_report_status != '':
            if redis_report_status == 'SUCCESS':
                report = self.get_repo().find_report(self.REDIS_KEY.format(cnpj_raiz))
                if report is None or report == '':
                    self.generate(cnpj_raiz)
                    return {'status': 'RENEWING'}
                return report
            if redis_report_status == 'PROCESSING':
                # When there's a no success status in REDIS (PROCESSING, FAILED), returns status
                return {'status': redis_report_status}
            # In any other case, sends to reprocessing
            self.generate(cnpj_raiz)
            if redis_report_status in ['FAILED', 'RENEWING', 'UNLOCKING']:
                # If failed, produces report item in Kafka an sends back the failed status
                return {'status': redis_report_status}
            # In any other case, responds as not found
            return {'status': "NOTFOUND"}
        # If no status is found
        report = self.get_repo().find_report(self.REDIS_KEY.format(cnpj_raiz))
        if report is None or report == '':
            self.generate(cnpj_raiz)
            return {'status': "NOTFOUND"}
        self.update_status(cnpj_raiz, "SUCCESS")
        return report

    def generate(self, cnpj_raiz):
        ''' Inclui/atualiza dicionário de competências e datasources no REDIS '''
        # Restart status from REDIS
        self.update_status(cnpj_raiz, "PROCESSING")
        try:
            self.get_repo().store(cnpj_raiz)
        except:
            self.update_status(cnpj_raiz, "FAILED")

    def update_status(self, cnpj_raiz, status):
        ''' Updates status in REDIS '''
        reqtime = datetime.now()
        for st in self.STATUS:
            if st == status:
                self.get_repo().store_status(self.REDIS_STATUS_KEY.format(st, cnpj_raiz), reqtime.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                # Removes old status from REDIS
                try:
                    self.get_repo().del_status(self.REDIS_STATUS_KEY.format(st, cnpj_raiz))
                except:
                    continue

    def check_status(self, cnpj_raiz):
        ''' Checks the status or if the report should be updated '''
        for st in self.STATUS:
            redis_report_status = self.get_repo().find_status(self.REDIS_STATUS_KEY.format(st, cnpj_raiz))
            # Decodes if status is stored as binary
            try:
                redis_report_status = redis_report_status.decode()
            except (UnicodeDecodeError, AttributeError):
                pass
            if redis_report_status is None:
                continue
            if st == 'PROCESSING' and (datetime.now() - datetime.strptime(redis_report_status, "%Y-%m-%d %H:%M:%S")).days > 1:
                return 'RENEWING'
            elif st == 'SUCCESS' and (datetime.now() - datetime.strptime(redis_report_status, "%Y-%m-%d %H:%M:%S")).days > 30:
                return 'UNLOCKING'
            return st
        return None # No status found