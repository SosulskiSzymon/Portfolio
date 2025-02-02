import tkinter as tk
from tkinter import messagebox
import backend
from views.change_gui_after_login import change_gui_after_login


def login_window(btn_login, btn_register, title_label, balance_label, btn_profile):
    def login():
        login = entry_login.get()
        password = entry_password.get()

        if not login or not password:
            messagebox.showwarning("Błąd", "Wszystkie pola muszą być wypełnione!")
            return

        if backend.login_user(login, password):
            user_data = backend.get_user_data(login)
            backend.set_current_user(user_data)  # Ustawienie aktualnego użytkownika
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            window_login.destroy()
            change_gui_after_login(user_data, btn_login, btn_register, title_label, balance_label, btn_profile)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowe dane logowania!")

    window_login = tk.Toplevel()
    window_login.title("Logowanie użytkownika")
    window_login.geometry("400x300")
    window_login.configure(bg="#1c1c1c")

    # Nagłówek
    tk.Label(window_login, text="Logowanie", font=("Arial", 18, "bold"), bg="#1c1c1c", fg="#9b59b6").pack(pady=10)

    # Pole na login
    tk.Label(window_login, text="Login:", font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(anchor="w", padx=20)
    entry_login = tk.Entry(window_login, font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", insertbackground="#ffffff")
    entry_login.pack(fill="x", padx=20, pady=5)

    # Pole na hasło
    tk.Label(window_login, text="Hasło:", font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(anchor="w", padx=20)
    entry_password = tk.Entry(window_login, show="*", font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", insertbackground="#ffffff")
    entry_password.pack(fill="x", padx=20, pady=5)

    tk.Button(window_login, text="Zaloguj", font=("Arial", 12, "bold"), bg="#9b59b6", fg="#ffffff", activebackground="#6c3483", activeforeground="#ffffff",  command=login).pack(pady=20)
