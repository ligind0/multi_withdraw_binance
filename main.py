import random
import tkinter as tk
from time import sleep
from tkinter import ttk

from binance.client import Client
from config import api_key, api_secret

client = Client(api_key, api_secret)

def withdraw(coin, address, amount, network=None):
    try:
        result = client.withdraw(
            coin=coin,
            address=address,
            amount=amount,
            network=network
        )
        print(result)
    except Exception as e:
        print(e)

def add_rand_to_num(num):
    return str(round(random.uniform(num,1.15*num), 6))


def withdraw_multiple(coin, addresses, amount, delay, rand, network=None ):
    addresses_list = [address.strip() for address in addresses.split('\n') if address.strip()]
    for address in addresses_list:
        if rand:
            amount = add_rand_to_num(float(amount))
        withdraw(coin, address, amount, network=network)
        print(f"{coin}, {address}, {amount}, {network}")
        print(f"Sleeping {delay} seconds")
        sleep(delay)

def withdraw_gui():
    def do_withdraw():
        coin = coin_entry.get()
        address = address_entry.get('1.0', 'end-1c')
        amount = amount_entry.get()
        network = network_var.get()
        delay = delay_entry.get()
        if delay == '': delay = 0
        rand = rand_var.get()
        
        if address:
            withdraw_multiple(coin, address, amount, int(delay), rand, network=network)
        else:
            withdraw(coin, address, amount, network=network)

    root = tk.Tk()
    root.title('Binance Withdraw')
    root.geometry('420x300')

    rand_var = tk.BooleanVar()
    rand_check_box = tk.Checkbutton(root, text='Rand 15%',variable=rand_var, onvalue=True, offvalue=False)
    rand_check_box.grid(row=5, column=2, padx=0, pady=20)
    coin_label = ttk.Label(root, text='Coin:')
    coin_label.grid(row=0, column=0, padx=5, pady=5)
    assets = client.get_withdraw_history()
    assets_list = [asset['coin'] for asset in assets]
    coin_entry = ttk.Combobox(root, values=assets_list, width=30)
    coin_entry.grid(row=0, column=1, padx=5, pady=5)

    address_label = ttk.Label(root, text='Addresses:')
    address_label.grid(row=1, column=0, padx=5, pady=5)
    address_entry = tk.Text(root, height=4, width=30)
    address_entry.grid(row=1, column=1, padx=5, pady=5)

    delay_label = ttk.Label(root, text='Delay:')
    delay_label.grid(row=4, column=0, padx=5, pady=5)
    delay_entry = tk.Entry(root, width=30)
    delay_entry.grid(row=4, column=1, padx=5, pady=5)

    amount_label = ttk.Label(root, text='Amount:')
    amount_label.grid(row=2, column=0, padx=5, pady=5)
    amount_entry = ttk.Entry(root, width=30)
    amount_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text='Network').grid(row=3, column=0, padx=5, pady=5)
    network_var = tk.StringVar()
    network_var.set('')  # set default value
    network_optionmenu = tk.ttk.Combobox(root, textvariable=network_var, values=['BNB', 'BSC', 'ETH', 'TRX', 'CELO'])
    network_optionmenu.grid(row=3, column=1, padx=5, pady=5)

    withdraw_button = ttk.Button(root, text='Withdraw', command=do_withdraw)
    withdraw_button.grid(row=5, column=1, padx=5, pady=20)

    clear_button = ttk.Button(root, text='Clear', command=lambda: address_entry.delete('1.0', tk.END))
    clear_button.grid(row=5, column=0, padx=10, pady=5)

    root.mainloop()

withdraw_gui()
