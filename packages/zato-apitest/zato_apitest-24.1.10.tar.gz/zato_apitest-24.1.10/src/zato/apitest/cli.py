# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Proprietary product. This is not open source software, reproduction is prohibited.
"""

# stdlib
import os, sys, tempfile, uuid

# Click
import click

# Zato
from zato.apitest import init as _init, run as _run

# ################################################################################################################################
# ################################################################################################################################

if 0:
    from click import Context

# ################################################################################################################################
# ################################################################################################################################

@click.group()
def main():
    pass

# ################################################################################################################################
# ################################################################################################################################

def cli_init(ctx:'Context', path:'str', prompt_run:'bool'=True) -> 'None':
    if os.path.exists(path) and os.listdir(path):
        click.echo(ctx.get_help())
        click.echo('\nError: directory `{}` is not empty, quitting.'.format(path))
        sys.exit(1)

    if not os.path.exists(path):
        click.echo('Creating directory `{}`.'.format(path))
        os.makedirs(path)

    _init.handle(path)
    click.echo('OK, initialized.')

    if prompt_run:
        click.echo('Run `apitest run {}` for a live demo.'.format(path))

# ################################################################################################################################
# ################################################################################################################################

@click.command()
@click.argument('path', type=click.Path(exists=False, file_okay=False, resolve_path=True))
@click.pass_context
def init(ctx:'Context', path:'str') -> 'None':
    cli_init(ctx, path)

# ################################################################################################################################
# ################################################################################################################################

@click.command(context_settings=dict(allow_extra_args=True, ignore_unknown_options=True))
@click.argument('path', type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.pass_context
def run(ctx:'Context', path:'str') -> 'None':
    sys.exit(_run.handle(path, ctx.args))

# ################################################################################################################################
# ################################################################################################################################

@click.command()
@click.argument('path', default=tempfile.gettempdir(), type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.pass_context
def demo(ctx:'Context', path:'str') -> 'None':
    # We're not using tempfile.mkdtemp because we may as well be run
    # in a user-provided directory.
    path = os.path.join(path, 'apitest.' + uuid.uuid4().hex)
    cli_init(ctx, path, False)
    _ = _run.handle(path)

# ################################################################################################################################
# ################################################################################################################################

main.add_command(init) # type: ignore
main.add_command(run) # type: ignore
main.add_command(demo) # type: ignore

# ################################################################################################################################
# ################################################################################################################################

if __name__ == '__main__':
    main()

# ################################################################################################################################
# ################################################################################################################################
