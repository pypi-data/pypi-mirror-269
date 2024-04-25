###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from everysk.core.fields import IntField, StrField

###############################################################################
#   Settings Implementation
###############################################################################
SIMPLE_UNIQUE_ID_LENGTH = IntField(default=8, readonly=True)

APP_URL = StrField(default='https://app.everysk.com', readonly=True)
