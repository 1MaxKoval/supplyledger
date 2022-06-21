import os
from .supplyledger_client import SupplyLedgerClient

FAMILY_NAME = 'supplyledger'
DEFAULT_URL = 'http://rest-api:8008'

def main_wrapper():
    client = SupplyLedgerClient(DEFAULT_URL, _get_keyfile('max'))
    client.create_actor('UTwente')

def _get_keyfile(profileName):
    '''Get the private key for a customer.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    return '{}/{}.priv'.format(key_dir, profileName)

def _get_pubkeyfile(profileName):
    '''Get the public key for a customer.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    return '{}/{}.pub'.format(key_dir, profileName)

if __name__ == '__main__':
    main_wrapper()
