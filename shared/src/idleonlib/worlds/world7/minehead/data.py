from __future__ import annotations

"""Minehead static data extracted from the decompile.

This module is intentionally "dumb": it contains arrays and small
helpers with no dependence on profile parsing.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MineheadUpgradeDef:
    """Definition for a Minehead upgrade.

    Attributes:
        key: Upgrade key from the decompile (e.g. "Base_Damage_I").
        max_level: Max level from MineheadUPG[*][1]. 9999 means "no cap".
        cost_multiplier: Per-level exponential base MineheadUPG[*][2].
        qty_multiplier: UpgradeQTY multiplier MineheadUPG[*][3].
        raw_tokens: The full original row token list.
    """

    key: str
    max_level: int
    cost_multiplier: float
    qty_multiplier: float
    raw_tokens: tuple[str, ...]


def _row(tokens: list[str]) -> MineheadUpgradeDef:
    return MineheadUpgradeDef(
        key=tokens[0],
        max_level=int(float(tokens[1])),
        cost_multiplier=float(tokens[2]),
        qty_multiplier=float(tokens[3]),
        raw_tokens=tuple(tokens),
    )


# Extracted from `ob.MineheadUPG` in idleon1.06.txt.
MINEHEAD_UPGRADES: tuple[MineheadUpgradeDef, ...] = (
    _row("Base_Damage_I 9999 1.10 1 0 Boosts_your_base_damage_in_the_classic_game_of_Depth_Charge_by_+{".split(" ")),
    _row("Numbahs 17 6 1 0 Increase_the_max_possible_Tile_Number_you_can_find_to_$!_These_are_a_MULTI_for_damage!".split(" ")),
    _row("Grid_Expansion 16 7.5 1 0 $".split(" ")),
    _row("Bettah_Numbahs 9999 1.15 10 0 Boosts_your_odds_of_getting_bigger_Tile_Numbers_by_}x".split(" ")),
    _row("Mega_Damage_I 9999 1.12 5 0 Permanently_increases_all_damage_you_deal_in_the_classic_game_of_Depth_Charge_by_+{%".split(" ")),
    _row("Miney_Farmey_I 9999 1.10 10 0 Boosts_the_amount_of_Mine_Currency_you_generate_per_hour_by_+{%".split(" ")),
    _row("Extra_Lives 7 250 1 0 Start_each_game_with_+1_extra_life!".split(" ")),
    _row("Base_Damage_II 9999 1.10 3 0 Boosts_your_base_damage_in_the_classic_game_of_Depth_Charge_by_+{".split(" ")),
    _row("Golden_Tiles 16 8 1 0 Click_on_up_to_{_Golden_Tiles_per_game,_which_are_guaranteed_to_be_safe_from_Depth_Charges!".split(" ")),
    _row("Big_Hit_Combos 9999 1.30 1 0 Increases_damage_by_+{%_for_every_tile_revealed,_resetting_at_the_start_of_each_turn.".split(" ")),
    _row("Boom_Blocker 2 1000000000.0 1 0 Start_each_game_of_Depth_Charge_with_+{_Blocks._Depth_Charges_HATE_this_feature!".split(" ")),
    _row("Final_Round_Fury 9999 1.30 2 0 Your_damage_is_}x_higher_when_down_to_your_last_life!".split(" ")),
    _row("Multiplier_Madness 10 35 1 0 You_can_now_find_Multiplier_Tiles,_up_to_$!_These_multiply_damage_for_the_current_turn.".split(" ")),
    _row("Moar_Moar_Multi's 9999 1.15 6 0 Boosts_your_odds_of_getting_bigger_Multiplier_Tiles_by_}x".split(" ")),
    _row("Triple_Crown_Hunter 250 1.16 1 0 Tiles_can_now_have_a_Blue_Crown_background,_reveal_3_to_multiply_current_damage_by_$".split(" ")),
    _row("Crown_Craze 100 1.40 1 0 Boosts_your_odds_of_revealing_Blue_Crown_backgrounds_by_}x".split(" ")),
    _row("Legal_Cheating_Button 20 6 1 0 Reveals_a_Depth_Charges,_has_{_uses,_but_has_a_25%_chance_to_break_until_next_turn!".split(" ")),
    _row("Awesome_Additives 10 35 1 0 You_can_now_find_Additive_Tiles,_up_to_$!_These_boost_your_damage_for_the_ENTIRE_game!".split(" ")),
    _row("Always_Adding 9999 1.15 5 0 Boosts_your_odds_of_revealing_bigger_Additive_Tiles_by_}x".split(" ")),
    _row("Clutch_Overtime_Block 1 100000 1 0 When_down_to_your_last_life,_get_+{_Block!_Depth_Charges_STILL_HATE_this_feature!!!".split(" ")),
    _row("Classic_Flags 8 500 1 0 You_can_place_down_{_Flags,_which_show_the_amount_of_surrounding_Depth_Charges!".split(" ")),
    _row("Mega_Damage_II 9999 1.10 20 0 Permanently_increases_all_damage_you_deal_in_the_classic_game_of_Depth_Charge_by_+{%".split(" ")),
    _row("Miney_Farmey_II 9999 1.15 15 0 Boosts_the_amount_of_Mine_Currency_you_generate_per_hour_by_+{%".split(" ")),
    _row("Jackpot_Time 9999 1.14 1 0 Boosts_your_odds_of_finding_Jackpot_tiles!_You've_currently_got_a_1_in_$_chance!".split(" ")),
    _row("Record_Breaking_Jackpots 6 1000 1 0 Jackpot_Tiles_now_reveal_$_tiles_when_found!".split(" ")),
    _row("Base_Damage_III 9999 1.10 12 0 Boosts_your_base_damage_in_the_classic_game_of_Depth_Charge_by_+{".split(" ")),
    _row("El'_Cheapo_Upgrado 9999 1.15 1 0 All_upgrades_are_$%_cheaper,_now_and_forever!".split(" ")),
    _row("Mega_Damage_III 9999 1.12 50 0 Permanently_increases_all_damage_you_deal_in_the_classic_game_of_Depth_Charge_by_+{%".split(" ")),
    _row("Miney_Damagey_Synergy 9999 1.25 2 0 $".split(" ")),
    _row("Rift_Guy's_Upgrade 0 9999999 1 0 Uh,_yea._This_is_MY_upgrade,_NOT_yours._I_maxed_it_out_because_I'm_me,_duh.".split(" ")),
)


# Extracted from CustomLists.Research[9] (idleon1.06.txt line ~294710).
GRID_SIZES: tuple[tuple[int, int], ...] = tuple(
    (int(a), int(b))
    for a, b in (
        s.split(",")
        for s in (
            "3,3 4,3 5,3 4,4 6,3 5,4 6,4 7,4 6,5 7,5 8,5 9,5 10,5 9,6 10,6 11,6 12,6".split(
                " "
            )
        )
    )
)


def grid_dims(grid_expansion_level: int) -> tuple[int, int]:
    """Return (rows, cols) for a given Grid Expansion level."""
    if grid_expansion_level < 0:
        return GRID_SIZES[0]
    if grid_expansion_level >= len(GRID_SIZES):
        return GRID_SIZES[-1]
    return GRID_SIZES[grid_expansion_level]
