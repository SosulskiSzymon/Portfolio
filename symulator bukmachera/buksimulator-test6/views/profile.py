import tkinter as tk
from views.deposit import deposit_func
from views.my_bets import show_user_bets
import backend
from views.withdraw import withdraw


#funkcja wywołujaca okno profil
def show_profile(btn_login, btn_register, btn_profile, balance_label):
    #funkcja wylogowania
    def logout():
        backend.set_current_user(None)  #ustawienie zalogowanego usera na None
        btn_login.grid(row=0, column=2, padx=5, sticky="e")
        btn_register.grid(row=0, column=3, padx=5, sticky="e")
        balance_label.grid_forget()
        btn_profile.grid_forget()       #zmiana gui
        window_profile.destroy()

    window_profile = tk.Toplevel()
    window_profile.title("Profil")
    window_profile.geometry("300x500")
    window_profile.resizable(False, False)
    window_profile.configure(bg="#1c1c1c")


    window_profile.columnconfigure(0, weight=1)
    window_profile.columnconfigure(1, weight=1)
    window_profile.columnconfigure(2, weight=1)

    def on_enter(e):
        e.widget["bg"] = "#6c3483"
    def on_leave(e):
        e.widget["bg"] = "#9b59b6"

    #przycisk moje kupony
    btn_parlays = tk.Button(window_profile, text="Moje kupony", font=("Arial", 12, "bold"), width=20, height=2, bg="#9b59b6", fg="white", activebackground="#6c3483", command=lambda: (window_profile.destroy(), show_user_bets(balance_label)))
    #przycisk depozyt
    btn_deposit = tk.Button(window_profile, text="Wpłać", font=("Arial", 12, "bold"), width=20, height=2, bg="#9b59b6", fg="white", activebackground="#6c3483", command=lambda: (deposit_func(balance_label), window_profile.destroy()))
    #przycisk wypłata
    btn_withdraw = tk.Button(window_profile, text="Wypłać", font=("Arial", 12, "bold"), width=20, height=2, bg="#9b59b6", fg="white", activebackground="#6c3483", command=lambda: (withdraw(balance_label), window_profile.destroy()))   #dodać wypłaty
    #przycisk wyloguj
    btn_logout = tk.Button(window_profile, text="Wyloguj", font=("Arial", 12, "bold"), width=20, height=2, bg="#9b59b6", fg="white", activebackground="#6c3483",command=logout)

    btn_parlays.grid(row=1, column=1, pady=(50,10))
    btn_deposit.grid(row=2, column=1, pady=10)
    btn_withdraw.grid(row=3, column=1, pady=10)
    btn_logout.grid(row=4, column=1, pady=10)

    for button in [btn_parlays, btn_deposit, btn_withdraw, btn_logout]:
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)



