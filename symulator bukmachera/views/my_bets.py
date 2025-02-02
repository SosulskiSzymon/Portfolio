import backend
import tkinter as tk
import random
from backend import load_user_parlays, get_current_user

# Kolory
BG_COLOR = "#1e1e2e"  # Ciemny fiolet
FG_COLOR = "#c792ea"  # Jasny fiolet
OTHFG_COLOR = "#3c3c52"
BTN_BG = "#292941"  # Fioletowy odcień
BTN_HOVER = "#3b3b58"
TEXT_COLOR = "white"



# Moje Kupony w profilu, funkcja wyświetlająca wszystkie kupony zalogowanego uzytkownika
def show_user_bets(balance_label):
    user = backend.get_current_user()               #przypisanie zalogowanego usera do zmiennej user
    user_login = user["login"]                      # przypisanie loginu usera do zmiennej user

    bets = backend.load_user_parlays(user_login)    # wczytanie kuponów zalogowanego użytkownika

    bets_window = tk.Toplevel()
    bets_window.title("Moje kupony")
    bets_window.geometry("400x600")
    bets_window.configure(bg=OTHFG_COLOR)
    bets_window.columnconfigure(0, weight=1)


    header_frame = tk.Frame(bets_window, bg=BG_COLOR)
    header_frame.grid(row=0, column=0, sticky="ew")
    header_frame.rowconfigure(0, weight=1)
    header_frame.columnconfigure(0, weight=0)
    header_frame.columnconfigure(1, weight=1)

    #przycisk powrotu do poprzedniego okna
    back_button = tk.Button(header_frame, text="↩", font=("Arial", 16), bg=OTHFG_COLOR, command=lambda: bets_window.destroy())
    back_button.grid(row=0, column=0, sticky="w", padx=(10,0))

    bets_title_label = tk.Label(header_frame, text="Twoje kupony:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 18, "bold"))
    bets_title_label.grid(row=0, column=1, sticky="nsw", padx=(40,0), pady=(5,15))

    if not bets:
        no_bets_label = tk.Label(bets_window, text="Nie masz jeszcze żadnych kuponów!", bg=FG_COLOR, font=("Arial", 12))
        no_bets_label.grid(row=1, column=0, sticky="ew")

        exit_button = backend.styled_button_4(bets_window, text="Wyjdź", width=15, command=bets_window.destroy)
        exit_button.grid(row=2, column=0, pady=10)

    else:

        all_bets_frame = tk.Frame(bets_window, bg=OTHFG_COLOR)
        all_bets_frame.grid(row=1, column=0, pady=10)
        all_bets_frame.columnconfigure(0, weight=0)
        all_bets_frame.rowconfigure(0, weight=0)

        # pętla wypisująca wszystkie kupony użytkownika razem z ich numeracją
        for i, bet in enumerate(bets):
            bet_button = backend.styled_button_4(all_bets_frame, text=f"Kupon {i+1}", command=lambda bet=bet: (bets_window.destroy(), show_bet_details(bet, balance_label)))
            bet_button.grid(row=i, column=0, sticky="ew", pady=5)

# szczegóły kuponu
def show_bet_details(bet,balance_label):

    bet_details_window = tk.Toplevel()
    bet_details_window.title("Szczegóły kuponu")
    bet_details_window.geometry("400x600")
    bet_details_window.resizable(False, False)
    bet_details_window.configure(bg=OTHFG_COLOR)
    bet_details_window.columnconfigure(0, weight=1)
    bet_details_window.rowconfigure((0,1), weight=0)
    bet_details_window.rowconfigure(2, weight=1)

    header_frame = tk.Frame(bet_details_window, bg=BG_COLOR)
    header_frame.grid(row=0, column=0, sticky="ew")
    header_frame.columnconfigure(0, weight=0)
    header_frame.columnconfigure(1, weight=1)

    back_button = tk.Button(header_frame, text="↩", font=("Arial", 16), bg=OTHFG_COLOR, command=lambda: (bet_details_window.destroy(), show_user_bets(balance_label)))
    back_button.grid(row=0, column=0, sticky="w", padx=(10,40))

    title_label = tk.Label(header_frame, text="Szczegóły kuponu", fg=FG_COLOR, bg=BG_COLOR, font=("Arial", 18, "bold"))
    title_label.grid(row=0, column=1, sticky="w", pady=(5,9))

    bets_details_frame = tk.Frame(bet_details_window, bg=OTHFG_COLOR)
    bets_details_frame.grid(row=1, column=0, sticky="ew")
    bets_details_frame.columnconfigure((0,1), weight=1)


# petla wypisujaca mecze i kursy danych meczy
    for idx, single_bet in enumerate(bet.get("bets")):
        i = idx * 3 #zmienna do poprawnego ułożenia gui i=numer wiersza

        bet_label = tk.Label(bets_details_frame, text=f"({single_bet[1]} vs {single_bet[2]})",font=("Arial", 12), bg=OTHFG_COLOR)
        bet_label.grid(row=i, column=0, columnspan=2, sticky="ew", pady=(15,8))

        result_label = tk.Label(bets_details_frame, text=f"{single_bet[3]}", font=("Arial", 12, "bold"), bg=OTHFG_COLOR)
        result_label.grid(row=i+1, column=0, sticky="ew")

        odd_label = tk.Label(bets_details_frame, text=f"Kurs: {single_bet[0]}", font=("Arial", 12), bg=OTHFG_COLOR)
        odd_label.grid(row=i+1, column=1, sticky="ew")

        linia = tk.Canvas(bets_details_frame, height=2, bg="black", bd=0, highlightthickness=0)
        linia.grid(sticky="nsew", row=i+2, column=0, columnspan=2, pady=5)

    footer_frame_bet = tk.Frame(bet_details_window, bg=BG_COLOR)
    footer_frame_bet.grid(row=2, column=0, sticky="sew")
    footer_frame_bet.columnconfigure(0, weight=1)
    footer_frame_bet.rowconfigure(0, weight=1)

    if bet.get('status') == "active":   #gui kiedy kupon jest aktywny (oczekujący)
        parlay_simulator_button = tk.Button(bet_details_window, text="Rozlicz kupon (Symulacja)", font=("Arial", 15), command=lambda: parlay_simulator(balance_label, win_label, parlay_simulator_button, bet))
        parlay_simulator_button.grid(row=3, column=0, sticky="sew")
        win_label = tk.Label(footer_frame_bet, text=f"Potencjalna wygrana: {bet.get('potential_win')} PLN", font=("Arial", 15, "bold"), bg=BG_COLOR, fg=FG_COLOR)
        win_label.grid(row=0, column=0, sticky="sew")

    elif bet.get('status') == "lost":   #gui kiedy kupon okazał się przegrany
        win_label = tk.Label(footer_frame_bet, text="Kupon przegrany", font=("Arial", 15, "bold"), fg="red", bg=BG_COLOR)
        win_label.grid(row=0, column=0, sticky="sew")

    else:   #gui kiedy kupon okazał się wygrany
        win_label = tk.Label(footer_frame_bet, text=f"Wygrana: {bet.get('potential_win')} PLN", font=("Arial", 15, "bold"), fg="green", bg=BG_COLOR)
        win_label.grid(row=0, column=0, sticky="sew")


#symulacja wyniku kuponu, zmiana gui w przypadku wygranej/przegranej oraz zapisy do pliku
def parlay_simulator(balance_label, win_label, parlay_simulator_button, bet):
    win_or_lose = random.choice([True, False]) #losowanie 50/50

    if win_or_lose is False:
        win_label.configure(text="Kupon przegrany", fg="red")     #jeśli kupon jest przegrany
        parlay_simulator_button.grid_forget()
        bet['status'] = "lost"                          #zmiana statusu na przegrany

    else:
        parlay_simulator_button.grid_forget()           #jeśli kupon jest wygrany
        bet['status'] = "won"                           #zmiana statusu na wygrany
        win_label.configure(text=f"Wygrana: {bet.get('potential_win')} PLN", fg="green") #zmiana napisu

        current_user = backend.get_current_user()
        win = round(float(bet.get('potential_win')), 2) #zaokrąglenie wygranej do 2 miejsc po przecinku
        current_user['balance'] += win  #dodania salda użytkownikowi
        current_user['balance'] = round(current_user['balance'], 2)

        users = backend.load_users()
        for user in users:
            if user["login"] == current_user["login"]:      #zapisanie nowego salda do pliku
                user["balance"] = current_user["balance"]
                break
        backend.save_users(users)

        balance_label.config(text=f"Saldo: {current_user['balance']} PLN") #aktualizacja nowego salda w gui

    backend.update_bet_status(bet) #aktualizacja statusu kuponu na wygrany/przegrany




