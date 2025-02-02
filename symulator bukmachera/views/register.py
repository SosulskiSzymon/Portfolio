import tkinter as tk
from tkinter import messagebox
import backend

def register_window():
    def register():
        login = entry_login.get()
        password = entry_password.get()
        age = entry_age.get()

        if not login or not password or not age:
            messagebox.showwarning("Błąd", "Wszystkie pola muszą być wypełnione!")
            return

        if not age.isdigit() or int(age) < 18:
            messagebox.showwarning("Błąd", "Wiek musi być liczbą i wynosić co najmniej 18!")
            return

        if backend.register_user(login, password, int(age)):
            messagebox.showinfo("Sukces", "Rejestracja zakończona pomyślnie!")
            window_register.destroy()

    window_register = tk.Toplevel()
    window_register.title("Rejestracja użytkownika")
    window_register.geometry("400x300")
    window_register.configure(bg="#1c1c1c")

    tk.Label(window_register, text="Rejestracja", font=("Arial", 18, "bold"), bg="#1c1c1c", fg="#9b59b6").pack(pady=10)

    # Pole na login
    tk.Label(window_register, text="Login:", font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(anchor="w", padx=20)
    entry_login = tk.Entry(window_register, font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", insertbackground="#ffffff")
    entry_login.pack(fill="x", padx=20, pady=5)

    # Pole na hasło
    tk.Label(window_register, text="Hasło:", font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(anchor="w", padx=20)
    entry_password = tk.Entry(window_register, show="*", font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", insertbackground="#ffffff")
    entry_password.pack(fill="x", padx=20, pady=5)

    # Pole na wiek
    tk.Label(window_register, text="Wiek:", font=("Arial", 12), bg="#1c1c1c", fg="#ffffff").pack(anchor="w", padx=20)
    entry_age = tk.Entry(window_register, font=("Arial", 12), bg="#2c2c2c", fg="#ffffff", insertbackground="#ffffff")
    entry_age.pack(fill="x", padx=20, pady=5)

    tk.Button(window_register, text="Zarejestruj", font=("Arial", 12, "bold"), bg="#9b59b6", fg="#ffffff", activebackground="#6c3483", activeforeground="#ffffff", command=register).pack(pady=20)
