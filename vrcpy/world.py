from vrcpy.baseobject import BaseObject

class LimitedWorld(BaseObject):
    def __init__(self, client, obj=None, loop=None):
        super().__init__(client, loop)

        self.required.update({
            "name": {
                "dict_key": "name",
                "type": str
            },
            "id": {
                "dict_key": "id",
                "type": str
            },
            "author_name": {
                "dict_key": "authorName",
                "type": str
            },
            "author_id": {
                "dict_key": "authorId",
                "type": str
            },
            "tags": {
                "dict_key": "tags",
                "type": list
            },
            "created_at": {
                "dict_key": "created_at",
                "type": str
            },
            "updated_at": {
                "dict_key": "updated_at",
                "type": str
            },
            "release_status": {
                "dict_key": "releaseStatus",
                "type": str
            },
            "visis": {
                "dict_key": "visis",
                "type": int
            },
            "capacity": {
                "dict_key": "capacity",
                "type": int
            },
            "favorites": {
                "dict_key": "favorites",
                "type": int
            },
            "popularity": {
                "dict_key": "popularity",
                "type": int
            },
            "image_url": {
                "dict_key": "imageUrl",
                "type": str
            },
            "thumbnail_image_url": {
                "dict_key": "thumbnailImageUrl",
                "type": str
            },
            "heat": {
                "dict_key": "heat",
                "type": int
            },
            "publication_date": {
                "dict_key": "publicationDate",
                "type": str
            },
            "labs_publication_date": {
                "dict_key": "labsPublicationDate",
                "type": str
            },
            "unity_packages": {
                "dict_key": "unityPackages",
                "type": str
            },
            "occupants": {
                "dict_key": "occupants",
                "type": int
            }
        })

        if obj is not None:
            self._assign(obj)

class World(LimitedWorld):
    def __init__(self, client, obj, loop=None):
        super().__init__(client, loop)

        self.required.update({
            "description": {
                "dict_key": "description",
                "type": str
            },
            "version": {
                "dict_key": "version",
                "type": int
            },
            "featured": {
                "dict_key": "featured",
                "type": bool
            },
            "public_occupants": {
                "dict_key": "publicOccupants",
                "type": int
            },
            "private_occupants": {
                "dict_key": "privateOccupants",
                "type": int
            },
            "asset_url": {
                "dict_key": "assetUrl",
                "type": str
            },
            "instances": {
                "dict_key": "instances",
                "type": list
            }
        })

        self._assign(obj)

        instances = []
        for instance in self.instances:
            instances.append(Instance(self.client, instance, self.loop))

        self.instances = instances

# TODO: Finish Instance class
class Instance(BaseObject):
    def __init__(self, client, obj, loop=None):
        super().__init__(client, loop)

        self.required.update({
            "name": {
                "dict_key": "name",
                "type": str
            },
            "id": {
                "dict_key": "id",
                "type": str
            },
            "type": {
                "dict_key": "type",
                "type": str
            },
            "active": {
                "dict_key": "active",
                "type": bool
            },
            "n_users": {
                "dict_key": "n_users",
                "type": int
            },
            "capacity": {
                "dict_key": "capacity",
                "type": int
            },
            "full": {
                "dict_key": "full",
                "type": bool
            },
            "can_request_invite": {
                "dict_key": "canRequestInvite",
                "type": bool
            },
            "location": {
                "dict_key": "location",
                "type": str
            },
            "instance_id": {
                "dict_key": "instanceId",
                "type": str
            },
            "short_name": {
                "dict_key": "shortName",
                "type": str
            },
            "owner_id": {
                "dict_key": "ownerId",
                "type": str
            },
            "world_id": {
                "dict_key": "worldId",
                "type": str
            },
            "tags": {
                "dict_key": "tags",
                "type": list
            },
            "platforms": {
                "dict_key": "platforms",
                "type": dict
            },
            "permanent": {
                "dict_key": "permanent",
                "type": bool
            },
            "hidden": {
                "dict_key": "hidden",
                "type": str
            }
        })

        self._assign(obj)
