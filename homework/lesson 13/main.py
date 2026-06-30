import requests

def get_user_by_id(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    user = response.json()

    return {
        "name": user["name"],
        "email": user["email"],
        "city": user["address"]["city"],
        "company": user["company"]["name"]
    }


print(get_user_by_id(3))
print(get_user_by_id(20))