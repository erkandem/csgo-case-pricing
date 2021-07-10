import json
import logging
from typing import Optional
from uuid import (
    UUID,
    uuid4,
)

from django.db import transaction
from django.db.models import Sum
import requests

from cases.cases_data.constants import Exteriors
from cases.models import (
    Case,
    CaseItem,
)
from prices.models import (
    CalculationBatch,
    CaseItemPriceApiResult,
    CaseItemPriceDetails,
    CasePrice,
    CsgoBackPackApiUrl,
    cast_item_api_result,
)

from .choices import CURRENCY_USD

logger = logging.getLogger(__name__)


def calculate_case_price_fragment(
        probability: Optional[float],
        median_price: Optional[float]
) -> Optional[float]:
    case_price_fragment = (
        probability * median_price
        if median_price and probability
        else None
    )
    return case_price_fragment


def create_case_item_price_details(
        batch_uuid: UUID,
        api_result: CaseItemPriceApiResult,
):
    case_price_fragment = calculate_case_price_fragment(
        api_result.case_item.probability,
        float(api_result.median_price) if api_result.median_price else None
    )
    CaseItemPriceDetails.objects.create(
        case_item=api_result.case_item,
        batch=CalculationBatch.objects.get(uuid=batch_uuid),
        currency=api_result.currency,
        api_result=api_result,
        case_price_fragment=case_price_fragment,
    )


def get_prices_from_api(case_name: str):
    case_items = CaseItem.objects.filter(
        case__name=case_name,
    )
    case_items_count = case_items.count()
    if not case_items_count:
        raise ValueError('check case_name. No items found.')
    calculation_batch = CalculationBatch.objects.create(
        uuid=uuid4(),
        case=Case.objects.get(name=case_name)
    )
    print(
        "starting queries for %s with batch id %s" % (
            case_items_count,
            calculation_batch.uuid,
        )
    )
    for idx, case_item in enumerate(case_items):
        print("[%.3d / %.3d] " % (
                idx + 1,
                case_items_count
            )
        )
        api_url, new = CsgoBackPackApiUrl.objects.get_or_create(
            case_item=case_item,
        )
        response = requests.get(api_url.api_url)
        result_dict = cast_item_api_result(response)
        print(json.dumps(result_dict))
        if result_dict["success"]:
            case_item_price_api_result = CaseItemPriceApiResult.objects.create(
                api_url=api_url,
                batch=calculation_batch,
                status_code=response.status_code,
                case_item=case_item,
                success=result_dict.pop("success"),
                average_price=result_dict["average_price"],
                median_price=result_dict["median_price"],
                amount_sold=result_dict["amount_sold"],
                standard_deviation=result_dict["standard_deviation"],
                lowest_price=result_dict["lowest_price"],
                highest_price=result_dict["highest_price"],
                first_sale_date=result_dict["first_sale_date"],
                time=result_dict["time"],
                currency=result_dict["currency"],
            )
        else:
            case_item_price_api_result = CaseItemPriceApiResult.objects.create(
                api_url=api_url,
                batch=calculation_batch,
                status_code=response.status_code,
                case_item=case_item,
                success=result_dict.pop("success"),
            )

        create_case_item_price_details(
            calculation_batch.uuid,
            case_item_price_api_result
        )
    create_or_update_case_price(
        calculation_batch.uuid,
        case_name,
    )
    print(
        "finished queries for %s with batch id %s" % (
            case_items_count,
            calculation_batch.uuid,
        )
    )


def get_case_price(
        batch_uuid: UUID,
):
    result = CaseItemPriceDetails.objects.filter(
        batch__uuid=batch_uuid
    ).aggregate(
        Sum("case_price_fragment"),
    )
    return result


def create_or_update_case_price(
        batch_uuid: UUID,
        case_name: str,
):
    result = get_case_price(batch_uuid)
    price_object, new = CasePrice.objects.get_or_create(
        case=Case.objects.get(name=case_name),
        currency=CURRENCY_USD,
        batch=CalculationBatch.objects.get(uuid=batch_uuid),
    )
    price_object.case_price = result["case_price_fragment__sum"]
    price_object.save(update_fields=["case_price"])


def fix_db_prices(
        batch_uuid: UUID,
        case_name: str
):
    with transaction.atomic():
        result = CaseItemPriceDetails.objects.filter(
            batch__uuid=batch_uuid,
            case_price_fragment__isnull=True
        )
        for idx, row in enumerate(result):
            new_price = None
            print("[%.3d / %.3d] optimizing %s" % (
                    idx + 1,
                    result.count(),
                    row.api_result.case_item,
                )
            )
            all_price_data = CaseItemPriceApiResult.objects.filter(
                case_item__name=row.api_result.case_item.name,
                batch__uuid=batch_uuid
            )
            exterior_ranking = {
                0: Exteriors.BATTLE_SCARRED_EXTERIOR,
                1: Exteriors.WELL_WORN_EXTERIOR,
                2: Exteriors.FIELD_TESTED_EXTERIOR,
                3: Exteriors.MINIMAL_WEAR_EXTERIOR,
                4: Exteriors.FACTORY_NEW_EXTERIOR,
            }
            reversed_index = {v: k for k, v in exterior_ranking.items()}
            ind = reversed_index[row.api_result.case_item.exterior]
            while ind != 0:
                if row.api_result.case_item.can_be_stattrack:
                    new_price = all_price_data.filter(
                        case_item__name=row.api_result.case_item.name,
                        case_item__is_stattrack=not row.api_result.case_item.is_stattrack,
                        case_item__exterior=row.api_result.case_item.exterior,
                    ).values_list("median_price", flat=True)
                    if len(new_price) > 0:
                        break
                ind -= 1
                new_price = all_price_data.filter(
                    case_item__name=row.api_result.case_item.name,
                    case_item__exterior=exterior_ranking[ind],
                ).values_list("median_price", flat=True)
                if len(new_price) > 0:
                    break
            if new_price:
                print(
                    "found new price for %s via %s" % (
                        row.api_result.case_item,
                        new_price,
                    )
                )

                row.api_result.median_price = new_price.first()
                row.api_result.is_interpolated = True
                row.api_result.save(
                    update_fields=[
                        "median_price",
                        "is_interpolated",
                    ]
                )
                row.case_price_fragment = calculate_case_price_fragment(
                    row.api_result.case_item.probability,
                    float(row.api_result.median_price) if row.api_result.median_price else None,
                )
                row.save(update_fields=["case_price_fragment"])
        new_result = CaseItemPriceDetails.objects.filter(
            batch__uuid=batch_uuid,
            case_price_fragment__isnull=True
        )
        print("now %s elements without price" % new_result.count())
        pre_update = CasePrice.objects.filter(batch__uuid=batch_uuid).values_list('case_price', flat=True)
        pre_update_value = list(pre_update)
        create_or_update_case_price(batch_uuid, case_name=case_name)
        post_update = CasePrice.objects.filter(batch__uuid=batch_uuid).values_list('case_price', flat=True)
        post_update_value = list(post_update)
        print("before", pre_update_value, "after", post_update_value)
