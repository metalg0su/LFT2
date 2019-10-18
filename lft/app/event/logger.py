import datetime
import json
from lft.consensus.events import (Event, InitializeEvent, DoneRoundEvent,
                                  ReceivedDataEvent, ReceivedVoteEvent, StartRoundEvent,
                                  ProposeSequence, VoteSequence, BroadcastDataEvent,
                                  BroadcastVoteEvent)
from lft.event import EventSimulator
from lft.serialization import Serializable


class Logger:
    def __init__(self, node_id: bytes, event_simulator: EventSimulator):
        self._node_id = node_id
        self._simulator = event_simulator
        self._encoder = _JSONEncoder()

        self._handlers = {
            InitializeEvent:
                self._simulator.register_handler(InitializeEvent, self._on_initialize_event),
            DoneRoundEvent:
                self._simulator.register_handler(DoneRoundEvent, self._on_done_round_event),
            ReceivedDataEvent:
                self._simulator.register_handler(ReceivedDataEvent, self._on_received_consensus_data_event),
            ReceivedVoteEvent:
                self._simulator.register_handler(ReceivedVoteEvent, self._on_received_consensus_vote_event),
            StartRoundEvent:
                self._simulator.register_handler(StartRoundEvent, self._print_log),
            ProposeSequence:
                self._simulator.register_handler(ProposeSequence, self._print_log),
            VoteSequence:
                self._simulator.register_handler(VoteSequence, self._print_log),
            BroadcastDataEvent:
                self._simulator.register_handler(BroadcastDataEvent, self._print_log),
            BroadcastVoteEvent:
                self._simulator.register_handler(BroadcastVoteEvent, self._print_log)
        }

    def __del__(self):
        self.close()

    def close(self):
        for event_type, handler in self._handlers.items():
            self._simulator.unregister_handler(event_type, handler)
        self._handlers.clear()

    def _on_initialize_event(self, event: InitializeEvent):
        self._print_log(event)

    def _on_done_round_event(self, event: DoneRoundEvent):
        self._print_log(event)

    def _on_received_consensus_data_event(self, event: ReceivedDataEvent):
        self._print_log(event)

    def _on_received_consensus_vote_event(self, event: ReceivedVoteEvent):
        self._print_log(event)

    def _print_log(self, event: Event):
        event_serialized = self._encoder.encode(event)
        print(f"{shorten(self._node_id)}, {datetime.datetime.now()}:: {event_serialized}")


class _JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return "0x" + shorten(o)
        elif isinstance(o, str):
            return "0r" + o
        elif isinstance(o, Serializable):
            return o.serialize()
        else:
            return super().encode(o)


def shorten(b: bytes):
    return b.hex()[:8]
