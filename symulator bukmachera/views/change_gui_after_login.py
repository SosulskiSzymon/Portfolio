import tkinter as tk

def change_gui_after_login(user_data, btn_login, btn_register, title_label, balance_label, btn_profile):
    btn_login.grid_forget()     #przycisk login znika
    btn_register.grid_forget()  #rejestracja znika
    balance_label.grid(row=0, column=0, padx=1, sticky="e") #pojawia sie balance
    balance_label.config(text=f"Saldo: {user_data['balance']} PLN")
    btn_profile.grid(row=0, column=2, padx=(10,10), sticky="e") #pojawia sie ikona profilu