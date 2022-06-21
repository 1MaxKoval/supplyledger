
FAMILY_NAME = 'supplyledger'


import hashlib
import random
import requests

from ledger.proto_builds.protos import payload_pb2

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
    

def _hash(data):
    return hashlib.sha512(data).hexdigest()

class SupplyLedgerClient:

    def __init__(self, baseUrl, keyFile):
        self.baseUrl = baseUrl
        self.keyFile = keyFile

        self._baseUrl = baseUrl

        if keyFile is None:
            self._signer = None
            return

        try:
            with open(keyFile) as fd:
                privateKeyStr = fd.read().strip()
        except OSError as err:
            raise Exception('Failed to read private key {}: {}'.format(
                keyFile, str(err)))

        try:
            privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
        except ParseError as err:
            raise Exception('Failed to load private key: {}'.format(str(err)))

        self._signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(privateKey)

        self._publicKey = self._signer.get_public_key().as_hex()

    def create_actor(self, organization_name):
        create_actor = payload_pb2.CreateActorAction()
        create_actor.organization_name = organization_name
        data = create_actor.SerializeToString()
        self._wrap_and_send(data, [], [])

    def _send_to_restapi(self,
                         suffix,
                         data=None,
                         contentType=None):
        '''Send a REST command to the Validator via the REST API.'''

        if self._baseUrl.startswith("http://"):
            url = "{}/{}".format(self._baseUrl, suffix)
        else:
            url = "http://{}/{}".format(self._baseUrl, suffix)

        headers = {}

        if contentType is not None:
            headers['Content-Type'] = contentType

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if not result.ok:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))

        except requests.ConnectionError as err:
            raise Exception(
                'Failed to connect to {}: {}'.format(url, str(err)))

        except BaseException as err:
            raise Exception(err)

        return result.text

    def _wrap_and_send(self, data, inputAddresses, outputAdresses):
        
        header = TransactionHeader(
            signer_public_key=self._publicKey,
            family_name=FAMILY_NAME,
            family_version="1.0",
            inputs=inputAddresses,
            outputs=outputAdresses,
            dependencies=[],
            payload_sha512=_hash(data),
            batcher_public_key=self._publicKey,
            nonce=random.random().hex().encode()
        ).serializeToString()

        transaction = Transaction(
            header=header,
            payload=data,
            header_signature=self._signer.sign(header)
        )

        batch_header = BatchHeader(
            signer_public_key=self._publicKey,
            transaction_ids=[transaction.header_signature]
        ).serializeToString()

        batch = Batch(
            header=batch_header,
            transactions=[transaction],
            header_signature=self._signer.sign(header)
        )

        batch_list = BatchList(batches=[batch]).serializeToString()

        return self._send_to_restapi(
            "batches",
            batch_list.SerializeToString(),
            'application/octet-stream')

def request_empty_address():
    """
    Retrieves an empty address from the
    """
    pass

        
    

    
    

