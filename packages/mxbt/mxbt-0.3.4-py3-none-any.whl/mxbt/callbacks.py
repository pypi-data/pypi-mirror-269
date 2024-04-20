import nio.events.room_events
import nio.events.to_device
from nio import AccountDataEvent, InviteMemberEvent

from .utils import info, error

class Callbacks:
    """
    A class for handling callbacks.
    """

    def __init__(self, async_client, bot) -> None:
        self.async_client = async_client
        self.bot = bot

    async def setup(self) -> None:
        """
        Add callbacks to async_client
        """
        self.async_client.add_event_callback(self.invite_callback,
                                                 InviteMemberEvent)
        self.async_client.add_global_account_data_callback(
            self.custom_emotes_callback, AccountDataEvent
        )

        for event_listener in self.bot.listener._registry:
            if issubclass(event_listener[1],
                          nio.events.to_device.ToDeviceEvent):
                self.async_client.add_to_device_callback(
                    event_listener[0], event_listener[1])
            else:
                self.async_client.add_event_callback(event_listener[0],
                                                     event_listener[1])

    async def custom_emotes_callback(self, event) -> None:
        """
        This callback receive AccountDataEvent
        Check type of event:
            - im.ponies.user_emotes: Bot user custom emojis
                Emojis dict will be saved to Api.user_emotes
            - im.ponies.emote_rooms: Custom emojis from a bot rooms
                We need to receive room_get_state event with 'im.ponies.room_emotes' event type
                and emoji pack name as state_key
                Then emojis dict from this room will be saved to Api.room_emotes[room_id][pack_name]
        """
        if hasattr(event, 'type'):
            if event.type == 'im.ponies.user_emotes':
                if self.bot.api.user_emotes != event.content:
                    self.bot.api.user_emotes = event.content
            elif event.type == 'im.ponies.emote_rooms':
                for room_id, packs in event.content['rooms'].items():
                    self.bot.api.room_emotes[room_id] = dict()
                    for pack in packs.keys():
                        result = await self.async_client.room_get_state_event(
                            room_id, 'im.ponies.room_emotes', pack
                        )
                        emojis = result.content
                        self.bot.api.room_emotes[room_id][pack] = emojis

    async def invite_callback(self, room, event, tries=1) -> None:
        """
        Callback for handling invites.

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
        event : nio.events.room_events.InviteMemberEvent
        tries : int, optional
            Amount of times that this function has been called in a row for the same exact event.

        """
        if not event.membership == "invite":
            return

        try:
            await self.async_client.join(room.room_id)
            info(f"Joined {room.room_id}")
        except Exception as e:
            error(f"Error joining {room.room_id}: {e}")
            tries += 1
            if not tries == 3:
                info("Trying again...")
                await self.invite_callback(room, event, tries)
            else:
                error(f"Failed to join {room.room_id} after 3 tries")


