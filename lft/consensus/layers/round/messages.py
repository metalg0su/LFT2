from typing import List, Dict, DefaultDict, Set

from lft.consensus.candidate import Candidate
from lft.consensus.messages.data import Data, Vote
from lft.consensus.term import Term
from lft.consensus.exceptions import CannotComplete, AlreadyCompleted, AlreadyVoted, NotCompleted, DataIDNotFound

Datums = Dict[bytes, Data]  # dict[data_id] = data
Votes = DefaultDict[bytes, List[Vote]]  # dict[data_id][0] = vote


class RoundMessages:
    def __init__(self, term: Term):
        self._term = term

        self._datums: Datums = {}
        self._votes: Votes = DefaultDict(list)
        self._voters: Set[bytes] = set()

        self._is_completed = False

    @property
    def is_completed(self):
        return self._is_completed

    def add_data(self, data: Data):
        if self.is_completed:
            raise AlreadyCompleted

        self._datums[data.id] = data

    def add_vote(self, vote: Vote):
        if self.is_completed:
            raise AlreadyCompleted

        if vote.voter_id in self._voters:
            raise AlreadyVoted(vote.id, vote.voter_id)

        self._voters.add(vote.voter_id)
        self._votes[vote.data_id].append(vote)

    def complete(self):
        if self.is_completed:
            raise AlreadyCompleted

        try:
            max_data_id = self._find_max_data_id()
        except ValueError:
            raise CannotComplete(f"Datums is empty. {self._datums}")

        majority = len(self._votes[max_data_id])
        if self._term.quorum_num > majority and self._term.voters_num != len(self._voters):
            raise CannotComplete(f"Majority({majority}) does not reach quorum({self._term.quorum_num} or "
                                 f"All voters have not voted. ({len(self._voters)}/{self._term.voters_num})")

        try:
            self._datums[max_data_id]
        except KeyError:
            raise DataIDNotFound(f"Upper layers did not send data. {max_data_id}")
        else:
            self._is_completed = True

    def result(self):
        if not self.is_completed:
            raise NotCompleted

        candidate_data_id = self._find_max_data_id()

        unordered_votes = self._votes[candidate_data_id]
        candidate_votes = self._order_votes(unordered_votes)

        if self._term.quorum_num > len(unordered_votes):
            return Candidate(None, candidate_votes)

        try:
            candidate_data = self._datums[candidate_data_id]
        except KeyError:
            raise DataIDNotFound(f"Upper layers did not send data. {candidate_data_id}")
        else:
            if candidate_data.is_not() or candidate_data.is_none():
                return Candidate(None, candidate_votes)
            else:
                return Candidate(candidate_data, candidate_votes)

    def _find_max_data_id(self):
        return max(self._votes, key=lambda key: len(self._votes.get(key)))

    def _order_votes(self, votes: List[Vote]):
        ordered_votes = []
        for voter in self._term.voters:
            ordered_vote = next((vote for vote in votes if vote.voter_id == voter), None)
            ordered_votes.append(ordered_vote)
        return ordered_votes


