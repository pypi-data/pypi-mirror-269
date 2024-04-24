from switch_pb2 import SwitchReport, SWITCH_ON


def is_on(r: SwitchReport):
    return r.value == SWITCH_ON
