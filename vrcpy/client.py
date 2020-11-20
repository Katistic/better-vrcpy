from vrcpy.request import Request
from vrcpy.objects import *
from vrcpy.errors import ClientErrors
import asyncio
import base64
import json

class Client:
    def __init__(self, loop=None):
        self.request = Request()

        self.me = None
        self.friends = []

        self.ws = None
        self.loop = loop or asyncio.get_event_loop()

        if loop is not None:
            asyncio.set_event_loop(loop)

    async def _ws_loop(self):
        self.loop.create_task(self.on_connect())

        async for message in self.ws:
            message = message.json()
            content = json.loads(message["content"])

            switch = {
                "friend-location": self._on_friend_location,
                "friend-online": self._on_friend_online,
                "friend-offline": self._on_friend_offline,
                "friend-active": self._on_friend_active,
                "friend-add": self._on_friend_add,
                "friend-delete": self._on_friend_delete,
                "friend-update": self._on_friend_update,
                "notification": self._on_notification
            }

            if message["type"] in switch:
                self.loop.create_task(switch[message["type"]](content))

        self.loop.create_task(self.on_disconnect())

    # Utility

    def get_friend(self, id):
        for user in self.friends:
            if user.id == id:
                return user

        return None

    async def fetch_user_via_id(self, id):
        user = await self.request.call("/users/" + id)
        return User(self, user, loop=self.loop)

    # Main

    async def fetch_me(self, **kwargs):
        me = await self.request.call("/auth/user", **kwargs)
        me = CurrentUser(
            self,
            me,
            loop=self.loop
        )

        self.me = me
        return me

    async def login(self, username=None, password=None, b64=None):
        '''
        Used to login as a VRC user

        Must include one of the combinations:
            Username/Password login
                username, string
                Username/email of VRC account

                password, string
                Password of VRC account

            b64 login
                b64, string
                Base64 encoded username:password
        '''

        if b64 is None:
            if username is None or password is None:
                raise ClientErrors.MissingCredentials("Did not pass username+password or b64 for login")

            b64 = base64.b64encode((username+":"+password).encode()).decode()

        resp = await self.request.call(
            "/auth/user",
            headers={"Authorization": "Basic " + b64},
            no_auth=True
        )

        cookie = None
        for cookie in resp["response"].headers.getall("Set-Cookie"):
            if "auth=authcookie" in cookie:
                break

        self.request.new_session(b64)
        self.request.session.cookie_jar.update_cookies(
            [["auth", cookie.split(';')[0].split("=")[1]]]
        )

        if "requiresTwoFactorAuth" in resp["data"]:
            raise ClientErrors.MfaError("Account login requires 2fa")

        self.me = CurrentUser(self, resp["data"], self.loop)

    async def logout(self):
        '''
        Closes client session and logs out VRC user
        '''

        self.me = None
        self.friends = None

        await self.request.call("/logout", "PUT")
        await self.request.close_session()

        if self.ws is not None:
            await self.ws.close()

        await asyncio.sleep(0)

    def run(self, username=None, password=None, b64=None):
        '''
        Automates login+start
        This function is blocking
        '''

        try:
            asyncio.get_event_loop().run_until_complete(self._run(username, password, b64))
        except KeyboardInterrupt:
            asyncio.get_event_loop().run_until_complete(client.logout())

    async def _run(self, username=None, password=None, b64=None):
        await self.login(username, password, b64)
        await self.start()

    # Websocket Stuff

    async def start(self):
        '''
        Starts the ws event _ws_loop
        This function is blocking
        '''

        authToken = ""
        for cookie in self.request.session.cookie_jar:
            if cookie.key == "auth":
                authToken = cookie.value

        self.ws = await self.request.session.ws_connect("wss://pipeline.vrchat.cloud/?authToken="+authToken)
        await self._ws_loop()

    async def event(self, func):
        '''
        Decorator that overwrites class ws event hooks

        Example
        --------

        @client.event
        def on_connect():
            print("Connected to wss pipeline.")

        '''

        if func.__name__.startswith("on_") and hasattr(self, func.__name__):
            setattr(self, func.__name__, func)
            return func

    async def on_connect(self):
        # Called at the start of ws event loop
        pass

    async def on_disconnect(self):
        # Called at the end of ws event loop
        pass

    async def _on_friend_online(self, obj):
        user = User(self, obj["user"], self.loop)

        self.friends.remove(self.get_friend(user.id))
        self.friends.append(user)

        await self.on_friend_online(user)

    async def on_friend_online(self, friend):
        # Called when a friend comes online
        pass

    async def _on_friend_offline(self, obj):
        user = await self.fetch_user_via_id(obj["userId"])

        self.friends.remove(self.get_friend(user.id))
        self.friends.append(user)

        await self.on_friend_offline(user)

    async def on_friend_offline(self, friend):
        # Called when a friend goes offline
        pass

    async def _on_friend_active(self, obj):
        user = User(self, obj["user"], self.loop)

        self.friends.remove(self.get_friend(user.id))
        self.friends.append(user)

        await self.on_friend_active(user)

    async def on_friend_active(self, friend):
        # Called when a friend becomes active
        pass

    async def _on_friend_add(self, obj):
        user = User(self, obj["user"], self.loop)

        self.friends.remove(self.get_friend(user.id))
        self.friends.append(user)

        await self.on_friend_add(user)

    async def on_friend_add(self, friend):
        # Called when a new friend is added to your account
        pass

    async def _on_friend_delete(self, obj):
        user = await self.fetch_user_via_id(obj["userId"])

        self.friends.remove(self.get_friend(user.id))

        await self.on_friend_delete(user)

    async def on_friend_delete(self, friend):
        # Called when a friend is unfriended
        pass

    async def _on_friend_update(self, obj):
        user = User(self, obj["user"], self.loop)
        ouser = self.get_friend(user.id)

        self.friends.remove(ouser)
        self.friends.append(user)

        await self.on_friend_update(ouser, user)

    async def on_friend_update(self, before, after):
        '''
        Called when a friend makes an update to their profile

            before, User
            User before they updated their profile

            after, User
            User after they updated their profile
        '''
        pass

    async def _on_friend_location(self, obj):
        user = User(self, obj["user"], self.loop)
        ouser = self.get_friend(user.id)

        self.friends.remove(ouser)
        self.friends.append(user)

        await self.on_friend_location(ouser, user)

    async def on_friend_location(self, before, after):
        '''
        Called when a friend changes location

            before, User
            User before they changed location

            after, User
            User after they changed location
        '''
        pass

    async def _on_notification(self, obj):
        await self.on_notification(obj)

    async def on_notification(self, notification):
        # Called when recieved a notification
        pass
