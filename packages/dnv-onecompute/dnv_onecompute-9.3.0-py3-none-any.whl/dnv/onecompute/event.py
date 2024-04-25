import asyncio


class Event:
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError(
                "Handler is not handling this event, so cannot unhandle it."
            )
        return self

    async def fire_async(self, *args, **kwargs):
        handlers = [
            asyncio.ensure_future(handler(*args, **kwargs)) for handler in self.handlers
        ]
        await asyncio.gather(*handlers)

    @property
    def handlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire_async
    __len__ = handlerCount
