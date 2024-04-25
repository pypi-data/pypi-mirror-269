###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# pylint: disable=import-outside-toplevel, protected-access
from importlib import reload
from os import environ, rename
from pathlib import Path
from sys import platform
from unittest import TestCase, skipUnless
from everysk import config
from everysk.core.exceptions import FieldValueError


class SettingsModulesTestCase(TestCase):

    def setUp(self) -> None:
        if platform == 'linux':
            self.root = '/var/app'
        elif platform == 'win32':
            self.root = 'C:\\var\\app'

        self.old_project_root = environ.get('PROJECT_ROOT', Undefined)
        self.old_everysk_root = config.EVERYSK_ROOT

    def tearDown(self) -> None:
        if self.old_project_root is not Undefined:
            environ['PROJECT_ROOT'] = self.old_project_root
        elif 'PROJECT_ROOT' in environ:
            environ.pop('PROJECT_ROOT')

        config.EVERYSK_ROOT = self.old_everysk_root

    @skipUnless(platform == 'linux', 'Runs only in Linux system.')
    def test_linux_simple_path(self):
        entry = Path('/var/app/settings.py')
        module = config.get_full_dotted_path_module(entry, self.root)
        self.assertEqual(module, 'settings')

    @skipUnless(platform == 'win32', 'Runs only in Windows system.')
    def test_windows_simple_path(self):
        entry = Path('C:\\var\\app\\settings.py')
        module = config.get_full_dotted_path_module(entry, self.root)
        self.assertEqual(module, 'settings')

    @skipUnless(platform == 'linux', 'Runs only in Linux system.')
    def test_linux_complex_path(self):
        entry = Path('/var/app/src/everysk/sdk/entities/settings.py')
        module = config.get_full_dotted_path_module(entry, self.root)
        self.assertEqual(module, 'src.everysk.sdk.entities.settings')

    @skipUnless(platform == 'win32', 'Runs only in Windows system.')
    def test_windows_complex_path(self):
        entry = Path('C:\\var\\app\\src\\everysk\\sdk\\entities\\settings.py')
        module = config.get_full_dotted_path_module(entry, self.root)
        self.assertEqual(module, 'src.everysk.sdk.entities.settings')

    def test_get_all_modules_everysk_lib(self):
        if 'PROJECT_ROOT' in environ:
            environ.pop('PROJECT_ROOT')

        modules = config.get_all_modules()
        # We could no guarantee the order of this list
        # the only thing that is needed is 'everysk.settings' to be the first
        self.assertEqual(modules[0], 'everysk.settings')

        # Now we check that every settings was read
        self.assertEqual(sorted(modules), [
            'everysk.sdk.entities.custom_index.settings',
            'everysk.sdk.entities.datastore.settings',
            'everysk.sdk.entities.file.settings',
            'everysk.sdk.entities.portfolio.settings',
            'everysk.sdk.entities.private_security.settings',
            'everysk.sdk.entities.report.settings',
            'everysk.sdk.entities.settings',
            'everysk.sdk.settings',
            'everysk.settings'
        ])

    def test_get_all_modules_project_root(self):
        environ['PROJECT_ROOT'] = f'{config.EVERYSK_ROOT}/sdk/entities/file'
        config.EVERYSK_ROOT = ''
        modules = config.get_all_modules()
        self.assertListEqual(modules, ['settings'])


class SettingsTestCase(TestCase):
    """
    Because we need the correct project root folder we import the class/functions inside every test
    """
    # we need to rename these files to avoid use then on prod environ
    old_settings = [f'{config.EVERYSK_ROOT}/core/fixtures/other/_settings.py', f'{config.EVERYSK_ROOT}/core/fixtures/_settings.py']
    new_settings = [f'{config.EVERYSK_ROOT}/core/fixtures/other/settings.py', f'{config.EVERYSK_ROOT}/core/fixtures/settings.py']

    @classmethod
    def setUpClass(cls) -> None:
        rename(cls.old_settings[0], cls.new_settings[0])
        rename(cls.old_settings[1], cls.new_settings[1])
        # Because we changed the settings files we need to reload the module
        del config.settings
        reload(config)

    @classmethod
    def tearDownClass(cls) -> None:
        rename(cls.new_settings[0], cls.old_settings[0])
        rename(cls.new_settings[1], cls.old_settings[1])
        # Because we changed the settings files we need to reload the module
        del config.settings
        reload(config)

    def test_get_all_settings_singleton(self):
        settings01 = config.Settings()
        settings02 = config.Settings()
        self.assertEqual(settings01, settings02)

    def test_settings(self):
        self.assertEqual(config.settings.EVERYSK_TEST_NAME, 'test-case')
        self.assertEqual(config.settings.EVERYSK_TEST_OTHER_NAME, 'test-other-case')
        self.assertEqual(config.settings.EVERYSK_TEST_INT, 1)
        self.assertEqual(config.settings.EVERYSK_TEST_OTHER_INT, 2)
        self.assertTrue(config.settings.EVERYSK_TEST_FAKE)
        self.assertTrue(config.settings.EVERYSK_TEST_OTHER_FAKE)

        # See if the setting was replaced
        self.assertEqual(config.settings.EVERYSK_TEST_FIELD_INHERIT, 'test-case as True')
        self.assertEqual(config.settings.EVERYSK_TEST_VAR_INHERIT, 'True as test-case')
        self.assertEqual(config.settings.EVERYSK_TEST_OTHER_FIELD_INHERIT, 'test-case as True')
        self.assertEqual(config.settings.EVERYSK_TEST_OTHER_VAR_INHERIT, 'True as test-case')

        # Test readonly attributes
        with self.assertRaisesRegex(FieldValueError, "The field 'EVERYSK_TEST_NAME' value cannot be changed."):
            config.settings.EVERYSK_TEST_NAME = 'new-test'

        # Test validation
        with self.assertRaisesRegex(FieldValueError, "Key EVERYSK_TEST_INT must be <class 'int'>."):
            config.settings.EVERYSK_TEST_INT = 'new-test'

    def test_settings_environment_value(self):
        self.assertEqual(config.settings.EVERYSK_TEST_BOOL_VAR, False)
        self.assertEqual(config.settings.EVERYSK_TEST_FAKE, True)
        self.assertEqual(config.settings.EVERYSK_TEST_INT, 1)
        environ['EVERYSK_TEST_FAKE'] = '0'
        environ['EVERYSK_TEST_BOOL_VAR'] = '1'
        environ['EVERYSK_TEST_INT'] = '2'
        del config.settings
        reload(config)
        self.assertEqual(config.settings.EVERYSK_TEST_BOOL_VAR, True)
        self.assertEqual(config.settings.EVERYSK_TEST_FAKE, False)
        self.assertEqual(config.settings.EVERYSK_TEST_INT, 2)
        # Cleanup environ
        del environ['EVERYSK_TEST_FAKE']
        del environ['EVERYSK_TEST_BOOL_VAR']
        del environ['EVERYSK_TEST_INT']

    def test_config_pyi_file(self):
        config_pyi_file = None
        with open(f'{config.EVERYSK_ROOT}/config.pyi', 'r', encoding='utf-8') as arq:
            config_pyi_file = arq.read()

        self.assertIn('EVERYSK_TEST_OTHER_FAKE: bool', config_pyi_file)
        self.assertIn('EVERYSK_TEST_OTHER_FIELD_INHERIT: str', config_pyi_file)
        self.assertIn('EVERYSK_TEST_OTHER_INT: int', config_pyi_file)
        self.assertIn('EVERYSK_TEST_OTHER_NAME: str', config_pyi_file)
        self.assertIn('EVERYSK_TEST_OTHER_VAR_INHERIT: str', config_pyi_file)
        self.assertIn('EVERYSK_TEST_BOOL_VAR: bool', config_pyi_file)
        self.assertIn('EVERYSK_TEST_FAKE: bool', config_pyi_file)
        self.assertIn('EVERYSK_TEST_FIELD_INHERIT: str', config_pyi_file)
        self.assertIn('EVERYSK_TEST_INT: int', config_pyi_file)
        self.assertIn('EVERYSK_TEST_NAME: str', config_pyi_file)
        self.assertIn('EVERYSK_TEST_VAR_INHERIT: str', config_pyi_file)
        self.assertIn('DEBUG: bool', config_pyi_file)
        self.assertIn('EVERYSK_GOOGLE_CLOUD_LOCATION: str', config_pyi_file)
        self.assertIn('EVERYSK_GOOGLE_CLOUD_PROJECT: str', config_pyi_file)
        self.assertIn('REDIS_HOST: str', config_pyi_file)
        self.assertIn('REDIS_PORT: int', config_pyi_file)

    def test_none_default_value(self):
        # https://everysk.atlassian.net/browse/COD-3833
        self.assertIsNone(config.settings.EVERYSK_TEST_STR_DEFAULT_NONE)
        config.settings.EVERYSK_TEST_STR_DEFAULT_NONE = 'string'

    def test_undefined_default_value(self):
        # https://everysk.atlassian.net/browse/COD-3833
        self.assertEqual(config.settings.EVERYSK_TEST_STR_DEFAULT_UNDEFINED, Undefined)
        config.settings.EVERYSK_TEST_STR_DEFAULT_UNDEFINED = 'string'
