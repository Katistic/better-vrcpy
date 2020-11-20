from vrcpy.request import Request
import asyncio
import base64

class Client:
    def __init__(self):
        self.request = Request()
        self.me = None

        self.ws = None

    async def _ws_loop(self):
        async for message in self.ws:
            pass

    async def fetch_me(self, **kwargs):
        return await self.request.call("/auth/user", **kwargs)

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

        resp = await self.fetch_me(
            headers={"Authorization": "Basic " + b64},
            no_auth=True
        )

        self.request.new_session(b64)
        self.request.session.cookie_jar.update_cookies(
            [["auth", resp["response"].headers["Set-Cookie"].split(';')[0].split("=")[1]]]
        )

    async def logout(self):
        '''
        Closes client session and logs out VRC user
        '''

        await self.request.call("/logout", "PUT")
        await self.request.close_session()

        if self.ws is not None:
            await self.ws.close()

        await asyncio.sleep(0)

    # Websocket Stuff

    async def start(self):
        authToken = ""
        for cookie in self.request.session.cookie_jar:
            if cookie.key == "auth":
                authToken = cookie.value

        self.ws = await self.request.session.ws_connect("wss://pipeline.vrchat.cloud/?authToken="+authToken)
        await self._ws_loop()

