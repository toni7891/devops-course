def main():
        
    car_brand = "Toyota"
    car_model = "Corola"
    car_year = 2012
    car_tank = 1.4

    car_list = [("Brand", car_brand), ("Model", car_model), ("Year", car_year), ("Tank", car_tank)]
    print(car_list)

    #dictionary in list
    cars = [
        {"brand": "Toyota",    "model": "Corolla",  "year": 2012, "tank": 1.4},
        {"brand": "Honda",     "model": "Civic",    "year": 2018, "tank": 1.5},
        {"brand": "Ford",      "model": "Mustang",  "year": 2020, "tank": 5.0},
        {"brand": "BMW",       "model": "M3",       "year": 2021, "tank": 3.0},
        {"brand": "Tesla",     "model": "Model 3",  "year": 2022, "tank": 0.0},
        {"brand": "Chevrolet", "model": "Camaro",   "year": 2019, "tank": 6.2},
        {"brand": "Audi",      "model": "A4",       "year": 2017, "tank": 2.0},
        {"brand": "Mercedes",  "model": "C-Class",  "year": 2023, "tank": 2.0},
        {"brand": "Hyundai",   "model": "Elantra",  "year": 2016, "tank": 2.0},
        {"brand": "Volkswagen","model": "Golf",     "year": 2015, "tank": 1.6},
    ]

    #single dict
    human_philip = {
        "name": "Philip",
        "age": 24,
        "color": "ASHKENAZ",
        "occupation": "Junior DevOps Engineer",
        "is_cool": True,
        "hobbies": ["Army", "Gaming", "Cars"]
    }

    #tup inside list
    philip_list = [
        ("name", "Philip"),
        ("age", 24),
        ("color", "ASHKENAZ"),
        ("occupation", "Junior DevOps Engineer"),
        ("is_cool", True),
        ("hobbies", ["Army", "Gaming", "Cars"]),
    ]

    print(philip_list[1][1])
    print(human_philip["age"])

if __name__ == "__main__":
    main()