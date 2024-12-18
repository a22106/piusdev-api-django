import logging
import pycountry
from phonenumbers.data import _COUNTRY_CODE_TO_REGION_CODE

logger = logging.getLogger(__name__)

def get_country_choices():
    preferred_countries = ['US', 'GB', 'KR', 'JP', 'CN']
    preferred_list = []
    other_list = []

    for country_code in _COUNTRY_CODE_TO_REGION_CODE:
        for region_code in _COUNTRY_CODE_TO_REGION_CODE[country_code]:
            try:
                country = pycountry.countries.get(alpha_2=region_code)
                if country:
                    entry = {
                        'code': region_code,
                        'name': country.name,
                        'dial_code': f'+{country_code}'
                    }
                    # 우선순위 국가와 그 외 국가로 분류
                    if region_code in preferred_countries:
                        preferred_list.append(entry)
                    else:
                        other_list.append(entry)
            except (KeyError, AttributeError):
                continue

    # 우선순위 국가 -> 국가 이름순으로 정렬 -> 그 외 국가 이름순 정렬
    preferred_list_sorted = sorted(preferred_list, key=lambda x: x['name'])
    other_list_sorted = sorted(other_list, key=lambda x: x['name'])

    # 최종 리스트 합치기
    result = preferred_list_sorted + other_list_sorted
    logger.debug(f"get_country_choices: Returning {len(result)} countries")
    return result