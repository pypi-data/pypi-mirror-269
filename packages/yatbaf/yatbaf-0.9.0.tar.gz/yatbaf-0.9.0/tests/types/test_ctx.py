def test_ctx_empty(message):
    assert message.__usrctx__ == {"ctx": {}}
    assert not message.ctx


def test_ctx(message):
    message.ctx["foo"] = "bar"
    assert "foo" in message.__usrctx__["ctx"]
    assert message.__usrctx__["ctx"]["foo"] == "bar"
