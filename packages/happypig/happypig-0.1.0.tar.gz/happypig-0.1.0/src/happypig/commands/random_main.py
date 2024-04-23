import random
from happypig import animals, saying

def random_main():
    animal = random.choice(animals)
    print(saying(animal["animal"], animal["content"]))
