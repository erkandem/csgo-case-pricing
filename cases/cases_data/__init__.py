import importlib
import pathlib
import sys
from typing import (
    Any,
    Dict,
    List,
)

api = "https://csgobackpack.net/api/"
"""
API endpoint used for single item price lookups
"""


case_urls = [
      "https://csgostash.com/case/277/Shattered-Web-Case",
      "https://csgostash.com/case/293/CS20-Case",
      "https://csgostash.com/case/274/Prisma-Case",
      "https://csgostash.com/case/38/Chroma-Case",
      "https://csgostash.com/case/48/Chroma-2-Case",
      "https://csgostash.com/case/141/Chroma-3-Case",
      "https://csgostash.com/case/238/Clutch-Case",
      "https://csgostash.com/case/1/CS:GO-Weapon-Case",
      "https://csgostash.com/case/4/CS:GO-Weapon-Case-2",
      "https://csgostash.com/case/10/CS:GO-Weapon-Case-3",
      "https://csgostash.com/case/259/Danger-Zone-Case",
      "https://csgostash.com/case/2/eSports-2013-Case",
      "https://csgostash.com/case/5/eSports-2013-Winter-Case",
      "https://csgostash.com/case/19/eSports-2014-Summer-Case",
      "https://csgostash.com/case/50/Falchion-Case",
      "https://csgostash.com/case/144/Gamma-Case",
      "https://csgostash.com/case/172/Gamma-2-Case",
      "https://csgostash.com/case/179/Glove-Case",
      "https://csgostash.com/case/244/Horizon-Case",
      "https://csgostash.com/case/17/Huntsman-Weapon-Case",
      "https://csgostash.com/case/3/Operation-Bravo-Case",
      "https://csgostash.com/case/18/Operation-Breakout-Weapon-Case",
      "https://csgostash.com/case/208/Operation-Hydra-Case",
      "https://csgostash.com/case/11/Operation-Phoenix-Weapon-Case",
      "https://csgostash.com/case/29/Operation-Vanguard-Weapon-Case",
      "https://csgostash.com/case/112/Operation-Wildfire-Case",
      "https://csgostash.com/case/111/Revolver-Case",
      "https://csgostash.com/case/80/Shadow-Case",
      "https://csgostash.com/case/207/Spectrum-Case",
      "https://csgostash.com/case/220/Spectrum-2-Case",
      "https://csgostash.com/case/7/Winter-Offensive-Weapon-Case",
      "https://csgostash.com/case/308/Operation-Broken-Fang-Case",
      "https://csgostash.com/case/307/Fracture-Case",
      "https://csgostash.com/case/303/Prisma-2-Case"
]
"""
reference pages to get an overview of the prices in the cases
"""

CaseType = List[Dict[str, Any]]
DEFAULT_CASE_NAME_VARIABLE = 'CASE_NAME'
DEFAULT_CASE_ITEMS_VARIABLE = 'CASE_ITEMS'
DEFAULT_CASE_ITEMS_PACKAGE_NAME = 'cases'


def init_cases() -> Dict[str, CaseType]:
    """ Initializes case data from modules.

    imports all available data from modules in package
    and creates a single importable dict object.

    key: case name
    value: dict containing basic case contents

    """
    all_cases = {}
    folder = pathlib.Path(__file__).parent / DEFAULT_CASE_ITEMS_PACKAGE_NAME
    sys.path.append(str(folder))
    case_modules = list(
        p for p in folder.iterdir()
        if p.is_file()  # discard packages, e.g. __pycache__
        and '__' not in p.stem  # discard __init__ and similar files
    )
    for case_module in case_modules:
        module = importlib.import_module(case_module.stem)
        all_cases[getattr(module, DEFAULT_CASE_NAME_VARIABLE)] = getattr(module, DEFAULT_CASE_ITEMS_VARIABLE)
    return all_cases


ALL_CASES: Dict[str, CaseType] = init_cases()
