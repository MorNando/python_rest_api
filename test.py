"""
Testing the API locally. Will eventually turn in to a proper UnitTest
"""

from random import randrange
import requests

BASE= "http://127.0.0.1:5000/"

# generate data
data = []
for i in range(10):
    data += [
        {"name": f"video {str(i)}", "views": randrange(1000, 1000000), "likes": randrange(0, 1000)}
    ]

# put request check
for i, row in enumerate(data):
    response = requests.post(BASE + f"video/{str(i)}", row)
    print(response.json())

# get request check
for i, row in enumerate(data):
    response = requests.get(BASE + f"video/{str(i)}")
    print(response.json())

# update request check
for i, row in enumerate(data):
    response = requests.put(BASE + f"video/{str(i)}", {
        "name": f"amended video {str(i)}",
        "views": randrange(1000, 1000000),
        "likes": randrange(0, 1000)
    })
    print(response.json())

# get request check to see if they have been updated
for i, row in enumerate(data):
    response = requests.get(BASE + f"video/{str(i)}")
    print(response.json())

# delete request check
for i, row in enumerate(data):
    response = requests.delete(BASE + f"video/{str(i)}")
    print(response)
