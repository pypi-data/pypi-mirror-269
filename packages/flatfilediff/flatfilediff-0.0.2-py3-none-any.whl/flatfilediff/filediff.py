import json
import os

class FlatFileDiff:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as json_file:
                json.dump({}, json_file)

    def run(self, callback):
        result = callback()

        with open(self.filename, "r") as json_file:
            last_minute = json.load(json_file)

        diff = list(set(result) - set(last_minute.get("result", [])))

        with open(self.filename, "w") as json_file:
            json.dump({"result": result}, json_file)

        return diff