from pypbbot.affairs.registrar import onPrivateMessage, onStartsWith, onAllSatisfied
from pypbbot.affairs.builtin import ChatAffair


@onAllSatisfied([
    (onPrivateMessage, ),
    (onStartsWith, '#echo ')
])
def _(affair: ChatAffair) -> None:
    message = affair.raw_message
    affair.sendAndWait(message.replace('#echo ', ""))
