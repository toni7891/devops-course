import requests
import json


BASE_URL = "https://jsonplaceholder.typicode.com"


def get_all(res):
    response = requests.get(f"{BASE_URL}/{res}")
    print(f"getall: status {response.status_code}, count: {len(response.json())}")


def getby_id(post_id, res):
    response = requests.get(f"{BASE_URL}/{post_id}")
    print(f"getbyID full data in for ID {post_id}:", response.json())


def getby_userID(user_id, res):
    params = {'userId': user_id}
    response = requests.get(f"{BASE_URL}/{res}", params=params)
    posts = response.json()
    for post in posts:
        print(f"title: {post["title"]}")


def getby_item(item_id, res):
    response = requests.get(f"{BASE_URL}/{res}/{item_id}")
    print(f"getby_item raw data for {res} {item_id}:", response.json())


def create_new(res, payload=None):
    if payload is None:
        payload = {"title": "bim", "body": "bam", "userId": 1}
    
    response = requests.post(f"{BASE_URL}/{res}", json=payload)
    
    print(f"status: {response.status_code}")
    print(f"response: {response.json()}")


def update_post_put(post_id, res):
    updated_data = {"id": post_id, "title": "dim", "body": "sim", "userId": 1}
    response = requests.put(f"{BASE_URL}/{res}/{post_id}", json=updated_data)
    print(f"status: {response.status_code}", )
    print(response.json())
    


def patch_post(post_id, res):
    partial_data = {"title": "what the heli"}
    response = requests.patch(f"{BASE_URL}/{res}/{post_id}", json=partial_data)
    print(f"status: {response.status_code}")
    print(response.json())
    


def delete_post(post_id, res):
    response = requests.delete(f"{BASE_URL}/{res}/{post_id}")
    print(f"status: {response.status_code}")
    print(response.json())


def get_comments_for_post(post_id, res):

    response = requests.get(f"{BASE_URL}/{res}/{post_id}/comments")
    comments = response.json()
    print(response.json())


def filter_by_post(post_id, res):
    params = {'postId': post_id}
    response = requests.get(f"{BASE_URL}/{res}", params=params)
    emails = []
    raw = response.json()
    for comment in raw:
        email_address = comment['email']
        emails.append(email_address)
    print(f"filter by post {post_id}: \n emails: {emails}")


def get_photos_for_album(album_id, res):
    response = requests.get(f"{BASE_URL}/{res}/{album_id}/photos")
    titles = []
    for photo in response.json():
        titles.append(photo['title'])
    print(f"titles of photos in album {album_id}: {titles[:3]} len: {len(titles)})")


def get_first_five(res):
    response = requests.get(f"{BASE_URL}/{res}")
    data = response.json()
    print(f"get ({res}) first 5 items:", data[:5])


def filter_photos_by_album(album_id, res):
    params = {'albumId': album_id}
    response = requests.get(f"{BASE_URL}/{res}", params=params)
    urls = []
    raw = response.json()

    for photo in raw:
        photo_url = photo['url']
        urls.append(photo_url)
    
    print(f"filter by album {album_id}: URL found: {urls[:3]}...")


def get_photos_for_album(album_id, res):
    response = requests.get(f"{BASE_URL}/{res}/{album_id}/photos")
    titles = []
    items = response.json()
    for item in items:
        album_title = item['title']
        titles.append(album_title)
        
    print(f"titles in album {album_id}: {titles[:3]} len: {len(titles)})")


def filter_todos_by_user(user_id, res):
    params = {'userId': user_id}
    response = requests.get(f"{BASE_URL}/{res}", params=params)
    titles = []
    for todo in response.json():
        titles.append(todo['title'])
    print(f"TODO titles for user {user_id}: {titles[:3]}...")


def filter_todos_by_status(is_completed, res):
    params = {'completed': is_completed}
    response = requests.get(f"{BASE_URL}/{res}", params=params)
    titles = []
    for todo in response.json():
        titles.append(todo['title'])
    print(f"titles: {is_completed}: {titles[:3]}...")


def patch_todo_status(todo_id, res):
    partial_data = {"completed": True}
    response = requests.patch(f"{BASE_URL}/{res}/{todo_id}", json=partial_data)
    print(f"stat: {response.status_code}, raw data:", response.json())


def get_users_summary(res):
    response = requests.get(f"{BASE_URL}/{res}")
    users_list = []
    for user in response.json():
        summary = {"name": user['name'], "email": user['email']}
        users_list.append(summary)
    print(f"users fdata (name + mail): {users_list[:2]}...")


def get_user_city(user_id, res):
    response = requests.get(f"{BASE_URL}/{res}/{user_id}")
    data = response.json()

    city = data.get('address', {}).get('city')
    print(f"user {user_id} lives in: {city}")


def get_nested_user_titles(user_id, res):
    response = requests.get(f"{BASE_URL}/users/{user_id}/{res}")
    titles = []
    for item in response.json():
        titles.append(item['title'])
    print(f"user {user_id} {res} titles: {titles[:3]}...")


def users():
    res = "users"
    user_payload = {
        "name": "tony",
        "username": "4rch3r",
        "email": "tony@dimbim.com"
    }

    get_users_summary(res)
    get_user_city(1, res)
    get_nested_user_titles(1, "posts")
    get_nested_user_titles(1, "todos")
    get_nested_user_titles(1, "albums")
    create_new(res, payload=user_payload)
    delete_post(1, res)


def todos():
    res = "todos"
    todo_payload = {
        "userId": 1,
        "title": "simsim",
        "completed": False
    }

    get_all(res)
    getby_item(1, res)
    filter_todos_by_user(1, res)
    filter_todos_by_status(False, res)
    create_new(res, payload=todo_payload)
    patch_todo_status(1, res)
    delete_post(1, res)


def photos():
    res = "photos"
    photo_data = {
        "albumId": 1,
        "title": "New Pic",
        "url": "dim/bim"
    }

    get_first_five(res) 
    getby_id(1, res) 
    filter_photos_by_album(1, res) 
    create_new(res, payload=photo_data)
    delete_post(1, res)


def albums():
    res = "albums"
    get_all(res)
    getby_item(1, res)
    get_photos_for_album(1, res)
    create_new(res)
    delete_post(1, res)


def comments():
    res = "comments"
    get_all(res) 
    getby_id(5, res) 
    filter_by_post(1, res)
    create_new(res)
    delete_post(5, res)


def posts():
    res = "posts"
    get_all(res)
    getby_id(1, res)
    getby_userID(1, res)
    create_new(res)
    update_post_put(1, res)
    patch_post(1, res)
    delete_post(1, res)
    get_comments_for_post(1, res)


if __name__ == "__main__":
    posts()
    comments()
    albums()
    photos()
    todos()
    users()
