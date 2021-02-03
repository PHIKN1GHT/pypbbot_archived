
#def frame()
from pypbbot.protocol import PrivateMessageEvent

# build_frame, send_as

#async def build_frame(Event)
'''
async def send_frame_as(frame: Frame, botId: int) -> None:
    frame = Frame()
    frame.botId, frame.ok = botId, True#PrivateMessageEvent
    frame_type = Frame.FrameType.Name(frame.frame_type)
    logger.debug('Recv frame [{}] from client [{}]'.format(frame_type, frame.botId))
    _, driver = drivers[frame.botId]
    if frame_type.endswith('Event'):
        await driver.handle(getattr(frame, frame.WhichOneof('data')))
    else:
        if frame.echo in resp.keys():
            if isinstance(frame.WhichOneof('data'), str):
                resp[frame.echo].set_result(getattr(frame, frame.WhichOneof('data')))
            else:
                resp[frame.echo].set_result(None)

'''




