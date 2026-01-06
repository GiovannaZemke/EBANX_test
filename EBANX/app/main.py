from fastapi import FastAPI, HTTPException, Response, Body

from app import account_service

app = FastAPI()

@app.post("/reset")
def reset():
    try:
        account_service.accounts.clear()
    except Exception:
        raise HTTPException(status_code=500)
    return Response(content="OK", status_code=200)

@app.get("/balance")
def balance(account_id: int):
    if account_id not in account_service.accounts:
        return Response(content="0", status_code=404)
    return account_service.accounts[account_id]

@app.post("/event", status_code=201)
def post_event(event: dict = Body(...)):
    try:
        type = event.get("type")
        amount = event.get("amount")

        if type == "deposit":
            destination = event.get("destination")
            if not destination:
                raise HTTPException(status_code=400, detail="Missing destination")
            return account_service.deposit(int(destination), amount)

        if type == "withdraw":
            origin = event.get("origin")
            if not origin:
                raise HTTPException(status_code=400, detail="Missing origin")
            origin = int(origin)
            if origin not in account_service.accounts:
                return Response(content="0", status_code=404)
            return account_service.withdraw(origin, amount)

        if type == "transfer":
            origin = event.get("origin")
            destination = event.get("destination")
            if not origin or not destination:
                raise HTTPException(status_code=400, detail="Missing origin or destination")
            origin = int(origin)
            destination = int(destination)
            if origin not in account_service.accounts:
                return Response(content="0", status_code=404)
            return account_service.transfer(origin, destination, amount)

        raise HTTPException(status_code=400, detail="Invalid event type")

    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail="Invalid data format")
