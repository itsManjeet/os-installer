# SPDX-License-Identifier: GPL-3.0-or-later

import yaml

DEFAULT_CONFIG_PATH = '/etc/os-installer/config.yaml'


def _bool_to_int(b: bool):
    return 1 if b else 0


def _match(config, prop, *ok_types):
    if not prop in config:
        print(f'Config error: {prop} does not exist.')
        return False
    has_type = type(config[prop])
    for ok_type in ok_types:
        if has_type == ok_type:
            return True
    print(f'Config error: {prop} not of expected type (expected',
          f'{ok_types}, but got {has_type}')
    return False


def _install_variables_set(config):
    install_variables = ['locale', 'disk_device_path', 'disk_is_partition',
                         'disk_efi_partition', 'use_encryption', 'encryption_pin']
    return all([var in config for var in install_variables])


def _configure_variables_set(config):
    configure_variables = ['user_name', 'user_autologin', 'user_password',
                           'formats_locale', 'timezone', 'chosen_software_packages']
    return all([var in config for var in configure_variables])


def _load_default_config():
    return {
        # general
        'distribution_name': 'Untitled',
        # internet
        'internet_connection_required': True,
        'internet_checker_url': 'http://nmcheck.gnome.org/check_network_status.txt',
        # language
        'suggested_languages': [ 'hi', 'en', 'ar', 'de', 'es', 'fr', 'ja', 'ru', 'zh'],
        'fixed_language': False,
        # welcome
        'welcome_page': {'usage': True, 'logo': None, 'text': None},
        # disk
        'minimum_disk_size': 5,
        'offer_disk_encryption': True,
        # optional pages
        'skip_user': False,
        'skip_locale': False,
        # software
        'additional_software': [],
        # fail
        'failure_help_url': 'https://duckduckgo.com/?q="os-installer {}"+"failed installation"',
        # commands
        'browser_cmd': 'epiphany',
        'disks_cmd': 'gnome-disks',
        'wifi_cmd': 'gnome-control-center wifi',

        # not configurable
        'version': -1,
    }


def _load_optional_defaults(config):
    config['use_encryption'] = False
    config['encryption_pin'] = ''
    config['user_name'] = 'user'
    config['user_autologin'] = True
    config['user_password'] = 'password'
    config['formats_locale'] = 'en_US.UTF-8'
    config['formats_ui'] = 'United States'
    config['timezone'] = 'UTC'
    config['chosen_software_packages'] = ''
    config['chosen_software'] = []


def _set_testing_defaults(config):
    '''Default values used when skipping pages during testing.'''
    config["language"] = 'English for Dummies'
    config["language_code"] = 'en_US'
    config["locale"] = 'en_US.UTF-8'
    config["keyboard_layout"] = 'us'
    config["keyboard_layout_ui"] = 'English (US)'
    config["disk_device_path"] = '/dev/null'
    config["disk_is_partition"] = False
    config["disk_efi_partition"] = '/dev/null'
    config['disk_name'] = 'Test Dummy'


def _valid(config):
    assert not config['fixed_language'] == True, 'Need to specify or disable fixed language.'
    return (
        _match(config, 'welcome_page', dict) and
        _match(config['welcome_page'], 'usage', bool) and
        _match(config['welcome_page'], 'logo', str, type(None)) and
        _match(config['welcome_page'], 'text', str, type(None)) and
        _match(config, 'internet_connection_required', bool) and
        _match(config, 'internet_checker_url', str) and
        _match(config, 'suggested_languages', list) and
        _match(config, 'minimum_disk_size', int) and
        _match(config, 'offer_disk_encryption', bool) and
        _match(config, 'additional_software', list) and
        _match(config, 'distribution_name', str) and
        _match(config, 'fixed_language', bool, str))


### public methods ###
def init_config():
    config = _load_default_config()
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as file:
            config_from_file = yaml.load(file, Loader=yaml.Loader)
            for config_property in config_from_file:
                if type(config[config_property]) is dict:
                    for key, value in config_from_file[config_property].items():
                        config[config_property][key] = value
                else:
                    config[config_property] = config_from_file[config_property]
    except:
        print('No config provided or config contains syntax errors, '
              'using default config.')
        config = _load_default_config()
    if not _valid(config):
        print('Config errors, loading default config.')
        config = _load_default_config()
    _load_optional_defaults(config)
    _set_testing_defaults(config)
    return config


def create_envs(config, with_install_envs, with_configure_envs):
    if (with_install_envs and not _install_variables_set(config) or
            with_configure_envs and not _configure_variables_set(config)):
        return None
    envs = []
    if with_install_envs:
        envs += [
            f'OSI_LOCALE={config["locale"]}',
            f'OSI_DEVICE_PATH={config["disk_device_path"]}',
            f'OSI_DEVICE_IS_PARTITION={_bool_to_int(config["disk_is_partition"])}',
            f'OSI_DEVICE_EFI_PARTITION={config["disk_efi_partition"]}',
            f'OSI_USE_ENCRYPTION={_bool_to_int(config["use_encryption"])}',
            f'OSI_ENCRYPTION_PIN={config["encryption_pin"]}',
        ]
    if with_configure_envs:
        envs += [
            f'OSI_USER_NAME={config["user_name"]}',
            f'OSI_USER_AUTOLOGIN={_bool_to_int(config["user_autologin"])}',
            f'OSI_USER_PASSWORD={config["user_password"]}',
            f'OSI_FORMATS={config["formats_locale"]}',
            f'OSI_TIMEZONE={config["timezone"]}',
            f'OSI_ADDITIONAL_SOFTWARE={config["chosen_software_packages"]}',
        ]
    return envs + [None]
