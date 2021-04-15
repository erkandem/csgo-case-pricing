import json
from typing import List
from datetime import datetime
import typing_extensions
import copy
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
import pydantic
import requests
from urllib.parse import quote


GENERAL_STATTRACK_PROBABILITY = 0.1
"""
the probability that an item turns out to be stattrack on case opening
Not all items can be stattrack
"""

MILSPEC_GRADE = "Mil-spec"
RESTRICTED_GRADE = "Restricted"
CLASSIFIED_GRADE = "Classified"
COVERT_GRADE = "Covert"
SPECIAL_GRADE = "Special"

GRADE_PROBABILITY = {
    MILSPEC_GRADE: 0.7919,
    RESTRICTED_GRADE: 0.1596,
    CLASSIFIED_GRADE: 0.0366,
    COVERT_GRADE: 0.0091,
    SPECIAL_GRADE: 0.0031,
}
"""
Grade odds

    Blue (Mil-spec, High grade)—79.19 percent
    Purple (Restricted, Remarkable)—15.96 percent
    Pink (Classified, Exotic)—3.66 percent
    Red (Covert, Extraordinary)—0.91 percent
    Yellow (Melee Weapons)—0.31 percent

https://dotesports.com/counter-strike/news/csgo-cases-wear-and-grade-odds
"""
GRADES_LITERALS = list(GRADE_PROBABILITY.keys())
CaseType = List[Dict[str, Any]]


def count_grade(grade: str, case: CaseType) -> int:
    return len([x for x in filter(lambda x: x["grade"] == grade, case)])


def count_grades(case: CaseType):
    return {
        grade: count_grade(grade, case)
        for grade in GRADES_LITERALS
    }


broken_fang_case: List[dict] = [
    dict(name="CZ75-Auto | Vendetta", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="P90 | Cocoa Rampage", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="G3SG1 | Digital Mesh", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="Galil AR | Vandal", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="P250 | Contaminant", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="M249 | Deep Relief", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="MP5-SD | Condition Zero", can_be_stattrack=True, grade=MILSPEC_GRADE),
    dict(name="AWP | Exoskeleton", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="Dual Berettas | Dezastre", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="Nova | Clear Polymer", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="SSG 08 | Parallax", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="UMP-45 | Gold Bismuth", can_be_stattrack=True, grade=RESTRICTED_GRADE),
    dict(name="Five-SeveN | Fairy Tale", can_be_stattrack=True, grade=CLASSIFIED_GRADE),
    dict(name="M4A4 | Cyber Security", can_be_stattrack=True, grade=CLASSIFIED_GRADE),
    dict(name="USP-S | Monster Mashup", can_be_stattrack=True, grade=CLASSIFIED_GRADE),
    dict(name="M4A1-S | Printstream", can_be_stattrack=True, grade=COVERT_GRADE),
    dict(name="Glock-18 | Neo-Noir", can_be_stattrack=True, grade=COVERT_GRADE),
    dict(name="Gloves", can_be_stattrack=False, grade=SPECIAL_GRADE),
]
broken_fang_gloves = [
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

WELL_WORN_EXTERIOR = "Well-Worn"
BATTLE_SCARRED_EXTERIOR = "Battle-Scarred"
FIELD_TESTED_EXTERIOR = "Field-Tested"
MINIMAL_WEAR_EXTERIOR = "Minimal Wear"
FACTORY_NEW_EXTERIOR = "Factory New"


class Exteriors:
    WELL_WORN_EXTERIOR = WELL_WORN_EXTERIOR
    BATTLE_SCARRED_EXTERIOR = BATTLE_SCARRED_EXTERIOR
    FIELD_TESTED_EXTERIOR = FIELD_TESTED_EXTERIOR
    MINIMAL_WEAR_EXTERIOR = MINIMAL_WEAR_EXTERIOR
    FACTORY_NEW_EXTERIOR = FACTORY_NEW_EXTERIOR


EXTERIOR_PROBABILITY = {
    WELL_WORN_EXTERIOR: 0.0792,
    BATTLE_SCARRED_EXTERIOR: 0.093,
    FIELD_TESTED_EXTERIOR: 0.4318,
    MINIMAL_WEAR_EXTERIOR: 0.2468,
    FACTORY_NEW_EXTERIOR: 0.1471,
}
"""
Wear odds

    Well-Worn—7.92 percent
    Battle-Scarred—9.93 percent
    Field-Tested—43.18 percent
    Minimal Wear—24.68 percent
    Factory New—14.71 percent
        10.09 percent of the skins were also StatTrak versions.

applies on gloves and knives as well
https://dotesports.com/counter-strike/news/csgo-cases-wear-and-grade-odds

"""


class ItemPriceApiResultType(typing_extensions.TypedDict):
    """model used around used API JSON response.

    the actual types returned form the API are messed up.
    float an int are returned as str
    false is returned as str
    true as a bool

    See the pydantic model which does the heavy lifting
    """
    success: bool
    average_price: float
    median_price: float
    amount_sold: int
    standard_deviation: float
    lowest_price: float
    highest_price: float
    first_sale_date: int
    time: int
    currency: str


ItemPriceApiResultModel = pydantic.create_model_from_typeddict(ItemPriceApiResultType)


def get_container_adjusted_for_grade(case: CaseType) -> CaseType:
    """adds the ``general_item_probability`` to the each item of the case
    """
    grades_in_case = count_grades(case)
    container_adjusted_for_grade = [
        dict(
            **item,
            general_item_probability=GRADE_PROBABILITY[item["grade"]] / grades_in_case[item["grade"]],
        )
        for item in case
    ]
    return container_adjusted_for_grade


def get_case_info_with_all_combinations(case: CaseType) -> CaseType:
    container_adjusted_for_grade = get_container_adjusted_for_grade(case)
    tolerance = .003  # empiric value, just picked one, to have it and document it
    sum_of_probabilities = sum(map(lambda x: x["general_item_probability"], container_adjusted_for_grade))
    assert (1 - tolerance) < sum_of_probabilities < (1 + tolerance), "Deviation too big"

    # adjust for exterior quality probability
    container_adjusted_for_wear_and_exterior_and_stattrack = []
    for item in container_adjusted_for_grade:
        for exterior in EXTERIOR_PROBABILITY:
            stattrack_cases = [True, False] if item["can_be_stattrack"] else [False]
            stattrack_adjustment = 1.0
            for is_stattrack in stattrack_cases:
                if len(stattrack_cases) == 2 and is_stattrack:
                    stattrack_adjustment = GENERAL_STATTRACK_PROBABILITY
                elif len(stattrack_cases) == 2 and not is_stattrack:
                    stattrack_adjustment = 1.0 - GENERAL_STATTRACK_PROBABILITY
                elif len(stattrack_cases) == 1.0 and not is_stattrack:
                    stattrack_adjustment = 1.0
                else:
                    NotImplementedError("Not expected situation")
                new_item = dict(
                    **item,
                    exterior=exterior,
                    is_stattrack=is_stattrack,
                    probability=(
                        item["general_item_probability"]
                        * EXTERIOR_PROBABILITY[exterior]
                        * stattrack_adjustment
                    ),
                )
                container_adjusted_for_wear_and_exterior_and_stattrack.append(new_item)

    # check again for range of new
    tolerance = .003  # empiric value, just picked one, to have it and document it
    sum_of_probabilities = sum(map(lambda x: x["probability"], container_adjusted_for_wear_and_exterior_and_stattrack))  # noqa: E501
    assert (1 - tolerance) < sum_of_probabilities < (1 + tolerance), "Deviation too big"

    return container_adjusted_for_wear_and_exterior_and_stattrack


def suggest_price(container_price: float, key_price: float, container):
    total = container_price + key_price
    for item in container:
        item["price"] = total / item["general_item_probability"]
    return container


def construct_file_name(item: Dict[str, Any]) -> str:
    stat_track_string = "StatTrak™ " if item["is_stattrack"] else ""
    exterior_string = item["exterior"]
    file_name = f"{stat_track_string}{item['name']} ({exterior_string})"
    return file_name


def construct_steamcommunity_url(item: Dict[str, Any]) -> str:
    base = "https://steamcommunity.com/market/listings/730/"
    file_name = construct_file_name(item)
    return base + file_name


def construct_api_url(item: Dict[str, Any]) -> str:
    base = "https://csgobackpack.net/api/GetItemPrice/"
    file_name = quote(construct_file_name(item))
    url = f"{base}?id={file_name}"
    return url


def cast_item_api_result(response: requests.Response) -> Dict[str, Any]:
    if (
            response.status_code == 200
            # ``false`` is falsely returned as ``"false"`` is returned as a string,
            # whereas ``true`` is correctly returned ``true`` (JS bool type)
            and isinstance(response.json()["success"], bool)
            and response.json()["success"]
    ):
        return ItemPriceApiResultModel(**response.json()).dict()
    else:
        return {}


def get_prices_from_api(case: CaseType) -> CaseType:
    container = get_case_info_with_all_combinations(case)
    new_item_list = []
    for idx, item in enumerate(container):
        new_item = dict(**item)
        new_item["api_url"] = construct_api_url(item)
        new_item["last_api_call_date"] = datetime.now().isoformat()
        response = requests.get(new_item["api_url"])
        new_item["api_status_code"] = response.status_code
        new_item["api_result"] = cast_item_api_result(response)

        print(
            f"{idx + 1} / {len(container)}",
            "url", new_item["api_url"],
            "response.status_code", response.status_code,
            "response.text", response.text
        )
        new_item_list.append(new_item)
    return new_item_list


def calculate_case_price(container: CaseType):
    for idx, item in enumerate(container):
        item["id"] = idx
        if "median_price" in item["api_result"]:
            item["case_price_fragment"] = item["probability"] * float(item["api_result"]["median_price"])
            item["median_price_float"] = float(item["api_result"]["median_price"])
        else:
            item["case_price_fragment"] = None
            item["median_price_float"] = None
    return container


def calc_container_sum(container: CaseType):
    return sum(map(lambda x: x["case_price_fragment"] if x["case_price_fragment"] is not None else 0, container))


def read_container(file_name):
    with open(file_name, "r") as file:
        data: List[Dict[str, str]] = json.loads(file.read())
    return data


def load_and_calc_container_sum(container_data_with_prices_file_name: str):
    data = read_container(container_data_with_prices_file_name)
    return calc_container_sum(data)


def sort_fractal_prices(container_data_with_prices_file_name: str):
    data = read_container(container_data_with_prices_file_name)
    # picking a subset for readability
    subset_keys = ["id", "name", "exterior", "grade", "is_stattrack", "probability", "median_price_float", "case_price_fragment"]  # noqa: E501
    for item in sorted(data, reverse=True, key=lambda x: x["case_price_fragment"])[:100]:
        subset = {key: item[key] for key in subset_keys}
        print(json.dumps(subset))


def get_list_index(*, lst: List[Dict[str, Any]], key: str, value: Any) -> int:
    """get index of dict within a list of similar dicts

    Reference:
        https://stackoverflow.com/a/4391722/10124294
    """
    ind = next((ind for ind, d in enumerate(lst) if d.get(key) == value), None)
    if not isinstance(ind, int):
        raise ValueError("Could not find key value pair %s %s in list" % (key, value))
    return ind


def get_case_incl_special_items(
        case: CaseType,
        special_items: CaseType,
        special_items_name: str = "Gloves"
) -> CaseType:
    """replace the placeholder with the actual special items.

    """
    _case = copy.deepcopy(case)
    _special_items = copy.deepcopy(special_items)
    ind = get_list_index(
        lst=_case,
        key="name",
        value=special_items_name,
    )
    _case.pop(ind)
    _case += _special_items
    return _case




#%%


def suggest_price(row: Dict[str, Any], df: pd.DataFrame) -> Optional[float]:
    new_price = None
    exterior_ranking = {
        0: Exteriors.BATTLE_SCARRED_EXTERIOR,
        1: Exteriors.WELL_WORN_EXTERIOR,
        2: Exteriors.FIELD_TESTED_EXTERIOR,
        3: Exteriors.MINIMAL_WEAR_EXTERIOR,
        4: Exteriors.FACTORY_NEW_EXTERIOR,
    }
    reversed_index = {v: k for k, v in exterior_ranking.items()}
    ind = reversed_index[row["exterior"]]
    while ind != 0:
        if row["can_be_stattrack"]:
            row["is_stattrack"] = not row["is_stattrack"]
            new_price = (
                df.query(
                    "name == @row['name'] "
                    "and is_stattrack == @row['is_stattrack'] "
                    "and exterior == @row['exterior'] "
                ).median_price_float
                .iloc[0]
            )
            if not np.isnan(new_price):
                break
        ind -= 1
        row["exterior"] = exterior_ranking[ind]
        new_price = (
            df.query(
                "name == @row['name'] "
                "and is_stattrack == @row['is_stattrack'] "
                "and exterior == @row['exterior'] "
            ).median_price_float
            .iloc[0]
        )
        if not np.isnan(new_price):
            break
    return new_price


def fix_prices(file_name: str):
    df = pd.read_json(file_name)
    indices = list(df[df['case_price_fragment'].isna()]["name"].index)

    for row_index in indices:
        row = df.loc[row_index].to_dict()
        new_price = suggest_price(row, df)
        if new_price is not None:
            df.loc[row_index, "median_price_float"] = new_price
            df.loc[row_index, "case_price_fragment"] = df.loc[row_index, "median_price_float"] * df.loc[row_index, "probability"]

    df.to_json(file_name, orient='records', indent=2)



def main():
    timestamp = int(datetime.now().timestamp())

    case = get_case_incl_special_items(
        broken_fang_case,
        broken_fang_gloves,
    )
    case = case[::-1]  # reverse, gloves are at end, let's start with them
    container_data = get_prices_from_api(case)
    with open(f"{timestamp}_container_data.json", "w") as file:
        file.write(json.dumps(container_data, indent=2))

    container_data = calculate_case_price(container_data)
    with open(f"{timestamp}_container_data_with_prices.json", "w") as file:
        file.write(json.dumps(container_data, indent=2))

    price = calc_container_sum(container_data)
    print("calc_container_sum", price)
    return price


if __name__ == '__main__':
    main()
