import tkinter as tk
import random
import backend
from backend import select_multiple_teams
from views.create_parlay import add_bet

# slownik dla wylosowanych drużyn danych kategorii
selected_teams_for_each_category_dict = {
    "main_window": None,
    "football": None,
    "basketball": None,
    "volleyball": None,
    "hockey": None
}
# slownik dla kursów dla danych kategorii
selected_odds_for_each_category_dict = {
    "main_window": None,
    "football": None,
    "basketball": None,
    "volleyball": None,
    "hockey": None
}

BG_COLOR = "#1e1e2e"
FG_COLOR = "#c792ea"
BTN_BG = "#292941"
BTN_HOVER = "#3b3b58"
TEXT_COLOR = "white"

def generate_category_events(parent_frame, teams, balance_label, title, show_back_button, show_title_label, category):
    global selected_teams_for_each_category_dict, selected_odds_for_each_category_dict

# sprawdza czy druzyny i kursy zostaly juz wylosowane, jeśli nie to je losuje
    if selected_teams_for_each_category_dict[category] is None:
        selected_teams_for_each_category_dict[category] = select_multiple_teams(teams, 8) #losuje drużyny i przypisuje je do słownika do danej kategorii = danego sportu

        # tworzy liste która posiada listy kursów i przypisuje ją do slownika dla danej kategorii
        selected_odds_for_each_category_dict[category] = [[round(random.uniform(1.01, 5.00), 2), round(random.uniform(1.01, 5.00), 2), round(random.uniform(1.01, 5.00), 2)] for x in range(0, len(selected_teams_for_each_category_dict[category]), 2)]

    selected_teams = selected_teams_for_each_category_dict[category]
    selected_odds = selected_odds_for_each_category_dict[category]

    parent_frame.rowconfigure(0, weight=0)  # header_frame
    parent_frame.rowconfigure(1, weight=1)  # events_frame_inner
    parent_frame.configure(bg=BG_COLOR)

    if show_title_label:
        header_frame = tk.Frame(parent_frame, bg=BG_COLOR)
        header_frame.grid(row=0, column=0, sticky="nsew")
        header_frame.columnconfigure(0, weight=1)

        title_label = tk.Label(header_frame, text=title, font=("Arial", 18, "bold"), bg=BG_COLOR, fg="#c792ea")
        title_label.grid(row=0, column=0, sticky="nsew", pady=(10, 10))

    events_frame = tk.Frame(parent_frame, bg="#3c3c52")
    events_frame.grid(row=1, column=0, sticky="nsew")
    events_frame.columnconfigure(0, weight=1)
    events_frame.rowconfigure(0, weight=1)

    events_frame_inner = tk.Frame(events_frame, bg="#3c3c52")
    events_frame_inner.grid(row=0, column=0, sticky="nsew", pady=(20,0))
    events_frame_inner.columnconfigure(0, weight=1)

    #petla wypisujaca na ekran mecze z przyciskami do wyboru zakładu
    for i in range(0, len(selected_teams), 2):
        event_label = tk.Label(events_frame_inner, text=f"{selected_teams[i]} vs {selected_teams[i+1]}", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=FG_COLOR, relief="ridge", bd=2)
        event_label.grid(row=i, column=0, pady=(10, 3), sticky="ew")

        buttons_frame = tk.Frame(events_frame_inner, bg="#3c3c52")
        buttons_frame.grid(row=i + 1, column=0, pady=(5, 15), sticky="nsew")
        buttons_frame.columnconfigure((0, 1, 2), weight=1)

        win0_odds, draw_odds, win1_odds = selected_odds[i // 2] #przypisuje kursy wylosowane w selected_odds odpowiednio do zakładu

        # przyciski z przypisana funkcja add_bet do dodania wybranego zakładu do kuponu
        btn_win0 = backend.styled_button(buttons_frame, text=f"{selected_teams[i]} \n {win0_odds:.2f}", width=15, height=2, command=lambda t1=selected_teams[i], t2=selected_teams[i+1], odds=win0_odds: add_bet(t1, t2, odds, balance_label, t1))
        btn_draw = backend.styled_button(buttons_frame, text=f"Remis \n {draw_odds:.2f}", width=15, height=2, command=lambda t1=selected_teams[i], t2=selected_teams[i+1], odds=draw_odds: add_bet(t1, t2, odds, balance_label, "Remis"))
        btn_win1 = backend.styled_button(buttons_frame, text=f"{selected_teams[i+1]} \n {win1_odds:.2f}", width=15, height=2, command=lambda t1=selected_teams[i+1], t2=selected_teams[i], odds=win1_odds: add_bet(t1, t2, odds, balance_label, t1))

        btn_win0.grid(row=0, column=0, padx=5, sticky="ew")
        btn_draw.grid(row=0, column=1, padx=5, sticky="ew")
        btn_win1.grid(row=0, column=2, padx=5, sticky="ew")

    #przycisk powrotu
    if show_back_button:
        back_button = backend.styled_button(parent_frame, text="Powrót", command=parent_frame.destroy)
        back_button.grid(row=2, column=0, pady=(10, 10))

