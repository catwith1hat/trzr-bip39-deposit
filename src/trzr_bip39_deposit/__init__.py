#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3 python3Packages.trezor
from trezorlib.client import get_default_client
from trezorlib.tools import parse_path
from trezorlib import misc
from pkg_resources import resource_stream
import hashlib
import sys

# 3600 == ETH2 coin type
BIP32_PATH = parse_path("44'/3600'/0'/0/0")

def ent_to_bip39(entropy):
  assert len(entropy) == 16
  c = hashlib.sha256(entropy).digest()
  def seg11(l, m):
    if len(l) == 12:
      return l
    return seg11([m&0x7ff] + l, m >> 11)
  return seg11([], int.from_bytes(entropy, byteorder='big') << 4 | c[0] >> 4)
  
def make_entropy(network):
  return misc.encrypt_keyvalue(
    get_default_client(),
    BIP32_PATH,
    'Generate BIP39 deposit mnemonic for %s?' % network,
    b'0000000000000000',
    True,
    True)
  
def main():
  if len(sys.argv) != 2:
    print("Error: Must supply network as first argument")
    return
  network = sys.argv[1]
  if network not in ["HOLESKY", "GOERLI", "MAINNET", "SEPOLIA", "HOODI"]:
    print("Unrecognized network name")
    return
  with resource_stream('trzr_bip39_deposit', 'english.txt') as f:
    words = f.read().decode().split('\n')
  idxs = ent_to_bip39(make_entropy(network))
  # english.txt ==  https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt
  for i in idxs:
    print(i, words[i])
  
if __name__ == "__main__":
  main()
