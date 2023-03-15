options = [
    ">",
    ">=",
    "<",
    "<=",
    "!=",
    "="
]


clicked.set(">")

drop = OptionMenu(window, clicked, *options)
drop.grid(column=4,row=5)