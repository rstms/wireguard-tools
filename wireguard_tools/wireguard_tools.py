"""Main module."""

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
        self.toolbox = Toolbox()

    def newNode(self, name, index=0):
        cfg = ConfigNode(name, self.toolbox, index)

    def log(self, msg):
        self.output_hook(msg)

    def generate(self, *, gateway, port, network, count, peers_reachable, keepalive, base_network, offset):
        self.log('Generating keys...')
        gateway = self.newNode('gateway') 
        self.gateway_node = gateway
        self.peers = [self.newNode(f"peer{peer}", peer) for peer in range(count)]
        self.log('configuring: gateway')
        gateway.add('[Interface]')
        gateway.add(f'PrivateKey = {gateway.private}')
        gateway.add(f'Address = {base_network}.{network}.1/32')
        gateway.add(f'ListenPort = {port}')
        for peer in self.peers:
            self.log(f"configuring: {peer.name}")
            gateway.add('[Peer]')
            if keepalive:
                gateway.add(f'PersistentKeepAlive = {keepalive}')
            gateway.add(f'PublicKey = {peer.public}')
            gateway.add(f'AllowedIPs = {base_network}.{network}.{peer.index+offset}/32')
            gateway.add(f'PresharedKey = {peer.psk}')
            peer.add('[Interface]')
            peer.add(f'PrivateKey = {peer.private}')
            peer.add(f'Address = {base_network}.{network}.{peer.index+offset}/32')
            peer.add(f'[Peer]')
            if keepalive:
                peer.add(f'PersistentKeepalive = {keepalive}')
            peer.add(f'PublicKey = {gateway.public}')
            if self.peers_reachable:
                allowed_ips = f'{base_network}.{network}.0/24'
            else:
                allowed_ips = f'{base_network}.{network}.1/32'
            peer.add(f'AllowedIPs = {allowed_ips}')
            peer.add(f'PresharedKey = {psk}')
            peer.add(f'Endpoint = {gateway}:{port}')

    def write_files(self, output_dir)
        path = Path(self.output_dir)
        path.mkdir()
        self.write_node(self.gateway_node, path)
        for peer in self.peers:
            self.write_node(peer, path)

    def write_node(self, node, path):
        with (path / f"{node.name}.conf").open('w') as fp:
            fp.write(str(self.gateway_config))
        for peer in self.peers:
            with (path / f"{peer.name}.conf").open('w') as fp:
                fp.write(str(peer))
