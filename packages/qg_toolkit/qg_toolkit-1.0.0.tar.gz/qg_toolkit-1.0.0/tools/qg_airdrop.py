import concurrent.futures
import copy
from typing import List

from pydantic import Field
from web3 import Web3

from tools.qg_eth import QGEth
from tools.qg_file import QGFile


class QGAirDrop(QGEth):
    # 每个号留多少
    chain_name: str = None
    # 每个号转多少
    per_value: float = None
    # 自己号留多少
    left_value: float = None
    # 是否检查接受账户余额
    is_check_receiver: bool = False
    # 检查接受账户余额是否有足够的量，不足就转，足够不转
    check_balance: float = 0.0000001
    receiver_accounts: List = Field(None, validate=False)

    #
    class Config:
        avalidate_assignment = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.receiver_accounts = []
        self.contract_map = {
            "polygon": "0xDCB4a16EB4F5F8214962357c96584F6955B9b525",
            "bsc": "0x0Ff88bdD9BE134F29dD660C4F220DD1e392e49E4",
            "opbnb": "0x501Ab65Ec2E89aB6e9CBfE6eE3AED423995b1aef",
            "goerli": "0x9680D1e126bBeF521F97b6FFB2fe39Da5c88C290",
            "sepolia": "0xEf50B70800f0D5D89b7a0056A0746845C2Dbe7b7",
            "linea": "0x2Ce164CbdBFb8fA0BEbf1f2dCD2F364481Fa86d3",
            "mantle": "0x601074C151C229d04D339F807817e8cB87E6CF1e",
            "berachain": "0xaB06c32FCE992B423F17e57BCC78C1cA80dd7AaA",
            "blast": "0x8B4a4AA2fD4bB59eBBEB987D229A3eb01f987E7b",
            "zeta": "0xBc4A4b3846C3F2F8085689F0A4A09D76627b6c2E",
            "holesky": "0x42d5f4D80dC931644627127385F51F07eb8a485D",
            "xter": "0x7347Ae5a53F7b80A7eF6654E3b8eA0c0E396a4D3"
        }
        self.init_chains(self.chain_name)
        self.w3 = getattr(self, f"{self.chain_name}_w3", None)
        self.w3_balance = getattr(self, f"{self.chain_name}_balance", None)
        self.fenpei()

    def batch_send_eth_by_lian(self):
        print(f'【{self.address}】【{self.index}】接收地址数量：{len(self.receiver_accounts)}')
        if len(self.receiver_accounts) == 0:
            return
        address_arr = self.receiver_accounts
        value = self.per_value
        action_name = "batch_send_eth_by_lian"
        to_address = self.contract_map.get(self.chain_name) or None
        if to_address is None:
            return
        hex_value = hex(Web3.to_wei(value, "ether"))[2:].rjust(64, '0')
        length = len(address_arr)
        if length == 0:
            return
        length_hex = hex(length)[2:].rjust(64, '0')
        param_index = 32 * (3 + length)
        param_index_hex = hex(param_index)[2:].rjust(64, '0')
        all_values = "".join([hex_value for x in address_arr])
        all_address = "".join([x[2:].rjust(64, '0') for x in address_arr])
        to_value = str(round(float(value) * length, 5))
        input_data = f"0x566316eb" \
                     f"0000000000000000000000000000000000000000000000000000000000000040" \
                     f"{param_index_hex}" \
                     f"{length_hex}" \
                     f"{all_address}" \
                     f"{length_hex}" \
                     f"{all_values}"
        print(f'【{self.address}】【{self.index}】批量空投-input_data：{input_data}')
        # self.sent_tx_with_assembled(self.w3, to_address, to_value, input_data, action_name)
        self.sent_tx_with_assembled_by_type0(self.w3, to_address, to_value, input_data, action_name)

    def fenpei(self):
        can_num = int(float(float(self.w3_balance) - self.left_value) / float(self.per_value))
        if can_num < 0:
            can_num = 0
        global receiver_accounts
        QGAirDrop.lock.acquire()
        if self.is_check_receiver:
            rs = copy.deepcopy(receiver_accounts)
            for addr in rs:
                if self.get_balance_from_web3(self.w3, addr) < self.check_balance:
                    self.receiver_accounts.append(addr)
                receiver_accounts.pop(0)
                if len(self.receiver_accounts) >= can_num:
                    break
        else:
            self.receiver_accounts = receiver_accounts[:can_num]
            receiver_accounts = receiver_accounts[can_num:]
        QGAirDrop.lock.release()
        print(f'{self.address} 分配账号数量{len(self.receiver_accounts)}:{self.receiver_accounts}')


def qg_task(index, address, private_key, mnemonic):
    chain_name = "opbnb"
    # 每个号空投多少
    per_value = "0.00015"
    # 给自己号剩余多少
    left_value = 0.01
    # 是否检查接收者余额
    is_check_receiver = True
    # 检查接收者余额是否大于N
    check_balance = 0.0001
    batch = QGAirDrop(index=index, address=address, private_key=private_key, mnemonic=mnemonic,
                      chain_name=chain_name, per_value=per_value, left_value=left_value,
                      is_check_receiver=is_check_receiver, check_balance=check_balance)
    batch.batch_send_eth_by_lian()


if __name__ == '__main__':
    accounts = QGFile.read_yaml("galxe_qg.yaml")["accounts"]
    receiver_accounts = [x["address"] for x in QGFile.read_yaml("galxe_qg.yaml")["accounts"]][1:]
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    for i, account in enumerate(accounts, start=1):
        if not isinstance(account, list):
            addr1 = account.get('address')
            pk1 = account.get('private_key')
        else:
            addr1 = account[0]
            pk1 = account[1]
        mn1 = ""
        if 1 <= i <= 1:
            executor.submit(qg_task, i, addr1, pk1, mn1)
