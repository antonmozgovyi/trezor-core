from apps.wallet.get_address import _show_address
from apps.common import seed
from trezor.messages.NEMAddress import NEMAddress
from .helpers import *

_NEM_CURVE = 'ed25519-keccak'


async def nem_get_address(ctx, msg):
    network = nem_validate_network(msg.network)
    node = await seed.derive_node(ctx, msg.address_n, _NEM_CURVE)
    address = node.nem_address(network)

    if msg.show_display:
        while True:
            if await _show_address(ctx, address):
                break

    return NEMAddress(address=address)

