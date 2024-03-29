#!/bin/env python3
import datetime
from jobconfig import *

class PP_BKFLUSHConfig(Config):

    def __init__(self):

        START_DATETIME = datetime.datetime(2018, 4, 25, 11,30)
        EXECUTION_INTERVAL = 10*60
        SO_DATUM_FROM = '20160426'
        SO_DATUM_TO = '20160507'
        
        super(PP_BKFLUSHConfig, self).__init__()
        job = Job('ARV_PP_BKFLUSH')
        step = Step('PPARBFAR','BDC_RETAIL')
        step.add_screen_item(ScreenItem('PA_TESTR', ' '))
        step.add_screen_item(ScreenItem('PA_CREAT', 'X'))
        step.add_screen_item(ScreenItem('PA_RTP01', 'X'))
        step.add_screen_item(ScreenItem('PA_RTP02', 'X'))
        step.add_screen_item(ScreenItem('PA_RTP03', 'X'))
        step.add_screen_item(ScreenItem('PA_RTP04', 'X'))
        step.add_screen_item(ScreenItem('SO_WERKS', '*', 'S', 'I', 'CP'))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'SO_DATUM', SO_DATUM_FROM, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'P_TEXT', SO_DATUM_FROM))
        while (step.get_screen_item('SO_DATUM').low < SO_DATUM_TO):
            job.add_step(step)
            step = step.next()
        self.add_job(job)
        

class CO_ML_IDXConfig(Config):

    def primary_execution(self):

        START_DATETIME = datetime.datetime(2018, 5, 14, 22)
        EXECUTION_INTERVAL = 24*60*60
        PERIOD_FROM = datetime.datetime(2013, 7, 1)
        PERIOD_TO = '201607'

        super(CO_ML_IDXConfig, self).__init__()

        job = Job('ARV_CO_ML_IDX', start_datetime=START_DATETIME)
        step = Step('SAPRCKMM','BDC_RETAIL',1,False)
        step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'H_BDATJ'))
        step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'H_POPER'))
        step.add_screen_item(ScreenItem('TESTRUN', ' '))
        step.add_screen_item(ScreenItem('S_CREATE', 'X'))
        step.add_screen_item(ScreenItemYearPeriodDeltaByPeriod(PERIOD_FROM, 'PA_TEXT'))
        job.add_step(step)
        while (job.get_screen_item('PA_TEXT').low < PERIOD_TO):
            self.add_job(job)
            job = job.next(datetime.timedelta(seconds=(EXECUTION_INTERVAL)))

    def maintenance_execution(self):

        START_DATETIME = datetime.datetime(2018, 7, 3, 22)
        PERIOD_FROM = datetime.datetime(2016, 6, 1)
        PERIOD_TO = '210001'

        super(CO_ML_IDXConfig, self).__init__()

        job = Job('ARV_CO_ML_IDX', start_datetime=START_DATETIME)
        step = Step('SAPRCKMM','BDC_RETAIL')
        step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'H_BDATJ'))
        step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'H_POPER'))
        step.add_screen_item(ScreenItem('TESTRUN', ' '))
        step.add_screen_item(ScreenItem('S_CREATE', 'X'))
        step.add_screen_item(ScreenItemYearPeriodDeltaByPeriod(PERIOD_FROM, 'PA_TEXT'))
        job.add_step(step)
        while (job.get_screen_item('PA_TEXT').low < PERIOD_TO):
            self.add_job(job)
            job = job.next(MonthlyExecutionInterval())

    def __init__(self):
        self.maintenance_execution()

class CO_ITEMConfig(Config):

    def primary_execution(self):

        START_DATETIME = datetime.datetime(2018, 5, 14, 19, 30)
        EXECUTION_INTERVAL = 24*60*60
        PERIOD_FROM = datetime.datetime(2013, 5, 1)
        PERIOD_TO = '201607'

        job = Job('ARV_CO_ITEM', start_datetime=START_DATETIME)
        step = Step('CO_ITEM_WRI','BDC_RETAIL')
        step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'BISJA'))
        step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'BISPE'))
        step.add_screen_item(ScreenItem('P_WRITST', ' '))
        step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
        step.add_screen_item(ScreenItem('P_DELTST', ' '))
        step.add_screen_item(ScreenItemYearPeriodDeltaByPeriod(PERIOD_FROM, 'P_COMENT'))
        job.add_step(step)
        while (job.get_screen_item('P_COMENT').low < PERIOD_TO):
            self.add_job(job)
            job = job.next(datetime.timedelta(seconds=(EXECUTION_INTERVAL)))

    def maintenance_execution(self):

        START_DATETIME = datetime.datetime(2018, 7, 4, 22)
        PERIOD_FROM = datetime.datetime(2016, 6, 1)
        PERIOD_TO = '210001'

        job = Job('ARV_CO_ITEM', start_datetime=START_DATETIME)
        step = Step('CO_ITEM_WRI','BDC_RETAIL')
        step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'BISJA'))
        step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'BISPE'))
        step.add_screen_item(ScreenItem('P_WRITST', ' '))
        step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
        step.add_screen_item(ScreenItem('P_DELTST', ' '))
        step.add_screen_item(ScreenItemYearPeriodDeltaByPeriod(PERIOD_FROM, 'P_COMENT'))
        job.add_step(step)
        while (job.get_screen_item('P_COMENT').low < PERIOD_TO):
            self.add_job(job)
            job = job.next(MonthlyExecutionInterval())

    def __init__(self):

        super(CO_ITEMConfig, self).__init__()
        
        self.maintenance_execution()


class MM_MATBELConfig(Config):

    START_DATETIME = datetime.datetime(2018, 8, 15, 8)
    S_BUDAT_FROM = '20160101'
    S_BUDAT_FROM_HIGH = '20160103'
    S_BUDAT_TO = '20160830'
    EXECUTION_INTERVAL = 4*60*60

    def _create_step(self, _pos):

        step = Step('RM07MARCS','BDC_RETAIL')
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=3), 'S_BUDAT', MM_MATBELConfig.S_BUDAT_FROM, 'S', 'I', 'BT', MM_MATBELConfig.S_BUDAT_FROM_HIGH))
        step.add_screen_item(ScreenItem('POS', _pos))
        step.add_screen_item(ScreenItem('P_WRITST', ' '))
        step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
        step.add_screen_item(ScreenItem('P_DELTST', ' '))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=3), 'P_COMENT', MM_MATBELConfig.S_BUDAT_FROM))
        return step

    def __init__(self):

        #WORKDAY_EXECUTION_INTERVAL = 120*60

        super(MM_MATBELConfig, self).__init__()
        job = Job('ARV_MM_MATBEL', start_datetime=MM_MATBELConfig.START_DATETIME)

        step = self._create_step(' ')
        job.add_step(step)

        step = self._create_step('X')
        job.add_step(step)

        while (job.get_screen_item('S_BUDAT').low <= MM_MATBELConfig.S_BUDAT_TO):
            self.add_job(job)
            job = job.next(ExecutionInterval(datetime.timedelta(seconds=(MM_MATBELConfig.EXECUTION_INTERVAL))))


class SD_VTTKConfig(Config):

    def __init__(self):

        S_ERDAT_FROM = '20150301'
        S_ERDAT_FROM_HIGH = '20150307'
        S_ERDAT_TO = '20150531'
        START_DATETIME = datetime.datetime(2018, 7, 6, 11)
        EXECUTION_INTERVAL = 20*60

        super(SD_VTTKConfig, self).__init__()
        job = Job('ARV_SD_VTTK', start_datetime=START_DATETIME)
        step = Step('SDVTTKWRS','BDC_RETAIL')
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=7), 'S_ERDAT', S_ERDAT_FROM, 'S', 'I', 'BT', S_ERDAT_FROM_HIGH))
        step.add_screen_item(ScreenItem('P_WRITST', ' '))
        step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
        step.add_screen_item(ScreenItem('P_DELTST', ' '))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=7), 'P_COMENT', S_ERDAT_FROM))

        job.add_step(step)

        while (job.get_screen_item('S_ERDAT').low <= S_ERDAT_TO):
            self.add_job(job)
            job = job.next(ExecutionInterval(datetime.timedelta(seconds=(EXECUTION_INTERVAL))))



class RV_LIKPConfig(Config):

    def __init__(self):

        SO_ERDAT_FROM = '20101130'
        SO_ERDAT_FROM_HIGH = '20101206'
        SO_ERDAT_TO = '20160729'
        START_DATETIME = datetime.datetime(2018, 7, 18, 11, 15)
        EXECUTION_INTERVAL = 60*60

        super(RV_LIKPConfig, self).__init__()

        job = Job('ARV_RV_LIKP', start_datetime=START_DATETIME)

        for delty in [ 'O', 'I', 'R', ]:

            step = Step('S3LIKPPTS','BDC_RETAIL')
            step.add_screen_item(ScreenItem('P_DELTY', delty))
            step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=7), 'SO_ERDAT', SO_ERDAT_FROM, 'S', 'I', 'BT', SO_ERDAT_FROM_HIGH))
            step.add_screen_item(ScreenItem('C_NOTRA', 'X'))
            job.add_step(step)

            step = Step('S3LIKPWRS','BDC_RETAIL')
            step.add_screen_item(ScreenItem('P_DELTY', delty))
            step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=7), 'SO_ERDAT', SO_ERDAT_FROM, 'S', 'I', 'BT', SO_ERDAT_FROM_HIGH))
            step.add_screen_item(ScreenItem('C_NOTRA', 'X'))
            step.add_screen_item(ScreenItem('P_WRITST', ' '))
            step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
            step.add_screen_item(ScreenItem('P_DELTST', ' '))
            step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=7), 'P_COMENT', SO_ERDAT_FROM))
            job.add_step(step)

        while (job.get_screen_item('SO_ERDAT').low <= SO_ERDAT_TO):
            self.add_job(job)
            job = job.next(ExecutionInterval(datetime.timedelta(seconds=(EXECUTION_INTERVAL))))


class SD_VBRKConfig(Config):

    def __init__(self):

        SO_ERDAT_FROM = '20150415'
        SO_ERDAT_FROM_HIGH = '20150417'
        SO_ERDAT_TO = '20160830'
        START_DATETIME = datetime.datetime(2018, 8, 15, 9, 30)
        EXECUTION_INTERVAL = 2*60*60

        super(SD_VBRKConfig, self).__init__()
        job = Job('ARV_SD_VBRK', start_datetime=START_DATETIME)
        
        step = Step('S3VBRKPTS','BDC_RETAIL')
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=3), 'SO_ERDAT', SO_ERDAT_FROM, 'S', 'I', 'BT', SO_ERDAT_FROM_HIGH))
        job.add_step(step)

        step = Step('S3VBRKWRS','BDC_RETAIL')
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=3), 'SO_ERDAT', SO_ERDAT_FROM, 'S', 'I', 'BT', SO_ERDAT_FROM_HIGH))
        step.add_screen_item(ScreenItem('P_WRITST', ' '))
        step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
        step.add_screen_item(ScreenItem('P_DELTST', ' '))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=3), 'P_COMENT', SO_ERDAT_FROM))
        job.add_step(step)

        while (job.get_screen_item('SO_ERDAT').low <= SO_ERDAT_TO):
            self.add_job(job)
            job = job.next(ExecutionInterval(datetime.timedelta(seconds=(EXECUTION_INTERVAL))))



class S623Config(Config):

    def __init__(self):

        #SL_SPTAG_FROM = '20170106'
        #SL_SPTAG_FROM_HIGH = '20170112'
        #SL_SPTAG_TO = '20180131'
        SL_SPTAG_FROM = '20180325'
        #SL_SPTAG_FROM_HIGH = '20180520'
        SL_SPTAG_TO = '20180521'

        super(S623Config, self).__init__()
        job = Job('ARV_S623_DEIXA_30_DIAS')
        step = Step('RMCA6235','')
        step.add_screen_item(ScreenItem('VRSIO', '000'))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'SL_SPTAG', SL_SPTAG_FROM, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('F_O_DEL', 'X'))
        while (step.get_screen_item('SL_SPTAG').low < SL_SPTAG_TO):
            job.add_step(step)
            step = step.next()
        self.add_job(job)

class WINDConfig(Config):

    def __init__(self):

        S_DATE_FROM = '20180301'
        S_DATE_TO = '20180407'

        super(WINDConfig, self).__init__()

        job = Job('DEL_WIND_DEIXA_60_DIAS')
        steps = []

        for P_BLTYP in ['10', '50', '55']:
            step = Step('RWVKP03D','')
            step.add_screen_item(ScreenItem('P_BLTYP', P_BLTYP))
            step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'S_DATE', S_DATE_FROM, 'S', 'I', 'EQ'))
            step.add_screen_item(ScreenItem('DELRUN', 'X'))
            step.add_screen_item(ScreenItem('P_LIS1', 'X'))
            step.add_screen_item(ScreenItem('P_LIS2', ' '))
            steps.append(step)

        while (steps[0].get_screen_item('S_DATE').low < S_DATE_TO):
            for i in range(len(steps)):
                job.add_step(steps[i])
                steps[i] = steps[i].next()

        self.add_job(job)

class MM_EKKOConfig(Config):


    def __init__(self):

        TIPOS_PEDIDO_TRANSFERENCIA = [
            'EUB', 'UB', 'ZADI', 'ZPAL', 'ZPAT', 'ZPDD', 'ZPDI', 'ZPEX', 'ZPHO', 'ZPPD',
            'ZPPI', 'ZPPR', 'ZPTC', 'ZPTD', 'ZPTL', 'ZPTP', 'ZPTT', 'ZPUE', 'ZPVC', 'ZRCL',
            'ZREP', 'ZTCD', 'ZVDL', 'ZZRO',
            ]

        ER_BEDAT_FROM = '20130607'
        ER_BEDAT_TO = '20170710'
        EXECUTION_INTERVAL = 1*60*60
        START_DATETIME = datetime.datetime(2018, 7, 10, 16)

        super(MM_EKKOConfig, self).__init__()
        job = Job('ARV_MM_EKKO', start_datetime=START_DATETIME)

        step_pre = Step('RM06EV47','BDC_RETAIL')
        step_pre.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'ER_BEDAT', ER_BEDAT_FROM, 'S', 'I', 'EQ'))
        for bsart in TIPOS_PEDIDO_TRANSFERENCIA:
            step_pre.add_screen_item(ScreenItem('ER_BSART', bsart, 'S', 'I', 'EQ'))
        step_pre.add_screen_item(ScreenItem('ER_ANDAT', datetime.date.today().strftime('%Y%m%d')))
        step_pre.add_screen_item(ScreenItem('ER_CDAT', 'X'))
        step_pre.add_screen_item(ScreenItem('P_PRETST', ' '))
        step_pre.add_screen_item(ScreenItem('P_PREPRD', 'X'))

        step = Step('RM06EW70','BDC_RETAIL')
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'ER_BEDAT', ER_BEDAT_FROM, 'S', 'I', 'EQ'))
        for bsart in TIPOS_PEDIDO_TRANSFERENCIA:
            step.add_screen_item(ScreenItem('ER_BSART', bsart, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('ER_AEDAT', 'X'))
        step.add_screen_item(ScreenItem('P_WRITST', ' '))
        step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
        step.add_screen_item(ScreenItem('P_DELTST', ' '))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'P_COMENT', ER_BEDAT_FROM))

        job.add_step(step_pre)
        job.add_step(step)

        while (job.get_screen_item('ER_BEDAT').low <= ER_BEDAT_TO):
            self.add_job(job)
            job = job.next(ExecutionInterval(datetime.timedelta(seconds=(EXECUTION_INTERVAL))))




# @todo Testar
class FI_DOCUMNTConfig(Config):

    def main_execution(self):

        START_DATETIME = datetime.datetime(2018, 6, 20, 18)
        EXECUTION_INTERVAL = 24*60*60
        PERIOD_FROM = datetime.datetime(2010, 11, 1)
        PERIOD_TO = '201607'

        super(FI_DOCUMNTConfig, self).__init__()
        
        job = Job('ARV_FI_DOCUMNT', start_datetime=START_DATETIME)
        step = Step('FI_DOCUMNT_WRI','BDC_RETAIL')
        step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'P_VGJAHR'))
        step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'P_VMONAT'))
        step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'P_BGJAHR'))
        step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'P_BMONAT'))
        step.add_screen_item(ScreenItem('P_CPUTG', '731'))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'P_STAG', START_DATETIME.strftime('%Y%m%d')))
        step.add_screen_item(ScreenItem('P_WRITST', ' '))
        step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
        step.add_screen_item(ScreenItem('P_DELTST', ' '))
        step.add_screen_item(ScreenItemYearPeriodDeltaByPeriod(PERIOD_FROM, 'P_COMENT'))
        job.add_step(step)

        while (job.get_screen_item('P_COMENT').low <= PERIOD_TO):
            self.add_job(job)
            job = job.next(
                ExecutionInterval(datetime.timedelta(seconds=(EXECUTION_INTERVAL)))
                )


    def maintenance_execution(self):

        START_DATETIME = datetime.datetime(2018, 9, 5, 22)
        PERIOD_FROM = datetime.datetime(2016, 8, 1)
        PERIOD_TO = '201712'

        super(FI_DOCUMNTConfig, self).__init__()

        jobs = []
        
        start_datetimes = [START_DATETIME,
                START_DATETIME + datetime.timedelta(days=10),
                START_DATETIME + datetime.timedelta(days=20)]

        for i in range(len(start_datetimes)):

            sdt = start_datetimes[i]

            job = Job('ARV_FI_DOCUMNT_%s' % i, start_datetime=sdt)
            step = Step('FI_DOCUMNT_WRI','BDC_RETAIL')
            step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'P_VGJAHR'))
            step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'P_VMONAT'))
            step.add_screen_item(ScreenItemYearDeltaByPeriod(PERIOD_FROM,'P_BGJAHR'))
            step.add_screen_item(ScreenItemPeriodDeltaByPeriod(PERIOD_FROM,'P_BMONAT'))
            step.add_screen_item(ScreenItem('P_CPUTG', '731'))
            step.add_screen_item(
                ScreenItemDateDeltaByPeriod(
                    sdt-datetime.timedelta(days=1), 'P_STAG'))
            step.add_screen_item(ScreenItem('P_WRITST', ' '))
            step.add_screen_item(ScreenItem('P_WRIPRD', 'X'))
            step.add_screen_item(ScreenItem('P_DELTST', ' '))
            step.add_screen_item(ScreenItemYearPeriodDeltaByPeriod(PERIOD_FROM, 'P_COMENT'))
            job.add_step(step)
            jobs.append(job)

        while (jobs[0].get_screen_item('P_COMENT').low <= PERIOD_TO):
            new_jobs = []
            for job in jobs:
                self.add_job(job)
                new_jobs.append(job.next(MonthlyExecutionInterval()))
            jobs = new_jobs

    def __init__(self):
        self.maintenance_execution()


import sys

def main(configtypes):

    for configtype in configtypes:
        c = None
        if configtype == 'PP_BKFLUSH':
            c = PP_BKFLUSHConfig()
        elif configtype == 'CO_ML_IDX':
            c = CO_ML_IDXConfig()
        elif configtype == 'CO_ITEM':
            c = CO_ITEMConfig()
        elif configtype == 'MM_MATBEL':
            c = MM_MATBELConfig()
        elif configtype == 'SD_VTTK':
            c = SD_VTTKConfig()
        elif configtype == 'RV_LIKP':
            c = RV_LIKPConfig()
        elif configtype == 'SD_VBRK':
            c = SD_VBRKConfig()
        elif configtype == 'S623':
            c = S623Config()
        elif configtype == 'WIND':
            c = WINDConfig()
        elif configtype == 'MM_EKKO':
            c = MM_EKKOConfig()
        elif configtype == 'FI_DOCUMNT':
            c = FI_DOCUMNTConfig()
        else:
            print('Configuração "%s" não reconhecida.')
        c.save('./%s.xls' % configtype)

main(sys.argv[1:])

