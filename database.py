import pymongo
import os


class DBClient:
    def __init__(self, subname):
        dbStr = os.environ.get("SUGGESTIONS_DB_STR")
        dbClient = pymongo.MongoClient(dbStr)
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
        self.dataset.delete_many()

    def delete(self, query):
        self.dataset.delete_one(query)
