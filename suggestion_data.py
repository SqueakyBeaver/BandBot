import pymongo
from mongo_utils import MongoUtils # Delete if you don't want crash

class DBClient:
    def __init__(self):
        dbClient = pymongo.MongoClient(MongoUtils.dbStr)
        info = dbClient["info"]
        gameIdeas = info["gameIdeas"]
        self.gameIdeasDB = gameIdeas

    def get_suggestion_id():
        with open("suggestionID.txt", 'r+') as f:
            Id = int(f.readline())
            f.seek(0)
            f.write(str(Id + 1))
            f.truncate()
            return Id

    def add_suggestion(self, suggestionAuthor, suggestionContent):
        suggestionData = { "_id": DBClient.get_suggestion_id(),
            "author": suggestionAuthor, "content": suggestionContent}

        inserted = self.gameIdeasDB.insert_one(suggestionData)
        return inserted.inserted_id

    def find(self, query):
        return self.gameIdeasDB.find_one(query)

