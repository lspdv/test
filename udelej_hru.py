import random

balicek = []
for hodnota in range(1, 14):
    for barva in 'Pi', 'Sr', 'Ka', 'Kr':
        balicek.append((hodnota, barva, False))
random.shuffle(balicek)

sloupecek = [...]
for sloupecek in range(1, 8):
    for radek in range(sloupecek + 1):
        sloupecek.append(balicek)