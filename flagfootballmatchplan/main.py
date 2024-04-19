# REPRESENTATION CATCHES CONSTRAINTS: 1, 2, 3, 4, _, _, _, 8, 9, _
# TO SATISFY: 5, 6, 7, 10
import random
from copy import deepcopy

from constants import (
    NUM_GROUPS,
    NUM_TEAMS,
    TEAMS_PER_GROUP,
    GAMES_PER_DAY_MIN,
    NUM_GAMES_AGAINST_OTHERS,
    NUM_GAMES_AGAINST_GROUP_MEMBERS,
)
from model import Group, MatchDay, Pairing, Solution, Team
from util import (
    determine_constraint_violations,
    get_fitness_of_Solution,
    get_match_days_per_team_of_Solution,
)

# Save old random state (to restore later) and fix seed to get equal team locations.
initial_random_state = random.getstate()
random.seed(42)

# Create random teams.
teams: list[Team] = []

for i in range(NUM_TEAMS):
    teams.append(Team(i))


# Reset the old random state to have different progress from here on ...
random.setstate(initial_random_state)

# Shuffle teams. MAYBE SOMEWHEN ELSE
# random.shuffle(teams)

# Create groups.
groups: list[Group] = []

for i in range(NUM_GROUPS):
    group = Group(i)

    for j in range(TEAMS_PER_GROUP):
        group.teams.append(teams[i * TEAMS_PER_GROUP + j])

    groups.append(group)

all = Group(-1)
all.teams.extend(teams)

group_pairings = []
for group in groups:
    group_pairings.extend(group.generate_pairings(NUM_GAMES_AGAINST_GROUP_MEMBERS))

other_pairings = all.generate_pairings(NUM_GAMES_AGAINST_OTHERS)

# CONSTRAINTS 8+9

group_and_other_pairings = list(filter(lambda x: x not in group_pairings, other_pairings))
group_and_other_pairings.extend(group_pairings)

# Convert tuples to Pairing objects.
all_pairings: list[Pairing] = list(
    map(lambda x: Pairing(teams[x[0]], teams[x[1]]), group_and_other_pairings)
)

# Copy the pairings to have a separate 'remaining' pairings list to modify.
remaining_pairings: list[Pairing] = all_pairings.copy()


def create_solution(id: int):
    solution = Solution(id)

    for team in teams:
        # CONSTRAINT 3: every team is host of one match day
        match_day = MatchDay(team)

        av = list(
            filter(lambda x: team == x.team1 or team == x.team2, remaining_pairings)
        )
        s = min(GAMES_PER_DAY_MIN, len(av))
        match_day.games_of_host = s

        for i in range(s):
            match_day.pairings.append(av[i])
            remaining_pairings.remove(av[i])

        solution.match_days.append(match_day)

    assignment_to_matchday = random.choices(
        range(len(solution.match_days)), k=len(remaining_pairings)
    )

    for i in range(len(remaining_pairings)):
        solution.match_days[assignment_to_matchday[i]].pairings.append(
            remaining_pairings[i]
        )

    return solution


sol_init = create_solution(0)


def local_search() -> Solution:
    id_counter = 0
    sol_best = deepcopy(sol_init)
    fit_best = get_fitness_of_Solution(sol_best)[0]

    for _ in range(5000):
        id_counter += 1
        sol_new = sol_best.mutate(id_counter)
        fit_new = get_fitness_of_Solution(sol_new)[0]
        # fit_new = sol_new.get_travel_dist()

        if fit_new < fit_best:
            sol_best = sol_new
            fit_best = fit_new
            violations = determine_constraint_violations(sol_best)
            print(f"#{id_counter}: {fit_new}  violates #10 how often: {violations}")
            print(get_match_days_per_team_of_Solution(sol_best))

    return sol_best


# def simulated_annealing()->Solution:
#     id_counter = 0
#     sol_curr = deepcopy(sol_init)
#     fit_curr = sol_curr.get_fitness()[0]
#     # fit_curr = sol_curr.get_travel_dist()

#     sol_best = sol_curr
#     fit_best = fit_curr

#     T = 10000.0
#     t_max = 5000

#     for t in range(t_max):
#         id_counter += 1
#         sol_new = sol_curr.mutate(id_counter)
#         fit_new = sol_new.get_fitness()[0]
#         # fit_new = sol_new.get_travel_dist()

#         if fit_new <= fit_curr:
#             sol_curr = sol_new
#             fit_curr = fit_new
#             violations = sol_new.determine_constrains()
#             print(f"#{id_counter}: {fit_new}  violates #10 how often: {violations}")
#         else:
#             Tt = T * (1.0 - (float(t) / float(t_max)))
#             p = math.exp(-float(fit_new - fit_curr) / Tt)

#             if random.random() <= p:
#                 sol_curr = sol_new
#                 fit_curr = fit_new
#                 violations = sol_new.determine_constrains()
#                 # print(f">> #{id_counter}: {fit_new}  violates #10 how often: {violations}")

#         if fit_curr <= fit_best:
#             sol_best = sol_curr
#             fit_best = fit_curr

#     return sol_best

sol_1 = local_search()
print(sol_1)

# sol_2 = simulated_annealing()

print(f"LOCAL SEARCH: {sol_1.get_travel_dist()}")
# print(f"SIMULATED ANNEALNING: {sol_2.get_travel_dist()}")
