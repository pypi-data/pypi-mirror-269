# Requeue

In applications that receive messages, like chat bots, where you run callbacks
on incoming messages, you might want to capture follow-up messages within a callback.
A request queue allows you to do that.

## Examples

```python
from requeue import Requeue
queue = Requeue()
```

Where the messages come in and are processed;

```python
async def run_callbacks(message):
    # If the message completes a request, since it is forwarded,
    # it should not continue to be handled by the callbacks.
    if await queue.complete(message):
        return

    # If no request was completed, the message can be processed as usual.
    for callback in client.callbacks:
        await callback(message)
```

Inside a callback, to request and await an incoming message, you use `wait_for`.
To only accept a message that meets specific criteria, you can pass a function
as a filter to the `check` parameter.

```python
@client.callback
async def on_message(message):
    # An example of a knock knock joke back-and-forth,
    # using the request queue to pick out the responses

    if message == 'Knock knock!':
        await client.send("Who's there?")
        who = await queue.wait_for()
        await client.send(f'{who} who?')
        punchline = await queue.wait_for()
        await punchline.react('😂')
```
