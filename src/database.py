import pymongo
import os


class DBClient(pymongo.MongoClient):
    def __init__(self, subname: str):
        # Not letting random people into my mongoDB cluster
        dbStr = os.environ.get("DB_STR")
        dbClient: pymongo.MongoClient = pymongo.MongoClient(dbStr)
        info = dbClient["info"]
        table = info[subname]
        self.dataset = table

    def get_suggestion_id():
        with open("suggestionID.txt", 'r+') as f:
            Id = int(f.readline())
            f.seek(0)
            f.write(str(Id + 1))
            f.truncate()
            return Id

    def add_suggestion(self, suggestionAuthor, suggestionContent):
        suggestionData = {"_id": DBClient.get_suggestion_id(),
                          "author": suggestionAuthor, "content": suggestionContent}

        inserted = self.dataset.insert_one(suggestionData)
        return inserted.inserted_id

    def add_ping(self, pingUser):
        self.dataset.insert_one({"_id": pingUser})

    def find(self, query):
        return self.dataset.find_one(query)

    def clear(self):
        self.dataset.delete_many({})

    def delete(self, query):
        self.dataset.delete_one(query)

    def add(self, item):
        self.dataset.insert_one(item)

    def update(self, query, new):
        self.dataset.update_one(query, new)
