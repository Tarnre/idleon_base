from __future__ import annotations

import json

import pytest

from idleonlib.profiles.parsers.errors import ProfileParseError
from idleonlib.profiles.parsers.world7.world7 import parse_world7_profile_data


@pytest.mark.parametrize(
    ("raw", "strict"),
    [
        pytest.param({}, True, id="missing_research_strict"),
        pytest.param({}, False, id="missing_research_nonstrict"),
    ],
)
def test_world7_missing_research_returns_empty(raw: dict, strict: bool) -> None:
    world7 = parse_world7_profile_data(raw, strict=strict)
    assert world7.research.raw == []
    assert world7.minehead.core.opponent_index == 0
    assert world7.minehead.upgrades.level(0) == 0


@pytest.mark.parametrize(
    ("research_value", "strict", "expects_error"),
    [
        pytest.param("not-json", True, True, id="invalid_json_strict"),
        pytest.param("not-json", False, False, id="invalid_json_nonstrict"),
        pytest.param(json.dumps({"a": 1}), True, True, id="json_not_list_strict"),
        pytest.param(json.dumps({"a": 1}), False, False, id="json_not_list_nonstrict"),
    ],
)
def test_world7_research_decode_behavior(
    research_value: str,
    strict: bool,
    expects_error: bool,
) -> None:
    raw = {"Research": research_value}
    if expects_error:
        with pytest.raises(ProfileParseError):
            parse_world7_profile_data(raw, strict=strict)
        return

    world7 = parse_world7_profile_data(raw, strict=strict)
    assert world7.research.raw == []
    assert world7.minehead.core.opponent_index == 0
    assert world7.minehead.upgrades.level(0) == 0


def test_world7_research_sublists_are_preserved() -> None:
    research_blob = [
        ["x"],
        [1, 2, 3],
        "bad-sublist",
        [],
    ]
    raw = {"Research": json.dumps(research_blob)}
    world7 = parse_world7_profile_data(raw, strict=False)

    # Non-lists become [] in non-strict mode (per parser).
    assert world7.research.raw[0] == ["x"]
    assert world7.research.raw[1] == [1, 2, 3]
    assert world7.research.raw[2] == []
    assert world7.research.raw[3] == []


def test_world7_minehead_core_is_mapped_from_research_7() -> None:
    # Research[7] should map into MineheadCore (20 slots with padding/truncation)
    blob = [[] for _ in range(9)]
    blob[7] = [8, 1, 2, 3, 4, 123.5]  # opponent_index=8, bonus_unlock=4, currency=123.5
    blob[8] = [7] * 50

    raw = {"Research": json.dumps(blob)}
    world7 = parse_world7_profile_data(raw, strict=True)

    assert world7.minehead.core.opponent_index == 8
    assert world7.minehead.core.bonus_unlock_level == 4
    assert world7.minehead.core.currency == pytest.approx(123.5)

    # Known unknown placeholders remain accessible and stable
    assert world7.minehead.core.unk_01 == pytest.approx(1.0)
    assert world7.minehead.core.unk_02 == pytest.approx(2.0)
    assert world7.minehead.core.unk_03 == pytest.approx(3.0)

    # Padding behavior (missing indices => 0)
    assert world7.minehead.core.unk_19 == pytest.approx(0.0)


def test_world7_minehead_upgrades_are_mapped_from_research_8() -> None:
    blob = [[] for _ in range(9)]
    blob[7] = [0] * 20
    blob[8] = list(range(50))

    raw = {"Research": json.dumps(blob)}
    world7 = parse_world7_profile_data(raw, strict=True)

    assert world7.minehead.upgrades.level(0) == 0
    assert world7.minehead.upgrades.level(14) == 14
    assert world7.minehead.upgrades.level(49) == 49

    # Named placeholder fields exist and match levels
    assert world7.minehead.upgrades.upg_14 == 14
    assert world7.minehead.upgrades.upg_49 == 49

    # Out of range => 0
    assert world7.minehead.upgrades.level(-1) == 0
    assert world7.minehead.upgrades.level(50) == 0

def test_world7_minehead_upgrade_semantic_names_map_to_indices() -> None:
    blob = [[] for _ in range(9)]
    blob[7] = [0] * 20
    blob[8] = [0] * 50
    blob[8][1] = 111   # numbahs
    blob[8][3] = 333   # bettah_numbahs
    blob[8][14] = 1414  # triple_crown_hunter

    raw = {"Research": json.dumps(blob)}
    world7 = parse_world7_profile_data(raw, strict=True)

    upg = world7.minehead.upgrades
    assert upg.numbahs == 111
    assert upg.bettah_numbahs == 333
    assert upg.triple_crown_hunter == 1414

    assert upg.upgrade_name(1) == "numbahs"
    assert upg.upgrade_name(14) == "triple_crown_hunter"
    assert upg.upgrade_name(49) == "upg_49"