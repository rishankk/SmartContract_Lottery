from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
        # false if verify key not there :)
    )
    print("Deployed Lottery")
    return lottery


def start_Lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tn = lottery.startLottery({"from": account})
    starting_tn.wait(1)
    print("Lottery started")


def enter_Lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10000000
    tn = lottery.enter({"from": account, "value": value})
    tn.wait(1)
    print("you entered lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund contract using link, then end lottery
    tn = fund_with_link(lottery.address)
    tn.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180)
    print(f"{lottery.recentWinner()} is new winner!")


def main():
    deploy_lottery()
    start_Lottery()
    enter_Lottery()
    end_lottery()
