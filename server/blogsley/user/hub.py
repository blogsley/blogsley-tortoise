from blogsley.hub import Hub, Subscriber, Event

hub = Hub()

class UserEvent(Event):
    def __init__(self, id, kind):
        super().__init__(id, kind)

class UserSubscriber(Subscriber):
    def __init__(self, id):
        super().__init__()
        self.id = id

    async def send(self, msg):
        print('put in queue')
        if msg.id != self.id:
            return
        await self.queue.put(msg)
