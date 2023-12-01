import dataclasses
import re
import functools

@dataclasses.dataclass
class Blueprint:
    id: int
    oreRobotCost: tuple[int, int, int]
    clayRobotCost: tuple[int, int, int]
    obsidianRobotCost: tuple[int, int, int]
    geodeRobotCost: tuple[int, int, int]

blueprint_re = re.compile(r"Blueprint (?P<id>\d+): Each ore robot costs (?P<or_cost_o>\d+) ore. Each clay robot costs (?P<cr_cost_o>\d+) ore. Each obsidian robot costs (?P<obr_cost_o>\d+) ore and (?P<obr_cost_c>\d+) clay. Each geode robot costs (?P<gr_cost_o>\d+) ore and (?P<gr_cost_ob>\d+) obsidian.")

def parse_input(filename: str) -> list[Blueprint]:
    with open(filename, "r") as f:
        data = f.read()
        return [
            Blueprint(
                id=int(match_["id"]),
                oreRobotCost=(int(match_["or_cost_o"]), 0, 0),
                clayRobotCost=(int(match_["cr_cost_o"]), 0, 0),
                obsidianRobotCost=(int(match_["obr_cost_o"]), int(match_["obr_cost_c"]), 0),
                geodeRobotCost=(int(match_["gr_cost_o"]), 0, int(match_["gr_cost_ob"]))
            )
            for match_ in blueprint_re.finditer(data)
        ]

@dataclasses.dataclass
class State:
    robots: tuple[int, int, int, int] = (1, 0, 0, 0)
    resources: tuple[int, int, int, int] = (0, 0, 0, 0)


def individual_robot_purchasing_decisions_unused(cost: tuple[int, int, int], resources: tuple[int, int, int, int]) -> list[tuple[int, tuple[int, int, int, int]]]:
    """
    Returns a list of the possible numbers of robots that can be purchased based
    on the cost of that robot and the number of resources available. Returns those
    individual values as a list, tupled together with the number of resources that
    will be remaining if the quantity is purchased.
    """

    min_ = None

    if cost[0] != 0:
        min_ = resources[0] // cost[0]

    if cost[1] != 0:
        new_min = resources[1] // cost[1]
        if min_ is None or new_min < min_:
            min_ = new_min

    if cost[2] != 0:
        new_min = resources[2] // cost[2]
        if min_ is None or new_min < min_:
            min_ = new_min

    return [
        (qty, (
            resources[0] - (qty * cost[0]),
            resources[1] - (qty * cost[1]),
            resources[2] - (qty * cost[2]),
            resources[3],
        ))
        for qty in range(1, min_+1)
    ]


def available_robot_purchasing_decisions_unused(costs: list[tuple[int, int, int]], resources: tuple[int, int, int, int]) -> list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]:
    """
    Generates robot purchasing decisions based on the idea that you can
    construct any number of robots in a single minute. Turns out that
    this is not the case, we only have one robot producing factory, which
    can only make one robot per turn. Still, we can use this anyway and just
    reject the purchasing decisions which are invalid.
    """
    decisions = [(tuple(0 for _ in range(len(costs))), resources)]
    for idx, indv_robot_cost in enumerate(costs):
        new_decisions = []
        for robots_purchased_already, resources_remaining in decisions:
            for quant, remain in individual_robot_purchasing_decisions_unused(indv_robot_cost, resources_remaining):
                new_decisions.append((
                    tuple(
                        quant if i == idx else prev_quant
                        for i, prev_quant in
                        enumerate(robots_purchased_already)
                    ),
                    remain
                ))

        decisions.extend(new_decisions)

    return decisions


def available_robot_purchasing_decisions(costs: list[tuple[int, int, int]], resources: tuple[int, int, int, int]) -> list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]:
    decisions = [(tuple([0] * len(costs)), resources)]

    for idx, indv_robot_cost in enumerate(costs):
        if all(cost <= budget for cost, budget in zip(indv_robot_cost, resources)):
            decisions.append(
                (
                    tuple((1 if idx == i else 0 for i in range(len(costs)))),
                    (
                        resources[0] - indv_robot_cost[0],
                        resources[1] - indv_robot_cost[1],
                        resources[2] - indv_robot_cost[2],
                        resources[3],
                    )
                )
            )

    return decisions


def prune_purchasing_decisions_part_1(minutes_remaining: int, available_purchasing_decisions: list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]) -> list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]:
    # Found this optimization on Reddit. Ignore lower quanity blueprints
    # if there's not a lot of time left.
    round_based_rejections = [
        pd for pd in available_purchasing_decisions
        # if not (minutes_remaining < 15 and pd[0][0] > 0)
        # if not (minutes_remaining < 10 and pd[0][1] > 0)
        # if not (minutes_remaining < 8 and pd[0][2] > 0)
    ]

    # If any geode-cracking robots are available to be purchased, ignore
    # possibilities where none are purchased.
    if (max_purchasable := max(pd[0][3] for pd in round_based_rejections)) > 0:
        for decision in reversed(round_based_rejections):
            if decision[0][3] == max_purchasable:
                yield decision
        return

    # If any obsidian-generating robots are available to be purchased, ignore
    # possibilities where none are purchased.
    if (max_purchasable := max(pd[0][2] for pd in round_based_rejections)) > 0:
        for decision in reversed(round_based_rejections):
            if decision[0][2] == max_purchasable:
                yield decision
        return

    yield from reversed(round_based_rejections)


def prune_purchasing_decisions_part_2(minutes_remaining: int, available_purchasing_decisions: list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]) -> list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]]:
    # Found this optimization on Reddit. Ignore lower quanity blueprints
    # if there's not a lot of time left.
    round_based_rejections = [
        pd for pd in available_purchasing_decisions
        if not (minutes_remaining < 25 and pd[0][0] > 0)
        if not (minutes_remaining < 13 and pd[0][1] > 0)
        if not (minutes_remaining < 10 and pd[0][2] > 0)
    ]

    # # If any geode-cracking robots are available to be purchased, ignore
    # # possibilities where none are purchased.
    # if (max_purchasable := max(pd[0][3] for pd in round_based_rejections)) > 0:
    #     for decision in reversed(round_based_rejections):
    #         if decision[0][3] == max_purchasable:
    #             yield decision
    #     return

    # # If any obsidian-generating robots are available to be purchased, ignore
    # # possibilities where none are purchased.
    # if (max_purchasable := max(pd[0][2] for pd in round_based_rejections)) > 0:
    #     for decision in reversed(round_based_rejections):
    #         if decision[0][2] == max_purchasable:
    #             yield decision
    #     return

    yield from reversed(round_based_rejections)


def optimal_geode_output(blueprint: Blueprint, total_minutes: int, purchasing_decions_pruning_strategy) -> int:
    @functools.lru_cache(maxsize=1_000_000_000)
    def _optimal_geode_output(minutes_remaining: int, robots_owned: tuple[int, int, int, int], resources: tuple[int, int, int, int]):
        if minutes_remaining <= 0:
            return resources[-1]

        minutes_remaining -= 1

        available_purchasing_decisions = available_robot_purchasing_decisions(
            [
                blueprint.oreRobotCost,
                blueprint.clayRobotCost,
                blueprint.obsidianRobotCost,
                blueprint.geodeRobotCost,
            ],
            resources,
        )

        screened_purchasing_decisions = purchasing_decions_pruning_strategy(
            minutes_remaining,
            available_purchasing_decisions,
        )

        pds_tried = 0
        best_geode_output = 0
        for robots_purchased, resources_remaining in screened_purchasing_decisions:
            pds_tried += 1
            candidate_geode_output = _optimal_geode_output(
                minutes_remaining,
                (
                    robots_owned[0] + robots_purchased[0],
                    robots_owned[1] + robots_purchased[1],
                    robots_owned[2] + robots_purchased[2],
                    robots_owned[3] + robots_purchased[3],
                ),
                (
                    robots_owned[0] + resources_remaining[0],
                    robots_owned[1] + resources_remaining[1],
                    robots_owned[2] + resources_remaining[2],
                    robots_owned[3] + resources_remaining[3],
                ),
            )

            if candidate_geode_output > best_geode_output:
                best_geode_output = candidate_geode_output

        return best_geode_output

    return _optimal_geode_output(total_minutes, (1, 0, 0, 0), (0, 0, 0, 0))


def part1(input: list[Blueprint]):
    sum = 0

    for bp in input:
        output = optimal_geode_output(bp, 24, prune_purchasing_decisions_part_1)
        print(f"Part 1: Blueprint {bp.id} max output: {output}")
        sum += bp.id * output

    return sum

def part2(input: list[Blueprint]):
    usable_blueprints = input[:3]

    product = 1
    for bp in usable_blueprints:
        output = optimal_geode_output(bp, 32, prune_purchasing_decisions_part_2)
        print(f"Part 2: Blueprint {bp.id} max output: {output}")
        product = product * output

    return product


if __name__ == "__main__":
    input = parse_input("input.txt")
    sample_input = parse_input("sample_input.txt")

    # test_blueprint = sample_input[0]
    # print(f"Best Geode Output (sample input, BP ID: {test_blueprint.id}):", optimal_geode_output(test_blueprint))

    # print(f"Part 1 (sample):", part1(sample_input))
    # print(f"Part 1:", part1(input))

    # print("Part 1 (sample):", part1(sample_input))
    # print("Part 1:", part1(input))

    print(f"Part 2 (sample):", part2(sample_input))
    print(f"Part 2:", part2(input))
