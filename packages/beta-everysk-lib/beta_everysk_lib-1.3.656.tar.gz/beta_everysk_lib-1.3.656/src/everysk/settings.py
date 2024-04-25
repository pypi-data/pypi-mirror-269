###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from everysk.core.fields import BoolField, ChoiceField, IntField, StrField

## Project settings
DEBUG = BoolField(default=True)

# PROD | DEV | LOCAL
PROFILE = ChoiceField(default='DEV', choices=('PROD', 'DEV', 'LOCAL'))

## Redis
REDIS_HOST = StrField(default='0.0.0.0')
REDIS_PORT = IntField(default=6379)

## Google Cloud
EVERYSK_GOOGLE_CLOUD_LOCATION = StrField(default='us-central1')
EVERYSK_GOOGLE_CLOUD_PROJECT = StrField()
# This enables/disables the Google Cloud Logging Handler
EVERYSK_GOOGLE_CLOUD_LOGGING_INTEGRATION = BoolField(default=True)

## Slack URL to send messages
SLACK_URL = StrField()
