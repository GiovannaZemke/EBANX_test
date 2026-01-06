from app.account_data import accounts


def get_balance(account_id:int):
    return accounts.get(account_id,0)

    
def deposit(account: int, amount: int):
    accounts[account] = accounts.get(account, 0) + amount
    return {
        "destination": {
            "id": str(account),
            "balance": accounts[account]
        }
    }


def withdraw(account: int, amount: int):
    accounts[account] = accounts[account] - amount
    return {
        "origin": {
            "id": str(account),
            "balance": accounts[account]
        }
    }


def transfer(origin:int, destination:int, amount: int):
    accounts[origin] -= amount
    accounts[destination] = accounts.get(destination, 0) + amount

    return {
        "origin": {
            "id": str(origin),
            "balance": accounts[origin]
        },
        "destination": {
            "id": str(destination),
            "balance": accounts[destination]
        }
    }