import json

def test():
    with open("backend/starboard.json", "r+") as file:
        data= {"testing": "failed successfully"}
        json.dump(data, file)

test()
