import tkinter as tk
import uuid
import backend
from backend import save_bet, add_bet_to_user
from tkinter import messagebox

selected_bets = []
details_window = None
bets_frame = None
total_odds = 1

# Kolory
BG_COLOR = "#1e1e2e"  # Ciemny fiolet
FG_COLOR = "#c792ea"  # Jasny fiolet
BTN_BG = "#292941"  # Fioletowy odcień
BTN_HOVER = "#3b3b58"
TEXT_COLOR = "white"


def creating_parlay(balance_label):
    global selected_bets, details_window, bets_frame, total_odds, total_odds_label, canvas, bet_amount_entry, potential_win_label

    if len(selected_bets) == 0:
        messagebox.showinfo(None, "Nie masz wybranych żadnych zakładów")
    else:
        if not details_window or not details_window.winfo_exists():
            details_window = tk.Toplevel()
            details_window.title("Tworzenie kuponu")
            details_window.geometry("400x600")
            details_window.resizable(False, False)
            details_window.configure(bg=BG_COLOR)
            details_window.rowconfigure((0,2,3,4,5), weight=0)
            details_window.rowconfigure(1, weight=1)
            details_window.columnconfigure(0, weight=1)

            title_chosen_event_label = tk.Label(details_window, text=f"Wybrane zakłady:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14))
            title_chosen_event_label.grid(row=0, column= 0,columnspan=2, pady=(10,20))

            # scrollbar
            canvas = tk.Canvas(details_window, bg="#3c3c52", border=2, highlightthickness=0)
            canvas.grid(row=1, column=0, sticky="nsew", padx=10)
            canvas.columnconfigure(0, weight=1)

            scrollbar = tk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
            scrollbar.grid(row=1, column=1, sticky="ns")

            canvas.configure(yscrollcommand=scrollbar.set)

            # frame na wybrane zakłady
            bets_frame = tk.Frame(canvas, bg="#3c3c52")
            bets_frame.columnconfigure(0, weight=1)
            bets_frame.columnconfigure(1, weight=0)
            canvas.create_window((0,0), window=bets_frame, anchor="nw")

            def configure_scrollregion(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            bets_frame.bind("<Configure>", configure_scrollregion)

            total_odds_label = tk.Label(details_window, text=f"Łączny kurs zakładu: {total_odds:.2f}", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
            total_odds_label.grid(row=2, column=0, pady=(0,3))

            # frame na kwote zakładu
            bet_amount_frame = tk.Frame(details_window)
            bet_amount_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(10,10))
            bet_amount_frame.columnconfigure(0, weight=0)
            bet_amount_frame.columnconfigure(1, weight=1)

            bet_amount_label = tk.Label(bet_amount_frame, text="Kwota zakładu: ", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
            bet_amount_label.grid(row=0, column=0, sticky="w")

            bet_amount_entry = tk.Entry(bet_amount_frame, font=('Arial', 12), bg="#2c2c2c", fg="#ffffff", border= 2,  insertbackground="#ffffff")
            bet_amount_entry.grid(row=0, column=1, sticky="ew")

            # Label dla wygranej
            potential_win_label = tk.Label(details_window, text="Potencjalna wygrana: 0.00 PLN", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
            potential_win_label.grid(row=4, column=0, pady=(10, 10))

            # Dodanie eventu do Entry
            bet_amount_entry.bind("<KeyRelease>", lambda event: update_potential_win())

            # frame na przyciski dolne
            button_frame = tk.Frame(details_window, bg=BG_COLOR)
            button_frame.grid(row=5, column=0, sticky="ew", pady=10)
            button_frame.columnconfigure((0,1,2), weight=1)


            exit_button = backend.styled_button_2(button_frame, text="Zamknij", command=details_window.destroy)
            exit_button.grid(row=0, column=2, padx=10)

            clear_button = backend.styled_button_2(button_frame, text="Wyczyść kupon", command=lambda: clear_bets())
            clear_button.grid(row=0, column=1, padx=10)

            place_bet_button = backend.styled_button_2(button_frame, text="Postaw zakład", command=lambda: place_bet(bet_amount_entry, balance_label))
            place_bet_button.grid(row=0, column=0, padx=10)


        update_bets_display()
        update_total_odd()

#funkcja wyświetlająca wybrane zakłady na stawianym kuponie
def update_bets_display():
    global selected_bets, bets_frame, potential_win_label, total_odds_label

    #usuwanie zakładów żeby w przypadku zamknięcia i ponownym otwarciu stawianego kuponu zakłady nie duplikowały się
    for x in bets_frame.winfo_children():
        x.destroy()

    row_index = 1

    # wypisywanie wybranych zakładów
    for bet in selected_bets:
        if bet[3] == "Remis":  # Zakład na remis
            chosen_event_game_label = tk.Label(bets_frame, text=f"{bet[1]} vs {bet[2]}", font=("Arial", 12), bg="#3c3c52")
            chosen_event_game_label.grid(sticky="nsew", row=row_index, column=0, padx=10, pady=5)

            delete_event_button = tk.Button(bets_frame, text="X", font=("Arial", 12), width=2, command=lambda bet=bet: (delete_bet(bet), check_if_empty()))
            delete_event_button.grid(sticky="e", row=row_index, column=1, padx=(0,15))

            chosen_event_label = tk.Label(bets_frame, text="Remis", font=("Arial", 12, "bold"), bg="#3c3c52")
            chosen_event_label.grid(sticky="nsew", row=row_index + 1, column=0, padx=10, pady=5)

            chosen_event_odd_label = tk.Label(bets_frame, text=f"Kurs: {bet[0]:.2f}", font=("Arial", 12), bg="#3c3c52")
            chosen_event_odd_label.grid(sticky="nsew", row=row_index + 1, column=1, padx=15, pady=5)

        else:  # Zakład na drużynę
            chosen_event_game_label = tk.Label(bets_frame, text=f"{bet[1]} vs {bet[2]}", font=("Arial", 12), bg="#3c3c52")
            chosen_event_game_label.grid(sticky="nsew", row=row_index, column=0, padx=10, pady=5)

            delete_event_button = tk.Button(bets_frame, text="X", font=("Arial", 12), width=2, command=lambda bet=bet: (delete_bet(bet), check_if_empty()))
            delete_event_button.grid(sticky="e", row=row_index, column=1, padx=(0,15))

            chosen_event_label = tk.Label(bets_frame, text=f"{bet[1]}", font=("Arial", 12, "bold"), bg="#3c3c52")
            chosen_event_label.grid(sticky="nsew", row=row_index + 1, column=0, padx=10, pady=5)

            chosen_event_odd_label = tk.Label(bets_frame, text=f"Kurs: {bet[0]:.2f}", font=("Arial", 12), bg="#3c3c52")
            chosen_event_odd_label.grid(sticky="nsew", row=row_index + 1, column=1, padx=15, pady=5)

        # linia oddzielajaca zaklady
        linia = tk.Canvas(bets_frame, height=2, bg="black", bd=0, highlightthickness=0)
        linia.grid(sticky="nsew", row=row_index + 2, column=0, columnspan=2, pady=5)

        # ustawianie zakładow w odpowiednich wierszach
        row_index = row_index + 3

        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

# dodawanie zakladow do kuponu
def add_bet(team, team1, odds, balance_label, result):
    global selected_bets, total_odds

    #sprawdzenie czy wybrany mecz jest już na kuponie
    if any((team == bet[1] and team1 == bet[2] or (team1 == bet[1] and team == bet[2])) for bet in selected_bets):
        messagebox.showerror("Błąd", "Ten mecz jest już na twoim kuponie")
        return

    #dodanie zakładu do listy wybranych zakładów (selected_bets)
    selected_bets.append((round(odds,2), team, team1, result))

    #zliczenie kursów
    total_odds = total_odds * odds
    messagebox.showinfo(None, "Dodano zakład do kuponu")
    creating_parlay(balance_label) #ponowne wywołanie okna ze stawianym kuponem po dodaniu kolejnego zakładu
    update_potential_win()

def update_total_odd():
    global total_odds_label, total_odds

    total_odds = 1
    for bet in selected_bets:
        total_odds = total_odds * bet[0]    #z każdego zakładu zliczany jest łączny kurs do globalnej zmiennej total_odds

    if total_odds_label is not None:
        total_odds_label.config(text=f"Łączny kurs zakładu: {total_odds:.2f}")

#zatwierdzanie zakładu
def place_bet(bet_amount_entry, balance_label):
    global selected_bets, total_odds, details_window

    current_user = backend.get_current_user()   #getter aktualnie zalogowane użytkownika
    bet_amount_entry_str = bet_amount_entry.get().replace(",", ".") #zastąpienie przecinka kropką w celu unikniecia błędów

    try:
        bet_amount = float(bet_amount_entry_str)
    except ValueError:
        messagebox.showerror("Błąd", "Podaj poprawną kwotę zakładu.")
        return

    if len(selected_bets) == 0:
        messagebox.showerror("Błąd", "Nie wybrałeś żadnego zakładu!")
        return

    if bet_amount <= 0:
        messagebox.showerror("Błąd", "Kwota zakładu musi być większa niż zero.")
        return

    if current_user is None:
        messagebox.showerror("Błąd", "Musisz się zalogować.")
        return

    if current_user['balance'] < bet_amount:
        messagebox.showerror("Błąd", "Niewystarczające środki na koncie.")
        return

    total_win = round(bet_amount * total_odds, 2)       #podliczenie ewentualnej wygranej
    current_user['balance'] -= round(bet_amount, 2)     # odjecie od salda kwoty za ktora postawiono kupon


    # zapisanie nowego salda do pliku
    users = backend.load_users()

    for user in users:
        if user["login"] == current_user["login"]:
            user["balance"] = current_user["balance"]
            break

    backend.save_users(users)

    bet_id = str(uuid.uuid4()) # identyfikator kuponu

# wzor slownika dla postawionego kuponu
    bet_data = {
        "id": bet_id,
        "bets": selected_bets,
        "user": current_user["login"],
        "amount": bet_amount,
        "total_odds": round(total_odds,2),
        "potential_win": total_win,
        "status": "active"
    }
    save_bet(bet_data)
    add_bet_to_user(current_user["login"], bet_id) #przypisanie zakładu do usera wraz z id

    messagebox.showinfo("Zakład postawiony!", f"Do wygrania: {total_win:.2f} PLN")

    balance_label.config(text=f"Saldo: {current_user['balance']} PLN")

    # zresetowanie danych
    selected_bets = []
    total_odds = 1
    update_total_odd()
    details_window.destroy()

#usuwanie pojedynczego zakladu
def delete_bet(bet):
    global selected_bets, total_odds

    selected_bets.remove(bet)
    update_total_odd()
    update_potential_win()
    update_bets_display()

# sprawdzenie czy kupon nie jest pusty
def check_if_empty():
    global selected_bets, details_window
    if len(selected_bets) == 0:
        details_window.destroy()

#wyczyszczenie wybranych zakładów
def clear_bets():
    global selected_bets, total_odds, details_window
    selected_bets = []
    total_odds = 1
    update_total_odd()
    update_potential_win()
    details_window.destroy()

#obliczanie potencjalnej wygranej
def update_potential_win():
    global total_odds, bet_amount_entry, potential_win_label

    try:
        bet_amount = float(bet_amount_entry.get().replace(",", ".")) #zastapienie przecinka kropką
    except ValueError:
        bet_amount = 0.0

    potential_win = round(bet_amount * total_odds, 2) #obliczenie potencjalnej wygranej i zaokraglenie do 2 miejsc po przecinku

    potential_win_label.config(text=f"Potencjalna wygrana: {potential_win} PLN")