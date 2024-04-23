## yatbaf

Asynchronous [Telegram Bot API](https://core.telegram.org/bots/api) framework.

## Requirements

Python 3.11+

## Installation

```shell
$ pip install yatbaf
```

## Simple echo bot

```python
import yatbaf.filters as f
from yatbaf import Bot, on_message
from yatbaf.types import Message


@on_message(filters=[f.text])
async def echo(message: Message) -> None:
    await message.answer(message.text)


Bot("<REPLACE-WITH-YOUR-TOKEN>", [echo]).run()
```

## License
[MIT](./LICENSE)
