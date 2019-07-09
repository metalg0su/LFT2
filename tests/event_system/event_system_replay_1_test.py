from io import StringIO
from typing import TypeVar
from lft.event import EventSystem
from lft.event.mediators import DelayedEventMediator, TimestampEventMediator, JsonRpcEventMediator
from tests.event_system.event_system_replay_0_test import Event1, Event2, Event3, on_test1, on_test2, on_test3

T = TypeVar("T")


def test_event_system():
    results = []

    event_system = EventSystem(False)
    event_system.set_mediator(TimestampEventMediator)
    event_system.set_mediator(DelayedEventMediator)
    event_system.set_mediator(JsonRpcEventMediator)

    event_system.simulator.register_handler(Event1, lambda e: on_test1(e, results, event_system))
    event_system.simulator.register_handler(Event2, lambda e: on_test2(e, results, event_system))
    event_system.simulator.register_handler(Event3, lambda e: on_test3(e, results, event_system))

    record_io = StringIO()
    record_io.write(record)
    record_io.seek(0)

    timestamp_io = StringIO()
    timestamp_io.write(timestamp)
    timestamp_io.seek(0)

    json_rpc_io = StringIO()
    json_rpc_io.write(json_rpc)
    json_rpc_io.seek(0)

    event_system.start_replay(record_io, {TimestampEventMediator: timestamp_io, JsonRpcEventMediator: json_rpc_io})


record = """
{"number": 0, "event": {"event_name": "tests.event_system.event_system_replay_0_test.Event1", "event_contents": {}}}
{"number": 2, "event": {"event_name": "tests.event_system.event_system_replay_0_test.Event3", "event_contents": {"num": 3}}}
"""

timestamp = """
1:1561965244228174,1561965244228195,
2:1561965244365848,
3:1561965247453797,
"""

json_rpc = """
#1
$159
gANjanNvbnJwY2NsaWVudC5leGNlcHRpb25zClJlY2VpdmVkTm9uMnh4UmVzcG9uc2VFcnJvcgpx
AFgYAAAAUmVjZWl2ZWQgNDAwIHN0YXR1cyBjb2RlcQGFcQJScQN9cQRYBAAAAGNvZGVxBU2QAXNi
Lg==

$1735
gANjcmVxdWVzdHMuZXhjZXB0aW9ucwpDb25uZWN0aW9uRXJyb3IKcQBjdXJsbGliMy5leGNlcHRp
b25zCk1heFJldHJ5RXJyb3IKcQFOWAcAAAAvYXBpL3YzcQJOh3EDUnEEhXEFUnEGfXEHKFgIAAAA
cmVzcG9uc2VxCE5YBwAAAHJlcXVlc3RxCWNyZXF1ZXN0cy5tb2RlbHMKUHJlcGFyZWRSZXF1ZXN0
CnEKKYFxC31xDChYBgAAAG1ldGhvZHENWAQAAABQT1NUcQ5YAwAAAHVybHEPWCcAAABodHRwczov
L3dhbGxldC5pY29uLmZvdW5kYXRpb24xbC9hcGkvdjNxEFgHAAAAaGVhZGVyc3ERY3JlcXVlc3Rz
LnN0cnVjdHVyZXMKQ2FzZUluc2Vuc2l0aXZlRGljdApxEimBcRN9cRRYBgAAAF9zdG9yZXEVY2Nv
bGxlY3Rpb25zCk9yZGVyZWREaWN0CnEWKVJxFyhYCgAAAHVzZXItYWdlbnRxGFgKAAAAVXNlci1B
Z2VudHEZWBYAAABweXRob24tcmVxdWVzdHMvMi4yMC4wcRqGcRtYDwAAAGFjY2VwdC1lbmNvZGlu
Z3EcWA8AAABBY2NlcHQtRW5jb2RpbmdxHVgNAAAAZ3ppcCwgZGVmbGF0ZXEehnEfWAYAAABhY2Nl
cHRxIFgGAAAAQWNjZXB0cSFYEAAAAGFwcGxpY2F0aW9uL2pzb25xIoZxI1gKAAAAY29ubmVjdGlv
bnEkWAoAAABDb25uZWN0aW9ucSVYCgAAAGtlZXAtYWxpdmVxJoZxJ1gMAAAAY29udGVudC10eXBl
cShYDAAAAENvbnRlbnQtVHlwZXEpaCKGcSpYDgAAAGNvbnRlbnQtbGVuZ3RocStYDgAAAENvbnRl
bnQtTGVuZ3RocSxYAgAAADU3cS2GcS51c2JYCAAAAF9jb29raWVzcS9jcmVxdWVzdHMuY29va2ll
cwpSZXF1ZXN0c0Nvb2tpZUphcgpxMCmBcTF9cTIoWAcAAABfcG9saWN5cTNjaHR0cC5jb29raWVq
YXIKRGVmYXVsdENvb2tpZVBvbGljeQpxNCmBcTV9cTYoWAgAAABuZXRzY2FwZXE3iFgHAAAAcmZj
Mjk2NXE4iVgTAAAAcmZjMjEwOV9hc19uZXRzY2FwZXE5TlgMAAAAaGlkZV9jb29raWUycTqJWA0A
AABzdHJpY3RfZG9tYWlucTuJWBsAAABzdHJpY3RfcmZjMjk2NV91bnZlcmlmaWFibGVxPIhYFgAA
AHN0cmljdF9uc191bnZlcmlmaWFibGVxPYlYEAAAAHN0cmljdF9uc19kb21haW5xPksAWBwAAABz
dHJpY3RfbnNfc2V0X2luaXRpYWxfZG9sbGFycT+JWBIAAABzdHJpY3RfbnNfc2V0X3BhdGhxQIlY
EAAAAF9ibG9ja2VkX2RvbWFpbnNxQSlYEAAAAF9hbGxvd2VkX2RvbWFpbnNxQk5YBAAAAF9ub3dx
Q0pfmhVddWJoL31xRGhDSl+aFV11YlgEAAAAYm9keXFFQzl7Impzb25ycGMiOiAiMi4wIiwgIm1l
dGhvZCI6ICJpY3hfZ2V0TGFzdEJsb2NrIiwgImlkIjogMX1xRlgFAAAAaG9va3NxR31xSGgIXXFJ
c1gOAAAAX2JvZHlfcG9zaXRpb25xSk51YnViLg==


#2
$7745
gANjanNvbnJwY2NsaWVudC5yZXNwb25zZQpSZXNwb25zZQpxACmBcQF9cQIoWAQAAAB0ZXh0cQNY
mgQAAHsianNvbnJwYyI6ICIyLjAiLCAicmVzdWx0IjogeyJ2ZXJzaW9uIjogIjAuMWEiLCAicHJl
dl9ibG9ja19oYXNoIjogImZkYjgwYWE3ZDJmZDEzMTlmNWEwZWIyMjVmMGNjNzkyMDJhMjE4YmJi
MjE0ZmU4M2UxMjQyYmZkMDMyOGUxYzIiLCAibWVya2xlX3RyZWVfcm9vdF9oYXNoIjogIjFlNjI3
NjQzODdhNGRlNzkxZWUyZDU3Mjg4ZTJlNDNhMWQzOTQyZTdjZTZiZDU3ZjcwMzMyNDEwMzIzNDZk
M2QiLCAidGltZV9zdGFtcCI6IDE1NjE2OTY4NjA3OTE3ODUsICJjb25maXJtZWRfdHJhbnNhY3Rp
b25fbGlzdCI6IFt7InZlcnNpb24iOiAiMHgzIiwgImZyb20iOiAiaHhkMmQwMDFjMzkzOGM3ZjZk
MzFiYzc2YjFjZGE5MjJhNjRjNTFjOGJmIiwgInRvIjogImN4ZjkxNDhkYjRmOGVjNzg4MjNhNTBj
YjA2YzRmZWQ4MzY2MGFmMzhkMCIsICJzdGVwTGltaXQiOiAiMHhmNDI0MCIsICJ0aW1lc3RhbXAi
OiAiMHg1OGM1YWUyOWFkNTgwIiwgIm5pZCI6ICIweDEiLCAibm9uY2UiOiAiMHg2NCIsICJkYXRh
VHlwZSI6ICJjYWxsIiwgImRhdGEiOiB7Im1ldGhvZCI6ICJwdXNoR2FtZVJlc3VsdFRvQmxvY2si
LCAicGFyYW1zIjogeyJfaGFzaCI6ICJ5TXlHaGVPUkhwWk5TNmVadnBBS0t2Q29FOVh0ZFF4bnBG
UzVJUnkyemxCQ3c4K2Jlc3Y0RFVubUF6bERrVlpjIn19LCAic2lnbmF0dXJlIjogIm45eEtUd1g3
Y3NxdTZ6U0ZXeDFsVWluR3N6ZEQwb0oxQWJxWTBxZG1kMFpRTmRPd3RsRVBDQUF1bnVvT240UFI5
c01kVFB2OUdhNk5QN3pxWWdqb2ZBQT0iLCAidHhIYXNoIjogIjB4MWU2Mjc2NDM4N2E0ZGU3OTFl
ZTJkNTcyODhlMmU0M2ExZDM5NDJlN2NlNmJkNTdmNzAzMzI0MTAzMjM0NmQzZCJ9XSwgImJsb2Nr
X2hhc2giOiAiZTAwODViZDZkY2JlZjViNmRlMjA3NWU3ZTU2OGE2MTBjYTdjN2VmOTY5ZGIzYjRk
MDRkNDkzMDhhZjcxMjZjZCIsICJoZWlnaHQiOiA1NTUxNzQ3LCAicGVlcl9pZCI6ICJoeDU5NjFk
MWJmNThlNzBiNmM0MjUzOWZlODNmNmU1ZDY4YTNiMDkzZDQiLCAic2lnbmF0dXJlIjogImNsT0g1
YXNXWHpLSVRhcVAyMEMxcjYxQjYzd3FiU25kMFZWQWY3cjFHZTA5ekRldE1KY0lFN2hFUldaZjI5
TzE5M0FvMVhadThLK2RiRldrZVJ2YktRRT0iLCAibmV4dF9sZWFkZXIiOiAiaHg1OTYxZDFiZjU4
ZTcwYjZjNDI1MzlmZTgzZjZlNWQ2OGEzYjA5M2Q0In0sICJpZCI6IDF9cQRYAwAAAHJhd3EFY3Jl
cXVlc3RzLm1vZGVscwpSZXNwb25zZQpxBimBcQd9cQgoWAgAAABfY29udGVudHEJQpoEAAB7Impz
b25ycGMiOiAiMi4wIiwgInJlc3VsdCI6IHsidmVyc2lvbiI6ICIwLjFhIiwgInByZXZfYmxvY2tf
aGFzaCI6ICJmZGI4MGFhN2QyZmQxMzE5ZjVhMGViMjI1ZjBjYzc5MjAyYTIxOGJiYjIxNGZlODNl
MTI0MmJmZDAzMjhlMWMyIiwgIm1lcmtsZV90cmVlX3Jvb3RfaGFzaCI6ICIxZTYyNzY0Mzg3YTRk
ZTc5MWVlMmQ1NzI4OGUyZTQzYTFkMzk0MmU3Y2U2YmQ1N2Y3MDMzMjQxMDMyMzQ2ZDNkIiwgInRp
bWVfc3RhbXAiOiAxNTYxNjk2ODYwNzkxNzg1LCAiY29uZmlybWVkX3RyYW5zYWN0aW9uX2xpc3Qi
OiBbeyJ2ZXJzaW9uIjogIjB4MyIsICJmcm9tIjogImh4ZDJkMDAxYzM5MzhjN2Y2ZDMxYmM3NmIx
Y2RhOTIyYTY0YzUxYzhiZiIsICJ0byI6ICJjeGY5MTQ4ZGI0ZjhlYzc4ODIzYTUwY2IwNmM0ZmVk
ODM2NjBhZjM4ZDAiLCAic3RlcExpbWl0IjogIjB4ZjQyNDAiLCAidGltZXN0YW1wIjogIjB4NThj
NWFlMjlhZDU4MCIsICJuaWQiOiAiMHgxIiwgIm5vbmNlIjogIjB4NjQiLCAiZGF0YVR5cGUiOiAi
Y2FsbCIsICJkYXRhIjogeyJtZXRob2QiOiAicHVzaEdhbWVSZXN1bHRUb0Jsb2NrIiwgInBhcmFt
cyI6IHsiX2hhc2giOiAieU15R2hlT1JIcFpOUzZlWnZwQUtLdkNvRTlYdGRReG5wRlM1SVJ5Mnps
QkN3OCtiZXN2NERVbm1BemxEa1ZaYyJ9fSwgInNpZ25hdHVyZSI6ICJuOXhLVHdYN2NzcXU2elNG
V3gxbFVpbkdzemREMG9KMUFicVkwcWRtZDBaUU5kT3d0bEVQQ0FBdW51b09uNFBSOXNNZFRQdjlH
YTZOUDd6cVlnam9mQUE9IiwgInR4SGFzaCI6ICIweDFlNjI3NjQzODdhNGRlNzkxZWUyZDU3Mjg4
ZTJlNDNhMWQzOTQyZTdjZTZiZDU3ZjcwMzMyNDEwMzIzNDZkM2QifV0sICJibG9ja19oYXNoIjog
ImUwMDg1YmQ2ZGNiZWY1YjZkZTIwNzVlN2U1NjhhNjEwY2E3YzdlZjk2OWRiM2I0ZDA0ZDQ5MzA4
YWY3MTI2Y2QiLCAiaGVpZ2h0IjogNTU1MTc0NywgInBlZXJfaWQiOiAiaHg1OTYxZDFiZjU4ZTcw
YjZjNDI1MzlmZTgzZjZlNWQ2OGEzYjA5M2Q0IiwgInNpZ25hdHVyZSI6ICJjbE9INWFzV1h6S0lU
YXFQMjBDMXI2MUI2M3dxYlNuZDBWVkFmN3IxR2UwOXpEZXRNSmNJRTdoRVJXWmYyOU8xOTNBbzFY
WnU4SytkYkZXa2VSdmJLUUU9IiwgIm5leHRfbGVhZGVyIjogImh4NTk2MWQxYmY1OGU3MGI2YzQy
NTM5ZmU4M2Y2ZTVkNjhhM2IwOTNkNCJ9LCAiaWQiOiAxfXEKWAsAAABzdGF0dXNfY29kZXELS8hY
BwAAAGhlYWRlcnNxDGNyZXF1ZXN0cy5zdHJ1Y3R1cmVzCkNhc2VJbnNlbnNpdGl2ZURpY3QKcQ0p
gXEOfXEPWAYAAABfc3RvcmVxEGNjb2xsZWN0aW9ucwpPcmRlcmVkRGljdApxESlScRIoWAQAAABk
YXRlcRNYBAAAAERhdGVxFFgdAAAARnJpLCAyOCBKdW4gMjAxOSAwNDo0MTowMyBHTVRxFYZxFlgM
AAAAY29udGVudC10eXBlcRdYDAAAAENvbnRlbnQtVHlwZXEYWBAAAABhcHBsaWNhdGlvbi9qc29u
cRmGcRpYEQAAAHRyYW5zZmVyLWVuY29kaW5ncRtYEQAAAFRyYW5zZmVyLUVuY29kaW5ncRxYBwAA
AGNodW5rZWRxHYZxHlgKAAAAY29ubmVjdGlvbnEfWAoAAABDb25uZWN0aW9ucSBYCgAAAGtlZXAt
YWxpdmVxIYZxIlgGAAAAc2VydmVycSNYBgAAAFNlcnZlcnEkWAUAAABuZ2lueHElhnEmWAQAAAB2
YXJ5cSdYBAAAAFZhcnlxKFgPAAAAQWNjZXB0LUVuY29kaW5ncSmGcSpYGwAAAGFjY2Vzcy1jb250
cm9sLWFsbG93LW9yaWdpbnErWBsAAABBY2Nlc3MtQ29udHJvbC1BbGxvdy1PcmlnaW5xLFgBAAAA
KnEthnEuWBAAAABjb250ZW50LWVuY29kaW5ncS9YEAAAAENvbnRlbnQtRW5jb2RpbmdxMFgEAAAA
Z3ppcHExhnEydXNiWAMAAAB1cmxxM1glAAAAaHR0cHM6Ly93YWxsZXQuaWNvbi5mb3VuZGF0aW9u
L2FwaS92M3E0WAcAAABoaXN0b3J5cTVdcTZYCAAAAGVuY29kaW5ncTdOWAYAAAByZWFzb25xOFgC
AAAAT0txOVgHAAAAY29va2llc3E6Y3JlcXVlc3RzLmNvb2tpZXMKUmVxdWVzdHNDb29raWVKYXIK
cTspgXE8fXE9KFgHAAAAX3BvbGljeXE+Y2h0dHAuY29va2llamFyCkRlZmF1bHRDb29raWVQb2xp
Y3kKcT8pgXFAfXFBKFgIAAAAbmV0c2NhcGVxQohYBwAAAHJmYzI5NjVxQ4lYEwAAAHJmYzIxMDlf
YXNfbmV0c2NhcGVxRE5YDAAAAGhpZGVfY29va2llMnFFiVgNAAAAc3RyaWN0X2RvbWFpbnFGiVgb
AAAAc3RyaWN0X3JmYzI5NjVfdW52ZXJpZmlhYmxlcUeIWBYAAABzdHJpY3RfbnNfdW52ZXJpZmlh
YmxlcUiJWBAAAABzdHJpY3RfbnNfZG9tYWlucUlLAFgcAAAAc3RyaWN0X25zX3NldF9pbml0aWFs
X2RvbGxhcnFKiVgSAAAAc3RyaWN0X25zX3NldF9wYXRocUuJWBAAAABfYmxvY2tlZF9kb21haW5z
cUwpWBAAAABfYWxsb3dlZF9kb21haW5zcU1OWAQAAABfbm93cU5KX5oVXXViWAgAAABfY29va2ll
c3FPfXFQaE5KX5oVXXViWAcAAABlbGFwc2VkcVFjZGF0ZXRpbWUKdGltZWRlbHRhCnFSSwBLAEpD
awEAh3FTUnFUWAcAAAByZXF1ZXN0cVVjcmVxdWVzdHMubW9kZWxzClByZXBhcmVkUmVxdWVzdApx
VimBcVd9cVgoWAYAAABtZXRob2RxWVgEAAAAUE9TVHFaaDNoNGgMaA0pgXFbfXFcaBBoESlScV0o
WAoAAAB1c2VyLWFnZW50cV5YCgAAAFVzZXItQWdlbnRxX1gWAAAAcHl0aG9uLXJlcXVlc3RzLzIu
MjAuMHFghnFhWA8AAABhY2NlcHQtZW5jb2RpbmdxYlgPAAAAQWNjZXB0LUVuY29kaW5ncWNYDQAA
AGd6aXAsIGRlZmxhdGVxZIZxZVgGAAAAYWNjZXB0cWZYBgAAAEFjY2VwdHFnWBAAAABhcHBsaWNh
dGlvbi9qc29ucWiGcWlYCgAAAGNvbm5lY3Rpb25xalgKAAAAQ29ubmVjdGlvbnFrWAoAAABrZWVw
LWFsaXZlcWyGcW1YDAAAAGNvbnRlbnQtdHlwZXFuWAwAAABDb250ZW50LVR5cGVxb2hohnFwWA4A
AABjb250ZW50LWxlbmd0aHFxWA4AAABDb250ZW50LUxlbmd0aHFyWAIAAAA1N3FzhnF0dXNiaE9o
OymBcXV9cXYoaD5oPymBcXd9cXgoaEKIaEOJaEROaEWJaEaJaEeIaEiJaElLAGhKiWhLiWhMKWhN
TmhOSl+aFV11YmhPfXF5aE5KX5oVXXViWAQAAABib2R5cXpDOXsianNvbnJwYyI6ICIyLjAiLCAi
bWV0aG9kIjogImljeF9nZXRMYXN0QmxvY2siLCAiaWQiOiAxfXF7WAUAAABob29rc3F8fXF9WAgA
AAByZXNwb25zZXF+XXF/c1gOAAAAX2JvZHlfcG9zaXRpb25xgE51YnViWAQAAABkYXRhcYFjanNv
bnJwY2NsaWVudC5yZXNwb25zZQpTdWNjZXNzUmVzcG9uc2UKcYIpgXGDfXGEKFgHAAAAanNvbnJw
Y3GFWAMAAAAyLjBxhlgCAAAAaWRxh0sBWAYAAAByZXN1bHRxiH1xiShYBwAAAHZlcnNpb25xilgE
AAAAMC4xYXGLWA8AAABwcmV2X2Jsb2NrX2hhc2hxjFhAAAAAZmRiODBhYTdkMmZkMTMxOWY1YTBl
YjIyNWYwY2M3OTIwMmEyMThiYmIyMTRmZTgzZTEyNDJiZmQwMzI4ZTFjMnGNWBUAAABtZXJrbGVf
dHJlZV9yb290X2hhc2hxjlhAAAAAMWU2Mjc2NDM4N2E0ZGU3OTFlZTJkNTcyODhlMmU0M2ExZDM5
NDJlN2NlNmJkNTdmNzAzMzI0MTAzMjM0NmQzZHGPWAoAAAB0aW1lX3N0YW1wcZCKB+ljouJajAVY
GgAAAGNvbmZpcm1lZF90cmFuc2FjdGlvbl9saXN0cZFdcZJ9cZMoaIpYAwAAADB4M3GUWAQAAABm
cm9tcZVYKgAAAGh4ZDJkMDAxYzM5MzhjN2Y2ZDMxYmM3NmIxY2RhOTIyYTY0YzUxYzhiZnGWWAIA
AAB0b3GXWCoAAABjeGY5MTQ4ZGI0ZjhlYzc4ODIzYTUwY2IwNmM0ZmVkODM2NjBhZjM4ZDBxmFgJ
AAAAc3RlcExpbWl0cZlYBwAAADB4ZjQyNDBxmlgJAAAAdGltZXN0YW1wcZtYDwAAADB4NThjNWFl
MjlhZDU4MHGcWAMAAABuaWRxnVgDAAAAMHgxcZ5YBQAAAG5vbmNlcZ9YBAAAADB4NjRxoFgIAAAA
ZGF0YVR5cGVxoVgEAAAAY2FsbHGiWAQAAABkYXRhcaN9caQoWAYAAABtZXRob2RxpVgVAAAAcHVz
aEdhbWVSZXN1bHRUb0Jsb2NrcaZYBgAAAHBhcmFtc3GnfXGoWAUAAABfaGFzaHGpWEAAAAB5TXlH
aGVPUkhwWk5TNmVadnBBS0t2Q29FOVh0ZFF4bnBGUzVJUnkyemxCQ3c4K2Jlc3Y0RFVubUF6bERr
VlpjcapzdVgJAAAAc2lnbmF0dXJlcatYWAAAAG45eEtUd1g3Y3NxdTZ6U0ZXeDFsVWluR3N6ZEQw
b0oxQWJxWTBxZG1kMFpRTmRPd3RsRVBDQUF1bnVvT240UFI5c01kVFB2OUdhNk5QN3pxWWdqb2ZB
QT1xrFgGAAAAdHhIYXNoca1YQgAAADB4MWU2Mjc2NDM4N2E0ZGU3OTFlZTJkNTcyODhlMmU0M2Ex
ZDM5NDJlN2NlNmJkNTdmNzAzMzI0MTAzMjM0NmQzZHGudWFYCgAAAGJsb2NrX2hhc2hxr1hAAAAA
ZTAwODViZDZkY2JlZjViNmRlMjA3NWU3ZTU2OGE2MTBjYTdjN2VmOTY5ZGIzYjRkMDRkNDkzMDhh
ZjcxMjZjZHGwWAYAAABoZWlnaHRxsUqDtlQAWAcAAABwZWVyX2lkcbJYKgAAAGh4NTk2MWQxYmY1
OGU3MGI2YzQyNTM5ZmU4M2Y2ZTVkNjhhM2IwOTNkNHGzaKtYWAAAAGNsT0g1YXNXWHpLSVRhcVAy
MEMxcjYxQjYzd3FiU25kMFZWQWY3cjFHZTA5ekRldE1KY0lFN2hFUldaZjI5TzE5M0FvMVhadThL
K2RiRldrZVJ2YktRRT1xtFgLAAAAbmV4dF9sZWFkZXJxtVgqAAAAaHg1OTYxZDFiZjU4ZTcwYjZj
NDI1MzlmZTgzZjZlNWQ2OGEzYjA5M2Q0cbZ1dWJ1Yi4=


#3
$7741
gANjanNvbnJwY2NsaWVudC5yZXNwb25zZQpSZXNwb25zZQpxACmBcQF9cQIoWAQAAAB0ZXh0cQNY
mgQAAHsianNvbnJwYyI6ICIyLjAiLCAicmVzdWx0IjogeyJ2ZXJzaW9uIjogIjAuMWEiLCAicHJl
dl9ibG9ja19oYXNoIjogImZkYjgwYWE3ZDJmZDEzMTlmNWEwZWIyMjVmMGNjNzkyMDJhMjE4YmJi
MjE0ZmU4M2UxMjQyYmZkMDMyOGUxYzIiLCAibWVya2xlX3RyZWVfcm9vdF9oYXNoIjogIjFlNjI3
NjQzODdhNGRlNzkxZWUyZDU3Mjg4ZTJlNDNhMWQzOTQyZTdjZTZiZDU3ZjcwMzMyNDEwMzIzNDZk
M2QiLCAidGltZV9zdGFtcCI6IDE1NjE2OTY4NjA3OTE3ODUsICJjb25maXJtZWRfdHJhbnNhY3Rp
b25fbGlzdCI6IFt7InZlcnNpb24iOiAiMHgzIiwgImZyb20iOiAiaHhkMmQwMDFjMzkzOGM3ZjZk
MzFiYzc2YjFjZGE5MjJhNjRjNTFjOGJmIiwgInRvIjogImN4ZjkxNDhkYjRmOGVjNzg4MjNhNTBj
YjA2YzRmZWQ4MzY2MGFmMzhkMCIsICJzdGVwTGltaXQiOiAiMHhmNDI0MCIsICJ0aW1lc3RhbXAi
OiAiMHg1OGM1YWUyOWFkNTgwIiwgIm5pZCI6ICIweDEiLCAibm9uY2UiOiAiMHg2NCIsICJkYXRh
VHlwZSI6ICJjYWxsIiwgImRhdGEiOiB7Im1ldGhvZCI6ICJwdXNoR2FtZVJlc3VsdFRvQmxvY2si
LCAicGFyYW1zIjogeyJfaGFzaCI6ICJ5TXlHaGVPUkhwWk5TNmVadnBBS0t2Q29FOVh0ZFF4bnBG
UzVJUnkyemxCQ3c4K2Jlc3Y0RFVubUF6bERrVlpjIn19LCAic2lnbmF0dXJlIjogIm45eEtUd1g3
Y3NxdTZ6U0ZXeDFsVWluR3N6ZEQwb0oxQWJxWTBxZG1kMFpRTmRPd3RsRVBDQUF1bnVvT240UFI5
c01kVFB2OUdhNk5QN3pxWWdqb2ZBQT0iLCAidHhIYXNoIjogIjB4MWU2Mjc2NDM4N2E0ZGU3OTFl
ZTJkNTcyODhlMmU0M2ExZDM5NDJlN2NlNmJkNTdmNzAzMzI0MTAzMjM0NmQzZCJ9XSwgImJsb2Nr
X2hhc2giOiAiZTAwODViZDZkY2JlZjViNmRlMjA3NWU3ZTU2OGE2MTBjYTdjN2VmOTY5ZGIzYjRk
MDRkNDkzMDhhZjcxMjZjZCIsICJoZWlnaHQiOiA1NTUxNzQ3LCAicGVlcl9pZCI6ICJoeDU5NjFk
MWJmNThlNzBiNmM0MjUzOWZlODNmNmU1ZDY4YTNiMDkzZDQiLCAic2lnbmF0dXJlIjogImNsT0g1
YXNXWHpLSVRhcVAyMEMxcjYxQjYzd3FiU25kMFZWQWY3cjFHZTA5ekRldE1KY0lFN2hFUldaZjI5
TzE5M0FvMVhadThLK2RiRldrZVJ2YktRRT0iLCAibmV4dF9sZWFkZXIiOiAiaHg1OTYxZDFiZjU4
ZTcwYjZjNDI1MzlmZTgzZjZlNWQ2OGEzYjA5M2Q0In0sICJpZCI6IDF9cQRYAwAAAHJhd3EFY3Jl
cXVlc3RzLm1vZGVscwpSZXNwb25zZQpxBimBcQd9cQgoWAgAAABfY29udGVudHEJQpoEAAB7Impz
b25ycGMiOiAiMi4wIiwgInJlc3VsdCI6IHsidmVyc2lvbiI6ICIwLjFhIiwgInByZXZfYmxvY2tf
aGFzaCI6ICJmZGI4MGFhN2QyZmQxMzE5ZjVhMGViMjI1ZjBjYzc5MjAyYTIxOGJiYjIxNGZlODNl
MTI0MmJmZDAzMjhlMWMyIiwgIm1lcmtsZV90cmVlX3Jvb3RfaGFzaCI6ICIxZTYyNzY0Mzg3YTRk
ZTc5MWVlMmQ1NzI4OGUyZTQzYTFkMzk0MmU3Y2U2YmQ1N2Y3MDMzMjQxMDMyMzQ2ZDNkIiwgInRp
bWVfc3RhbXAiOiAxNTYxNjk2ODYwNzkxNzg1LCAiY29uZmlybWVkX3RyYW5zYWN0aW9uX2xpc3Qi
OiBbeyJ2ZXJzaW9uIjogIjB4MyIsICJmcm9tIjogImh4ZDJkMDAxYzM5MzhjN2Y2ZDMxYmM3NmIx
Y2RhOTIyYTY0YzUxYzhiZiIsICJ0byI6ICJjeGY5MTQ4ZGI0ZjhlYzc4ODIzYTUwY2IwNmM0ZmVk
ODM2NjBhZjM4ZDAiLCAic3RlcExpbWl0IjogIjB4ZjQyNDAiLCAidGltZXN0YW1wIjogIjB4NThj
NWFlMjlhZDU4MCIsICJuaWQiOiAiMHgxIiwgIm5vbmNlIjogIjB4NjQiLCAiZGF0YVR5cGUiOiAi
Y2FsbCIsICJkYXRhIjogeyJtZXRob2QiOiAicHVzaEdhbWVSZXN1bHRUb0Jsb2NrIiwgInBhcmFt
cyI6IHsiX2hhc2giOiAieU15R2hlT1JIcFpOUzZlWnZwQUtLdkNvRTlYdGRReG5wRlM1SVJ5Mnps
QkN3OCtiZXN2NERVbm1BemxEa1ZaYyJ9fSwgInNpZ25hdHVyZSI6ICJuOXhLVHdYN2NzcXU2elNG
V3gxbFVpbkdzemREMG9KMUFicVkwcWRtZDBaUU5kT3d0bEVQQ0FBdW51b09uNFBSOXNNZFRQdjlH
YTZOUDd6cVlnam9mQUE9IiwgInR4SGFzaCI6ICIweDFlNjI3NjQzODdhNGRlNzkxZWUyZDU3Mjg4
ZTJlNDNhMWQzOTQyZTdjZTZiZDU3ZjcwMzMyNDEwMzIzNDZkM2QifV0sICJibG9ja19oYXNoIjog
ImUwMDg1YmQ2ZGNiZWY1YjZkZTIwNzVlN2U1NjhhNjEwY2E3YzdlZjk2OWRiM2I0ZDA0ZDQ5MzA4
YWY3MTI2Y2QiLCAiaGVpZ2h0IjogNTU1MTc0NywgInBlZXJfaWQiOiAiaHg1OTYxZDFiZjU4ZTcw
YjZjNDI1MzlmZTgzZjZlNWQ2OGEzYjA5M2Q0IiwgInNpZ25hdHVyZSI6ICJjbE9INWFzV1h6S0lU
YXFQMjBDMXI2MUI2M3dxYlNuZDBWVkFmN3IxR2UwOXpEZXRNSmNJRTdoRVJXWmYyOU8xOTNBbzFY
WnU4SytkYkZXa2VSdmJLUUU9IiwgIm5leHRfbGVhZGVyIjogImh4NTk2MWQxYmY1OGU3MGI2YzQy
NTM5ZmU4M2Y2ZTVkNjhhM2IwOTNkNCJ9LCAiaWQiOiAxfXEKWAsAAABzdGF0dXNfY29kZXELS8hY
BwAAAGhlYWRlcnNxDGNyZXF1ZXN0cy5zdHJ1Y3R1cmVzCkNhc2VJbnNlbnNpdGl2ZURpY3QKcQ0p
gXEOfXEPWAYAAABfc3RvcmVxEGNjb2xsZWN0aW9ucwpPcmRlcmVkRGljdApxESlScRIoWAQAAABk
YXRlcRNYBAAAAERhdGVxFFgdAAAARnJpLCAyOCBKdW4gMjAxOSAwNDo0MTowNiBHTVRxFYZxFlgM
AAAAY29udGVudC10eXBlcRdYDAAAAENvbnRlbnQtVHlwZXEYWBAAAABhcHBsaWNhdGlvbi9qc29u
cRmGcRpYEQAAAHRyYW5zZmVyLWVuY29kaW5ncRtYEQAAAFRyYW5zZmVyLUVuY29kaW5ncRxYBwAA
AGNodW5rZWRxHYZxHlgKAAAAY29ubmVjdGlvbnEfWAoAAABDb25uZWN0aW9ucSBYCgAAAGtlZXAt
YWxpdmVxIYZxIlgGAAAAc2VydmVycSNYBgAAAFNlcnZlcnEkWAUAAABuZ2lueHElhnEmWAQAAAB2
YXJ5cSdYBAAAAFZhcnlxKFgPAAAAQWNjZXB0LUVuY29kaW5ncSmGcSpYGwAAAGFjY2Vzcy1jb250
cm9sLWFsbG93LW9yaWdpbnErWBsAAABBY2Nlc3MtQ29udHJvbC1BbGxvdy1PcmlnaW5xLFgBAAAA
KnEthnEuWBAAAABjb250ZW50LWVuY29kaW5ncS9YEAAAAENvbnRlbnQtRW5jb2RpbmdxMFgEAAAA
Z3ppcHExhnEydXNiWAMAAAB1cmxxM1glAAAAaHR0cHM6Ly93YWxsZXQuaWNvbi5mb3VuZGF0aW9u
L2FwaS92M3E0WAcAAABoaXN0b3J5cTVdcTZYCAAAAGVuY29kaW5ncTdOWAYAAAByZWFzb25xOFgC
AAAAT0txOVgHAAAAY29va2llc3E6Y3JlcXVlc3RzLmNvb2tpZXMKUmVxdWVzdHNDb29raWVKYXIK
cTspgXE8fXE9KFgHAAAAX3BvbGljeXE+Y2h0dHAuY29va2llamFyCkRlZmF1bHRDb29raWVQb2xp
Y3kKcT8pgXFAfXFBKFgIAAAAbmV0c2NhcGVxQohYBwAAAHJmYzI5NjVxQ4lYEwAAAHJmYzIxMDlf
YXNfbmV0c2NhcGVxRE5YDAAAAGhpZGVfY29va2llMnFFiVgNAAAAc3RyaWN0X2RvbWFpbnFGiVgb
AAAAc3RyaWN0X3JmYzI5NjVfdW52ZXJpZmlhYmxlcUeIWBYAAABzdHJpY3RfbnNfdW52ZXJpZmlh
YmxlcUiJWBAAAABzdHJpY3RfbnNfZG9tYWlucUlLAFgcAAAAc3RyaWN0X25zX3NldF9pbml0aWFs
X2RvbGxhcnFKiVgSAAAAc3RyaWN0X25zX3NldF9wYXRocUuJWBAAAABfYmxvY2tlZF9kb21haW5z
cUwpWBAAAABfYWxsb3dlZF9kb21haW5zcU1OWAQAAABfbm93cU5KYpoVXXViWAgAAABfY29va2ll
c3FPfXFQaE5KYpoVXXViWAcAAABlbGFwc2VkcVFjZGF0ZXRpbWUKdGltZWRlbHRhCnFSSwBLAE3f
+YdxU1JxVFgHAAAAcmVxdWVzdHFVY3JlcXVlc3RzLm1vZGVscwpQcmVwYXJlZFJlcXVlc3QKcVYp
gXFXfXFYKFgGAAAAbWV0aG9kcVlYBAAAAFBPU1RxWmgzaDRoDGgNKYFxW31xXGgQaBEpUnFdKFgK
AAAAdXNlci1hZ2VudHFeWAoAAABVc2VyLUFnZW50cV9YFgAAAHB5dGhvbi1yZXF1ZXN0cy8yLjIw
LjBxYIZxYVgPAAAAYWNjZXB0LWVuY29kaW5ncWJYDwAAAEFjY2VwdC1FbmNvZGluZ3FjWA0AAABn
emlwLCBkZWZsYXRlcWSGcWVYBgAAAGFjY2VwdHFmWAYAAABBY2NlcHRxZ1gQAAAAYXBwbGljYXRp
b24vanNvbnFohnFpWAoAAABjb25uZWN0aW9ucWpYCgAAAENvbm5lY3Rpb25xa1gKAAAAa2VlcC1h
bGl2ZXFshnFtWAwAAABjb250ZW50LXR5cGVxblgMAAAAQ29udGVudC1UeXBlcW9oaIZxcFgOAAAA
Y29udGVudC1sZW5ndGhxcVgOAAAAQ29udGVudC1MZW5ndGhxclgCAAAANTdxc4ZxdHVzYmhPaDsp
gXF1fXF2KGg+aD8pgXF3fXF4KGhCiGhDiWhETmhFiWhGiWhHiGhIiWhJSwBoSoloS4loTCloTU5o
TkpimhVddWJoT31xeWhOSmKaFV11YlgEAAAAYm9keXF6Qzl7Impzb25ycGMiOiAiMi4wIiwgIm1l
dGhvZCI6ICJpY3hfZ2V0TGFzdEJsb2NrIiwgImlkIjogMX1xe1gFAAAAaG9va3NxfH1xfVgIAAAA
cmVzcG9uc2Vxfl1xf3NYDgAAAF9ib2R5X3Bvc2l0aW9ucYBOdWJ1YlgEAAAAZGF0YXGBY2pzb25y
cGNjbGllbnQucmVzcG9uc2UKU3VjY2Vzc1Jlc3BvbnNlCnGCKYFxg31xhChYBwAAAGpzb25ycGNx
hVgDAAAAMi4wcYZYAgAAAGlkcYdLAVgGAAAAcmVzdWx0cYh9cYkoWAcAAAB2ZXJzaW9ucYpYBAAA
ADAuMWFxi1gPAAAAcHJldl9ibG9ja19oYXNocYxYQAAAAGZkYjgwYWE3ZDJmZDEzMTlmNWEwZWIy
MjVmMGNjNzkyMDJhMjE4YmJiMjE0ZmU4M2UxMjQyYmZkMDMyOGUxYzJxjVgVAAAAbWVya2xlX3Ry
ZWVfcm9vdF9oYXNocY5YQAAAADFlNjI3NjQzODdhNGRlNzkxZWUyZDU3Mjg4ZTJlNDNhMWQzOTQy
ZTdjZTZiZDU3ZjcwMzMyNDEwMzIzNDZkM2Rxj1gKAAAAdGltZV9zdGFtcHGQigfpY6LiWowFWBoA
AABjb25maXJtZWRfdHJhbnNhY3Rpb25fbGlzdHGRXXGSfXGTKGiKWAMAAAAweDNxlFgEAAAAZnJv
bXGVWCoAAABoeGQyZDAwMWMzOTM4YzdmNmQzMWJjNzZiMWNkYTkyMmE2NGM1MWM4YmZxllgCAAAA
dG9xl1gqAAAAY3hmOTE0OGRiNGY4ZWM3ODgyM2E1MGNiMDZjNGZlZDgzNjYwYWYzOGQwcZhYCQAA
AHN0ZXBMaW1pdHGZWAcAAAAweGY0MjQwcZpYCQAAAHRpbWVzdGFtcHGbWA8AAAAweDU4YzVhZTI5
YWQ1ODBxnFgDAAAAbmlkcZ1YAwAAADB4MXGeWAUAAABub25jZXGfWAQAAAAweDY0caBYCAAAAGRh
dGFUeXBlcaFYBAAAAGNhbGxxolgEAAAAZGF0YXGjfXGkKFgGAAAAbWV0aG9kcaVYFQAAAHB1c2hH
YW1lUmVzdWx0VG9CbG9ja3GmWAYAAABwYXJhbXNxp31xqFgFAAAAX2hhc2hxqVhAAAAAeU15R2hl
T1JIcFpOUzZlWnZwQUtLdkNvRTlYdGRReG5wRlM1SVJ5MnpsQkN3OCtiZXN2NERVbm1BemxEa1Za
Y3Gqc3VYCQAAAHNpZ25hdHVyZXGrWFgAAABuOXhLVHdYN2NzcXU2elNGV3gxbFVpbkdzemREMG9K
MUFicVkwcWRtZDBaUU5kT3d0bEVQQ0FBdW51b09uNFBSOXNNZFRQdjlHYTZOUDd6cVlnam9mQUE9
caxYBgAAAHR4SGFzaHGtWEIAAAAweDFlNjI3NjQzODdhNGRlNzkxZWUyZDU3Mjg4ZTJlNDNhMWQz
OTQyZTdjZTZiZDU3ZjcwMzMyNDEwMzIzNDZkM2RxrnVhWAoAAABibG9ja19oYXNoca9YQAAAAGUw
MDg1YmQ2ZGNiZWY1YjZkZTIwNzVlN2U1NjhhNjEwY2E3YzdlZjk2OWRiM2I0ZDA0ZDQ5MzA4YWY3
MTI2Y2RxsFgGAAAAaGVpZ2h0cbFKg7ZUAFgHAAAAcGVlcl9pZHGyWCoAAABoeDU5NjFkMWJmNThl
NzBiNmM0MjUzOWZlODNmNmU1ZDY4YTNiMDkzZDRxs2irWFgAAABjbE9INWFzV1h6S0lUYXFQMjBD
MXI2MUI2M3dxYlNuZDBWVkFmN3IxR2UwOXpEZXRNSmNJRTdoRVJXWmYyOU8xOTNBbzFYWnU4Sytk
YkZXa2VSdmJLUUU9cbRYCwAAAG5leHRfbGVhZGVycbVYKgAAAGh4NTk2MWQxYmY1OGU3MGI2YzQy
NTM5ZmU4M2Y2ZTVkNjhhM2IwOTNkNHG2dXVidWIu
"""

if __name__ == "__main__":
    test_event_system()
