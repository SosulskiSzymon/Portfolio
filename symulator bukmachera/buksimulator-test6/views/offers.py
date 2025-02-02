import tkinter as tk
import backend

BG_COLOR = "#1e1e2e"  # Ciemny fiolet
FG_COLOR = "#c792ea"  # Jasny fiolet
BTN_BG = "#292941"  # Fioletowy odcień
BTN_HOVER = "#3b3b58"
TEXT_COLOR = "white"



# oferty w oknie głównym
def display_offers():
    window_offers = tk.Toplevel()
    window_offers.title("Oferty")
    window_offers.geometry("400x300")
    window_offers.resizable(False, False)
    window_offers.columnconfigure(0, weight=1)
    window_offers.rowconfigure(0, weight=0)
    window_offers.rowconfigure(1, weight=1)

    title_frame = tk.Frame(window_offers, bg=BG_COLOR)
    title_frame.grid(row=0, column=0, sticky="new")

    title_frame.columnconfigure(0, weight=1)
    title_frame.rowconfigure(0, weight=1)

    title_offers = tk.Label(title_frame, text="Aktualne promocje:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 20, "bold"))
    title_offers.grid(row=0, column=0)

    offers_frame = tk.Frame(window_offers, bg="#3c3c52")
    offers_frame.grid(row=1, column=0, sticky="nsew")

    offers_frame.columnconfigure((0,1,2), weight=1)
    offers_frame.rowconfigure((0,1), weight=1)

    offer1_btn = backend.styled_button_3(offers_frame, text="Oferta 1", height=5, width=10)
    offer1_btn.grid(row=0, column=0)
    offer2_btn = backend.styled_button_3(offers_frame, text="Oferta 2", height=5, width=10)
    offer2_btn.grid(row=0, column=1)
    offer3_btn = backend.styled_button_3(offers_frame, text="Oferta 3", height=5, width=10)
    offer3_btn.grid(row=0, column=2)
    offer4_btn = backend.styled_button_3(offers_frame, text="Oferta 4", height=5, width=10)
    offer4_btn.grid(row=1, column=0)
    offer5_btn = backend.styled_button_3(offers_frame, text="Oferta 5", height=5, width=10)
    offer5_btn.grid(row=1, column=1)
    offer6_btn = backend.styled_button_3(offers_frame, text="Oferta 6", height=5, width=10)
    offer6_btn.grid(row=1, column=2)

