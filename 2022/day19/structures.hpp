/**
 * Created by mark on 21/12/22.
 */

#ifndef STRUCTURES_HPP
#define STRUCTURES_HPP

#include <algorithm>

enum class RobotOption {
    ore,
    clay,
    obsidian,
    geode,
    none
};

class Blueprint {
public:
    int id_{};
    int rb_ore_cost_ore{};
    int rb_clay_cost_ore{};
    int rb_obsidian_cost_ore{};
    int rb_obsidian_cost_clay{};
    int rb_geode_cost_ore{};
    int rb_geode_cost_obsidian{};
    int max_ore_cost{};
    Blueprint(int id,
              int rb_ore_cost_ore,
              int rb_clay_cost_ore,
              int rb_obsidian_cost_ore,
              int rb_obsidian_cost_clay,
              int rb_geode_cost_ore,
              int rb_geode_cost_obsidian) :
        id_(id),
        rb_ore_cost_ore(rb_ore_cost_ore),
        rb_clay_cost_ore(rb_clay_cost_ore),
        rb_obsidian_cost_ore(rb_obsidian_cost_ore),
        rb_obsidian_cost_clay(rb_obsidian_cost_clay),
        rb_geode_cost_ore(rb_geode_cost_ore),
        rb_geode_cost_obsidian(rb_geode_cost_obsidian)
    {
        max_ore_cost = std::max(rb_ore_cost_ore, rb_clay_cost_ore);
        max_ore_cost = std::max(max_ore_cost, rb_obsidian_cost_ore);
        max_ore_cost = std::max(max_ore_cost, rb_geode_cost_ore);
    }
};

class GameState {
public:
    int time_remaining{32};
    int rb_ore{1};
    int rb_clay{};
    int rb_obsidian{};
    int rb_geode{};
    int ore{1};
    int clay{};
    int obsidian{};
    int geode{};
    int best_score{};
    int new_rb_ore{};
    int new_rb_clay{};
    int new_rb_obsidian{};
    int new_rb_geode{};

    void collect_resources()
    {
        ore += rb_ore;
        clay += rb_clay;
        obsidian += rb_obsidian;
        geode += rb_geode;
        rb_ore += new_rb_ore;
        rb_clay += new_rb_clay;
        rb_obsidian += new_rb_obsidian;
        rb_geode += new_rb_geode;
        new_rb_ore = 0;
        new_rb_clay = 0;
        new_rb_obsidian = 0;
        new_rb_geode = 0;
    }

    void build_ore_robot(const Blueprint &blueprint)
    {
        ore -= blueprint.rb_ore_cost_ore;
        new_rb_ore += 1;
    }

    void build_clay_robot(const Blueprint &blueprint)
    {
        ore -= blueprint.rb_clay_cost_ore;
        new_rb_clay += 1;
    }

    void build_obsidian_robot(const Blueprint &blueprint)
    {
        ore -= blueprint.rb_obsidian_cost_ore;
        clay -= blueprint.rb_obsidian_cost_clay;
        new_rb_obsidian += 1;
    }

    void build_geode_robot(const Blueprint &blueprint)
    {
        ore -= blueprint.rb_geode_cost_ore;
        obsidian -= blueprint.rb_geode_cost_obsidian;
        new_rb_geode += 1;
    }

    void try_build_robot(RobotOption option, const Blueprint &blueprint)
    {
        switch (option) {
            case RobotOption::ore:
                build_ore_robot(blueprint);
                break;
            case RobotOption::clay:
                build_clay_robot(blueprint);
                break;
            case RobotOption::obsidian:
                build_obsidian_robot(blueprint);
                break;
            case RobotOption::geode:
                build_geode_robot(blueprint);
                break;
            default:
            case RobotOption::none:
                break;
        }
    }
};

#endif // STRUCTURES_HPP
