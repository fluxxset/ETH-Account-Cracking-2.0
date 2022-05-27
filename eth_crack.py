
import threading
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional
import time
import os
from lxml import html
import requests
import string
import random
import sys
from colorama import Fore, Style

def readdr():    
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    PASSPHRASE: Optional[str] = None  # "meherett"
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    bip44_hdwallet.clean_derivation()
    address_index=0
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
    )
    bip44_hdwallet.from_path(path=bip44_derivation)

    #bip44_hdwallet.clean_derivation()
    return bip44_hdwallet.mnemonic(),bip44_hdwallet.address()
#0x1fd489fb3d71223a647fbf8a36cc2ff4f2e4bea6
def xBal(addr):
    urlblock = "https://ethereum.atomicwallet.io/address/" + addr
    # urlblock = "https://ethereum.atomicwallet.io/address/0x1fd489fb3d71223a647fbf8a36cc2ff4f2e4bea6"
    respone_block = requests.get(urlblock)
    byte_string = respone_block.content
    source_code = html.fromstring(byte_string)
    xpatch_txid = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[1]/td[2]'
    treetxid = source_code.xpath(xpatch_txid)
    xVol = str(treetxid[0].text_content())
    xVol=xVol.replace("ETH","")
    return xVol

def xbal2(addr):
    urlblock = "https://etherchain.org/account/" + addr
    respone_block = requests.get(urlblock)
    byte_string = respone_block.content
    source_code = html.fromstring(byte_string)
    # print(source_code)
    xpatch_txid = '/html/body/main/div/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/span'
    treetxid = source_code.xpath(xpatch_txid)
    # print(treetxid)
    xVol = str(treetxid[0].text_content())
    xVol = xVol.replace("ETH","")
    # xVol = xVol.replace("$","")
    # xVol = xVol.replace(",","")
    # print(float(xVol))
    return float(xVol)

def getone(nname):
    # eth = Etherscan(num)
    while True:
        me,addr = readdr()
        
        # bal = str(float(eth.get_eth_balance(addr))/10000000000000000000)
        if nname == "bot1" or nname == "bot2" or nname == "bot3" or nname == "bot4" or nname == "bot5":
            bal = xbal2(addr)
        else:
            bal = float(xBal(addr))
        if bal > 0:
            print(nname,Fore.GREEN,bal,addr,me)
            # sys.stdout.flush()
            file1 = open("valid.txt", "a")
            file1.write(f"{bal}'ETH' {addr} {me} \n")
            file1.close()
            # os.system(f'echo {bal} {me} {addr} >> valid.txt')
        else:
            print(nname,Fore.RED,"bal=",bal,addr,end='\r')
            sys.stdout.flush()
            continue
        
    
  
if __name__ == "__main__":
    # creating thread
 
    # getone()
    numt = sys.argv
    # print(numt[1])
    lis = []
    for i in range(int(numt[1])):
        letters = string.ascii_uppercase
        vas = ''.join(random.choice(letters) for i in range(10)) 
        globals()[f'xx{vas}'] = threading.Thread(target=getone,args=(f'bot{i}',))
        lis.append(f'xx{vas}')
        globals()[f'xx{vas}'].start()
    for j in range(len(lis)):
        globals()[f'{lis[j]}'].join()
    print("done",len(lis))


