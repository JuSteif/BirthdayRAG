import random
import json
from datetime import datetime, timedelta

# 200 englische und asiatische Vornamen
first_names = [
    # Englisch (Beispiele)
    "Aaron", "Abigail", "Adam", "Alex", "Alice", "Amy", "Andrew", "Angela", "Arthur", "Ava",
    "Benjamin", "Bella", "Blake", "Brianna", "Brian", "Brooke", "Bruce", "Brandon", "Bryan", "Brittany",
    "Cameron", "Catherine", "Charles", "Charlotte", "Chloe", "Christian", "Christine", "Christopher", "Claire", "Cole",
    "Daniel", "David", "Diana", "Dominic", "Donna", "Dylan", "Derek", "Deborah", "Denise", "Douglas",
    "Edward", "Ella", "Emily", "Eric", "Emma", "Ethan", "Evelyn", "Evan", "Elijah", "Elizabeth",
    "Faith", "Fiona", "Frank", "Freddie", "Florence", "Felicia", "Felicity", "Francis", "Finn", "Faye",
    "George", "Grace", "Graham", "Gloria", "Gabriel", "Gavin", "Giselle", "Grant", "Genevieve", "Gemma",
    "Hannah", "Harry", "Heather", "Henry", "Hailey", "Hunter", "Holly", "Harvey", "Hope", "Howard",
    "Isabella", "Isaac", "Ian", "Ivy", "Irene", "Imogen", "Iris", "Isabel", "Indigo", "Ignacio",
    "Jack", "Jacob", "Jasmine", "Jason", "Jenna", "Jessica", "Jeremy", "Jonathan", "Joseph", "Julia",
    "Katherine", "Kevin", "Kimberly", "Kayla", "Kyle", "Kendra", "Keith", "Kelly", "Kurt", "Kara",
    # Asiatisch (Beispiele, gemischt aus chinesischen, japanischen, koreanischen, vietnamesischen Namen)
    "Akira", "Aiko", "Aya", "Bao", "Binh", "Bo", "Chen", "Chun", "Chiyo", "Daiki",
    "Daisuke", "Dung", "Emi", "Eun", "Fang", "Fumi", "Guo", "Hana", "Hiro", "Huan",
    "Hyun", "Isamu", "Jia", "Jin", "Jiro", "Kai", "Kenji", "Lan", "Li", "Linh",
    "Mai", "Manami", "Mei", "Min", "Minh", "Miho", "Nao", "Nam", "Ngoc", "Nori",
    "Ping", "Qi", "Qing", "Ran", "Riku", "Ryota", "Sang", "Shin", "Sho", "Soo",
    "Tian", "Tomo", "Trang", "Tuan", "Wei", "Xiao", "Xin", "Yasu", "Yoko", "Yuna",
    "Yuri", "Zhen", "Zhi", "Zhu", "Zhiyuan", "Zixin", "Ying", "Ling", "Shuang", "Hui"
]

# 250 englische und asiatische Nachnamen
last_names = [
    # Englisch
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
    # Asiatisch (Beispiele)
    "Wong", "Chen", "Zhang", "Li", "Liu", "Yang", "Huang", "Zhao", "Wu", "Xu",
    "Sun", "Ma", "Zhou", "Hu", "Zhu", "Gao", "Lin", "He", "Guo", "Luo",
    "Tang", "Han", "Feng", "Peng", "Fan", "Cai", "Lu", "Wei", "Xie", "Shi",
    "Yamamoto", "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Nakamura", "Kobayashi", "Yoshida",
    "Yamada", "Sasaki", "Yamaguchi", "Matsumoto", "Inoue", "Kimura", "Hayashi", "Shimizu", "Nakajima", "Morita",
    "Park", "Choi", "Jeong", "Cho", "Kang", "Yoon", "Im", "Han", "Seo", "Jung",
    "Tran", "Nguyen", "Pham", "Le", "Hoang", "Vo", "Dang", "Bui", "Do", "Duong",
    "Dao", "Dinh", "Ngo", "Hua", "Quach", "Chau", "Ngoc", "Quyen", "Phan", "Loc",

    "Müller", "Schmidt", "Schneider", "Fischer", "Weber",
    "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",

    # Französisch (10)
    "Bernard", "Dubois", "Robert", "Richard", "Petit",
    "Durand", "Leroy", "Moreau", "Simon", "Laurent",

    # Italienisch (10)
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi",
    "Romano", "Ricci", "Marino", "Greco", "Gallo",

    # Russisch (10)
    "Ivanov", "Smirnov", "Kuznetsov", "Popov", "Petrov",
    "Sokolov", "Lebedev", "Morozov", "Novikov", "Fedorov",

    # Polnisch (10)
    "Nowak", "Kowalski", "Wiśniewski", "Wójcik", "Kowalczyk",
    "Kamiński", "Lewandowski", "Zieliński", "Szymański", "Dąbrowski",

    # Nigerianisch (10)
    "Okafor", "Adeyemi", "Chukwu", "Adebayo", "Eze",
    "Ibrahim", "Mohammed", "Musa", "Obasanjo", "Nwosu",

    # Arabisch (10)
    "Hussein", "Abbas", "Khalil", "Nasser", "Hamdan",
    "Khatib", "Haddad", "Saleh", "Faraj", "Tawfiq",

    # Indisch (10)
    "Kumar", "Singh", "Sharma", "Khan", "Gupta",
    "Reddy", "Iyer", "Choudhary", "Pillai", "Nair",

    # Türkisch (10)
    "Yılmaz", "Kaya", "Demir", "Şahin", "Çelik",
    "Yıldırım", "Aydin", "Arslan", "Öztürk", "Polat",

    # Griechisch (10)
    "Papadopoulos", "Papadakis", "Nikolaou", "Georgiou", "Vassiliou",
    "Christodoulou", "Anastasiou", "Konstantinou", "Pappas", "Angelopoulos"
]

def generate_random_birthdate():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2010, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_birth_date = start_date + timedelta(days=random_number_of_days)
    return random_birth_date.day, random_birth_date.month, random_birth_date.year

# Generiere 200 zufällige Personen
people = []
for _ in range(2000):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    day, month, year = generate_random_birthdate()
    person = {
        "firstname": first_name,
        "lastname": last_name,
        "day": day,
        "month": month,
        "year": year
    }
    people.append(person)

# Ausgabe als JSON-String
json_output = json.dumps(people, indent=2, ensure_ascii=False)
print(json_output)
with open('birthdays.json', 'w', encoding='utf-8') as f:
    json.dump(people, f, ensure_ascii=False, indent=2)
