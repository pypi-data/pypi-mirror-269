import pytest

from yatbaf.methods import AddStickerToSet
from yatbaf.methods import Close
from yatbaf.methods import CreateNewStickerSet
from yatbaf.methods import EditMessageMedia
from yatbaf.methods import GetMe
from yatbaf.methods import GetUpdates
from yatbaf.methods import SendAnimation
from yatbaf.methods import SendAudio
from yatbaf.methods import SendDocument
from yatbaf.methods import SendMediaGroup
from yatbaf.methods import SendPhoto
from yatbaf.methods import SendSticker
from yatbaf.methods import SendVideo
from yatbaf.methods import SendVideoNote
from yatbaf.methods import SendVoice
from yatbaf.methods import SetStickerSetThumbnail
from yatbaf.methods import SetWebhook
from yatbaf.methods import StopMessageLiveLocation
from yatbaf.methods import UploadStickerFile
from yatbaf.methods.abc import TelegramMethodWithFile
from yatbaf.methods.abc import TelegramMethodWithMedia
from yatbaf.types import Message
from yatbaf.types import Update
from yatbaf.types import User


def test_base_subclass_attrs():
    assert not hasattr(TelegramMethodWithMedia, "__meth_name__")
    assert not hasattr(TelegramMethodWithMedia, "__meth_result_model__")

    assert not hasattr(TelegramMethodWithFile, "__meth_name__")
    assert not hasattr(TelegramMethodWithFile, "__meth_result_model__")


def test_attrs():
    assert hasattr(GetMe, "__meth_name__")
    assert hasattr(GetMe, "__meth_result_model__")


def test_file_fields():
    assert SendAnimation.__meth_file_fields__ == ("animation", "thumbnail")
    assert SendAudio.__meth_file_fields__ == ("audio", "thumbnail")
    assert SendDocument.__meth_file_fields__ == ("document", "thumbnail")
    assert SendPhoto.__meth_file_fields__ == ("photo",)
    assert SendSticker.__meth_file_fields__ == ("sticker",)
    assert SendVideo.__meth_file_fields__ == ("video", "thumbnail")
    assert SendVideoNote.__meth_file_fields__ == ("video_note", "thumbnail")
    assert SendVoice.__meth_file_fields__ == ("voice",)
    assert UploadStickerFile.__meth_file_fields__ == ("sticker",)
    assert SetWebhook.__meth_file_fields__ == ("certificate",)
    assert SetStickerSetThumbnail.__meth_file_fields__ == ("thumbnail",)


def test_media_fields():
    assert AddStickerToSet.__meth_media_fields__ == ("sticker",)
    assert SendMediaGroup.__meth_media_fields__ == ("media",)
    assert EditMessageMedia.__meth_media_fields__ == ("media",)
    assert CreateNewStickerSet.__meth_media_fields__ == ("stickers",)


def test_method_name():
    assert GetMe.__meth_name__ == "getme"
    assert str(GetMe()) == "getme"
    assert GetMe()._get_name() == "getme"


@pytest.mark.parametrize(
    "method,model",
    (
        (GetMe, User),
        (Close, bool),
        (GetUpdates, list[Update]),
        (StopMessageLiveLocation, Message | bool),
    ),
)
def test_method_result_model(method, model):
    assert method.__meth_result_model__ == model
    assert method._get_result_model() == model
