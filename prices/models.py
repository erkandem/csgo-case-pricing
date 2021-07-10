from decimal import Decimal
from typing import (
    Any,
    Dict,
)
from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import (
    F,
    Sum,
)
from django_extensions.db.models import TimeStampedModel
import pydantic
import requests

from cases.cases_data import CaseType
from cases.cases_data.constants import (
    EXTERIOR_PROBABILITY,
    GENERAL_STATTRACK_PROBABILITY,
    GRADE_PROBABILITY,
)
from cases.models import (
    Case,
    CaseItem,
    construct_file_name,
)
from utils import count_grades

from .choices import CURRENCY_CHOICES


class ItemPriceApiResultPydantic(pydantic.BaseModel):
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


class CsgoBackPackApiUrl(TimeStampedModel):
    api_url = models.URLField(
        blank=True,
        null=True,
    )
    case_item = models.ForeignKey(
        CaseItem,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def save(self, **kwargs):
        """api_url.url = construct_api_url({
            'name': case_item.name,
            'exterior': case_item.exterior,
            'is_stattrack': case_item.is_stattrack,
        })
        api_url.
        """
        if not self.case_item:
            raise ValidationError('At least case_item must be set before saving')
        if not self.api_url:
            self.api_url = construct_api_url({
                'name': self.case_item.name,
                'exterior': self.case_item.exterior,
                'is_stattrack': self.case_item.is_stattrack,
            })
        super().save()


class CalculationBatch(TimeStampedModel):
    uuid = models.UUIDField(
        blank=True,
        null=True,
    )
    case = models.ForeignKey(
        Case,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'uuid',
                ],
                name='unique batch uuid'
            ),
        ]


class CaseItemPriceApiResult(TimeStampedModel):

    batch = models.ForeignKey(
        CalculationBatch,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    api_url = models.ForeignKey(
        CsgoBackPackApiUrl,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    case_item = models.ForeignKey(
        CaseItem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    success = models.BooleanField()
    status_code = models.IntegerField(
        blank=True,
        null=True,
    )
    average_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    median_price = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        blank=True,
    )
    amount_sold = models.IntegerField(
        null=True,
        blank=True,
    )
    standard_deviation = models.FloatField(
        null=True,
        blank=True
    )
    lowest_price = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        blank=True,
    )
    highest_price = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        blank=True,
    )
    first_sale_date = models.IntegerField(
        null=True,
        blank=True,
    )
    time = models.IntegerField(
        null=True,
        blank=True,
    )
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        null=True,
        blank=True,
    )
    is_interpolated = models.BooleanField(
        default=False,
    )


class CaseItemPriceDetails(TimeStampedModel):
    batch = models.ForeignKey(
        CalculationBatch,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    case_item = models.ForeignKey(
        CaseItem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    api_result = models.OneToOneField(
        CaseItemPriceApiResult,
        related_name='details',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        null=True,
        blank=True,
    )
    case_price_fragment = models.DecimalField(
        max_digits=40,
        decimal_places=20,
        null=True,
        blank=True,
    )


class CasePrice(TimeStampedModel):
    batch = models.ForeignKey(
        CalculationBatch,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    case = models.ForeignKey(
        Case,
        related_name='case_price',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    case_price = models.DecimalField(
        max_digits=40,
        decimal_places=20,
        null=True,
        blank=True,
    )
    case_key_price = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        blank=True,
        default=Decimal(2.50)
    )
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "%.3f - %s" % (self.case_price, getattr(self.case, 'name', 'n/a'),)


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
        return ItemPriceApiResultPydantic(**response.json()).dict()
    else:
        return {
            "success": False,
        }


def get_container_adjusted_for_grade(case: CaseType) -> CaseType:
    """adds the ``general_item_probability`` to the each item of the case

    ``general_item_probability`` represents a first draw in which we estimate the
     - the grade and
     - the the item (with that grade) drops.

    If a case contains e.g. Mil-spec category and that category  has 10 items,
    the probability (phi) that the item X will drop is
    - the probability that we will get a Mil-spec drop (e.g. 0.7919 according to sources)
    - divided by the number of Mil-spec items in that case (10)
    phi(X) = 10 * 0.7919 = 0.07919

    This is unadjusted to the exterior quality.
    In a second "draw" we will estimate the exterior quality.
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


def get_case_case_standard_deviation() -> Dict[str, float]:
    """Calculate the standard deviation of the case price.

    Helpful to get a better range for the estimated case price

    """
    batch = CalculationBatch.objects.all().order_by('-id').first()
    std_case = CaseItemPriceApiResult.objects.filter(
        batch__uuid=batch.uuid,
    ).aggregate(
        case_standard_deviation=(
                Sum(
                    F('standard_deviation')
                    * F('case_item__probability')
                )
                / CaseItemPriceApiResult.objects.filter(
                    batch__uuid=batch.uuid,
                    standard_deviation__isnull=False,
                    case_item__probability__isnull=False,
                ).count()
        )
    )
    return std_case


def get_case_info_with_all_combinations(
        case: CaseType,
) -> CaseType:
    """create a a data structure which accounts for all possible combinations"""
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


def suggest_naive_price(
        container_price: float,
        key_price: float,
        container: CaseType,
):
    """Suggest a price based on drop probability

    Args:
        container_price:
        key_price: price of the key to open a container
        container: list of dict representing the items of a container

    Returns:

    """
    total = container_price + key_price
    for item in container:
        item["price"] = total / item["general_item_probability"]
    return container
