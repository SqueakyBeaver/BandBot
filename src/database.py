import pymongo
import os
import json


class DBClient():
    def __init__(self, file_name: str):
        self.file_name = "backend/" + file_name + ".json"
        with open(self.file_name, "r") as file:
            self.data = json.load(file)

    def update_data(self, file):
        self.data = json.load(file)

    def get_data(self):
        for i in self.data:
            yield i

    def get_suggestion_id(self):
            return self.data["id"]

    def add_suggestion(self, suggestionAuthor, suggestionContent):
        self.data["suggestions"].append({"id": self.get_suggestion_id(),
                            "author": suggestionAuthor, "content": suggestionContent})

        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)

    def add_ping(self, pingUser):
        self.data["pings"].append(pingUser)
        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)

    def find(self, key, value=None):
        if value is None:
            return self.data[key]

        for (i, x) in self.data.items():
            if key == i and value == x:
                return self.data[key]

    def clear(self):
        self.data = {}
        with open(self.file_name, "w") as file:
            json.dump({}, file, indent=4)

    def delete(self, query: dict):
        self.data.pop(query)

        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)

    def add(self, item: dict):
        for key in item.keys():
            self.data[key] = item[key]

        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)

    def update(self, key, value):
        self.data[key] = value

        with open(self.file_name, "w") as file:
            json.dump(self.data, file, indent=4)
