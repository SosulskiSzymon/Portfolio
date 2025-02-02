import tkinter as tk
import backend
from backend import football_teams, basketball_teams, volleyball_teams, hockey_teams
from utils.generating_events import generate_category_events

# Kolory
BG_COLOR = "#1e1e2e"  # Ciemny fiolet
FG_COLOR = "#c792ea"  # Jasny fiolet
BTN_BG = "#292941"  # Fioletowy odcień
BTN_HOVER = "#3b3b58"
TEXT_COLOR = "white"


# Kategorie
def open_categories_window(balance_label):
    window_categories = tk.Toplevel()
    window_categories.title("Kategorie")
    window_categories.geometry("300x500")
    window_categories.resizable(False, False)
    window_categories.configure(bg=BG_COLOR)
    window_categories.columnconfigure(0, weight=1)

    header_frame = tk.Frame(window_categories, bg=BG_COLOR)
    header_frame.grid(row=0, column=0, sticky="ew", pady=(10,15))
    header_frame.columnconfigure(0, weight=0)
    header_frame.columnconfigure(1, weight=1)

    back_button = backend.styled_button(header_frame, "↩", lambda: window_categories.destroy())
    back_button.grid(row=0, column=0, sticky="w", padx=(10, 50))

    categories_title_label = tk.Label(header_frame, text="Kategorie:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 18, "bold"))
    categories_title_label.grid(row=0, column=1, sticky="w", pady=(10, 10))

    main_categories_frame = tk.Frame(window_categories, bg=BG_COLOR)
    main_categories_frame.grid(row=1, column=0, sticky="nsew")
    main_categories_frame.columnconfigure(0, weight=1)
    main_categories_frame.rowconfigure([0, 1, 2, 3], weight=1)

    # przyciski wszystkich kategorii
    football_category_button = backend.styled_button(main_categories_frame, text="Piłka nożna", command=lambda: (open_category_window("Piłka nożna", football_teams, balance_label, "football"), window_categories.destroy()))
    football_category_button.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
    basketball_category_button = backend.styled_button(main_categories_frame, text="Koszykówka", command=lambda: (open_category_window("Koszykówka", basketball_teams, balance_label, "basketball"), window_categories.destroy()))
    basketball_category_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
    volleyball_category_button = backend.styled_button(main_categories_frame, text="Siatkówka", command=lambda: (open_category_window("Siatkówka", volleyball_teams, balance_label, "volleyball"), window_categories.destroy()))
    volleyball_category_button.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
    hockey_category_button = backend.styled_button(main_categories_frame, text="Hokej", command=lambda: (open_category_window("Hokej", hockey_teams, balance_label, "hockey"), window_categories.destroy()))
    hockey_category_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

# funkcja otwierajaca okno danej kategorii
def open_category_window(title, teams, balance_label, category):
    category_window = tk.Toplevel()
    category_window.title(title)
    category_window.geometry("450x550")
    category_window.minsize(450, 550)
    category_window.configure(bg=BG_COLOR)
    category_window.columnconfigure(0, weight=1)
    category_window.rowconfigure(0, weight=0)

    generate_category_events(category_window, teams, balance_label, title, show_back_button=True, category=category, show_title_label=True)
