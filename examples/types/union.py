from typing import Union

def square(x: Union[int, float]) -> float:
    return x * x

x = 5
y = 1.234
# z = 'This is a string.' this results in error

print(square(x))
print(square(y))
# print(square(z))