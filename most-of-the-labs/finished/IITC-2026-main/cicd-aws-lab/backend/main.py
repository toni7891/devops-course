from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DataBite API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---

class MenuItem(BaseModel):
    id: int
    name: str
    price: float
    category: str
    restaurant: str


class Restaurant(BaseModel):
    id: int
    name: str
    cuisine: str
    location: str
    menu_items: int
    rating: float


class Stats(BaseModel):
    total_restaurants: int
    total_menu_items: int
    cuisines_tracked: int
    cities_covered: int


# --- Mock Data ---

RESTAURANTS = [
    Restaurant(id=1, name="La Piazza", cuisine="Italian", location="Tel Aviv", menu_items=45, rating=4.7),
    Restaurant(id=2, name="Sakura", cuisine="Japanese", location="Herzliya", menu_items=62, rating=4.5),
    Restaurant(id=3, name="The Burger Joint", cuisine="American", location="Tel Aviv", menu_items=28, rating=4.2),
    Restaurant(id=4, name="Falafel King", cuisine="Middle Eastern", location="Jerusalem", menu_items=18, rating=4.8),
    Restaurant(id=5, name="Pasta Mia", cuisine="Italian", location="Haifa", menu_items=37, rating=4.4),
    Restaurant(id=6, name="Dragon Palace", cuisine="Chinese", location="Tel Aviv", menu_items=55, rating=4.3),
]

MENU_ITEMS = [
    MenuItem(id=1, name="Margherita Pizza", price=52.0, category="Main", restaurant="La Piazza"),
    MenuItem(id=2, name="Carbonara", price=58.0, category="Main", restaurant="La Piazza"),
    MenuItem(id=3, name="Tiramisu", price=38.0, category="Dessert", restaurant="La Piazza"),
    MenuItem(id=4, name="Salmon Sashimi", price=68.0, category="Starter", restaurant="Sakura"),
    MenuItem(id=5, name="Dragon Roll", price=72.0, category="Main", restaurant="Sakura"),
    MenuItem(id=6, name="Miso Soup", price=22.0, category="Starter", restaurant="Sakura"),
    MenuItem(id=7, name="Classic Burger", price=62.0, category="Main", restaurant="The Burger Joint"),
    MenuItem(id=8, name="Sweet Potato Fries", price=28.0, category="Side", restaurant="The Burger Joint"),
    MenuItem(id=9, name="Falafel Plate", price=35.0, category="Main", restaurant="Falafel King"),
    MenuItem(id=10, name="Hummus", price=25.0, category="Starter", restaurant="Falafel King"),
    MenuItem(id=11, name="Kung Pao Chicken", price=56.0, category="Main", restaurant="Dragon Palace"),
    MenuItem(id=12, name="Spring Rolls", price=32.0, category="Starter", restaurant="Dragon Palace"),
]


# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "DataBite API", "version": "1.0.0"}


@app.get("/api/stats", response_model=Stats)
def get_stats():
    cuisines = set(r.cuisine for r in RESTAURANTS)
    cities = set(r.location for r in RESTAURANTS)
    return Stats(
        total_restaurants=len(RESTAURANTS),
        total_menu_items=len(MENU_ITEMS),
        cuisines_tracked=len(cuisines),
        cities_covered=len(cities),
    )


@app.get("/api/restaurants", response_model=List[Restaurant])
def get_restaurants():
    return RESTAURANTS


@app.get("/api/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int):
    for r in RESTAURANTS:
        if r.id == restaurant_id:
            return r
    return {"error": "Restaurant not found"}


@app.get("/api/menu-items", response_model=List[MenuItem])
def get_menu_items(restaurant: Optional[str] = None, category: Optional[str] = None):
    items = MENU_ITEMS
    if restaurant:
        items = [i for i in items if i.restaurant.lower() == restaurant.lower()]
    if category:
        items = [i for i in items if i.category.lower() == category.lower()]
    return items
