import requests


class Paebot:
    def __init__(self, token):
        self.endpoint = f"https://api.telegram.org/bot{token}/"
        self.commands = {}

    def api(self, method, **params):
        return requests.get(self.endpoint + method, params=params).json()

    def command(self, command):
        def decorator(f):
            self.commands[command] = f
            return f

        return decorator

    def handle(self, update):
        try:
            text = update["message"]["text"]
            if text.startswith("/"):
                command, *args = text.split()
                command = command.split("@")[0]
                if command in self.commands:
                    return self.commands[command](update, update["message"]["chat"]["id"], args)
        except KeyError:
            return

    def run(self, timeout=60):
        offset = -1
        while True:
            updates = self.api("getUpdates", offset=offset, timeout=timeout)
            for update in updates.get("result", []):
                self.handle(update)
                offset = update.get("update_id", offset) + 1
