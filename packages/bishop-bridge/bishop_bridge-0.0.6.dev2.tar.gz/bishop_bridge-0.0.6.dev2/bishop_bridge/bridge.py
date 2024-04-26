import msgpack
import socketio
from .logger import logger


class Bridge:
    """
    A class that represents a Bishop bridge. A bridge is a server that stores
    data and allows clients to subscribe to and update the data.
    """

    def __init__(self, app):
        self.data = {}
        self.updated_paths = []
        self.callbacks = []

        self.sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="aiohttp")
        self.sio.attach(app)

        @self.sio.event
        def connect(sid, environ):
            logger.info(f"Client connected: {sid}")

        @self.sio.event
        def disconnect(sid):
            logger.info(f"Client disconnected: {sid}")

        @self.sio.event
        async def subscribe(sid, path: str):
            logger.info(f"Client {sid} subscribed to {path}")
            await self.sio.enter_room(sid, path)
            # Send the current value of the object to the client.
            await self.send_data(path, sid)

        @self.sio.event
        async def unsubscribe(sid, path: str):
            logger.info(f"Client {sid} unsubscribed from {path}")
            await self.sio.leave_room(sid, path)

        @self.sio.event
        async def set(sid, data):
            if isinstance(data, dict):
                if "path" in data and "value" in data:
                    if isinstance(data["path"], str):
                        logger.info(
                            f"Client {sid} set {data['path']} to {data['value']}"
                        )
                        for callback in self.callbacks:
                            await callback(data["path"], data["value"])
                    else:
                        logger.error(
                            f"'path' must be of type str, " f"not {type(data['path'])}"
                        )
                else:
                    logger.error("Data must contain 'path' and 'value'")
            else:
                logger.error("Data must be a dictionary")

    @staticmethod
    def get_all_paths(value: dict, base_path: str = ""):
        """
        Get all paths in a nested dictionary.
        """
        paths = []

        if isinstance(value, dict):
            for key, val in value.items():
                new_path = base_path + "/" + key
                paths.append(new_path)
                paths += Bridge.get_all_paths(val, new_path)
        return paths

    def get_data(self, path: str):
        """
        Get the data at the given path.
        """
        if path == "/":
            return self.data

        keys = path.strip("/").split("/")
        current_dict = self.data

        try:
            for key in keys:
                if key in current_dict:
                    current_dict = current_dict[key]
                else:
                    return None
            return current_dict
        except TypeError:
            logger.error("Path must be a string")
            return None

    def set_data(self, path: str, value: any):
        """
        Set the data at the given path to the given value.
        """
        keys = path.strip("/").split("/")
        current_dict = self.data

        current_path = []
        for path_part_index in range(len(keys) - 1):
            key = keys[path_part_index]

            current_path += [key]
            if key in current_dict:
                current_dict = current_dict[key]
            else:
                current_dict[key] = {}  # create a new dictionary for the key
                self.updated_paths.append("/" + "/".join(current_path))
                self.updated_paths.append("/" + "/".join(current_path[:-1]))
                current_dict = current_dict[key]

        key_is_new = keys[-1] not in current_dict
        key_has_changed = (not key_is_new) and current_dict[keys[-1]] != value

        if key_is_new:
            self.updated_paths.append("/" + "/".join(current_path))

        if key_is_new or key_has_changed:
            current_dict[keys[-1]] = value
            # add the path of the value
            self.updated_paths.append(path)
            # add all subpaths from within the value
            self.updated_paths += self.get_all_paths(value, path)

    async def send_data(self, path: str, sid: str = None):
        """
        Publish data to all clients subscribed to the path.
        """
        encoded_data = msgpack.packb({"path": path, "value": self.get_data(path)})
        if sid is None:
            await self.sio.emit(path, encoded_data, room=path)
        else:
            await self.sio.emit(path, encoded_data, room=sid)

    async def send_updated_data(self):
        """
        Publish updated data to all clients.
        """
        # logger.info("Sending updated data")

        self.updated_paths = list(set(self.updated_paths))
        self.updated_paths.sort(key=lambda s: s.count("/"), reverse=True)

        for path in self.updated_paths:
            await self.send_data(path)
            # logger.info(f"Sent {path}")
        self.updated_paths = []

    def add_callback(self, callback):
        """
        Add a callback function to be called when a data update is received by
        a client.
        Returns a function that will remove the callback when called.
        The callback function should take two arguments: path and value.
        """
        self.callbacks.append(callback)

        def remove_callback():
            self.callbacks.remove(callback)

        return remove_callback
