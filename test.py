import requests
from datetime import datetime
import pytz

def add_food_to_database(food_name):
    food = {
        "banana": "\"5e020f6242f6c58ad78915b6\"",
        "apple": "\"5e01d71f8e78f787a276ff90\"",
        "pineapple": "\"5e05b0746e6b65003bc2d67e\"",
        "mandarin": "\"5e12eb99995b1b003bad23ce\"",
        "Onion (White)": "\"5e05ad4c6e6b65003bc2d65c\"",
        "lime": "\"5e05ae306e6b65003bc2d662\"",
        "tomato": "\"5e05ad106e6b65003bc2d656\"",
        "watermelon": "\"5e05ae4c6e6b65003bc2d664\"",
        "pepper": "\"5e05b13a6e6b65003bc2d68a\"",
        "orange": "asdfs"
    }
    foodId = food[food_name]
    # today = f"\"{datetime.now()}\""
    today = f"\"{datetime.now().isoformat()}\""
    url = 'https://dumb-fridge.herokuapp.com/admin/api' 
    headers = {'Accept': 'application/vnd.cap-collectif.preview+json'} 
    req = {"query": "mutation addFood{updateFood(id: " + foodId +", data: {quantity: 15, entryDate:" + today + "}){name,quantity,duration,entryDate,id}}"}
    r = requests.post('https://dumb-fridge.herokuapp.com/admin/api', json= req, headers= {'Accept': 'application/vnd.cap-collectif.preview+json'})
    if r.status_code == 200:
        print(r.json())
add_food_to_database('banana')