from fastapi import FastAPI, HTTPException
from fastapi import Response
from fastapi import Body 

from app import service

app = FastAPI()

@app.post("/reset")
def reset():
    service.accounts.clear()
    return Response(content="OK", status_code=200)
#fazer uma verificação de verdade aqui

@app.get("/balance")
def balance(account_id: int):
    if account_id not in service.accounts:
        return Response(content="0", status_code=404)
    return service.accounts[account_id]


@app.post("/event",status_code=201)

def post_event(event: dict = Body(...)): #mano essa parte é comicamente importante, não mexe aqui não
    type = event.get("type")
    amount = event.get("amount")
    destination = event.get("destination")
    origin = event.get("origin")

    if type == "deposit":
        destination = int(destination)
        return service.deposit(destination, amount)
    
    if type == "withdraw":
        origin = int(origin)
        if origin not in service.accounts:
            return Response(content="0", status_code=404)
        return service.withdraw(origin, amount)
    
    if type == "transfer":
        origin = int(origin)
        if origin not in service.accounts:
            return Response(content="0", status_code=404)
        return service.transfer(origin, destination, amount)

    raise HTTPException(status_code=400, detail="Invalid event type")


 


