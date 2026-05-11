INCIDENTS = [
    {
        "id": "П-2024-0891",
        "type": "Пожар",
        "address": "ул. Александровска 45, Бургас",
        "status": "active",
        "severity": "high",
        "team": "Екип Алфа",
        "time": "14:32",
        "gps": {"lat": 42.4975, "lng": 27.4715},
        "hazmat": "Пропан-бутан",
        "tasks": [
            {"label": "Оглед на обекта",          "done": True},
            {"label": "Евакуация на жителите",    "done": True},
            {"label": "Гасене на огъня",           "done": False},
            {"label": "Доставка на вода — цистерна","done": False},
        ],
    },
    {
        "id": "П-2024-0890",
        "type": "ПТП",
        "address": "АМ Тракия, км 310",
        "status": "active",
        "severity": "medium",
        "team": "Екип Бета",
        "time": "13:10",
        "gps": {"lat": 42.3845, "lng": 27.1921},
        "hazmat": None,
        "tasks": [
            {"label": "Осигуряване на периметър", "done": True},
            {"label": "Изваждане на пострадали",  "done": False},
        ],
    },
    {
        "id": "П-2024-0889",
        "type": "Газова авария",
        "address": "бул. Демокрация 12, Бургас",
        "status": "closed",
        "severity": "high",
        "team": "Екип Гама",
        "time": "09:45",
        "gps": {"lat": 42.5012, "lng": 27.4682},
        "hazmat": "Природен газ",
        "tasks": [
            {"label": "Евакуация",                "done": True},
            {"label": "Изолиране на газа",        "done": True},
        ],
    },
    {
        "id": "П-2024-0888",
        "type": "Наводнение",
        "address": "с. Дебелт",
        "status": "closed",
        "severity": "low",
        "team": "Екип Делта",
        "time": "07:20",
        "gps": {"lat": 42.3312, "lng": 27.2541},
        "hazmat": None,
        "tasks": [
            {"label": "Изпомпване на вода",       "done": True},
        ],
    },
]

TEAMS = [
    {"id": 1, "name": "Екип Алфа",    "vehicle": "БА-01 (Mercedes Actros)", "members": 5, "available": 5, "status": "deployed",  "incident": "П-2024-0891"},
    {"id": 2, "name": "Екип Бета",    "vehicle": "БА-02 (Scania P360)",      "members": 4, "available": 4, "status": "deployed",  "incident": "П-2024-0890"},
    {"id": 3, "name": "Екип Гама",    "vehicle": "БА-03 (MAN TGM)",          "members": 6, "available": 5, "status": "standby",   "incident": None},
    {"id": 4, "name": "Екип Делта",   "vehicle": "БА-04 (Iveco Magirus)",    "members": 5, "available": 3, "status": "standby",   "incident": None},
    {"id": 5, "name": "Екип Епсилон", "vehicle": "БА-05 (Mercedes Unimog)",  "members": 4, "available": 0, "status": "offduty",   "incident": None},
]

STAFF = [
    {"id": 1, "name": "ст. инсп. Петров Г.",    "team": "Екип Алфа",    "role": "Командир",    "status": "deployed"},
    {"id": 2, "name": "инсп. Иванов Д.",         "team": "Екип Алфа",    "role": "Пожарникар",  "status": "deployed"},
    {"id": 3, "name": "инсп. Колева М.",          "team": "Екип Гама",    "role": "Пожарникар",  "status": "standby"},
    {"id": 4, "name": "инсп. Симеонов Р.",        "team": "Екип Делта",   "role": "Пожарникар",  "status": "leave"},
    {"id": 5, "name": "инсп. Тодорова С.",        "team": "Екип Делта",   "role": "Пожарникар",  "status": "sick"},
    {"id": 6, "name": "ст. инсп. Маринов К.",     "team": "Екип Епсилон", "role": "Командир",    "status": "offduty"},
]

VEHICLES = [
    {"id": "БА-01", "model": "Mercedes Actros 1840", "type": "Автостълба",       "year": 2019, "status": "deployed",    "fuel": 72, "crew": "Екип Алфа"},
    {"id": "БА-02", "model": "Scania P360",           "type": "Цистерна",         "year": 2021, "status": "deployed",    "fuel": 55, "crew": "Екип Бета"},
    {"id": "БА-03", "model": "MAN TGM 18.290",        "type": "Пожарен автомобил","year": 2020, "status": "standby",    "fuel": 91, "crew": "Екип Гама"},
    {"id": "БА-04", "model": "Iveco Magirus",          "type": "Цистерна",         "year": 2018, "status": "standby",    "fuel": 38, "crew": "Екип Делта"},
    {"id": "БА-05", "model": "Mercedes Unimog U430",  "type": "Теренен",          "year": 2022, "status": "maintenance","fuel": 60, "crew": None},
]

SCHEDULE = [
    {"name": "ст. инсп. Петров Г.",  "team": "Екип Алфа",    "shift": "08:00–20:00", "leave": None,            "sick": False},
    {"name": "инсп. Иванов Д.",       "team": "Екип Алфа",    "shift": "08:00–20:00", "leave": None,            "sick": False},
    {"name": "инсп. Колева М.",        "team": "Екип Гама",    "shift": "08:00–20:00", "leave": None,            "sick": False},
    {"name": "инсп. Симеонов Р.",      "team": "Екип Делта",   "shift": "—",           "leave": "12.01–18.01",   "sick": False},
    {"name": "инсп. Тодорова С.",      "team": "Екип Делта",   "shift": "—",           "leave": None,            "sick": True},
    {"name": "ст. инсп. Маринов К.",   "team": "Екип Епсилон", "shift": "20:00–08:00", "leave": None,            "sick": False},
]
