"""Main module."""

from .toolbox import Toolbox
from pprint import pprint
from pathlib import Path

class ConfigNode():
    def __init__(self, name, toolbox, index=0):
        self.name = name
        self.private, self.public, self.psk = toolbox.make_keys()
        self.index = index
        self.lines = []

    def add(self, line):
        self.lines.append(line)

    def __str__(self):
        return '\n'.join(self.lines)

class WireguardConfig():
    def __init__(self, output_hook=pprint):
        self.output_hook = output_hook
        self.log('Creating execution environment...')
        self.toolbox = Toolbox(output_hook=output_hook)

    def newNode(self, name, index=0):
        cfg = ConfigNode(name, self.toolbox, index)

    def log(self, msg):
        self.output_hook(msg)

    def generate(self, *, endpoint_addr, endpoint_port, network_base, network, count, peers_reachable, keepalive, offset, output_dir):
        self.log('Generating keys...')
        self.output_path = output_dir
        gateway = self.newNode('gateway') 
        self.gateway_node = gateway
        self.peers = [self.newNode(f"peer{peer}", peer) for peer in range(count)]
        self.log('configuring: gateway')
        gateway.add('[Interface]')
        gateway.add(f'PrivateKey = {gateway.private}')
        gateway.add(f'Address = {network_base}.{network}.1/32')
        gateway.add(f'ListenPort = {endpoint_port}')
        for peer in self.peers:
            self.log(f"configuring: {peer.name}")
            gateway.add('[Peer]')
            if keepalive:
                gateway.add(f'PersistentKeepAlive = {keepalive}')
            gateway.add(f'PublicKey = {peer.public}')
            gateway.add(f'AllowedIPs = {networkd_base}.{network}.{peer.index+offset}/32')
            gateway.add(f'PresharedKey = {peer.psk}')
            peer.add('[Interface]')
            peer.add(f'PrivateKey = {peer.private}')
            peer.add(f'Address = {network_base}.{network}.{peer.index+offset}/32')
            peer.add(f'[Peer]')
            if keepalive:
                peer.add(f'PersistentKeepalive = {keepalive}')
            peer.add(f'PublicKey = {gateway.public}')
            if self.peers_reachable:
                allowed_ips = f'{network_base}.{network}.0/24'
            else:
                allowed_ips = f'{network_base}.{network}.1/32'
            peer.add(f'AllowedIPs = {allowed_ips}')
            peer.add(f'PresharedKey = {psk}')
            peer.add(f'Endpoint = {endpoint_addr}:{endpoint_port}')

    def write_files(self):
        self.output_path.mkdir()
        self.write_node(self.gateway_node)
        for peer in self.peers:
            self.write_node(peer)

    def write_node(self, node):
        with (self.output_path / f"{node.name}.conf").open('w') as fp:
            fp.write(str(self.gateway_config))
        for peer in self.peers:
            with (self.output_path / f"{peer.name}.conf").open('w') as fp:
                fp.write(str(peer))
