#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import six
import click

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
    mod_config = get_mod_conf()
    
@cli.command()
@click.option('-v', '--verbose', is_flag=True)
def version(**kwargs):
    """
    Output Version Info
    """
    from bwtougu import version_info
    six.print_("Current Version: ", version_info)
    
if __name__ == '__main__':
    entry_point()