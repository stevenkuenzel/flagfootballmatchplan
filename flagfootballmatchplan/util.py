import numpy as np
from model import Team, MatchDay, Solution
from constants import NUM_TEAMS


def dist_teams(team1: Team, team2: Team) -> int:
    if team1.id == team2.id:
        return 0

    return round(dist_sqr(team1.pos_x, team1.pos_y, team2.pos_x, team2.pos_y))


def dist_sqr(x1: float, y1: float, x2: float, y2: float) -> float:
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def get_travel_dist_of_MatchDay(match_day: MatchDay) -> int:
    total = 0

    for pairing in match_day.pairings:
        total += dist_teams(match_day.host, pairing.team1)
        total += dist_teams(match_day.host, pairing.team2)

    return total


def get_travel_dist_of_Solution(solution: Solution) -> int:
    total = 0

    for match_day in solution.match_days:
        total += match_day.get_travel_dist()

    return total


def get_match_days_per_team_of_Solution(solution: Solution) -> np.ndarray:
    match_days_per_team = np.zeros(NUM_TEAMS, dtype=int)
    for match_day in solution.match_days:
        team_present = np.zeros(NUM_TEAMS, dtype=bool)

        for pairing in match_day.pairings:
            team_present[pairing.team1.id] = True
            team_present[pairing.team2.id] = True

        match_days_per_team = match_days_per_team + team_present.astype(int)

    return match_days_per_team


def get_fitness_of_Solution(solution: Solution) -> list[float]:
    # TODO: THIS IS AN INITIAL DRAFT
    stddev = float(np.std(get_match_days_per_team_of_Solution(solution)))
    return [stddev]


def determine_constraint_violations(solution: Solution) -> int:
    # Constraint 10:
    total_violation = 0
    for match_day in solution.match_days:
        occurrences = set()
        violation = 0
        for pairing in match_day.pairings:
            if pairing in occurrences:
                violation += 1
            else:
                occurrences.add(pairing)

        total_violation += violation

    return total_violation
