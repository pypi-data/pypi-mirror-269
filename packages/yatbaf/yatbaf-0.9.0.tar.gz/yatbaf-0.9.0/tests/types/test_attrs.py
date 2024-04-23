from yatbaf.types import InputMediaAnimation
from yatbaf.types import InputMediaAudio
from yatbaf.types import InputMediaDocument
from yatbaf.types import InputMediaPhoto
from yatbaf.types import InputMediaVideo
from yatbaf.types import InputSticker


def test_attr_is_private(message):
    assert "__usrctx__" not in message.__struct_fields__
    assert "__usrctx__" not in message.__slots__


def test_type_file_fields():
    assert InputSticker.__type_file_fields__ == ("sticker",)
    assert InputMediaPhoto.__type_file_fields__ == ("media",)
    assert InputMediaAudio.__type_file_fields__ == ("media", "thumbnail")
    assert InputMediaVideo.__type_file_fields__ == ("media", "thumbnail")
    assert InputMediaDocument.__type_file_fields__ == ("media", "thumbnail")
    assert InputMediaAnimation.__type_file_fields__ == ("media", "thumbnail")
