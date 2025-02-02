import tkinter as tk
from tkinter import messagebox
import backend
import math

def withdraw(balance_label):

    withdraw_window = tk.Toplevel()
    withdraw_window.title("Wypłać środki")
    withdraw_window.geometry("500x200")
    withdraw_window.resizable(False, False)
    withdraw_window.configure(bg="#1c1c1c")

    withdraw_window.rowconfigure((0,2), weight=0)
    withdraw_window.rowconfigure(1, weight=1)
    withdraw_window.columnconfigure(0, weight=1)

    withdraw_label = tk.Label(withdraw_window, text="Ile chcesz wypłacić?", font=('Arial', 12, 'bold'), bg="#1c1c1c", fg="#9b59b6")
    withdraw_label.grid(row=0, column=0, sticky="new", pady=10)

    user_input = tk.Entry(withdraw_window, font=('Arial', 12), bg="#2c2c2c", fg="#ffffff", insertbackground="#ffffff")
    user_input.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

    buttons_frame = tk.Frame(withdraw_window, bg="#1c1c1c")
    buttons_frame.grid(row=2, column=0, pady=10)
    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)

    def submit_withdraw():
        users = backend.load_users()
        current_user = backend.get_current_user()
        try:
            amount_str = user_input.get().replace(",", ".")
            amount = round(float(amount_str), 2)

            for user in users:
                if user['login'] == current_user['login']:
                    current_user['balance'] = round(float(user['balance']), 2)

            if amount>current_user['balance']:
                messagebox.showerror("Błąd", "Nie posiadasz tyle środków na swoim koncie")
                return
            if amount <= 0:
                messagebox.showerror("Błąd", "Kwota musi być większa od 0.")
                return

            for user in users:
                if user['login'] == current_user['login']:
                    user['balance'] -= amount
                    current_user['balance'] = round(float(user['balance']),2)


            backend.save_users(users)
            messagebox.showinfo("Sukces", f"Wypłaciłeś {amount:.2f} PLN ze swojego konta")
            balance_label.config(text=f"Saldo: {current_user['balance']} PLN")
            exit_withdraw()

        except ValueError:
            messagebox.showerror("Błąd", "Proszę wpisać poprawną kwotę")


    def exit_withdraw():
        withdraw_window.destroy()


    submit_button = backend.styled_button_2(buttons_frame, text="Zatwierdź", command=submit_withdraw)
    submit_button.grid(row=0, column=0, padx=10)

    exit_button = backend.styled_button_2(buttons_frame, text="Wyjdź", command=exit_withdraw)
    exit_button.grid(row=0, column=1, padx=10)

    submit_button.bind("<Enter>", backend.on_enter)
    submit_button.bind("<Leave>", backend.on_leave)
    exit_button.bind("<Enter>", backend.on_enter)
    exit_button.bind("<Leave>", backend.on_leave)