#!/usr/bin/env python
import click
import totp_vanilla


@click.command()
@click.version_option(version="0.4", prog_name="totp")
@click.option('-s', '--secret', required=True, help='Base32 encoded secret bytes.')
def main(secret):

    print(totp_vanilla.totp(secret))


if __name__ == "__main__":
    main()
