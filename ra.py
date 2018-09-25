#!/bin/env python3
import datetime
from jobconfig import *

import raconfig

DATA_INICIO = datetime.datetime(2018, 9, 19)
QUANTIDADE_DIAS_PLANEJAR = 7

class Bandeira:

    def __init__(self, bandeira, centros_fornecedores, planejadores_mrp, aplicaPasso10=True):
        self.bandeira = bandeira
        self.centros_fornecedores = centros_fornecedores
        self.planejadores_mrp = planejadores_mrp
        self.aplicaPasso10 = aplicaPasso10

BANDEIRAS = {
    '4002': Bandeira('4002',
        centros_fornecedores='B607;B552'.split(';'),
        planejadores_mrp='A02;01F;02F;05F;06F;07F;08F;09F;10F;11F;14F;17F;18F;20F;24F;25F;26F;29F;30F;31F;32F;35F;37F;40F;43F;44F;45F;48F;50F;50F;57F;61F;62F;67F;68F;80F;82F;83F;84F;F01:F99'.split(';')),
    '4000': Bandeira('4000',
        centros_fornecedores='B001;B098;B184;B191;B289'.split(';'),
        planejadores_mrp=['A02']),
    '4003': Bandeira('4003',
        centros_fornecedores=['B703'],
        planejadores_mrp=[],
        aplicaPasso10=False),
}

def create_loja_from_line(line):

    BANDEIRA = 0
    LOJA = 1
    HORARIO_INICIO = 2

    reg = [x.strip() for x in line.split('\t') ]
    hora, minuto, segundo = map(int,reg[HORARIO_INICIO].split(':'))
    return Loja(reg[LOJA], BANDEIRAS[reg[BANDEIRA]],
        DATA_INICIO.replace(hour=hora, minute=minuto, second=segundo))

LOJAS = map(create_loja_from_line, raconfig.LOJAS.splitlines());

class Loja:

    SEMANAL = 'W'
    DIARIO = 'T'
    PERIODO_ATUAL = 'A'

    def __init__(self, id, bandeira, data_inicio):
        self.id = id
        self.bandeira = bandeira
        self.data_inicio = data_inicio
        self.DATA_EXECUCAO_FROM = data_inicio.strftime('%Y%m%d')

    def get_id(self):
        return self.id

    def get_filial(self):
        return 'A'

    def get_tipos_mrp(self):
        return raconfig.TIPOS_MRP

    def criar_paso_1(self):

        step = Step('ZVPRG_ANULA_POS_SOL_PEDIDO', RAConfig.USUARIO)
        step.add_screen_item(ScreenItemDeltaDate(datetime.timedelta(days=1), 'SO_BADAT', self.DATA_EXECUCAO_FROM, 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('SO_WERKS', self.get_id(), 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('PA_BSART', 'NB'))

        return step

    def criar_paso_2(self):

        step = Step('RMPROG00', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('WERK', self.get_id(), 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('VLFKZ', self.get_filial()))
        step.add_screen_item(ScreenItem('PERKZ', Loja.DIARIO))
        step.add_screen_item(ScreenItem('PRDUR', Loja.PERIODO_ATUAL))
        step.add_screen_item(ScreenItem('UPDTE', 'X'))
        step.add_screen_item(ScreenItem('PROTO', ' '))

        return step

    def criar_paso_3(self):

        step = Step('RMPROG00', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('WERK', self.get_id(), 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('VLFKZ', self.get_filial()))
        step.add_screen_item(ScreenItem('PERKZ', Loja.SEMANAL))
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
        step.add_screen_item(ScreenItem('G_PKT', '10000'))
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

        step = Step('RM06BB30', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('S_EKORG', '4005', 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('S_WERKS', self.get_id(), 'S', 'I', 'EQ'))

        for centro_fornecedor in self.bandeira.centros_fornecedores:
            step.add_screen_item(ScreenItem('S_RESWK', centro_fornecedor, 'S', 'I', 'EQ'))

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

        for planejador_mrp in self.bandeira.planejadores_mrp:
            step.add_screen_item(ScreenItem('S_DISPO', planejador_mrp, 'S', 'I', 'EQ'))

        step.add_screen_item(ScreenItem('P_VRTYPK', 'X'))

        return step

    def criar_paso_10(self):

        step = Step('RM06BB30', RAConfig.USUARIO)
        step.add_screen_item(ScreenItem('S_EKORG', '4005', 'S', 'I', 'EQ'))
        step.add_screen_item(ScreenItem('S_WERKS', self.get_id(), 'S', 'I', 'EQ'))

        for centro_fornecedor in self.bandeira.centros_fornecedores:
            step.add_screen_item(ScreenItem('S_RESWK', centro_fornecedor, 'S', 'I', 'EQ'))

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

    def aplicaPasso10(self):
        return self.bandeira.aplicaPasso10

    def criar_job_ra(self):
        job = Job('CORRIDA_RA_%s' % self.get_id(), start_datetime=self.data_inicio)
        job.add_step(self.criar_paso_1())
        job.add_step(self.criar_paso_2())
        job.add_step(self.criar_paso_3())
        job.add_step(self.criar_paso_4())
        job.add_step(self.criar_paso_5())
        job.add_step(self.criar_paso_6())
        job.add_step(self.criar_paso_7())
        job.add_step(self.criar_paso_9())
        if self.aplicaPasso10():
            job.add_step(self.criar_paso_10())
        return job



class RAConfig(Config):

    USUARIO = 'BDC_RETAIL'

    def __init__(self):
        super(RAConfig, self).__init__()

        EXECUTION_INTERVAL = 24*60*60
        DATA_EXECUCAO_TO = (DATA_INICIO + datetime.timedelta(days=(QUANTIDADE_DIAS_PLANEJAR-1))).strftime('%Y%m%d')

        jobs = []
        for loja in LOJAS:
            job = loja.criar_job_ra()
            jobs.append(job)

        while (jobs[0].steps[0].get_screen_item('SO_BADAT').low <= DATA_EXECUCAO_TO):
            for job in jobs:
                self.add_job(job)
            jobs = [ job.next(ExecutionInterval(datetime.timedelta(seconds=(EXECUTION_INTERVAL)))) for job in jobs ]

c = RAConfig()
c.save('./ra.xls')
