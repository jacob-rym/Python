import requests
from datetime import datetime


GENDER = ""
WEIGHT = 0
HEIGHT = 0
AGE = 0

NUTRITIONIX_APP_ID = ""
NUTRITIONIX_API_KEY = ""

SHEETY_ADD_ENDPOINT = "https://api.sheety.co/98faa4768980391cee564a2b40633463/copyOfMyWorkouts/workouts"
SHEETY_TOKEN = ""


nutritionix_headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}

# For example: "I ran for 40 minutes and walked for 10 minutes"
exercises_str = input("Tell me which exercises you did: ")

nutritionix_parameters = {
    "query": exercises_str,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

nutritionix_url = "https://trackapi.nutritionix.com"
nutritionix_exercise_endpoint = f"{nutritionix_url}/v2/natural/exercise"

nutritionix_response = requests.post(url=nutritionix_exercise_endpoint, json=nutritionix_parameters,
                                     headers=nutritionix_headers)
nutritionix_response.raise_for_status()

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

date_now = datetime.now()
current_date = date_now.strftime("%d/%m/%Y")
current_time = date_now.strftime("%X")
print(current_date, current_time)


for exercise in nutritionix_response.json()["exercises"]:
    sheety_parameters = {
        "workout": {
            "date": current_date,
            "time": current_time,
            "exercise": exercise["name"].title(),
            "duration": str(exercise["duration_min"]),
            "calories": str(exercise["nf_calories"]),
        }
    }

    sheety_response = requests.post(url=SHEETY_ADD_ENDPOINT, json=sheety_parameters, headers=sheety_headers)
    sheety_response.raise_for_status()
    print(sheety_response.text)
