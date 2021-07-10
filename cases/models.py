from typing import (
    Any,
    Dict,
)

from django.db import models
from django_extensions.db.models import TimeStampedModel

from cases.cases_data.constants import (
    EXTERIOR_CHOICES,
    GRADE_CHOICES,
)


class Case(TimeStampedModel):
    name = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    overview_url = models.URLField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return "%s" % self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                ],
                name='unique case name'
            ),
        ]


class CaseItem(TimeStampedModel):
    name = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    case = models.ManyToManyField(
        Case,
        related_name='case_item',
    )
    can_be_stattrack = models.BooleanField(
        default=False,
    )
    grade = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        blank=True,
        null=True,
    )
    exterior = models.CharField(
        max_length=20,
        choices=EXTERIOR_CHOICES,
        blank=True,
        null=True,
    )

    is_stattrack = models.BooleanField(
        default=False,
    )
    general_item_probability = models.FloatField(
        default=0,
        null=True,
        blank=True,
    )
    probability = models.FloatField(
        default=0,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return "%s | %s | %s | %s" % (self.name, self.grade, str(self.is_stattrack)[0], self.exterior)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'grade',
                    'name',
                    'is_stattrack',
                    'exterior',
                ],
                name='unique case item'
            ),
        ]


def construct_file_name(item: Dict[str, Any]) -> str:
    """create the name string representing an item on the the steam community market page

    Args:
        item: has to have ``is_stattrack``, ``exterior`` and ``name`` fields
    """
    stat_track_string = "StatTrak™ " if item["is_stattrack"] else ""
    exterior_string = item["exterior"]
    file_name = f"{stat_track_string}{item['name']} ({exterior_string})"
    return file_name


def construct_steamcommunity_url(item: Dict[str, Any]) -> str:
    """create the URL to the steam community market for a given ``item``

    Args:
        item:

    Returns: full URL to an items page

    """
    base = "https://steamcommunity.com/market/listings/730/"
    file_name = construct_file_name(item)
    return base + file_name
