import geckoterminal

from .config import NETWORK, TOKEN_ADDRESS, TOKEN_ADDRESSES, POOL_ADDRESS, POOL_ADDRESSES

def test_get_prices():
    prices = geckoterminal.get_prices('eth', ['0xdac17f958d2ee523a2206206994597c13d831ec7'])

    assert prices['data']
    assert prices['data']['attributes']
    assert prices['data']['attributes']['token_prices']
    assert len(prices['data']['attributes']['token_prices'].values()) == 1

    prices = geckoterminal.get_prices('eth', ['0xdac17f958d2ee523a2206206994597c13d831ec7', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'])

    assert prices['data']
    assert prices['data']['attributes']
    assert prices['data']['attributes']['token_prices']
    assert len(prices['data']['attributes']['token_prices'].values()) == 2

def test_get_networks():
    assert geckoterminal.get_networks()['data']

def test_get_dexes():
    assert geckoterminal.get_dexes(network=NETWORK)['data']

def test_get_pool():
    assert geckoterminal.get_pool(network=NETWORK, pool_address=POOL_ADDRESS)['data']

def test_get_pools():
    assert geckoterminal.get_pools(network=NETWORK, pool_addresses=POOL_ADDRESSES)['data']

def test_get_top_pools():
    assert geckoterminal.get_top_pools(network=NETWORK)['data']

def test_get_new_pools():
    assert geckoterminal.get_new_pools(network=NETWORK)['data']

def test_get_token():
    assert geckoterminal.get_token(network=NETWORK, token_address=TOKEN_ADDRESS)['data']

def test_get_tokens():
    assert geckoterminal.get_tokens(network=NETWORK, token_addresses=TOKEN_ADDRESSES)['data']

def test_get_top_pools_for_token():
    assert geckoterminal.get_top_pools_for_token(network=NETWORK, token_address=TOKEN_ADDRESS)['data']

def test_get_token_info():
    assert geckoterminal.get_token_info(network=NETWORK, token_address=TOKEN_ADDRESS)['data']

def test_get_pool_info():
    assert geckoterminal.get_pool_info(network=NETWORK, pool_address=POOL_ADDRESS)['data']

def test_get_pool_ohlcv():
    assert geckoterminal.get_pool_ohlcv(network=NETWORK, pool_address=POOL_ADDRESS)['data']

def test_get_pool_ohlcv():
    assert geckoterminal.get_pool_ohlcv(network=NETWORK, pool_address=POOL_ADDRESS)['data']

def test_get_trades():
    assert geckoterminal.get_trades(network=NETWORK, pool_address=POOL_ADDRESS)['data']