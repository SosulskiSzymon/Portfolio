import tkinter as tk
from PIL import Image, ImageTk
from backend import main_teams
from views.categories import open_categories_window
from views.offers import display_offers
from views.register import register_window
from views.login import login_window
from views.profile import show_profile
from utils.generating_events import generate_category_events
from views.create_parlay import creating_parlay

# Kolory
BG_COLOR = "#1e1e2e"  # Ciemny fiolet
FG_COLOR = "#c792ea"  # Jasny fiolet
BTN_BG = "#292941"  # Fioletowy odcień
BTN_HOVER = "#3b3b58"
TEXT_COLOR = "white"

# Główne okno
main_window = tk.Tk()
main_window.title("Bukmacher Online")
main_window.geometry("500x600")
main_window.minsize(500,600)
main_window.configure(bg=BG_COLOR)
main_window.rowconfigure(0, weight=0)#header
main_window.rowconfigure(1, weight=1)#main
main_window.rowconfigure(2, weight=0)#footer
main_window.columnconfigure(0, weight=1)

# Styl przycisków
def on_enter(e):
    e.widget["bg"] = BTN_HOVER

def on_leave(e):
    e.widget["bg"] = BTN_BG

def styled_button(parent, text, command):
    btn = tk.Button(parent, text=text, font=('Arial', 10), bg=BTN_BG, fg=TEXT_COLOR, activebackground=BTN_HOVER,
                    activeforeground=TEXT_COLOR, command=command, bd=0, relief='flat', padx=10, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# header
top_frame = tk.Frame(main_window, bg=BG_COLOR)
top_frame.grid(row=0, column=0, sticky="nsew", pady=10)
top_frame.columnconfigure([0, 1, 2], weight=1)
title_label = tk.Label(top_frame, text="Bukmacher", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, padx=(10, 100), sticky="w")


# Ikony
image = Image.open("assets/profile.png")
resized_image = image.resize((50, 45))
profile_icon = ImageTk.PhotoImage(resized_image)

# Przyciski funkcyjne
login_frame = tk.Frame(top_frame, bg=BG_COLOR)
login_frame.grid(row=0, column=2, sticky="e")

btn_login = styled_button(login_frame, "Zaloguj się", lambda: login_window(btn_login, btn_register, title_label, balance_label, btn_profile))
btn_register = styled_button(login_frame, "Zarejestruj się", register_window)
balance_label = tk.Label(login_frame, font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
btn_profile = tk.Button(login_frame, image=profile_icon, bg=BG_COLOR, bd=0, command=lambda: show_profile(btn_login, btn_register, btn_profile, balance_label))

btn_login.grid(row=0, column=1, padx=5, sticky="e")
btn_register.grid(row=0, column=2, padx=(0,5), sticky="e")

#Main

main_frame = tk.Frame(main_window, bg=BG_COLOR)
main_frame.grid(row=1, column=0, sticky="nsew")
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
generate_category_events(main_frame, main_teams, balance_label, "", show_back_button=False, category="main_window", show_title_label=False)

#Footer
footer_frame = tk.Frame(main_window, bg=BG_COLOR)
footer_frame.grid(row=2, column=0, sticky="sew", pady=10)
footer_frame.columnconfigure([0, 1, 2], weight=1)
footer_frame.rowconfigure(0, weight=1)

btn_categories = styled_button(footer_frame, "Kategorie", lambda: open_categories_window(balance_label))
btn_parlay = styled_button(footer_frame, "Postaw kupon", lambda: creating_parlay(balance_label))
btn_offers = styled_button(footer_frame, "Oferty", command=display_offers)

btn_categories.grid(row=0, column=0, sticky="nsew", padx=5)
btn_parlay.grid(row=0, column=1, sticky="nsew", padx=5)
btn_offers.grid(row=0, column=2, sticky="nsew", padx=5)


main_window.mainloop()
