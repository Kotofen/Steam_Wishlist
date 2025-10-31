import datetime, json, os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


def get_wishlist_games(user_id):
    query = {
        "steamid": user_id,
    }
    resp = requests.get(f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/", params=query)
    return resp.json()

def get_game_info(game_id):
    query = {
        "appids": game_id,
        "cc": "KZ"
    }
    resp = requests.get(f"http://store.steampowered.com/api/appdetails/", params=query).json()
    query['cc'] = "RU"
    resp2 = requests.get(f"http://store.steampowered.com/api/appdetails/", params=query).json()
    price_ru = get_price_attribute(resp2[f'{game_id}'], 'final_formatted')
    price_kz = get_price_attribute(resp[f'{game_id}'], 'final_formatted')
    discount = get_price_attribute(resp[f'{game_id}'], 'discount_percent')
    game_data = {
        "id": game_id,
        "game_name": resp[f'{game_id}']['data']['name'],
        "description": resp[f'{game_id}']['data']['short_description'],
        "image": resp[f'{game_id}']['data']['capsule_image'],
        "price_kz": price_kz,
        "price_ru": price_ru,
        "discount": discount
    }
    return game_data

def get_price_attribute(game_data, attr_name):
    if game_data['success'] == True:
        if 'price_overview' in game_data['data']:
            return game_data['data']['price_overview'][attr_name]
        else: return 0
    else: return 0

def load_json_wishlist(userid):
    if os.path.exists(f"{wishlists_directory}{datetime.date.today().strftime('%d-%m-%Y')}/{userid}.json"):
        with open(f"{wishlists_directory}{datetime.date.today().strftime('%d-%m-%Y')}/{userid}.json", 'r') as f:
            return (json.load(f))
    else:
        return (get_wishlist_games(userid)['response'])

def save_json_wishlist(wishlist_data, userid):
    save_directory = f"{wishlists_directory}{datetime.date.today().strftime('%d-%m-%Y')}"
    os.makedirs(save_directory, exist_ok=True)
    with open(save_directory + f"/{userid}.json", 'w') as f:
        json.dump(wishlist_data, f)

def load_json_gamelist():
    if os.path.exists(f"{gamelist_directory}{datetime.date.today().strftime('%d-%m-%Y')}/games.json"):
        with open(f"{gamelist_directory}{datetime.date.today().strftime('%d-%m-%Y')}/games.json", 'r') as f:
            return (json.load(f))
    else:
        return {}

def save_json_gamelist(gamelist):
    save_directory = f"{gamelist_directory}{datetime.date.today().strftime('%d-%m-%Y')}"
    os.makedirs(save_directory, exist_ok=True)
    with open(save_directory + f"/games.json", 'w') as f:
        json.dump(gamelist, f)


wishlists_directory = "Wishlists/"
gamelist_directory = "Gamelists/"
app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_wishlist_games")
def root(userid: str = "", start: int = 10, end: int = 15):
    wishlist_data = load_json_wishlist(userid)
    gamelist = load_json_gamelist()
    wishlist_games = []
    for i in range(start, end):
        try:
            game_data = gamelist[f"{wishlist_data['items'][i]['appid']}"]
            wishlist_games.append(game_data)
        except:
            game_data = get_game_info(wishlist_data['items'][i]['appid'])
            gamelist[game_data['id']] = game_data
            wishlist_games.append(game_data)
    save_json_wishlist(wishlist_data, userid)
    save_json_gamelist(gamelist)
    return JSONResponse(content=jsonable_encoder(wishlist_games))

@app.get("/get_wishlist_size")
async def get_wishlist_size(userid: str = ""):
    try:
        data = load_json_wishlist(userid)
        print(len(data['items']))
        save_json_wishlist(data, userid)
        return {"data": len(data['items'])}
    except: print("Incorrect Steam UserID")
