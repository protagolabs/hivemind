import torch
from hivemind.proto import averaging_pb2

from hivemind import DHT, P2PContext, PeerID
from hivemind.averaging.averager import DecentralizedAverager
a = 10
if a < 1 :
    d = DecentralizedAverager(torch.ones(2,2), DHT(start=True),start=True,prefix="")
    d.rpc_join_group(averaging_pb2.JoinRequest(),P2PContext(handle_name="fack",local_id=PeerID(b"fack")))
    d.rpc_aggregate_part([averaging_pb2.AveragingData],P2PContext(handle_name="fack",local_id=PeerID(b"fack")))
