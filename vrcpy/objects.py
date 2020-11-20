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
                if t is not dict:
                    return t(obj)


    def _assign(self, obj):
        self._object_integrety(obj)

        for key in self.required:
            setattr(
                self,
                key,
                self._get_proper_obj(
                    obj[self.required[key]["dict_key"]],
                    self.required[key]["type"]
                )
            )

        for key in self.optional:
            if self.optional[key]["dict_key"] in obj:
                setattr(
                    self,
                    key,
                    self._get_proper_obj(
                        obj[self.optional[key]["dict_key"]],
                        self.optional[key]["type"]
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

class LimitedUser(BaseObject):
    def __init__(self, client, obj=None, loop=None):
        super().__init__(client, loop=loop)

        self.required.update({
            "username": {
                "dict_key": "username",
                "type": str
            },
            "display_name": {
                "dict_key": "displayName",
                "type": str
            },
            "id": {
                "dict_key": "id",
                "type": str
            },
            "bio": {
                "dict_key": "bio",
                "type": str
            },
            "avatar_image_url": {
                "dict_key": "currentAvatarImageUrl",
                "type": str
            },
            "avatar_thumbnail_url": {
                "dict_key": "currentAvatarThumbnailImageUrl",
                "type": str
            },
            "last_platform": {
                "dict_key": "last_platform",
                "type": str
            },
            "tags": {
                "dict_key": "tags",
                "type": list
            },
            "developer_type": {
                "dict_key": "developerType",
                "type": str
            },
            "is_friend": {
                "dict_key": "isFriend",
                "type": bool
            }
        })

        self.optional.update({
            "status": {
                "dict_key": "status",
                "type": str
            },
            "location": {
                "dict_key": "location",
                "type": str
            }
        })

        if obj is not None:
            self._assign(obj)

class User(LimitedUser):
    def __init__(self, client, obj=None, loop=None):
        super().__init__(client, loop=loop)

        self.required.update({
            "bio_links": {
                "dict_key": "bioLinks",
                "type": list
            },
            "status_description": {
                "dict_key": "statusDescription",
                "type": str
            },
            "last_login": {
                "dict_key": "last_login",
                "type": str
            },
            "allow_avatar_copying": {
                "dict_key": "allowAvatarCopying",
                "type": bool
            }
        })

        self.optional.update({
            "state": {
                "dict_key": "state",
                "type": str
            },
            "friend_key": {
                "dict_key": "friendKey",
                "type": str
            },
            "world_id": {
                "dict_key": "worldId",
                "type": str
            },
            "instance_id": {
                "dict_key": "instanceId",
                "type": str
            }
        })

        if obj is not None:
            self._assign(obj)

class CurrentUser(User):
    def __init__(self, client, obj, loop=None):
        super().__init__(client, loop=loop)

        self.required.update({
            "past_display_names": {
                "dict_key": "pastDisplayNames",
                "type": list
            },
            "email_verified": {
                "dict_key": "emailVerified",
                "type": bool
            },
            "has_email": {
                "dict_key": "hasEmail",
                "type": bool
            },
            "has_pending_email": {
                "dict_key": "hasPendingEmail",
                "type": bool
            },
            "accepted_tos_version": {
                "dict_key": "acceptedTOSVersion",
                "type": int
            },
            "has_birthday": {
                "dict_key": "hasBirthday",
                "type": bool
            },
            "friends": {
                "dict_key": "friends",
                "type": list
            },
            "online_friends": {
                "dict_key": "onlineFriends",
                "type": list
            },
            "active_friends": {
                "dict_key": "activeFriends",
                "type": list
            },
            "offline_friends": {
                "dict_key": "offlineFriends",
                "type": list
            },
            "friend_group_names": {
                "dict_key": "friendGroupNames",
                "type": list
            },
            "avatar": {
                "dict_key": "currentAvatar",
                "type": dict
            },
            "avatar_asset_url": {
                "dict_key": "currentAvatarAssetUrl",
                "type": str
            },
            "home_location": {
                "dict_key": "homeLocation",
                "type": str
            },
            "has_logged_in_from_client": {
                "dict_key": "hasLoggedInFromClient",
                "type": bool
            },
            "mfa_enabled": {
                "dict_key": "twoFactorAuthEnabled",
                "type": bool
            },
            "unsubscribe": {
                "dict_key": "unsubscribe",
                "type": bool
            },
            "feature": {
                "dict_key": "feature",
                "type": dict
            }
        })

        self.optional.update({
            "email": {
                "dict_key": "email",
                "type": str
            },
            "obfuscated_email": {
                "dict_key": "obfuscatedEmail",
                "type": str
            },
            "obfuscated_pending_email": {
                "dict_key": "obfuscatedPendingEmail",
                "type": str
            },
            "steam_id": {
                "dict_key": "steamId",
                "type": str
            },
            "steam_details": {
                "dict_key": "steamDetails",
                "type": dict
            },
            "oculus_id": {
                "dict_key": "oculusId",
                "type": str
            },
            "account_deletion_date": {
                "dict_key": "accountDeletionDate",
                "type": str
            }
        })

        self._assign(obj)
