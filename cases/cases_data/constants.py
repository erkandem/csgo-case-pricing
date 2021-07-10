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


class Grades:
    """class to organize possible grades
    """
    MILSPEC_GRADE = MILSPEC_GRADE
    RESTRICTED_GRADE = RESTRICTED_GRADE
    CLASSIFIED_GRADE = CLASSIFIED_GRADE
    COVERT_GRADE = COVERT_GRADE
    SPECIAL_GRADE = SPECIAL_GRADE


GRADE_PROBABILITY = {
    Grades.MILSPEC_GRADE: 0.7919,
    Grades.RESTRICTED_GRADE: 0.1596,
    Grades.CLASSIFIED_GRADE: 0.0366,
    Grades.COVERT_GRADE: 0.0091,
    Grades.SPECIAL_GRADE: 0.0031,
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
GRADE_CHOICES = tuple((value, value,) for value in GRADES_LITERALS)

WELL_WORN_EXTERIOR = "Well-Worn"
BATTLE_SCARRED_EXTERIOR = "Battle-Scarred"
FIELD_TESTED_EXTERIOR = "Field-Tested"
MINIMAL_WEAR_EXTERIOR = "Minimal Wear"
FACTORY_NEW_EXTERIOR = "Factory New"


class Exteriors:
    """class to organise possible exteriors
    """
    WELL_WORN_EXTERIOR = WELL_WORN_EXTERIOR
    BATTLE_SCARRED_EXTERIOR = BATTLE_SCARRED_EXTERIOR
    FIELD_TESTED_EXTERIOR = FIELD_TESTED_EXTERIOR
    MINIMAL_WEAR_EXTERIOR = MINIMAL_WEAR_EXTERIOR
    FACTORY_NEW_EXTERIOR = FACTORY_NEW_EXTERIOR


EXTERIOR_PROBABILITY = {
    Exteriors.WELL_WORN_EXTERIOR: 0.0792,
    Exteriors.BATTLE_SCARRED_EXTERIOR: 0.093,
    Exteriors.FIELD_TESTED_EXTERIOR: 0.4318,
    Exteriors.MINIMAL_WEAR_EXTERIOR: 0.2468,
    Exteriors.FACTORY_NEW_EXTERIOR: 0.1471,
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
EXTERIOR_LITERALS = list(EXTERIOR_PROBABILITY.keys())
EXTERIOR_CHOICES = tuple((value, value,) for value in EXTERIOR_LITERALS)
