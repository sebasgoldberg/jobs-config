#!/bin/env python3
import datetime
from jobconfig import *

class Loja:

    SEMANAL = 'W'
    DIARIO = 'T'
    PERIODO_ATUAL = 'A'

    def __init__(self, id, tipo_filial):
        self.id = id
        self.tipo_filial = tipo_filial

    def get_id(self):
        return self.id

    def get_filial(self):
        return self.tipo_filial

    def get_tipos_mrp(self):
        return 'G1;X1;GD;GL;X8;Z1;XR;S2;FT;NN;S1'.split(';')

    def criar_paso_1(self):

        step = Step('ZVPRG_ANULA_POS_SOL_PEDIDO', RAConfig.USUARIO)
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'SO_BADAT', self.DATA_EXECUCAO_FROM, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('SO_WERKS', self.get_id(), 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('PA_BSART', ' '))

        return step

    def criar_paso_2(self):

        step = Step('RMPROG00', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('WERK', self.get_id(), 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('VLFKZ', self.get_filial()))
        step.add_screen_item(ScreenItem('PERKZ', Loja.SEMANAL))
        step.add_screen_item(ScreenItem('PRDUR', Loja.PERIODO_ATUAL))
        step.add_screen_item(ScreenItem('UPDTE', 'X'))
        step.add_screen_item(ScreenItem('PROTO', ' '))

        return step

    def criar_paso_3(self):

        step = Step('RMPROG00', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('WERK', self.get_id(), 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('VLFKZ', self.get_filial()))
        step.add_screen_item(ScreenItem('PERKZ', Loja.DIARIO))
        step.add_screen_item(ScreenItem('PRDUR', Loja.PERIODO_ATUAL))
        step.add_screen_item(ScreenItem('UPDTE', 'X'))
        step.add_screen_item(ScreenItem('PROTO', ' '))

        return step

    def criar_paso_4(self):

        step = Step('RMMRP000', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('WERKS', self.get_id()))
        step.add_screen_item(ScreenItem('VERSL', 'NETCH'))
        step.add_screen_item(ScreenItem('BANER', '1'))
        step.add_screen_item(ScreenItem('LIFKZ', '1'))
        step.add_screen_item(ScreenItem('DISER', '1'))
        step.add_screen_item(ScreenItem('PLMOD', '3'))
        step.add_screen_item(ScreenItem('TRMPL', '1'))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'DISPD', self.DATA_EXECUCAO_FROM))
        step.add_screen_item(ScreenItem('PARAL', 'X'))

        return step

    def criar_paso_5(self):

        step = Step('RWRPLPRO', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('CUSTRNGE', self.get_id(), 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('G_ATP', 'X'))
        step.add_screen_item(ScreenItem('G_FCAST', 'X'))
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'G_DAY', self.DATA_EXECUCAO_FROM))
        step.add_screen_item(ScreenItem('G_PLHOR', '5'))
        step.add_screen_item(ScreenItem('G_NETCH', ' '))
        step.add_screen_item(ScreenItem('G_PKT', '1000'))
        step.add_screen_item(ScreenItem('G_TOL', '5'))

        return step

    def criar_paso_6(self):

        step = Step('ZPRG_CAPI_GERA_CACHE_ZRIS', RAConfig.USUARIO)
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'S_BADAT', self.DATA_EXECUCAO_FROM, 'S','I','EQ'))
        step.add_screen_item(ScreenItem('S_WERKS', self.get_id(), 'S', 'I', 'EQ'))

        return step

    def criar_paso_7(self):

        step = Step('/1CADMC/SAP_LSMW_CONV_00000794', RAConfig.USUARIO)
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'P_FECHA', self.DATA_EXECUCAO_FROM))
        step.add_screen_item(ScreenItem('S_WERKS', self.get_id(), 'S', 'I', 'EQ'))
        for tipo_mrp in self.get_tipos_mrp():
            step.add_screen_item(ScreenItem('S_DISMM', tipo_mrp, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('P_FILEPT', 'X'))
        step.add_screen_item(ScreenItem('P_TRFCPT', ' '))
        step.add_screen_item(ScreenItem('P_PACKGE', '50'))

        return step

    def criar_paso_8(self):

        step = Step('ZVPRG_VALPED', RAConfig.USUARIO)
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'S_BADAT', self.DATA_EXECUCAO_FROM, 'S','I','EQ'))
        step.add_screen_item(ScreenItem('S_WERKS', self.get_id(), 'S', 'I', 'EQ'))

        return step

    def criar_paso_9(self):

        FORNECEDORES_FIXOS = [
            'B001',
            'B098',
            'B184',
            'B191',
            'B289',
            ]

        step = Step('RM06BB30', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('S_EKORG', '4005', 'S', 'I', 'EQ'))
        for fornecedor in FORNECEDORES_FIXOS:
            step.add_screen_item(ScreenItem('S_FLIEF', fornecedor, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('S_WERKS', self.get_id(), 'S', 'I', 'EQ'))
        for fornecedor in FORNECEDORES_FIXOS:
            step.add_screen_item(ScreenItem('S_RESWK', fornecedor, 'S', 'I', 'EQ'))

        step.add_screen_item(ScreenItem('P_GEKGRP', 'X'))
        step.add_screen_item(ScreenItem('P_GLFDAT', 'X'))
        step.add_screen_item(ScreenItem('P_GWERKS', 'X'))
        step.add_screen_item(ScreenItem('P_GLTSNR', 'X'))
        step.add_screen_item(ScreenItem('P_GLGORT', 'X'))
        step.add_screen_item(ScreenItem('P_GBUKRS', 'X'))
        step.add_screen_item(ScreenItem('P_GKONNR', 'X'))
        step.add_screen_item(ScreenItem('P_DETPRO', '2'))
        step.add_screen_item(ScreenItem('P_POSERR', 'X'))
        step.add_screen_item(ScreenItem('P_SEBAKZ', '2'))

        step.add_screen_item(ScreenItem('S_DISPO', 'A02', 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('P_VRTYPK', 'X'))

        return step

    def criar_paso_10(self):

        FORNECEDORES_FIXOS = [
            'B001',
            'B098',
            'B184',
            'B191',
            'B289',
            ]

        step = Step('RM06BB30', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('S_EKORG', '4005', 'S', 'I', 'EQ'))
        for fornecedor in FORNECEDORES_FIXOS:
            step.add_screen_item(ScreenItem('S_FLIEF', fornecedor, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('S_WERKS', self.get_id(), 'S', 'I', 'EQ'))
        for fornecedor in FORNECEDORES_FIXOS:
            step.add_screen_item(ScreenItem('S_RESWK', fornecedor, 'S', 'I', 'EQ'))

        step.add_screen_item(ScreenItem('P_GEKGRP', 'X'))
        step.add_screen_item(ScreenItem('P_GLFDAT', 'X'))
        step.add_screen_item(ScreenItem('P_GWERKS', 'X'))
        step.add_screen_item(ScreenItem('P_GLTSNR', 'X'))
        step.add_screen_item(ScreenItem('P_GLGORT', 'X'))
        step.add_screen_item(ScreenItem('P_GBUKRS', 'X'))
        step.add_screen_item(ScreenItem('P_GKONNR', 'X'))
        step.add_screen_item(ScreenItem('P_DETPRO', '2'))
        step.add_screen_item(ScreenItem('P_POSERR', 'X'))
        step.add_screen_item(ScreenItem('P_SEBAKZ', '2'))

        step.add_screen_item(ScreenItem('P_VRTYPK', 'X'))

        return step

    def criar_job_ra(self, start_datetime):
        self.DATA_EXECUCAO_FROM = start_datetime.strftime('%Y%m%d')
        job = Job('CORRIDA_RA_%s' % self.get_id(), start_datetime=start_datetime)
        job.add_step(self.criar_paso_1())
        job.add_step(self.criar_paso_2())
        job.add_step(self.criar_paso_3())
        job.add_step(self.criar_paso_4())
        job.add_step(self.criar_paso_5())
        job.add_step(self.criar_paso_6())
        job.add_step(self.criar_paso_7())
        job.add_step(self.criar_paso_8())
        job.add_step(self.criar_paso_9())
        job.add_step(self.criar_paso_10())
        return job



class RAConfig(Config):

    USUARIO = 'BDC_RETAIL'

    def get_start_datetime(self, i, n):
        TEMPO_DISPONIVEL_INICIO = 4*60*60
        intervalo_entre_inicios = float(TEMPO_DISPONIVEL_INICIO) / n
        return self.START_DATETIME + datetime.timedelta(
            seconds=int(i*intervalo_entre_inicios)
        )

    def __init__(self):
        super(RAConfig, self).__init__()

        EXECUTION_INTERVAL = 24*60*60
        self.START_DATETIME = datetime.datetime(3000, 1, 1, 2)
        DATA_EXECUCAO_TO = (self.START_DATETIME + datetime.timedelta(days=2)).strftime('%Y%m%d')
        LOJAS = [ 
                Loja(id, 'A')
                    for id in 'B002;B003;B004;B006;B007;B008;B009;B010;B011;B012;B013;B014;B015'.split(';')
                ]

        jobs = []
        for i in range(len(LOJAS)):
            loja = LOJAS[i]
            job = loja.criar_job_ra(self.get_start_datetime(i,len(LOJAS)))
            jobs.append(job)

        while (jobs[0].steps[0].get_screen_item('SO_BADAT').low <= DATA_EXECUCAO_TO):
            for job in jobs:
                self.add_job(job)
            jobs = [ job.next(datetime.timedelta(seconds=(EXECUTION_INTERVAL))) for job in jobs ]

c = RAConfig()
c.save('./ra.xls')
