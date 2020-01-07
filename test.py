import requests
from datetime import datetime
import pytz
from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

def fetch_food_from_database():
    results = []
    url = 'https://dumb-fridge.herokuapp.com/admin/api' 
    headers = {'Accept': 'application/vnd.cap-collectif.preview+json'} 
    # req = {"query": "mutation addFood{updateFood(id: " + foodId +", data: {quantity: 15, entryDate:" + today + "}){name,quantity,duration,entryDate,id}}"}
    req = {"query": "query foodInFridge{allFoods(where: { quantity_gt: 0 } ){name,duration,quantity,entryDate,id,image{publicUrlTransformed,filename}}}"}
    r = requests.post('https://dumb-fridge.herokuapp.com/admin/api', json= req, headers= {'Accept': 'application/vnd.cap-collectif.preview+json'})
    if r.status_code == 200:
        allFoods = r.json()['data']['allFoods']
        for food in allFoods:
            results.append(food['name'])
        return results
    else:
        return "Error fetching food"

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
        "orange": "\"5e12f212995b1b003bad23d1\"",
        "yogurt": "\"5e05aba56e6b65003bc2d645\"",
        "egg": "\"5e02f53281d93c02c572190a\""
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

def remove_food_from_database(food_name):
    food = {
        "banana": "\"5e020f6242f6c58ad78915b6\"",
        "apple": "\"5e01d71f8e78f787a276ff90\"",
        "pineapple": "\"5e05b0746e6b65003bc2d67e\"",
        "mandarin": "\"5e12eb99995b1b003bad23ce\"",
        "onion (white)": "\"5e05ad4c6e6b65003bc2d65c\"",
        "lime": "\"5e05ae306e6b65003bc2d662\"",
        "tomato": "\"5e05ad106e6b65003bc2d656\"",
        "watermelon": "\"5e05ae4c6e6b65003bc2d664\"",
        "pepper": "\"5e05b13a6e6b65003bc2d68a\"",
        "orange": "\"5e12f212995b1b003bad23d1\"",
        "yogurt": "\"5e05aba56e6b65003bc2d645\"",
        "egg": "\"5e02f53281d93c02c572190a\""
    }
    foodId = food[food_name]
    # today = f"\"{datetime.now()}\""
    today = f"\"{datetime.now().isoformat()}\""
    url = 'https://dumb-fridge.herokuapp.com/admin/api' 
    headers = {'Accept': 'application/vnd.cap-collectif.preview+json'} 
    req = {"query": "mutation addFood{updateFood(id: " + foodId +", data: {quantity: 0, entryDate:" + today + "}){name,quantity,duration,entryDate,id}}"}
    r = requests.post('https://dumb-fridge.herokuapp.com/admin/api', json= req, headers= {'Accept': 'application/vnd.cap-collectif.preview+json'})
    if r.status_code == 200:
        print(r.json())

# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            })
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        rollbar.report_exc_info(
            extra_data={'token': token, 'message': message, 'extra': extra})
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            })
        raise self.retry(exc=exc)
foodName = "apple"
# print(fetch_food_from_database()
# add_food_to_database(foodName)
# send_push_message("ExponentPushToken[6OqKDEOxeNk-Rz2tJEm81w]", f"Added {foodName} to the database")
def check_difference_in_DB_or_fridge(item, db_food, food_detected):
    for food in db_food:
        if item == food:
            print(f"removing {item} from db")
            remove_food_from_database(item)
            # send_push_message("ExponentPushToken[6OqKDEOxeNk-Rz2tJEm81w]", f"Removed {item} from the database")
            return
    for food in food_detected:
        if item == food:
            print(f"adding {item} to db")
            add_food_to_database(item)
            # send_push_message("ExponentPushToken[6OqKDEOxeNk-Rz2tJEm81w]", f"Added {item} to the database")
            return

def update_db(food_detected):
    # db_food = ['banana', "apple"]
    # db_food = fetch_food_from_database()
    db_food = [food.lower() for food in fetch_food_from_database()]
    food_detected = [food.lower() for food in food_detected]
    food_detected.sort()
    db_food.sort()
    if db_food == food_detected:
        print("no need to update fridge")
        return
    else:
        if list(set(db_food) - set(food_detected)) != []:
            difference = list(set(db_food) - set(food_detected))
            for item in difference:
                check_difference_in_DB_or_fridge(item, db_food, food_detected)
        if list(set(food_detected) - set(db_food)) != []:
            difference = list(set(food_detected) - set(db_food))
            for item in difference:
                check_difference_in_DB_or_fridge(item, db_food, food_detected)
        # for item in db_food:
        #     for new_item in food_detected:
        #         if item == new_item:
        #             # items_in_fridge_to_be_updated.append(item.lower())
        #             db_food.remove(item)
        # print(db_food)
# update_db(['apple', 'banana', 'orange'])
update_db(['apple', 'Banana', 'egg', 'Cucumber', 'Butter', 'Orange', 'pineapple'])