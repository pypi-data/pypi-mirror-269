###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

import holidays
from holidays.countries import BR
from everysk.core.datetime import Date

class BRHolidays(BR):

    def _populate(self, year):
        super()._populate(year)

        self.pop_named('Início da Quaresma')
        self.pop_named('Dia do Servidor Público')
        self.pop_named('Véspera de Natal')
        self.pop_named('Véspera de Ano-Novo')

class ANBIMA(BRHolidays):
    pass

class BVMF(BRHolidays):
    def _populate(self, year):
        super()._populate(year)

        if year < 2022:
            self[Date(year, 1, 25)] = 'Aniversário de São Paulo'
            self[Date(year, 11, 20)] = 'Dia da Consciência Negra'

def get_holidays(calendar: str, years: list = range(2000, 2100)) -> dict:
    """
    Uses https://pypi.org/project/holidays/ to make a list of dates.
    Pass a list of years if you need a more specific list.

    Args:
        calendar (str): Two digit country symbol.
        years (list, optional): List of int years. Ex: [2021, 2022]. Defaults to [2000, ..., 2099].
    """

    holidays.BVMF = BVMF
    holidays.ANBIMA = ANBIMA

    return {Date(dt.year, dt.month, dt.day): name for dt, name in holidays.country_holidays(calendar, years=years).items()}
