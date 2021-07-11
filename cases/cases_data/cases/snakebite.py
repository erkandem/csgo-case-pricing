from typing import (
    Dict,
    List,
    Union,
)

from cases.cases_data.constants import (
    CLASSIFIED_GRADE,
    COVERT_GRADE,
    MILSPEC_GRADE,
    RESTRICTED_GRADE,
    SPECIAL_GRADE,
)

REGULAR_ITEMS: List[Dict[str, Union[str, bool]]] = [
    dict(name="SG 553 | Heavy Metal", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="Glock-18 | Clear Polymer", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="M249 | O.S.I.P.R.", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="CZ75-Auto | Circaetus", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="UMP-45 | Oscillator", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="R8 Revolver | Junk Yard", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="Nova | Windblown", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="P250 | Cyber Shell", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="Negev | dev_texture", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="MAC-10 | Button Masher", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="Desert Eagle | Trigger Discipline", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="AK-47 | Slate", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="MP9 | Food Chain", can_be_stattrack=True, grade=CLASSIFIED_GRADE),
    dict(name="XM1014 | XOXO", can_be_stattrack=True, grade=CLASSIFIED_GRADE),
    dict(name="Galil AR | Chromatic Aberration", can_be_stattrack=True, grade=CLASSIFIED_GRADE),
    dict(name="USP-S | The Traitor", can_be_stattrack=True, grade=COVERT_GRADE),
    dict(name="M4A4 | In Living Color", can_be_stattrack=True, grade=COVERT_GRADE),
]

SPECIAL_ITEMS: List[Dict[str, Union[str, bool]]] = [
    dict(name="★ Broken Fang Gloves | Yellow-banded", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Broken Fang Gloves | Needle Point", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Broken Fang Gloves | Unhinged", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Driver Gloves | Snow Leopard", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Driver Gloves | Black Tie", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Driver Gloves | Queen Jaguar", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Driver Gloves | Rezan the Red", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Hand Wraps | CAUTION!", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Hand Wraps | Desert Shamagh", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Hand Wraps | Giraffe", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Hand Wraps | Constrictor", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Moto Gloves | Finish Line", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Moto Gloves | Smoke Out", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Moto Gloves | Blood Pressure", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Moto Gloves | 3rd Commando Company", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Specialist Gloves | Lt. Commander", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Specialist Gloves | Tiger Strike", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Specialist Gloves | Field Agent", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Specialist Gloves | Marble Fade", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Sport Gloves | Slingshot", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Sport Gloves | Scarlet Shamagh", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Sport Gloves | Big Game", can_be_stattrack=False, grade=SPECIAL_GRADE),
    dict(name="★ Sport Gloves | Nocts", can_be_stattrack=False, grade=SPECIAL_GRADE),
]

CASE_ITEMS = REGULAR_ITEMS + SPECIAL_ITEMS
CASE_NAME = "snakebite_case"
