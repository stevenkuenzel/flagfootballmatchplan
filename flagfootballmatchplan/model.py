import random
from copy import deepcopy
from constants import ROUNDING_PRECISION, MAP_SCALE

class Team:
    def __init__(self, id: int) -> None:
        self.id: int = id

        self.pos_x = round(random.random(), ROUNDING_PRECISION) * MAP_SCALE
        self.pos_y = round(random.random(), ROUNDING_PRECISION) * MAP_SCALE

    def __repr__(self) -> str:
        return f"Team #{self.id} from {self.pos_x}, {self.pos_y}"

    def __eq__(self, value: "Team") -> bool:
        return self.id == value.id


class Group:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.teams: list[Team] = []

    def generate_pairings(self, num_matches: int) -> list[tuple[int, int]]:
        return [
            (a.id, b.id)
            for idx, a in enumerate(self.teams)
            for b in self.teams[idx + 1 :]
            for _ in range(num_matches)
        ]


class Pairing:
    def __init__(self, team1: Team, team2: Team) -> None:
        self.team1: Team = team1
        self.team2: Team = team2

    def __repr__(self) -> str:
        return f"{self.team1.id}-{self.team2.id}"

    def __eq__(self, value: "Pairing") -> bool:
        return self.team1 == value.team1 and self.team2 == value.team2

    def __hash__(self) -> int:
        return hash((self.team1.id, self.team2.id))


class MatchDay:
    def __init__(self, host: Team) -> None:
        self.host: Team = host
        self.pairings: list[Pairing] = []
        self.games_of_host : int = 0

    def __repr__(self) -> str:
        return f"{self.host}: {'  '.join([str(x) for x in self.pairings])}"




class Solution:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.match_days: list[MatchDay] = []

    def __repr__(self) -> str:
        return "\n".join([str(x) for x in self.match_days])


    def mutate(self, new_id: int) -> "Solution":
        cpy = deepcopy(self)
        cpy.id = new_id
        days = random.sample(range(len(self.match_days)), k=2)

        day1 = days[0]
        day2 = days[1]
        match_day1 = self.match_days[day1]
        match_day2 = self.match_days[day2]

        # TODO: Mutation op is still dirty -- just a quick draft; design more nice :)

        # select slots from [.games_of_host, len(pairings)] <-- never allow to change one of the first ~3 slots: CONSTRAINT 4
        # slot1 = random.randint(match_day1.games_of_host, len(match_day1.pairings) - 1)
        slot1 = random.randint(0, len(match_day1.pairings) - 1)

        if random.random() < 0.1:
            slot2 = -1
        else:
            # slot2 = random.randint(match_day2.games_of_host, len(match_day2.pairings) - 1)
            slot2 = random.randint(0, len(match_day2.pairings) - 1)
        
        # pairing1 = match_day1.pairings[slot1]
        # pairing2 = match_day2.pairings[slot2]
        # if pairing1.team1 == match_day1.host or pairing1.team2 == match_day1.host:
        #     return None
        # if pairing2.team1 == match_day2.host or pairing2.team2 == match_day2.host:
        #     return None

        x1 = cpy.match_days[day1].pairings.pop(slot1)
        if slot2 != -1:
            x2 = cpy.match_days[day2].pairings.pop(slot2)
            cpy.match_days[day1].pairings.append(x2)
        cpy.match_days[day2].pairings.append(x1)

        return cpy