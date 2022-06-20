import traceback
import sys
import hashlib
import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

LOGGER = logging.getLogger(__name__)
FAMILY_NAME = 'supplyledger'

def setup_loggers():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()

SW_NAMESPACE = _hash(FAMILY_NAME.encode('utf-8'))[0:6]

def main():
    setup_loggers()

    try:
        # Register the transaction handler and start it.
        processor = TransactionProcessor(url='tcp://validator:4004')

        handler = SupplyLedgerTransactionHandler(SW_NAMESPACE)

        processor.add_handler(handler)

        LOGGER.info('Starting transaction processor!')
        processor.start()

    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

class SupplyLedgerTransactionHandler(TransactionHandler):

    def __init__(self, namespace):
        self._namespace_prefix = namespace

    @property
    def family_name(self):
        return FAMILY_NAME
    
    @property
    def family_versions(self):
        return ['1.0']
    
    @property
    def namespaces(self):
        return [self._namespace_prefix]
    
    def apply(self, transaction, context):

        LOGGER.info("RECEIVED TRANSACTION!")