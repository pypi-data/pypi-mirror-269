###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
__all__ = ['settings']
from importlib import import_module
from inspect import getmembers, isroutine, isclass
from os import getenv
from os.path import dirname, exists, sep
from pathlib import Path, PosixPath
from re import findall
from typing import Any
from everysk.core.object import BaseObject, MetaClass
from everysk.utils import bool_convert


# The root path of the everysk lib we need this to create the correct stub file
EVERYSK_ROOT = dirname(__file__)


def get_full_dotted_path_module(entry: PosixPath, root: str) -> str:
    """
    From the full path we need to generate the module that is valid for import.
    Changes '/var/app/src/everysk/settings.py' to 'everysk.settings'.

    Args:
        entry (PosixPath): The posix path object.
        root (str): The root path that will be removed.
    """
    # /var/app/src/everysk/settings.py
    module = str(entry)

    # everysk/settings.py
    module = module.replace(f'{root}{sep}', '')

    # everysk/settings
    module = module.replace('.py', '')

    # everysk.settings
    module = module.replace(sep, '.')

    return module


def get_all_modules() -> list:
    """
    We search inside EVERYSK_ROOT and PROJECT_ROOT for 'settings.py'
    files and convert this files into python modules.
    """
    search_name = 'settings.py'
    modules = []
    if EVERYSK_ROOT and exists(EVERYSK_ROOT):
        # we need to remove the '/everysk' from the path to create the correct module path
        root = EVERYSK_ROOT.replace(f'{sep}everysk', '')
        for entry in Path(EVERYSK_ROOT).rglob(search_name):
            modules.append(get_full_dotted_path_module(entry=entry, root=root))

    project_root = getenv('PROJECT_ROOT')
    if project_root and exists(project_root):
        for entry in Path(project_root).rglob(search_name):
            modules.append(get_full_dotted_path_module(entry=entry, root=project_root))

    return modules


def get_all_attributes() -> list[tuple[str, Any, Any]]:
    """ Get all attributes from the settings modules except ones that starts with '_' """
    result = []

    for module in get_all_modules():
        # Import the module
        module = import_module(module)

        for attr, value in getmembers(module, predicate=lambda x: not isroutine(x) and not isclass(x)):
            if not attr.startswith('_'):
                try:
                    attr_value = value.default
                    attr_type = value
                except AttributeError:
                    attr_value = value
                    # If this attribute already has an annotation on the module we use it
                    # otherwise we get the class of the value as the annotation
                    # https://everysk.atlassian.net/browse/COD-3833
                    attr_type = module.__annotations__.get(attr, type(value))

                result.append((attr, attr_type, attr_value))

    return result


def update_settings_attributes():
    """
    Set all settings in the Settings class and update the stub file config.pyi.
    """
    with open(f'{EVERYSK_ROOT}/config.pyi', 'w', encoding='utf-8') as stubs:
        # This fix the stub file for the RegexField
        stubs.write('from re import Pattern\n\n')

        # Write the class in the stub file
        stubs.write('class Settings:\n')

        attributes = set()
        for attr_name, attr_type, attr_value in get_all_attributes():
            Settings.__set_attribute__(attr_name, attr_type, attr_value)
            try:
                # If attr_type is a Everysk Field the real value will be in the attr_type attribute
                attr_type = attr_type.attr_type
            except AttributeError:
                pass
            # We could have some duplicated attributes so we keep then in a set
            attributes.add(f'    {attr_name}: {attr_type.__name__}\n')

        # Then we write all attributes in the stub file
        stubs.writelines(sorted(attributes))

        # This is needed to VS Code understand the instance
        stubs.write('\nsettings: Settings\n')


class Settings(BaseObject):

    def __new__(cls, *args, **kwargs) -> 'Settings':
        """ Changed to keep only one instance for the class """
        try:
            return settings
        except NameError:
            pass

        return object.__new__(cls, *args, **kwargs)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # after the initialization of the instance, we update the attributes list
        update_settings_attributes()

    def __getattribute__(self, name: str) -> Any:
        """
        This method try to first get the value from the environment
        if this does not exists get from the class.

        Args:
            name (str): The setting name.
        """
        # We get the value from the environment or from the class
        value = getenv(name) or super().__getattribute__(name)

        # This is a check to always get the correct value
        # https://everysk.atlassian.net/browse/COD-907
        # https://everysk.atlassian.net/browse/COD-3833
        if value is not None and value is not Undefined:
            attributes = getattr(Settings, MetaClass._attr_name, {})
            try:
                attr_type = attributes[name]
                try:
                    value = attr_type.clean_value(value)
                except AttributeError:
                    # For bool types we use a specific function
                    if attr_type != bool:
                        value = attr_type(value)
                    else:
                        value = bool_convert(value)
            except KeyError:
                pass

        if isinstance(value, str):
            try:
                # If is a normal string nothing happen
                value = value.format()
            except KeyError:
                # Then we get all {*} that appears
                keys = findall(r'{(.*?)}', value)
                # Then we get the real value of each key
                kwargs = {key: getattr(self, key) for key in keys}
                # Then we try to format the real string
                value = value.format(**kwargs)

        return value


## Here we load all computed settings on one var
settings: Settings = Settings()
