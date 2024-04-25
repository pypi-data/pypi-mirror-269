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
from everysk.core.fields import StrField, IntField, RegexField

###############################################################################
#   Settings Implementation
###############################################################################

FILE_URL_PATH = StrField(default='/file', readonly=True)
FILE_URL_LENGTH = IntField(default=32, readonly=True)
FILE_HASH_LENGTH = IntField(default=40, readonly=True)

FILE_ID_REGEX = RegexField(default=r'^file_[a-zA-Z0-9]', readonly=True)
FILE_ID_MAX_SIZE = IntField(default=30, readonly=True)
FILE_ID_PREFIX = StrField(default='file_', readonly=True)

FILE_DATA_MAX_SIZE_IN_RAW = IntField(default=int(50 * 1024 * 1024), readonly=True)
FILE_DATA_MAX_SIZE_IN_BASE64 = IntField(default=69905066, readonly=True) # int(FILE_DATA_MAX_SIZE_IN_RAW / 3 * 4) # 13.33MB in BASE64 ~= 10MB in RAW

FILE_CONTENT_TYPES: list = [
    None,
    'text/x-comma-separated-values',
    'image/jpeg',
    'application/zip',
    'application/vnd.ms-excel',
    'image/svg+xml',
    'application/javascript',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/bmp',
    'application/octet-stream',
    'text/xml',
    'application/x-zip-compressed',
    'application/pdf',
    'text/csv',
    'application/csv',
    'image/gif',
    'application/xml',
    'text/comma-separated-values',
    'application/json',
    'image/png',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain'
]
