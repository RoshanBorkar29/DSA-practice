inventory = {
    "Pen": 12,
    "Notebook": 7,
    "Pencil": 15
}

operations = [
    "ADD Pen 5",
    "SELL Pencil 3",
    "ADD Eraser 10",
    "REMOVE Notebook",
    "SELL Pen 20"
]
for operation in operations:
    ops=operation.split()
    command=ops[0]

    if command=="ADD":
        item=ops[1]
        qty=int(ops[2])

        if item in inventory:
            inventory[item]+=qty
        else:
            inventory[item]=qty

    elif command=="SELL":
        item=ops[1]
        qty=int(ops[2])
        if item in inventory :
            if inventory[item]>=qty:
                inventory[item]-=qty
            else:
                print(f"Not enough stock for {item}")

    elif command=="REMOVE":
        item=ops[1]
        if item in inventory:
            del inventory[item]


print(inventory)
