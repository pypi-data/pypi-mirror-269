from .cli import cli  # isort:skip

from TableauConMan.cli import provisioning


def main():
    cli()


__all__ = ["provisioning.py"]
