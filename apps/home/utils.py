import logging
import pycountry
import phonenumbers
from phonenumbers.data import _COUNTRY_CODE_TO_REGION_CODE

logger = logging.getLogger(__name__)

def get_country_choices():
    """국가 코드 리스트를 반환하는 함수

    Returns:
        List[Dict[str, str]]: 국가 이름과 국가 코드 리스트
    """
    countries = []
    for country in sorted(pycountry.countries, key=lambda x: x.name):
        try:
            country_code = phonenumbers.country_code_for_region(country.alpha_2)
            countries.append(
                {
                    "name": country.name,
                    "dial_code": f"+{country_code}",
                }
            )
        except:
            logger.error(f"Error getting country code for {country.name}")
            raise
    return countries