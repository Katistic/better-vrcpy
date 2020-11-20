import asyncio
from vrcpy.errors import ObjectErrors

class BaseObject:
    def __init__(self, client, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.client = client

        # "name": {"dict_key": "id", "type": str}
        self.required = {}
        self.optional = {}

    def _get_proper_obj(self, obj, t):
        vrcpy_types = [LimitedUser, User, CurrentUser]

        if type(obj) is not t:
            if t in vrcpy_types:
                return t(
                    obj,
                    self.client,
                    self.loop
                )
            else:
                return t(obj)


    def _assign(self, obj):
        self._object_integrety(obj)

        for key in self.required:
            setattr(
                self,
                key,
                self._get_proper_obj(
                    obj[self.required[key]["dict_key"]],
                    obj[self.required[key]["type"]]
                )
            )

        for key in self.optional:
            if self.optional[key]["dict_key"] in obj:
                setattr(
                    self,
                    key,
                    self._get_proper_obj(
                        obj[self.optional[key]["dict_key"]],
                        obj[self.optional[key]["type"]]
                    )
                )
            else:
                setattr(self, key, None)

        if hasattr(self, "__cinit__"):
            self.cacheTask = self.loop.create_task(self.__cinit__())

        # Save yo memory fool
        del self.required
        del self.optional

    def _object_integrety(self, obj):
        for key in self.required:
            if self.required[key]["dict_key"] not in obj:
                raise ObjectErrors.IntegretyError(
                    "{} object missing required key {}".format(
                        self.__class__.__name__, self.required[key]["dict_key"]
                    )
                )

