#!/Users/ben/Desktop/bndni/.venv/bin python3.11

from vertex_protocol import VertexProtocol
import os


class vtx_client:

    _pk = os.environ.get("PK")
    _wallet = os.environ.get("WALLET")
