from msgspec import json as jsonlib

from yatbaf.enums import ParseMode
from yatbaf.methods import EditMessageMedia
from yatbaf.methods import GetMe
from yatbaf.methods import SendMediaGroup
from yatbaf.methods import SendMessage
from yatbaf.methods import SendPhoto
from yatbaf.types import InputMediaDocument
from yatbaf.types import InputMediaPhoto


def test_encode_empty():
    method = GetMe()
    data, files = method._encode_params()
    assert data is None
    assert files is None


def test_encode_params():
    method = SendMessage(
        chat_id=12345,
        text="*foo bar*",
        disable_notification=True,
        parse_mode=ParseMode.MARKDOWN,
    )
    data, files = method._encode_params()
    assert isinstance(data, bytes)
    assert files is None
    assert jsonlib.decode(data) == {
        "chat_id": 12345,
        "text": "*foo bar*",
        "disable_notification": True,
        "parse_mode": "MarkdownV2",
    }


def test_encode_file_id():
    method = SendPhoto(chat_id=123, photo="fileid")
    data, files = method._encode_params()
    assert files is None
    assert jsonlib.decode(data) == {"chat_id": 123, "photo": "fileid"}


def test_encode_file_content():
    photo = object()
    method = SendPhoto(chat_id=123, photo=photo)
    data, files = method._encode_params()

    assert files is not None
    assert isinstance(data, dict)
    assert data == {"chat_id": 123, "photo": (fn := method.photo)}
    assert files[fn.split("//")[1]] is photo


def test_encode_media_file_content():
    photo = object()
    method = EditMessageMedia(
        chat_id=12345,
        message_id=12345,
        media=InputMediaPhoto(media=photo),
    )
    data, files = method._encode_params()
    media = jsonlib.decode(data["media"])

    assert files is not None
    assert isinstance(data, dict)

    assert data == {
        "chat_id": 12345,
        "message_id": 12345,
        "media": jsonlib.encode({
            "media": (fn := media["media"]),
            "type": "photo",
        }).decode(),
    }
    assert files[fn.split("//")[1]] is photo


def test_encode_media_filed_id():
    method = EditMessageMedia(
        chat_id=12345,
        message_id=12345,
        media=InputMediaPhoto(media="fileid"),
    )
    data, files = method._encode_params()

    assert files is None
    assert isinstance(data, bytes)

    assert jsonlib.decode(data) == {
        "chat_id": 12345,
        "message_id": 12345,
        "media": {
            "media": "fileid",
            "type": "photo",
        }
    }


def test_encode_media_group_file_content():
    photo = object()
    method = SendMediaGroup(
        media=[InputMediaPhoto(media=photo)],
        chat_id=12345,
    )
    data, files = method._encode_params()
    media = jsonlib.decode(data["media"])

    assert files is not None
    assert isinstance(data, dict)

    assert data == {
        "chat_id": 12345,
        "media": jsonlib.encode([
            {
                "media": (fn := media[0]["media"]),
                "type": "photo",
            },
        ]).decode(),
    }
    assert files[fn.split("//")[1]] is photo


def test_encode_media_group_file_content_1():
    doc1 = object()
    doc2 = object()
    doc2_th = object()
    doc3 = object()

    method = SendMediaGroup(
        media=[
            InputMediaDocument(media=doc1),
            InputMediaDocument(media=doc2, thumbnail=doc2_th),
            InputMediaDocument(media=doc3),
        ],
        chat_id=12345,
    )
    data, files = method._encode_params()
    media = jsonlib.decode(data["media"])

    assert files is not None
    assert isinstance(data, dict)

    assert data == {
        "chat_id": 12345,
        "media": jsonlib.encode([
            {
                "media": (fn1 := media[0]["media"]),
                "type": "document",
            },
            {
                "media": (fn2 := media[1]["media"]),
                "thumbnail": (fn2_th := media[1]["thumbnail"]),
                "type": "document",
            },
            {
                "media": (fn3 := media[2]["media"]),
                "type": "document",
            },
        ]).decode(),
    }
    assert files[fn1.split("//")[1]] is doc1
    assert files[fn2.split("//")[1]] is doc2
    assert files[fn2_th.split("//")[1]] is doc2_th
    assert files[fn3.split("//")[1]] is doc3


def test_encode_media_group_file_id_content_mix():
    doc = object()
    doc_th = object()

    method = SendMediaGroup(
        media=[
            InputMediaDocument(media="fileid1"),
            InputMediaDocument(media="fileid2", thumbnail=doc_th),
            InputMediaDocument(media=doc),
        ],
        chat_id=12345,
    )
    data, files = method._encode_params()
    media = jsonlib.decode(data["media"])

    assert files is not None
    assert isinstance(data, dict)

    assert data == {
        "chat_id": 12345,
        "media": jsonlib.encode([
            {
                "media": "fileid1",
                "type": "document",
            },
            {
                "media": "fileid2",
                "thumbnail": (fn2_th := media[1]["thumbnail"]),
                "type": "document",
            },
            {
                "media": (fn3 := media[2]["media"]),
                "type": "document",
            },
        ]).decode(),
    }

    assert files[fn2_th.split("//")[1]] is doc_th
    assert files[fn3.split("//")[1]] is doc


def test_encode_media_group_file_id():
    method = SendMediaGroup(
        media=[
            InputMediaDocument(media="fileid1"),
            InputMediaDocument(media="fileid2", thumbnail="thid"),
            InputMediaDocument(media="fileid3"),
        ],
        chat_id=12345,
    )
    data, files = method._encode_params()

    assert files is None
    assert isinstance(data, bytes)
    assert jsonlib.decode(data) == {
        "chat_id": 12345,
        "media": [
            {
                "media": "fileid1",
                "type": "document",
            },
            {
                "media": "fileid2",
                "thumbnail": "thid",
                "type": "document",
            },
            {
                "media": "fileid3",
                "type": "document",
            },
        ],
    }
