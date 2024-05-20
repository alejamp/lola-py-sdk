import json
import requests


def get_crypto_price(asset, currency='USD'):
    # asset to uppercase
    asset = asset.upper()
    url = f"https://api.coinbase.com/v2/prices/{asset}-{currency}/spot"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def get_crypto_prices_from_list(assets, currency='USD'):
    # assets is a list of assets
    # get price using get_crypto_price for each asset
    # return a dictionary of assets and prices
    data = {}
    for asset in assets:
        data[asset] = get_crypto_price(asset, currency)
    return data


if __name__ == '__main__':
    # print(get_crypto_price('btc'))
    # print(get_crypto_prices_from_list(['btc', 'eth', 'xrp']))
    print(get_crypto_prices_from_list('btc'.split(',')))
