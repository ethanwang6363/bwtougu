#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 程序入口文件，通过entry_point函数作为程序入口，接入程序主逻辑
# 然后通过命令行接口解析命令行参数，形成不同的入口分支
import os
import six
import click
from importlib import import_module

from bwtougu.utils.click_helper import Date
from bwtougu.utils.config import parse_config, dump_config

CONTEXT_SETTINGS={
    'default_map': {
        'run': {
        }
    }
}

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True)
@click.help_option('-h', '--help')
@click.pass_context
def cli(ctx, verbose):
    ctx.obj["VERBOSE"] = verbose

def entry_point():
    print("entry_point...")
    inject_mod_commands()
    cli(obj={})
    
def inject_mod_commands():
    from bwtougu.utils.config import get_mod_conf
    from bwtougu.mod import SYSTEM_MOD_LIST
    from bwtougu.utils.package_helper import import_mod
    mod_config = get_mod_conf()
    for mod_name, config in six.iteritems(mod_config['mod']):
        if 'lib' in config:
            lib_name = config["lib"]
        else:
            lib_name = "bwtougu_mod_{}".format(mod_name)
        if not config['enabled']:
            continue
        try:
            if mod_name in SYSTEM_MOD_LIST:
                import_mod("bwtougu.mod." + lib_name)
            else:
                import_mod(lib_name)
        except Exception as e:
            pass

@cli.command()
@click.option('-v', '--verbose', is_flag=True)
def version(**kwargs):
    """
    Output Version Info
    """
    from bwtougu import version_info
    six.print_("Current Version: ", version_info)

@cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.help_option('-h', '--help')
@click.argument('cmd', nargs=1, type=click.Choice(['list', 'enable', 'disable', 'install', 'uninstall']))
@click.argument('params', nargs=-1)
def mod(cmd, params):
    """
    Mod management command

    bwtougu mod list
    bwtougu mod install xxx
    bwtougu mod uninstall xxx
    bwtougu mod enable xxx
    bwtougu mod disable xxx
    """
    def list(params):

        from colorama import init, Fore
        from tabulate import tabulate
        from bwtougu.utils.config import get_mod_conf
        init()

        mod_config = get_mod_conf()
        table = []

        for mod_name, mod in six.iteritems(mod_config['mod']):
            table.append([
                Fore.RESET + mod_name,
                (Fore.GREEN + "enabled" if mod['enabled'] else Fore.RED + "disabled") + Fore.RESET
            ])

        headers = [
            Fore.CYAN + "name",
            Fore.CYAN + "status" + Fore.RESET
        ]

        six.print_(tabulate(table, headers=headers, tablefmt="psql"))
        six.print_(Fore.LIGHTYELLOW_EX + "You can use `bwtougu mod list/install/uninstall/enable/disable` to manage your mods")

    def enable(params):
        """
        enable mod
        """
        mod_name = params[0]
        if "bwtougu_mod_" in mod_name:
            mod_name = mod_name.replace("bwtougu_mod_", "")

        # check whether is installed
        module_name = "bwtougu_mod_" + mod_name
        if module_name.startswith("bwtougu_mod_sys_"):
            module_name = "bwtougu.mod." + module_name
        try:
            import_module(module_name)
        except ImportError:
            pass

        from bwtougu.utils.config import user_mod_conf_path, load_yaml
        user_conf = load_yaml(user_mod_conf_path()) if os.path.exists(user_mod_conf_path()) else {'mod': {}}

        try:
            user_conf['mod'][mod_name]['enabled'] = True
        except KeyError:
            user_conf['mod'][mod_name] = {'enabled': True}

        dump_config(user_mod_conf_path(), user_conf)

    def disable(params):
        """
        disable mod
        """
        mod_name = params[0]

        if "rqalpha_mod_" in mod_name:
            mod_name = mod_name.replace("rqalpha_mod_", "")

        from bwtougu.utils.config import user_mod_conf_path, load_yaml
        user_conf = load_yaml(user_mod_conf_path()) if os.path.exists(user_mod_conf_path()) else {'mod': {}}

        try:
            user_conf['mod'][mod_name]['enabled'] = False
        except KeyError:
            user_conf['mod'][mod_name] = {'enabled': False}

        dump_config(user_mod_conf_path(), user_conf)

    locals()[cmd](params)

@cli.command()
@click.help_option('-h', '--help')
@click.option('-d', '--data-bundle-path', 'base__data_bundle_path', type=click.Path(exists=True))
@click.option('-f', '--strategy-file', 'base__strategy_file', type=click.Path(exists=True))
@click.option('-s', '--start-date', 'base__start_date', type=Date())
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option('-a', '--account', 'base__accounts', nargs=2, multiple=True, help="set account type with starting cash")
@click.option('-fq', '--frequency', 'base__frequency', type=click.Choice(['1d', '1m', 'tick']))
def run(**kwargs):
    """
    Start to run a strategy
    """
    config_path = kwargs.get('config_path', None)

    from bwtougu import main
    source_code = kwargs.get("base__source_code")
    cfg = parse_config(kwargs, config_path=config_path, click_type=True, source_code=source_code)
    source_code = cfg.base.source_code
    results = main.run(cfg, source_code=source_code)

if __name__ == '__main__':
    entry_point()
