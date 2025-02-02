import random
import bcrypt
import json
import tkinter as tk

current_user = None
main_teams = ["Drużyna A", "Drużyna B", "Drużyna C", "Drużyna D","Drużyna E", "Drużyna F", "Drużyna G", "Drużyna H", "Drużyna I", "Drużyna J", "Drużyna K", "Drużyna L", "Drużyna M", "Drużyna N"]
basketball_teams = ["Koszykówka A", "Koszykówka B", "Koszykówka C", "Koszykówka D", "Koszykówka E", "Koszykówka F", "Koszykówka G", "Koszykówka H", "Koszykówka I", "Koszykówka J", "Koszykówka K", "Koszykówka L", "Koszykówka M", "Koszykówka N"]
volleyball_teams = ["Siatkówka A", "Siatkówka B", "Siatkówka C", "Siatkówka D", "Siatkówka E", "Siatkówka F", "Siatkówka G", "Siatkówka H", "Siatkówka I", "Siatkówka J", "Siatkówka K", "Siatkówka L", "Siatkówka M", "Siatkówka N"]
hockey_teams = ["Hokej A", "Hokej B", "Hokej C", "Hokej D", "Hokej E", "Hokej F", "Hokej G", "Hokej H", "Hokej I", "Hokej J", "Hokej K", "Hokej L", "Hokej M", "Hokej N"]
football_teams = ["Piłka nożna A", "Piłka nożna B", "Piłka nożna C", "Piłka nożna D", "Piłka nożna E", "Piłka nożna F", "Piłka nożna G", "Piłka nożna H", "Piłka nożna I", "Piłka nożna J", "Piłka nożna K", "Piłka nożna L", "Piłka nożna M", "Piłka nożna N"]

# Wczytujemy dane użytkowników z plik JSON
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  #  jesli plik nie istnieje = pusta lista



#  zapisuje  users data do pliku json
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)


# rejestracja
def register_user(login, password, age):
    users = load_users()

    # sprawdza czy taki login istnieje
    for user in users:
        if user['login'] == login:
            print("Login już istnieje!")
            return False

     # haszowanie hasła
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # dodajemy nowego usera do listy users
    users.append({
        'login': login,
        'password': hashed_password.decode('utf-8'),  # Dekodowanie hasła do formatu tekstowego
        'age': age,
        'balance': 0  # Początkowe saldo
    })

    # Zmodyfikowana lista zapisywana w pliku
    save_users(users)
    print("Rejestracja zakończona pomyślnie!")
    return True



# logowanie
def login_user(login, password):
    users = load_users()

    # szukanie userów na liscie
    for user in users:
        if user['login'] == login:
            # Sprawdzamy poprawność hasła
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                print("Zalogowano pomyślnie!")

                return True
            else:
                print("Błędne hasło!")
                return False

    print("Nie znaleziono użytkownika!")
    return False



#pobranie danych aktywnego użytkownika
def get_user_data(login):
    users = load_users()
    for user in users:
        if user["login"] == login:
            return user


#ustawianie aktualnie zalogowanego usera - setter
def set_current_user(user):
    global current_user
    current_user = user

#wziecie danych o aktualnie zalogowanym userze - getter
def get_current_user():
    global current_user
    return current_user


#wybór drużyn do wyświetlenia z parametrami teams = lista drużyn któregoś ze sportów, num_teams = liczba drużyn
def select_multiple_teams(teams,num_teams):
    return random.sample(teams,num_teams) #random.sample bierze unikalne drużyny z kolekcji


# zapisywanie kuponu do pliku bets.json
def save_bet(bet_data):
    with open('bets.json', 'r') as f:
        bets = json.load(f)
    bets.append(bet_data)

    with open('bets.json', 'w') as f:
        json.dump(bets, f, indent=4)


# przypisywanie kuponu do zalogowanego uzytkownika w users.json
def add_bet_to_user(user_login, bet_id):
    users = load_users()
    for user in users:
        if user["login"] == user_login:
            if "bets" not in user:
                user["bets"] = []
            user["bets"].append(bet_id)
            break
    save_users(users)


# funkcja zwracajaca wszystkie kupony zalogowanego uzytkownika
def load_user_parlays(user_login):
    with open('bets.json', 'r') as f:
        bets = json.load(f)
    user_bets = [bet for bet in bets if bet["user"] == user_login] # jeśli twórcą zakładu jest zalogowany użytkownik, przypisuje zakład do zmiennej user_bets
    return user_bets


# funkcja zmieniająca status kuponu po jego symulacji
def update_bet_status(updated_bet):
    with open('bets.json', 'r') as f:
        bets = json.load(f)

        for i,bet in enumerate(bets):               #w pliku bets.json szuka kuponu "bet" o odpowiednim id i zmienia jego status
            if bet["id"] == updated_bet["id"]:
                bets[i] = updated_bet
                break
        with open('bets.json', 'w') as f:       #zapis pliku
            json.dump(bets, f, indent=4)

BG_COLOR = "#1e1e2e"  # Ciemny fiolet
FG_COLOR = "#c792ea"  # Jasny fiolet
BTN_BG = "#292941"  # Fioletowy odcień
BTN_HOVER = "#3b3b58"
TEXT_COLOR = "white"

def on_enter(e):
    e.widget["bg"] = BTN_HOVER

def on_leave(e):
    e.widget["bg"] = BTN_BG

def styled_button(parent, text, command, **args):
    btn = tk.Button(parent, text=text, font=('Arial', 12), bg=BTN_BG, fg=TEXT_COLOR, activebackground=BTN_HOVER, activeforeground=TEXT_COLOR, command=command, bd=0, relief='flat')
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def styled_button_2(parent, text, command):
    btn = tk.Button(parent, text=text, font=('Arial', 12), bg=BTN_BG, fg=TEXT_COLOR, activebackground=BTN_HOVER, activeforeground=TEXT_COLOR, command=command, bd=0, relief='flat', padx=10, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def styled_button_3(parent, text, **args):
    btn = tk.Button(parent, text=text, font=('Arial', 10), bg=BTN_BG, fg=TEXT_COLOR, activebackground=BTN_HOVER, activeforeground=TEXT_COLOR, bd=1, relief='flat', padx=20, pady=20)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def styled_button_4(parent, text, command, **args):
    btn = tk.Button(parent, text=text, font=('Arial', 12), bg=BTN_BG, fg=TEXT_COLOR, activebackground=BTN_HOVER, activeforeground=TEXT_COLOR, command=command, bd=0, relief='flat', padx=70, pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn
