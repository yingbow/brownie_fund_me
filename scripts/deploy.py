from unittest.mock import Mock
from brownie import FundMe, MockV3Aggregator, network, config

from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like kovan, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        # [-1] means use the most recently deployed MockV3Aggregator
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(price_feed_address, {"from": account})
    # , publish_source=True)
    # publish_source = True flag means that we would like to verify our source code. Brownie knows to take the ETHERSCAN_TOKEN from .env and publish it to etherscan.io
    # Auto-verification, as of 13/01/2022, is still "touchy", prone to failure
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
