FROM python:3.8

RUN \
 pip3 install sawtooth-sdk secp256k1 protobuf build

WORKDIR /project/supplyledger/client

ENV PATH "$PATH:/project/supplyledger/client"

EXPOSE 3000

CMD python3 -m build && pip3 install dist/*.whl
