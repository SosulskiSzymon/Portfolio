import tkinter as tk
from tkinter import messagebox
import backend


def deposit_func(balance_label):

    window_deposit = tk.Toplevel()
    window_deposit.title("Depozyt")
    window_deposit.geometry("500x200")
    window_deposit.resizable(False, False)
    window_deposit.configure(bg="#1c1c1c")

    window_deposit.rowconfigure((0,1,2), weight=1)

    window_deposit.columnconfigure((0,1), weight=1)

    deposit_label = tk.Label(window_deposit, text="Ile chcesz wpłacić?", font=('Arial', 12, 'bold'), bg="#1c1c1c", fg="#9b59b6")
    deposit_label.grid(row=0, column=0, columnspan=2, sticky="new", pady=10)

    user_input = tk.Entry(window_deposit, font=('Arial', 12), bg="#2c2c2c", fg="#ffffff", insertbackground="#ffffff", justify="center")
    user_input.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

    buttons_frame = tk.Frame(window_deposit, bg="#1c1c1c")
    buttons_frame.grid(row=2, column=0, sticky="e", pady=10)
    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)



    #funkcja umieszczona wewnątrz deposit_func(), odpowiada za potwierdzenie depozytu, zapisanie go do pliku oraz aktualizację salda w gui
    def submit_deposit():
        current_user = backend.get_current_user()  # getter zalogowanego usera
        try:
            amount_str = user_input.get().replace(",", ".")  # zamiana przecinka kropką i zaokraglenie do 2 miejsc po przecinku
            amount = round(float(amount_str), 2)

            if amount <= 0:
                messagebox.showerror("Błąd", "Kwota musi być większa od 0.")
                return
            if amount > 100000:
                messagebox.showerror("Błąd", "Kwota depozytu jest zbyt wysoka")
                return

            users = backend.load_users()  # wczytanie listy użytkownikow

            for user in users:
                if user['login'] == current_user['login']:  # znalezienie użytkownika i dodanie mu salda
                    user['balance'] += amount
                    current_user['balance'] = round(float(user['balance']), 2)

            backend.save_users(users)  # zapisanie pliku

            messagebox.showinfo("Sukces", f"Złożono depozyt w wysokości {amount:.2f} PLN")

            balance_label.config(
                text=f"Saldo: {current_user['balance']} PLN")  # poprawienie wyświetlanego salda na nowe

            window_deposit.destroy()

        except ValueError:
            messagebox.showerror("Błąd", "Proszę wpisać poprawną kwotę.")


    # funkcja wewnętrzna odpowiadająca za wyjśćie z okna depozytu
    def exit_deposit():
        window_deposit.destroy()


    submit_button = backend.styled_button_2(buttons_frame, text="Zatwierdź", command=submit_deposit)
    submit_button.grid(row=0, column=0, padx=10, sticky="e")

    exit_button = backend.styled_button_2(buttons_frame, text="Wyjdź", command=exit_deposit)
    exit_button.grid(row=0, column=1, padx=10, sticky="e")

    submit_button.bind("<Enter>", backend.on_enter)
    submit_button.bind("<Leave>", backend.on_leave)
    exit_button.bind("<Enter>", backend.on_enter)
    exit_button.bind("<Leave>", backend.on_leave)