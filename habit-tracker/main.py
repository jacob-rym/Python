# import requests
from datetime import datetime

USERNAME = ""
TOKEN = ""
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# CREATE A USER
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Coding Graph",
    "unit": "minutes",
    "type": "int",
    "color": "sora",
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# CREATE A GRAPH
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

today = datetime.now().strftime("%Y%m%d")

pixel_data = {
    "date": today,
    "quantity": "60",
}

# CREATE A PIXEL
# response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
# print(response.text)

update_date = datetime(year=2021, month=5, day=4).strftime("%Y%m%d")
pixel_update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{update_date}"

pixel_update_data = {
    "quantity": "40",
}

# UPDATE A PIXEL
# response = requests.put(url=pixel_update_endpoint, json=pixel_update_data, headers=headers)
# print(response.text)

delete_date = datetime(year=2021, month=5, day=4).strftime("%Y%m%d")

pixel_delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{delete_date}"

# DELETE A PIXEL
# response = requests.delete(url=pixel_delete_endpoint, headers=headers)
# print(response.text)
