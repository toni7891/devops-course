def find_account(acc_id):
    for account in accounts:
        if account["account_id"] == acc_id:
            return account
    return None

def verify_pin(account, pin):
    return account["pin"] == pin

def adm_login_func():
    name = input("enter username: ") 
    passw = input("enter password: ")

    if name == ADMIN_USERNAME and passw == ADMIN_PASSWORD:
        return True

    print("Access denied")
    return False

def create_new():
    if not adm_login_func():
        return

    name = input("Enter name: ")
    pin = input("Set PIN: ")

    account = {
        "account_id": len(accounts) + 100,
        "name": name,
        "pin": pin,
        "balance": 0
    }

    accounts.append(account)
    print("Account added!")

def deposit():
    account_id = int(input("account id: "))
    pin = input("enter pin: ")
    amount = float(input("amount: "))

    account = find_acc(account_id)

    if not account:
        print("acc not found!")
        return

    if not verify_pin(account_id, pin):
        print("wrong pin")
        return
    
    if amount <= 0:
        print("invalid amount, has to be more than 0 to deposit!")

    account["balance"] += amount

def withdraw():
    account_id = int(input("Account ID: "))
    pin = input("PIN: ")
    amount = float(input("Amount: "))

    account = find_account(account_id)

    if not account:
        print("Account not found")
        return

    if not verify_pin(account, pin):
        print("Wrong PIN")
        return

    if account["balance"] < amount:
        print("Insufficient funds")
        return

    account["balance"] -= amount

def show_account():
    account_id = int(input("Account ID: "))
    pin = input("PIN: ")

    account = find_account(account_id)

    if not account:
        print("Account not found")
        return

    if not verify_pin(account, pin):
        print("Wrong PIN")
        return

    print("\n",account)

def show_all_accounts():
    if not adm_login_func():
        return

    for acc in accounts:
        print(acc)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"
global accounts
accounts = [
    {"account_id": 100, "name": "Liron", "pin": "1234", "balance": 500},
     {"account_id": 101, "name": "Daniel", "pin": "5678", "balance": 900},
]

def main():
    while True:
        print("\n1.Create \n2.Deposit \n3.Withdraw \n4.Show \n5.Admin View \n6.Exit\n ")

        choice = input("Choose: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            deposit()

        elif choice == "3":
            withdraw()

        elif choice == "4":
            show_account()

        elif choice == "5":
            show_all_accounts()

        elif choice == "6":
            break

if __name__ == "__main__":
    main()