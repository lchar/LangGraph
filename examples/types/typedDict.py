from typing import TypedDict

class Movie(TypedDict):
    name : str
    year : int

movie = Movie(name='Avengers Endgame', year=2019)

print(movie)