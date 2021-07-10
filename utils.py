from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from cases.cases_data import CaseType
from cases.cases_data.constants import GRADES_LITERALS


def count_grade(grade: str, case: CaseType) -> int:
    return len([x for x in filter(lambda x: x["grade"] == grade, case)])


def count_grades(case: CaseType):
    return {
        grade: count_grade(grade, case)
        for grade in GRADES_LITERALS
    }


def get_list_index(*, lst: List[Dict[str, Any]], key: str, value: Any) -> Optional[int]:
    """get index of dict within a list of similar dicts

    Reference:
        https://stackoverflow.com/a/4391722/10124294
    """
    ind = next((ind for ind, d in enumerate(lst) if d.get(key) == value), None)
    return ind
