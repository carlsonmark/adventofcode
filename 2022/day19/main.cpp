#include <iostream>
#include <set>

#include "structures.hpp"

std::set<RobotOption> robot_options(const Blueprint &blueprint, const GameState &state)
{
    std::set<RobotOption> options{RobotOption::none};
    bool needs_ore{};
    bool needs_clay{};
    bool needs_obsidian{};
    bool needs_geode{};

    // Consider it an option to build robots if there are enough resources
    // to do so.
    if (blueprint.rb_ore_cost_ore <= state.ore)
        needs_ore = true;
    if (blueprint.rb_clay_cost_ore <= state.ore)
        needs_clay = true;
    if (blueprint.rb_obsidian_cost_ore <= state.ore &&
        blueprint.rb_obsidian_cost_clay <= state.clay) {
        needs_obsidian = true;
    }
    if (blueprint.rb_geode_cost_ore <= state.ore &&
        blueprint.rb_geode_cost_obsidian <= state.obsidian) {
        needs_geode = true;
    }

    // If it is near the end, it is unlikely that another clay robot will be
    // helpful.
    if (state.time_remaining <= 3)
        needs_clay = false;

    // For any non-geode robot, it is not necessary to build one if the amount
    // of resources gathered per turn is < the amount needed to make other
    // robots.

    // Ore check
    auto t = state.time_remaining + 1;
    if (state.rb_ore * t + state.ore >= t * blueprint.max_ore_cost)
        needs_ore = false;

    // Clay check
    if (state.rb_clay * t + state.clay >= t * blueprint.rb_obsidian_cost_clay)
        needs_clay = false;

    // Obsidian check
    if (state.rb_obsidian * t + state.obsidian >= t * blueprint.rb_geode_cost_obsidian)
        needs_obsidian = false;

    if (needs_ore)
        options.insert(RobotOption::ore);
    if (needs_clay)
        options.insert(RobotOption::clay);
    if (needs_obsidian)
        options.insert(RobotOption::obsidian);
    if (needs_geode)
        options.insert(RobotOption::geode);

    return options;
}

GameState find_optimal(const Blueprint &blueprint, GameState &state, const std::set<RobotOption> &skipped_options)
{
    state.time_remaining -= 1;
    if (state.time_remaining == 1)
    {

        state.best_score = state.geode + state.rb_geode;
//        if (state.best_score >= 4)
//            std::cout << std::endl;
        return state;
    }
    auto options = robot_options(blueprint, state);
    for (const auto &option : skipped_options)
    {
        options.erase(option);
    }
    auto best_score = state.best_score;
    auto best_state = state;
    for (const auto &option : options)
    {
        GameState option_state(state);
        option_state.try_build_robot(option, blueprint);
        option_state.collect_resources();
        std::set<RobotOption> skipped_options;
        if (option == RobotOption::none)
        {
            skipped_options = options;
            skipped_options.erase(RobotOption::none);
        }
        option_state = find_optimal(blueprint, option_state, skipped_options);
        if (option_state.best_score > best_score)
        {
            best_score = option_state.best_score;
            best_state = option_state;
        }
    }
    return best_state;
}

int compute_quality_level(const Blueprint &blueprint)
{
    auto state = GameState();
    state = find_optimal(blueprint, state, {});
    auto quality = state.best_score;
    return quality;
}

int main() {

    std::vector<Blueprint> real_input {
//            {1, 4, 4, 4, 18, 4, 9},
            {2, 2, 2, 2, 17, 2, 10},
//            {3, 4, 4, 2, 7, 4, 13},
//            {4, 4, 3, 4, 20, 4, 8},
//            {5, 4, 4, 4, 5, 2, 10},
//            {6, 4, 4, 4, 8, 3, 19},
//            {7, 4, 4, 4, 8, 4, 14},
//            {8, 4, 4, 3, 6, 2, 14},
//            {9, 3, 3, 3, 6, 2, 16},
//            {10, 2, 4, 4, 19, 2, 18},
//            {11, 3, 4, 4, 14, 4, 10},
//            {12, 2, 3, 3, 13, 3, 15},
//            {13, 3, 4, 4, 13, 3, 7},
//            {14, 2, 4, 4, 16, 4, 17},
//            {15, 3, 4, 3, 15, 3, 20},
//            {16, 4, 4, 2, 18, 4, 20},
//            {17, 2, 4, 4, 18, 2, 11},
//            {18, 3, 4, 2, 14, 3, 14},
//            {19, 4, 4, 2, 11, 2, 7},
//            {20, 4, 3, 2, 19, 3, 10},
//            {21, 4, 4, 4, 7, 2, 19},
//            {22, 2, 3, 3, 18, 2, 19},
//            {23, 4, 3, 4, 20, 2, 15},
//            {24, 2, 4, 4, 13, 3, 11},
//            {25, 3, 3, 3, 8, 2, 12},
//            {26, 2, 4, 2, 20, 3, 15},
//            {27, 3, 4, 4, 18, 3, 13},
//            {28, 4, 4, 4, 17, 2, 13},
//            {29, 2, 4, 3, 14, 4, 9},
//            {30, 3, 4, 4, 6, 3, 16},
    };
    int prod = 0;
    for (const auto &blueprint : real_input)
    {
        auto quality = compute_quality_level(blueprint);
        if (prod == 0)
            prod = quality;
        else
            prod *= quality;
        std::cout << blueprint.id_ << ": " << quality << " -> " << prod << std::endl;
    }

    std::vector<Blueprint> test_input{
            {1, 4, 2, 3, 14, 2, 7},
            {2, 2, 3, 3, 8, 3, 12},
    };
    for (const auto &blueprint : test_input)
    {
        auto quality = compute_quality_level(blueprint);
        std::cout << blueprint.id_ << ": " << quality << std::endl;
    }

    return 0;
}


// 16, ?, 29
