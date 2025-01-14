#Import potrzebnych bibliotek.
import numpy as np, termcolor as tc, string, os, tabulate

#Funkcja Pobierająca losowe słowo zawierające 5 liter.
def getRandomWord(): 
    words = np.array(())
    with open("frekwencja.txt", encoding="UTF-8") as file:
        lines = file.readlines()
        for i in lines:
            i = i.split(";")[0]
            if len(i) == 5:
                words = np.append(words, i)
    return np.random.choice(words)

#Funkcja zawierająca baze słów.
def wordBase():
    with open("slowa.txt", encoding="UTF-8") as file:
        words = file.read()
        wordsChecked = words.split()
    with open("frekwencja.txt", encoding="UTF-8") as f:
        words2 = f.readlines()
        wordsChecked2 = []
        for i in words2:
            i = i.split(";")[0].lower()
            wordsChecked2.append(i)
    wordsChecked.extend(wordsChecked2)
    return wordsChecked

#Opcje oraz objaśnienie gry:
#Dodanie kolorów.
os.system("color")

#Symbole do użycia oraz ich kopia do późniejszego fortmatowania kolorów klawiatury.
symbolsToUse = [i for i in string.ascii_lowercase] + ["ę", "ó", "ą", "ś", "ł", "ż", "ź", "ć", "ń"]
symbolsToUseCopy = symbolsToUse.copy()

#Wyrazy do użycia, randomowe słowo jak i zmienna kopiująca wyraz po to aby został on nienaruszony.
#W późniejszym kodzie zmienna word zostaje lekko modyfikowana.
wordsToUse = wordBase()
word = getRandomWord().lower()
word2 = word

#Pozostałe opcje tabeli, klawiatury, prób oraz zgadnięcia słowa.
table = np.full((6,5), " ").tolist()
tries = 0
guess = None
keyboard = """
|  Ą Ć Ę Ł Ó Ś Ń Ż Ź  |
| Q W E R T Y U I O P | 
|  A S D F G H J K L  |
|   Z X C V B N M     |"""
print (f"\n=== Zasady gry ===\n\nTwoim zadaniem jest zgadnąć losowo wygenerowane słowo.\n{tc.colored('X', 'red', attrs=['bold'])} - oznacza, że litery w ogóle nie ma w wyrazie.\n{tc.colored('X', 'yellow', attrs=['bold'])} - oznacza, że litera znajduje się w wyrazie, ale na innym miejscu.\n{tc.colored('X', 'green', attrs=['bold'])} - oznacza, że litera stoi na właściwym miejscu.\n\nDodatkowo będziesz widział jakich liter już użyłeś.\n\nW sumie tyle, powodzenia :)\n")
while True:
    #Printowanie tabeli oraz sprawdzanie poprawności słowa.
    print(tabulate.tabulate(table, tablefmt="rounded_grid"), keyboard)
    if guess != word2:
        if tries < 6:
            guess = input("\nPodaj słowo: ").lower()
            #Sprawdzam czy wszystkie symbole podane przez gracza należą do listy symboli które można użyć.
            if all(i in symbolsToUse for i in guess):
                #Następnie sprawdzam długość słowa.
                if len(guess) == 5:
                    #Oraz czy słowo znajduje się w bazie słów.
                    if guess in wordsToUse:
                        wordCopy = ["-"] * len(word)
                        word = word2
                        #Pierwsza pętla sprawdzająca dokładną pozycję litery w słowie (Najwyższy priorytet)
                        for i in range(len(word)):
                            if guess[i] == word[i]:
                                wordCopy[i] = "X"
                                word = word.replace(guess[i], "-", 1)
                        #Druga pętla sprawdzająca ogólną pozycję litery w słowie (Niższy priorytet)
                        for i in range(len(word)):
                            if guess[i] in word and wordCopy[i] == "-":
                                wordCopy[i] = "O"
                                word = word.replace(guess[i], "-", 1)
                        #Trzecia pętla kolorująca odpowiednio litery w tabeli.
                        for i in range(len(guess)):
                            if wordCopy[i] == "-":
                                table[tries][i] = tc.colored(guess[i].upper(), "red", attrs=["bold"])
                            elif wordCopy[i] == "O":
                                table[tries][i] = tc.colored(guess[i].upper(), "yellow", attrs=["bold"])
                            elif wordCopy[i] == "X":
                                table[tries][i] = tc.colored(guess[i].upper(), "green", attrs=["bold"])
                        #Czwarta pętla kolorująca odpowiednio litery w klawiaturze.
                        for i in range(len(guess)):
                            if guess[i] == word2[i]:
                                if guess[i] in symbolsToUseCopy:
                                    keyboard = keyboard.replace(guess[i].upper(), tc.colored(guess[i].upper(), "white", "on_green"))
                                    symbolsToUseCopy.remove(guess[i])
                            elif guess[i] in word2:
                                if guess[i] in symbolsToUseCopy:
                                    keyboard = keyboard.replace(guess[i].upper(), tc.colored(guess[i].upper(), "white", "on_yellow"))
                            else:
                                keyboard = keyboard.replace(guess[i].upper(), tc.colored(guess[i].upper(), "white", "on_red"))
                        tries += 1
                    else:
                        print("Nie ma takiego słowa w bazie słów!")
                else:
                    print("Nie jest to 5 literowe słowo!")
            else:
                print("Możesz używać tylko polskich znaków!")
        else:
            print(f"\n\nNiestety przegrałeś! Szukanym słowem było: {word2}\n\n")
            quit()
    else:
        print("\n\nGRATULACJE MORDO WYGRAŁEŚ!\n\n")
        quit()