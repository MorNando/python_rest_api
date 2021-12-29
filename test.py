"""
Testing the API locally. Will eventually turn in to a proper UnitTest
"""

import requests

BASE= "http://127.0.0.1:5000/"

data = [
    {"name": "dave does dallas", "views": 200, "likes": 30},
    {"name": "john does dallas", "views": 200000, "likes": 10000},
    {"name": "bob does dallas", "views": 100, "likes": 10},
    {"name": "kev does dallas", "views": 40000, "likes": 1000},
    {"name": "chris does dallas", "views": 10, "likes": 1},
    {"name": "peter does dallas", "views": 3000, "likes": 100}
]

for i, row in enumerate(data):
    response = requests.put(BASE + "video/" + str(i), row)
    print(response.json())

response = requests.delete(BASE + "video/1")
print(response)

response = requests.get(BASE + "video/2")
print(response.json())

response = requests.patch(BASE + "video/2", {"views": 60000, "likes": 20})
print(response.json())

response = requests.get(BASE + "video/2")
print(response.json())

response = requests.patch(BASE + "video/2", {"views": 20, "likes": 1})
print(response.json())

response = requests.get(BASE + "video/2")
print(response.json())
