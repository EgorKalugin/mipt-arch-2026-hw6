import json
import logging
import os
import time
from typing import Optional

import requests

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

logger = logging.getLogger(__name__)


def fetch_rates(max_retries: int = 3, retry_delay: int = 2) -> Optional[dict]:
    for attempt in range(max_retries):
        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            return response.json()["rates"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error processing response: {e}")
            return None
    logger.error("Max retries reached. Unable to fetch rates.")
    return None


def fetch_rates_cached(cache_file: str = "exchange_rates.json", cache_expiry: int = 3600) -> Optional[dict]:
    rates = _load_from_cache(cache_file, cache_expiry)
    if rates is not None:
        return rates
    rates = fetch_rates()
    if rates is not None:
        _save_to_cache(rates, cache_file)
    return rates


def _load_from_cache(cache_file: str, cache_expiry: int) -> Optional[dict]:
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file) as f:
            data = json.load(f)
        if time.time() - data["timestamp"] < cache_expiry:
            return data["rates"]
    except (json.JSONDecodeError, KeyError):
        logger.warning("Invalid cache file. Fetching from API.")
    return None


def _save_to_cache(rates: dict, cache_file: str) -> None:
    try:
        with open(cache_file, "w") as f:
            json.dump({"timestamp": time.time(), "rates": rates}, f)
    except IOError as e:
        logger.error(f"Error saving to cache: {e}")
