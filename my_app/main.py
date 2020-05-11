import asyncio
import logging
from typing import Sequence

from lft.consensus.consensus import Consensus
from lft.consensus.epoch import Epoch
from lft.consensus.epoch import EpochPool
from lft.consensus.events import (
    Event, InitializeEvent, ReceiveVoteEvent, RoundEndEvent, RoundStartEvent,
    BroadcastDataEvent, BroadcastVoteEvent

)
from lft.consensus.messages.data import Data, DataPool, DataFactory
from lft.consensus.messages.vote import Vote, VotePool, VoteFactory
from lft.event import EventSystem
from lft.event.mediators import DelayedEventMediator

# VOTERS = [b"node_0", b"node_1", b"node_2", b"node_3"]
THIS_NODE = b"node_0"


import coloredlogs
logger = coloredlogs.install(level="DEBUG")
logger = logging.getLogger(__name__)
# from lft.app.logger import Logger
# logger = Logger(THIS_NODE).logger
logger.info("test!")


def coro_logger(func):
    async def _(*args, **kwargs):
        name = func.__qualname__
        logger.info(f"'{name}' started========")
        await func(*args, **kwargs)
        logger.info(f"'{name}' ended=========")
    return _


# ================= ================ ================ ===============
# Data
class AppData(Data):
    def __init__(
            self, height, prev_votes, epoch_num, round_num,
            id_, prev_id, proposer_id, is_none_data=False, is_lazy_data=False):
        self._number = height
        self._epoch_num = epoch_num
        self._round_num = round_num
        self._prev_votes = prev_votes

        self._id = id_
        self._prev_id = prev_id
        self._proposer_id = proposer_id

        self._is_none = is_none_data
        self._is_lazy = is_lazy_data

    def __repr__(self):
        return f"{self.__class__.__name__}(number={self._number}, _id={self._id})"

    @property
    def number(self) -> int:
        return self._number

    @property
    def prev_id(self) -> bytes:
        return self._prev_id

    @property
    def proposer_id(self) -> bytes:
        return self._proposer_id

    @property
    def prev_votes(self) -> Sequence['Vote']:
        return self._prev_votes

    def is_none(self) -> bool:
        return self._is_none

    def is_lazy(self) -> bool:
        return self._is_lazy

    @property
    def id(self) -> bytes:
        return self._id

    @property
    def epoch_num(self) -> int:
        return self._epoch_num

    @property
    def round_num(self) -> int:
        return self._round_num


class AppDataFactory(DataFactory):
    async def create_data(self, data_number: int, prev_id: bytes, epoch_num: int, round_num: int,
                          prev_votes: Sequence['Vote']) -> 'Data':
        data_id = f"data_{data_number}".encode()
        prev_data_id = f"data_{data_number-1}".encode()

        return AppData(
            height=data_number, prev_votes=prev_votes, epoch_num=epoch_num, round_num=round_num,
            id_=data_id, prev_id=prev_data_id, proposer_id=THIS_NODE
        )

    def create_none_data(self, epoch_num: int, round_num: int, proposer_id: bytes) -> 'Data':
        return AppData(
            height=None, prev_votes=[], epoch_num=epoch_num, round_num=round_num,
            id_=None, prev_id=None, proposer_id=None,
            is_none_data=True
        )

    def create_lazy_data(self, epoch_num: int, round_num: int, proposer_id: bytes) -> 'Data':
        return AppData(
            height=None, prev_votes=[], epoch_num=epoch_num, round_num=round_num,
            id_=None, prev_id=None, proposer_id=None,
            is_lazy_data=True
        )

    async def create_data_verifier(self) -> 'DataVerifier':
        pass


# Vote
class AppVote(Vote):
    def __init__(
            self, data_id: bytes, commit_id: bytes, voter_id: bytes, id_: bytes, epoch_num: int, round_num: int,
            is_none_vote=False, is_lazy_vote=False
    ):
        self._voter_id = voter_id
        self._data_id = data_id
        self._epoch_num = epoch_num
        self._round_num = round_num

        self._id = id_
        self._commit_id = commit_id

        self._is_none = is_none_vote
        self._is_lazy = is_lazy_vote

    def __repr__(self):
        return f"{self.__class__.__name__}(data_id={self._data_id}, _id={self._id})"

    @property
    def data_id(self) -> bytes:
        return self._data_id

    @property
    def commit_id(self) -> bytes:
        return self._commit_id

    @property
    def voter_id(self) -> bytes:
        return self._voter_id

    def is_none(self) -> bool:
        return self._is_none

    def is_lazy(self) -> bool:
        return self._is_lazy

    @property
    def id(self) -> bytes:
        return self._id

    @property
    def epoch_num(self) -> int:
        return self._epoch_num

    @property
    def round_num(self) -> int:
        return self._round_num


class AppVoteFactory(VoteFactory):
    async def create_vote(self, data_id: bytes, commit_id: bytes, epoch_num: int, round_num: int) -> 'Vote':
        voter_id = THIS_NODE
        vote_id = voter_id + data_id
        return AppVote(
            data_id=data_id, commit_id=commit_id, voter_id=voter_id,
            id_=vote_id, epoch_num=epoch_num, round_num=round_num
        )

    def create_none_vote(self, epoch_num: int, round_num: int) -> 'Vote':
        return AppVote(
            data_id=b"None", commit_id=b"None", voter_id=b"None",
            id_=b"None", epoch_num=epoch_num, round_num=round_num

        )

    def create_lazy_vote(self, voter_id: bytes, epoch_num: int, round_num: int) -> 'Vote':
        pass

    async def create_vote_verifier(self) -> 'VoteVerifier':
        pass


# Epoch
class AppEpoch(Epoch):
    def __init__(self, num: int, voters: Sequence[bytes]):
        self._num = num
        self._voters = voters
        self._voters_num = len(self._voters)

    def __repr__(self):
        return f"Epoch_{self._num}"


    @property
    def num(self) -> int:
        return self._num

    @property
    def quorum_num(self) -> int:
        return len(self._voters)

    @property
    def voters_num(self) -> int:
        return self._voters_num

    @property
    def voters(self) -> Sequence[bytes]:
        return self._voters

    def verify_data(self, data: Data):
        if isinstance(data, str):
            logger.info("Verify Data Success!")
        else:
            raise RuntimeError()

    def verify_vote(self, vote: Vote, vote_index: int = -1):
        if isinstance(vote, str):
            logger.info("Verify Vote Success!")
        else:
            raise RuntimeError()

    def verify_proposer(self, proposer_id: bytes, round_num: int) -> bool:
        pass

    def verify_voter(self, voter: bytes, vote_index: int = -1):
        pass

    def get_proposer_id(self, round_num: int) -> bytes:
        pass

    def get_voter_id(self, vote_index: int) -> bytes:
        pass

    def get_voters_id(self) -> Sequence[bytes]:
        pass

    def __eq__(self, other):
        pass


# ================= ================ ================ ===============
@coro_logger
async def consensus_engine(event_system):
    # TODO
    # Run
    data_fac = AppDataFactory()
    vote_fac = AppVoteFactory()

    Consensus(event_system, THIS_NODE, data_fac, vote_fac)


class AppLauncher:
    def __init__(self, event_system: EventSystem):
        self._target_height = 0
        self._epoch_num = 0
        self._round_num = 0

        self._event_system = event_system
        self._data_fac: AppDataFactory = AppDataFactory()
        self._vote_fac: AppVoteFactory = AppVoteFactory()

        self._epoch_pool = EpochPool()

        # Mapping Handlers
        self._event_system.simulator.register_handler(BroadcastDataEvent, self._from_LFT)
        self._event_system.simulator.register_handler(BroadcastVoteEvent, self._from_LFT)

        self._event_system.simulator.register_handler(RoundEndEvent, self._on_round_end)

    @coro_logger
    async def run(self):
        await self.init_genesis()
        # await asyncio.sleep(10)  # To maintain other coroutines

    @coro_logger
    async def init_genesis(self):
        # EpochPool을 여러개 갖다 넣어서 초기화시키면 알아서 라운드 시작해준다 (Voter 조건이 맞을 경우).
        self._epoch_pool.add_epoch(AppEpoch(num=self._epoch_num, voters=[]))  # Voter 없으니 자동 통과

        # 1번 블록에 대한 Epoch를 만들고 초기화
        self._epoch_num += 1
        self._epoch_pool.add_epoch(AppEpoch(num=self._epoch_num, voters=[THIS_NODE]))

        # Data for genesis
        self._target_height += 1  # Init과 동시에 0 번 데이터가 commit되었다고 가정
        genesis_data = await self._data_fac.create_data(
            data_number=self._target_height,
            prev_id=b"",
            epoch_num=0,  # epoch 0에서 커밋되었다고 가정
            round_num=self._round_num,  # 라운드는 적당히
            prev_votes=[]
        )

        # 이 데이터를 갖고 컨센서스 알고리즘을 시작하겠다고 하는 것임. commit_id는 init 시점에서 확정된 데이터 hash가 되겠군..
        event = InitializeEvent(
            commit_id=b"data_0",
            epoch_pool=[
                self._epoch_pool.get_epoch(0),
                self._epoch_pool.get_epoch(1),
            ],
            data_pool=[genesis_data],
            vote_pool=[],
        )
        # event.deterministic = False
        self._event_system.start(blocking=False)

        logger.info("App raise Init event.")
        self._event_system.simulator.raise_event(event)

    async def new_epoch(self):
        self._target_height += 1

        new_epoch = AppEpoch(num=self._epoch_num, voters=[THIS_NODE])
        self._epoch_pool.add_epoch(new_epoch)

    async def round_start(self):
        ev = RoundStartEvent(
            epoch=self._epoch_pool.get_epoch(self._epoch_num),
            round_num=self._target_height
        )
        self._event_system.simulator.raise_event(ev)

    @coro_logger
    async def pass_vote_to_consensus(self):
        data_id = f"data_{self._target_height}".encode()  # b'data_#'
        commit_id = f"data_{self._target_height-1}".encode()  # b'data_#'
        vote = await self._vote_fac.create_vote(
            data_id=data_id, commit_id=commit_id, epoch_num=self._epoch_num, round_num=self._target_height
        )

        event = ReceiveVoteEvent(vote)
        self._event_system.simulator.raise_event(event)

    async def _from_LFT(self, event: Event):
        logger.critical(f">> LFT requested: {type(event)}")

    async def _on_round_end(self, event: RoundEndEvent):
        logger.critical(f"\n\n\n>> ADD HEIGHT : {event.commit_id}!===========\n\n\n")

        await self.new_epoch()
        await self.round_start()
        print("Await votes...")
        await asyncio.sleep(1)
        await self.pass_vote_to_consensus()


@coro_logger
async def main():
    event_system = EventSystem(logger=logger)
    event_system.set_mediator(DelayedEventMediator)

    await consensus_engine(event_system),

    app = AppLauncher(event_system=event_system)
    running_services = [
        app.run()
    ]

    await asyncio.gather(*running_services)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
