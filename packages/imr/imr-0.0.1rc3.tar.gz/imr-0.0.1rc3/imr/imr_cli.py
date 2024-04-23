"""Path module.

For handling local files and directory operations.
"""

from pathlib import Path

import click

from imr.imr import IMRLocal, IMRRemote, load_config


class Context:
    """The context for all CLI commands."""

    home = Path.home()
    imr_dir = home / ".imr"
    imr_local: IMRLocal
    imr_remote: IMRRemote


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Get the cli command options."""
    ctx.obj = Context()


@cli.group()
@click.option("-c", "--config", type=str, help="name of the configuration.")
@click.pass_obj
def local(obj: Context, config: str) -> None:
    """Get local command options."""
    if config is not None:
        config_params = load_config(config)
        obj.imr_local = IMRLocal(config_params["path"])
    else:
        obj.imr_local = IMRLocal(str(obj.imr_dir))


@local.command("list")
@click.pass_obj
def list_local(obj: Context) -> None:
    """List local packages."""
    for package in obj.imr_local.list():
        click.echo(package)


@local.command("rm")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def rm_local(obj: Context, package: str, version: str) -> None:
    """Remove local packages."""
    obj.imr_local.rm(package, version)


@local.command("path")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def path_local(obj: Context, package: str, version: str) -> None:
    """Get remote model path."""
    click.echo(obj.imr_local.path(package, version))


@cli.group()
@click.option("-h", "--host", type=str, help="Server host address ie. http://mymodelhost.me.")
@click.option("-u", "--user", type=str, help="Server host user.")
@click.option("-p", "--password", type=str, help="Server host password.")
@click.option("-c", "--config", type=str, help="Remote configuration.")
@click.pass_obj
def remote(obj: Context, host: str, user: str, password: str, config: str) -> None:
    """Get remote command cli options."""
    if host is not None:
        obj.imr_remote = IMRRemote(host, user, password)
    else:
        config_params = load_config(config)
        obj.imr_remote = IMRRemote(
            config_params["host"], config_params["user"], config_params["password"]
        )


@remote.command("list")
@click.pass_obj
def list_remote(obj: Context) -> None:
    """List remote packages."""
    packages = obj.imr_remote.list()
    for p in packages:
        click.echo(p)


@remote.command("rm")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def rm_remote(obj: Context, package: str, version: str) -> None:
    """Remove remote package."""
    obj.imr_remote.rm(package, version)


@remote.command("push")
@click.argument("model_dir")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def push_remote(obj: Context, model_dir: str, package: str, version: str) -> None:
    """Push model to remote repository."""
    obj.imr_remote.push(model_dir, package, version)


@remote.command()
@click.argument("package")
@click.option(
    "-d",
    "--dir",
    type=str,
    help="directory to pull the model in.",
    show_default=True,
)
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def pull(obj: Context, package: str, model_dir: str, version: str) -> None:
    """Pull model from remote repository."""
    obj.imr_remote.pull(model_dir, package, version)


@remote.command("path")
@click.argument("package")
@click.option(
    "-v", "--version", type=str, default="latest", help="version of the model.", show_default=True
)
@click.pass_obj
def path_remote(obj: Context, package: str, version: str) -> None:
    """Get remote model path."""
    click.echo(obj.imr_remote.path(package, version))
