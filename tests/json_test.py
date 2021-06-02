import json
from datetime import datetime
import dateparser as dp
def test():
    with open("tests/test.json", "r+") as file:
        data= {"testing": str(datetime.now())}
        json.dump(data, file)

test()
