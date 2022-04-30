"""
Processors for incoming data
"""
from functools import partial

import arrow
import petl as etl
from requests import get


def _convert_edited(
    table: etl.Table, mapped_homeworlds: dict[str, str]
) -> (etl.Table, dict[str, str]):
    new_table = etl.addfield(
        table, 'date', lambda t: arrow.get(t['edited']).strftime('%Y-%m-%d')
    )
    new_table = new_table.cutout('edited')
    return new_table, mapped_homeworlds


def _convert_homeworld(
    table: etl.Table, mapped_homeworlds: dict[str, str]
) -> (etl.Table, dict[str, str]):
    new_table = etl.convert(
        table,
        'homeworld',
        partial(_fetch_homeworld, mapped_homeworlds=mapped_homeworlds),
    )
    return new_table, mapped_homeworlds


def _fetch_homeworld(url: str, mapped_homeworlds: dict[str, str] = None) -> str:
    # I could use lru_cache here, but I wanted to keep this cache live only for the time of the request
    if url in mapped_homeworlds:
        return mapped_homeworlds[url]
    mapped_homeworlds[url] = get(url).json()['name']
    return mapped_homeworlds[url]


def process_swe_data(
    raw_data: list[dict], mapped_homeworlds: dict[str, str]
) -> (etl.Table, dict[str, str]):
    fields_map = {
        'name': lambda x, y: (x, y),
        'height': lambda x, y: (x, y),
        'mass': lambda x, y: (x, y),
        'hair_color': lambda x, y: (x, y),
        'skin_color': lambda x, y: (x, y),
        'eye_color': lambda x, y: (x, y),
        'birth_year': lambda x, y: (x, y),
        'gender': lambda x, y: (x, y),
        'homeworld': _convert_homeworld,
        'edited': _convert_edited,
    }
    data = etl.fromdicts(raw_data)
    for column in data.columns():
        if column in fields_map:
            data, mapped_homeworlds = fields_map[column](data, mapped_homeworlds)
            continue
        data = data.cutout(column)
    return data, mapped_homeworlds
