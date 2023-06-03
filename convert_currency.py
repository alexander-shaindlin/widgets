import sys
#from forex_python.converter import CurrencyRates
import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel, Text, Scrollbar
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox

def convert_currency():
    try:
        source = from_currency_combo.get()
        destination = to_currency_combo.get()
        amount = amount_entry.get()

        result = requests.get(f'https://v6.exchangerate-api.com/v6/46d806004bf11d7fa2616a4a/pair/{source}/{destination}/{amount}').json()

        converted_result = result['conversion_result']
        formatted_result = f'{amount} {source} = {converted_result} {destination}'
        result_label.config(text=formatted_result)
        time_label.config(text='Last updated: ' + result['time_last_update_utc'])

    except Exception:
        showerror(title='Error', message='An error occurred!!')

def display_currency_guide():
    try:
        url = "https://en.wikipedia.org/wiki/ISO_4217"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="wikitable")
        rows = table.find_all("tr")

        currency_guide = {}
        for row in rows[1:]:
            columns = row.find_all("td")
            currency_code = columns[0].text.strip()
            currency_name = columns[1].text.strip()
            currency_guide[currency_code] = currency_name

        guide_window = Toplevel()
        guide_window.title("Currency Guide")

        guide_text = Text(guide_window)
        guide_text.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(guide_window)
        scrollbar.pack(side="right", fill="y")

        guide_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=guide_text.yview)

        for currency_code, currency_name in currency_guide.items():
            guide_text.insert("end", f"{currency_code} - {currency_name}\n")

        def close_guide():
            guide_window.destroy()

        close_button = Button(guide_window, text="Close", command=close_guide)
        close_button.pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def exit_program():
    if messagebox.askokcancel("Exit", "Do you want to exit the program?"):
        sys.exit(0)


window = Tk()
window.title("Currency Converter")

Label(window, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
amount_entry = Entry(window)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

Label(window, text="From Currency:").grid(row=1, column=0, padx=5, pady=5)
from_currency_combo = Combobox(window)
from_currency_combo.grid(row=1, column=1, padx=5, pady=5)

Label(window, text="To Currency:").grid(row=2, column=0, padx=5, pady=5)
to_currency_combo = Combobox(window)
to_currency_combo.grid(row=2, column=1, padx=5, pady=5)

convert_button = Button(window, text="Convert", command=convert_currency)
convert_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

guide_button = Button(window, text="Currency Guide", command=display_currency_guide)
guide_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

result_label = Label(window, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

time_label = Label(window, text="")
time_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()


