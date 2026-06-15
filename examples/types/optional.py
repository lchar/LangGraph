from typing import Optional

def nice_message(name: Optional[str]) -> None:
    if name is None:
        print('Hey there pardner!')
    else:
        print(f'Hey aren\'t you that {name} dude?')

name0 = None
name1 = "Bobo Jenkins"

nice_message(name0)
nice_message(name1)