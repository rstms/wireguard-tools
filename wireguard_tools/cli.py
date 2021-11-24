#!/usr/bin/env python3

"""Console script for wireguard_tools."""

import sys
import click
from pathlib import Path

from wireguard_tools import WireguardConfig

@click.command()
@click.argument('gateway-ip', metavar='GATEWAY_IP', type=str)
@click.argument('port', metavar='GATEWAY_PORT', type=int)
@click.argument('network', metavar='NETWORK_NUMBER', type=int)
@click.argument('count', metavar='NUMBER_OF_CLIENTS', type=int)
@click.option('-p/-P', '--peers_reachable/--no_peers_reachable', default=False)
@click.option('-k', '--keepalive', default=25, help='keepalive timeout')
@click.option('-b', '--base_network', metavar='CLASS_B_NETWORK', default='10.33', help='network base ex: 10.33')
@click.option('-o', '--offset', metavar='PEER_OFFSET', default=32, help='peer host number offset')
@click.option('-O', '--output_dir', metavar='OUTPUT_DIR', default='./config', help='output directory')
def wireguard_config_generator(args):
    cfg = WireguardConfig(click.echo)
    cfg.generate(args)
    cfg.write_files(args['output_dir'])
