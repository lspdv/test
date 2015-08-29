def popis_karty(karta):
    hodnota, barva, licem_nahoru = karta
    if not licem_nahoru:
        return"[???]"
    else:
        if hodnota == 10:
            hodnota = "X"
        elif hodnota == 1:
            hodnota = "A"
        elif hodnota == 11:
            hodnota = "J"
        elif hodnota == 12:
            hodnota = "Q"
        elif hodnota == 13:
            hodnota = "K"

        if barva == "Sr":
            barva = " " + "♥"
        elif barva == "Kr":
            barva = "♣" + " " 
        elif barva == "Pi":
            barva = "♠" + " "
        elif barva == "Ka":
            barva = " " + "♦"


        return"[{}{}]".format(hodnota, barva)

def otoc_kartu(karta, nove_licem_nahoru):
    hodnota, barva, licem_nahoru = karta
    return hodnota, barva, nove_licem_nahoru

def popis_balicku(balicek):
    if not balicek:
        return "[   ]"
    else:
        return popis_karty(balicek[-1])

def udelej_hru():

    import random

    balicek = []
    for hodnota in range(1, 14):
        for barva in 'Pi', 'Sr', 'Ka', 'Kr':
            balicek.append((hodnota, barva, False))
    random.shuffle(balicek)


    A = []
    A.append(otoc_kartu(balicek.pop(), True))

    sloupecky = []
    for cislo_sloupce in range(7):
        novy_sloupec = []
        #vlož schovanou kartu
        for schovana_karta in range(cislo_sloupce):
            novy_sloupec.append(balicek.pop())
        #vlož viditelnou kartu
        novy_sloupec.append(otoc_kartu(balicek.pop(), True))
        sloupecky.append(novy_sloupec)
        #sloupecky neměnné
    sloupecky = tuple(sloupecky)
    balicky = balicek, []
    hromadky = [], [], [], []

    hra = balicky, hromadky, sloupecky
    return hra

def vypis_hru(hra):
    balicky, hromadky, sloupecky = hra
    print('  U     V           W     X     Y     Z')
    print(popis_balicku(balicky[0])+" "+
        popis_balicku(balicky[1])+"       "+
        popis_balicku(hromadky[0])+" "+
        popis_balicku(hromadky[1])+" "+
        popis_balicku(hromadky[2])+" "+
        popis_balicku(hromadky[3]))
    print()
    
    print('  A     B     C     D     E     F     G')
    max_delka = 0
    for sloupec in sloupecky:
        if len(sloupec) > max_delka:
            max_delka = len(sloupec)

    for cislo_radku in range(max_delka):
        for sloupecek in sloupecky:
            if len(sloupecek) > cislo_radku:
                print(popis_karty(sloupecek[cislo_radku]), end=" ")
            else:
                print("     ", end =" ")
        print()


def hrac_vyhral(hra):
    balicky, hromadky, sloupecky = hra
    for hromadka in hromadky:
        if not hromadka:
            return False
        posledni_karta = hromadka[-1]
        hodnota, barva, otocena = posledni_karta
        if hodnota != 13:
            return False
    return True

MOZNOSTI_Z = 'ABCDEFGV'
MOZNOSTI_NA = 'ABCDEFGWXYZ'
NAPOVEDA = """
Příkazy:
? - Vypíše tuto nápovědu.
U - Otočí kartu balíčku (z U do V).
    Nebo doplní balíček U, pokud je prázdný.
EC - Přemístí karty z E na C.
     Za E dosaď odkud karty vzít: A-G nebo V.
     Za C dosaď kam chceš karty dát: A-G nebo W-Z.
E2G - Přemístí 2 karty z E na C
      Za E dosaď odkud kartu vzít: A-G nebo V.
      Za 2 dosaď počet karet.
      Za C dosaď kam chceš kartu dát: A-G nebo W-Z.
Ctrl+C - Ukončí hru
"""

def nacti_tah():
    """Zeptá se uživatele, co dělat

    Stará se o výpis nápovědy.

    Může vrátit buď řetězec 'U' ("lízni z balíčku"), nebo trojici
    (z, pocet, na), kde:
        - `z` je číslo místa, ze kterého karty vezmou (A-G: 0-6; V: 7)
        - `pocet` je počet karet, které se přemisťují
        - `na` je číslo místa, kam se karty mají dát (A-G: 0-6, W-Z: 7-10)

    Zadá-li uživatel špatný vstup, zeptá se znova.
    """
    while True:
        retezec = input('Zadej tah: ')
        retezec = retezec.upper()
        if retezec.startswith('?'):
            print(NAPOVEDA)
        elif retezec == 'U':
            return 'U'
        elif len(retezec) < 2:
            print('Nerozumím tahu')
        elif retezec[0] in MOZNOSTI_Z and retezec[-1] in MOZNOSTI_NA:
            if len(retezec) == 2:
                pocet = 1
            else:
                try:
                    pocet = int(retezec[1:-1])
                except ValueError:
                    print('"{}" není číslo'.format(retezec[1:-1]))
                    continue
            tah = (MOZNOSTI_Z.index(retezec[0]), pocet,
                   MOZNOSTI_NA.index(retezec[-1]))
            print(popis_tahu(tah))
            return tah
        
        else:
            print('Nerozumím tahu')


def popis_tahu(tah):
    if tah == 'U':
        return 'Balíček'
    else:
        z, pocet, na = tah
        return '{} karet z {} na {}'.format(
            pocet, MOZNOSTI_Z[z], MOZNOSTI_NA[na])

def priprav_tah(hra, tah):
    """Zkontroluje, že je tah podle pravidel
    Jako argument bere hru, a tah získaný z funkce `nacti_tah`.
    Vrací buď řetězec 'U' ("lízni z balíčku"), nebo trojici
    (zdrojovy_balicek, pocet, cilovy_balicek), kde `*_balicek` jsou přímo
    seznamy, ze kterých/na které se budou karty přemisťovat, a `pocet` je počet
    karet k přemístění.
    Není-li tah podle pravidel, vynkce vyvolá výjimku `ValueError` s nějakou
    rozumnou chybovou hláškou.
    """
    balicky, cile, sloupce = hra
    if tah == 'U':
        return 'U'
    else:
        z, pocet, na = tah
        if z == 7:
            if pocet != 1:
                raise ValueError('Z balíčku se nedá brát víc karet najednou')
            zdrojovy_balicek = balicky[1]
        else:
            zdrojovy_balicek = sloupce[z]
        if len(zdrojovy_balicek) < pocet:
            raise ValueError('Na to není v {} dost karet!'.format(MOZNOSTI_Z[z]))
        karty = zdrojovy_balicek[-pocet:]
        for hodnota, barva, licem_nahoru in karty:
            if not licem_nahoru:
                raise ValueError('Nemůžeš přesouvat karty, které jsou rubem nahoru!')
        if na < 7:
            cilovy_balicek = sloupce[na]
            if cilovy_balicek:
                zkontroluj_postupku([cilovy_balicek[-1]] + karty)
            else:
                if karty[0][0] != 13:
                    raise ValueError('Do prázdného sloupečku smí jen král, {} nesedí!'.format(
                        popis_karty(karty[0])))
                zkontroluj_postupku(karty)
        else:
            if pocet != 1:
                raise ValueError('Do cíle se nedá dávat víc karet najednou')
            hodnota, barva, otoceni = karty[0]
            cilovy_balicek = cile[na - 7]
            if cilovy_balicek:
                hodnota_p, barva_p, otoceni_p = cilovy_balicek[-1]
                if barva != barva_p:
                    raise ValueError('Cílová hromádka musí mít jednu barvu; {} na {} nesedí'.format(
                        popis_karty(karty[0]), popis_karty(cilovy_balicek[-1])))
                if hodnota != hodnota_p + 1:
                    raise ValueError('Do cíle musíš skládat karty postupně od nejnižších; {} na {} nejde'.format(
                        popis_karty(karty[0]), popis_karty(cilovy_balicek[-1])))
            else:
                if hodnota != 1:
                    raise ValueError('Do prázdného cíle smí jen eso!')
        return zdrojovy_balicek, pocet, cilovy_balicek


def udelej_tah(hra, info):
    balicky, hromadky, sloupce = hra
    if info == 'U':
        if balicky[0]:
            karta = balicky[0].pop()
            karta = otoc_kartu(karta, True)
            print('Karta z balíčku:', popis_karty(karta))
            balicky[1].append(karta)
        else:
            print('Otáčím balíček')
            while balicky[1]:
                karta = balicky[1].pop()
                karta = otoc_kartu(karta, False)
                balicky[0].append(karta)
    else:
        zdrojovy_balicek, pocet, cilovy_balicek = info
        karty = zdrojovy_balicek[-pocet:]

        print('Přesouvám:', end=' ')
        for karta in karty:
            print(popis_karty(karta), end=' ')
        print()
        #zdrojovy_balicek[-pocet:]
        del zdrojovy_balicek[-len(karty):]
        cilovy_balicek.extend(karty)

        if zdrojovy_balicek and not zdrojovy_balicek[-1][2]:
            karta = zdrojovy_balicek.pop()
            karta = otoc_kartu(karta, True)
            print('Otočená karta:', popis_karty(karta))
            zdrojovy_balicek.append(karta)


def druh_barvy(barva):
    if barva == 'Pi':
        return 'černá'
    elif barva == 'Sr':
        return 'červená'
    elif barva == 'Ka':
        return 'červená'
    elif barva == 'Kr':
        return 'černá'


def zkontroluj_postupku(karty):
    for karta_a, karta_b in zip(karty[1:], karty):
        hodnota_a, barva_a, lic_a = karta_a
        hodnota_b, barva_b, lic_b = karta_b
        if hodnota_a != hodnota_b - 1:
            raise ValueError('Musíš dělat sestupné postupky; {} a {} nesedí'.format(
                popis_karty(karta_a), popis_karty(karta_b)))
        if druh_barvy(barva_a) == druh_barvy(barva_b):
            raise ValueError('Musíš střídat barvy; {} je {} a {} taky'.format(
                popis_karty(karta_a), druh_barvy(barva_a), popis_karty(karta_b)))

