import re
import unittest.mock as mock

import pytest

from yatbaf import bot
from yatbaf import methods
from yatbaf import on_message


@on_message
async def handler(_):
    pass


def capitalize(w):
    return f"{w[0].upper()}{w[1:]}"


def snake_case(s):
    return '_'.join(
        re.sub(
            '([A-Z][a-z]+)',
            r' \1',
            re.sub('([A-Z]+)', r' \1', s.replace('-', ' '))
        ).split()
    ).lower()


@pytest.fixture
def api_methods(api_spec):
    return api_spec["methods"]


def test_method_object(api_methods):
    for api_method in api_methods.values():
        assert hasattr(methods, capitalize(api_method["name"]))


def test_method_object_fields(api_methods):
    for api_method in api_methods.values():
        method_obj = getattr(methods, capitalize(api_method["name"]))
        for field in api_method.get("fields", []):
            assert hasattr(method_obj, field["name"])


@pytest.mark.asyncio
async def test_method_func(monkeypatch, api_methods, token):
    monkeypatch.setattr(bot.Bot, "_call_api", mock.AsyncMock())
    bot_obj = bot.Bot(token, handlers=[handler])
    for api_method in api_methods.values():
        with mock.patch(f"yatbaf.bot.{capitalize(api_method['name'])}") as o:
            method = getattr(bot_obj, snake_case(api_method["name"]))
            fields = {}
            for i, field in enumerate(api_method.get("fields", [])):
                fields[field["name"]] = i
            await method(**fields)
            if fields:
                o.assert_called_once_with(**fields)
            else:
                o.assert_called_once()
