
#!/usr/bin/env python3

"""Console script for wireguard_tools."""

import sys
import click
from pathlib import Path

from wireguard_tools import WireguardConfig

def validate_endpoint(args):
    try:
        value = args['endpoint']
        addr, port = value.split(':')
        if addr and port:
            args['endpoint_addr'] = addr 
            args['endpoint_port'] = port
            del(args['endpoint'])
            return
        else:
            raise ValueError
    except ValueError:
        raise click.BadParameter("endpoint must be hostname:port or ip:port")


@click.command(context_settings=dict(show_default=True))
@click.argument('endpoint', metavar='ENDPOINT', type=str)
@click.option('-c', '--count', default=8, metavar='PEER_COUNT', type=int, help='number of peers to configure')
@click.option('-p', '--peers_reachable', is_flag=True, default=False, help='enable peer-to-peer connectivity')
@click.option('-k', '--keepalive', default=25, type=int, help='if nonzero, set keepalive timeout in seconds')
@click.option('-b', '--network-base', metavar='NETWORK_BASE', default='10.10', type=str, help='first two octets of network address')
@click.option('-n', '--network', metavar='NETWORK_NUMBER', default=10, type=int, help='3rd octet of network address')
@click.option('-o', '--offset', metavar='PEER_OFFSET', default=32, help='peer host number offset')
@click.option('-O', '--output_dir', type=click.Path(exists=False, file_okay=False, writable=True, path_type=Path),
        metavar='OUTPUT_DIR', show_default=True, default=Path('.')/'config', help='output directory')
def main(**args):
    """generate a set of wireguard configuration files for ENDPOINT [address:port]"""
    validate_endpoint(args)
    cfg = WireguardConfig(click.echo)
    cfg.generate(**args)
    cfg.write_files(args['output_dir'])

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
