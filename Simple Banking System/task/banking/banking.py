import random
import sqlite3


def menu():
    print("""1. Create an account
2. Log into account
0. Exit""")


def login_menu():
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")


def luhn_algorithm(card_number):
    temp_number = [int(i) for i in card_number]
    for n in range(0, 15, 2):
        temp = temp_number[n] * 2
        temp_number[n] = temp if temp < 10 else temp - 9
    return (0 - sum(temp_number)) % 10


def create_card_number():
    card_number = f"400000{random.randrange(1000000000):09d}"
    return card_number + str(luhn_algorithm(card_number))


def create_account():
    card_number = create_card_number()
    pin = f"{random.randrange(10000):04d}"
    global conn, cur
    card_id = int(card_number)
    cur.execute('INSERT INTO card (id, number, pin) VALUES (?, ?, ?)', [card_id, card_number, pin])
    conn.commit()
    print(
        f"Your card has been created\n"
        f"Your card number:\n{card_number}\n"
        f"Your card PIN:\n{pin}"
    )


def add_income(card_number):
    amount = int(input("Enter income\n"))
    cur.execute("SELECT id, pin, balance FROM card WHERE number = ?", [card_number])
    card_id, pin, balance = cur.fetchone()
    cur.execute("DELETE FROM card WHERE number = ?", [card_number])
    cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)", [card_id, card_number, pin, amount + balance])
    conn.commit()
    print("Income was added!")


def transfer(card_number):
    print("Transfer")
    to = input("Enter card number\n")
    if to == card_number:
        print("You can't transfer money to the same account!")
        return
    if luhn_algorithm(to) != 0:
        print("Probably you made a mistake in the card number. Please try again!")
        return
    cur.execute("SELECT * FROM card WHERE number=?", [to])
    card = cur.fetchone()
    print(card)
    if card:
        card_id_to, card_number_to, pin_to, balance_to = card
        amount = int(input("Enter how much money you want to transfer:\n"))
        cur.execute("SELECT id, pin, balance FROM card WHERE number=?", [card_number])
        card_id, pin, balance = cur.fetchone()
        if amount <= balance:
            cur.execute("DELETE FROM card WHERE number=? or number=?", [card_number, card_number_to])
            cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)", [card_id, card_number, pin, balance - amount])
            cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)",
                        [card_id_to, card_number_to, pin_to, amount + balance_to])
            conn.commit()
            print("Success!")
        else:
            print("Not enough money!")
    else:
        print("Such a card does not exist.")


def close_account(card_number):
    cur.execute("DELETE FROM card WHERE number=?", [card_number])
    conn.commit()
    print("The account has been closed!")


def login():
    card_number = input("Enter your card number:\n")
    pin = input("Enter your PIN:\n")
    logged = False
    global conn, cur
    cur.execute('SELECT balance FROM card WHERE number=? and pin=?', [card_number, pin])
    balance = cur.fetchone()
    if balance:
        logged = True
        print("You have successfully logged in!")
    else:
        print("Wrong card number or PIN!")

    while logged:
        login_menu()
        user_choice = input()
        if user_choice == "1":
            print(f"Balance: {balance[0]}")
        elif user_choice == "2":
            add_income(card_number)
        elif user_choice == "3":
            transfer(card_number)
        elif user_choice == "4":
            close_account(card_number)
        elif user_choice == "5":
            print("You have successfully logged out!")
            break
        elif user_choice == "0":
            print("Bye!")
            exit(0)


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('DROP TABLE card')
cur.execute('CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()

while True:
    menu()
    user_choice = input()
    if user_choice == "1":
        create_account()
    elif user_choice == "2":
        login()
    elif user_choice == "0":
        print("Bye!")
        break
