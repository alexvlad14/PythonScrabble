from random import random
from itertools import permutations
import io, os
import json
from sys import exit

"""Παρακάτω οι 5 κλάσεις οι οποίες περιγράφονται στην εκφώνηση της εργασίας
   SakClass, Player, Human, Computer, Game για την δημιουργία του Scrabble
   """

class SakClass:
    def __init__(self):
        # Tα γράμματα της αλφαβήτου και οι φορές που υπάρχουν.
        self.letters_frequency = {
            'Α': 12,'Β': 1,'Γ': 2,'Δ': 2,'Ε': 8,'Ζ': 1,'Η': 7,'Θ': 1, 'Ι': 8,'Κ': 4,'Λ': 3,'Μ': 3,'Ν': 6,
            'Ξ': 1,'Ο': 9, 'Π': 4, 'Ρ': 5, 'Σ': 7, 'Τ': 8, 'Υ': 4, 'Φ': 1, 'Χ': 1, 'Ψ': 1,'Ω': 3,
            '_': 2
        }

        self.copy_of_letters_frequency = self.letters_frequency.copy()
        # Tα γράμματα της αλφαβήτου και η αξία τους.
        self.letters_value = {
            'Α': 1,'Β': 8,'Γ': 4,'Δ': 4,'Ε': 1, 'Ζ': 10,'Η': 1,'Θ': 10,'Ι': 1,'Κ': 2,'Λ': 3,
            'Μ': 3, 'Ν': 1,'Ξ': 10,'Ο': 1,'Π': 2,'Ρ': 2,'Σ': 1,'Τ': 1,'Υ': 2,'Φ': 8,'Χ': 8,
            'Ψ': 10,'Ω': 3,'_': 0
        }

        self.letters_sum = sum(self.letters_frequency.values())  # Αθροισμα Γραμμάτων.

    # Αρχικοποιεί ξανά το σακουλάκι κάθε φορά που ξεκινάμε μια παρτίδα
    def randomize_bag(self):
        self.letters_frequency = self.copy_of_letters_frequency.copy()
        self.letters_sum = sum(self.letters_frequency.values())


  

    # Επιστρέφει κάποια γράμματα στο σακουλάκι
    def putbackletters(self, letters):
        for letter in letters:
            self.letters_frequency[letter] += 1
            self.letters_sum += 1

      # Η συνάρτηση θα επιστρέωει Ν πλήθος γραμμάτων τα οποία θα επιλεχθούν τυχαία.
    def getletters(self, N):
        letters = []
        for i in range(N):
            random_value = random()  # επιστρέφει αριθμό από 0 εως 1
            boundary = 0
            for key, val in self.letters_frequency.items():
                boundary += val / self.letters_sum
                if random_value <= boundary and val != 0:
                    self.letters_frequency[key] -= 1
                    self.letters_sum -= 1
                    letters.append(key)
                    break
        return letters

class Player:
    def __init__(self, bag, greek7):
        self.bag = bag
        self.pieces = []  # Το ταμπλό του παίκτη.
        self.greek7 = greek7  
        self.points = 0  

    def __repr__(self):
        return f'Player({self.bag},{self.greek7})'

  # H συνάρτηση του επιστρέφει γράμματα για να έχει 7 πάλι στο ταμπλό του.
    def replace_word(self, word):
        size_of_Bag = len(word)
        if size_of_Bag > self.bag.letters_sum:
            return 'end'
        self.pieces += self.bag.getletters(size_of_Bag)

    def init_table(self):
        self.pieces = self.bag.getletters(7)
        self.points = 0

    
    def show_table(self):
        for p in self.pieces:
            print(f'{p},{self.bag.letters_value[p]}',  end=' ' )
        print("\n")


    # Υπολογισμός score
    def score_word(self, word):
        score = 0
        for l in word:
            score += self.bag.letters_value[l]
        return score

  
  

    # Έλεγχος για το αν η λέξη που δίνει ο παίκτης είναι αποδεκτή.
    def correct_word(self, word):
        joker = word.count('_')
        if joker == 0:
            return word in self.greek7
        elif joker == 1:
            for g in self.bag.letters_frequency.keys():
                new_word = word.replace('_', g)
                if new_word in self.greek7:
                    return True
            return False
        for g in self.bag.letters_frequency.keys():
            new_word = word.replace('_', g, 1)  
            for g2 in self.bag.letters_frequency.keys():
                new_word_2 = new_word.replace('_', g2)
                if new_word_2 in self.greek7:
                    return True
        return False

    # Κληρονομικότητα
    def play(self):
        pass


class Human(Player):
    def __init__(self, bag, greek7):
        super().__init__(bag, greek7)

    def __repr__(self):
        return f'Human({self.bag},{self.greek7})'

    def play(self):
        # Συνθήκες τερματισμού
        while True:
            print("Στο σακουλάκι υπάρχουν:", self.bag.letters_sum, "γράμματα! Σειρά σου να παίξεις:")
            print("Διαθέσιμα γράμματα:")
            self.show_table()
            player_input = input("Γράψε λέξη αλλιώς πάτα το p ή enter για πάσο ή q για έξοδο):").upper() 
            if player_input == 'Q':  
                return 'end'
            if player_input == 'P' or player_input == '':  # Αντικατάσταση γραμμάτων
                self.bag.putbackletters(self.pieces)
                self.pieces = self.bag.getletters(7).copy()
                print("Επέλεξες πάσο.")
                return

            flag = True  # Έλεγχος για την δημιουργία της λέξης με τα γράμματα που υπάρχουν
            lost_letters = []
            for i in player_input:
                flag = False
                if i in self.pieces:
                    lost_letters.append(self.pieces.pop(self.pieces.index(i)))
                    flag = True
                if not flag:
                    print("Μη αποδεκτή λέξη. Προσπάθησε ξανά:")
                    self.pieces += lost_letters.copy()
                    break

            if not flag:
                continue
            # Eμφανίζονται οι βαθμοί της λέξης και αθροίζονται οι πόντοι του παίκτη 
            if self.correct_word(player_input):
                print("Βαθμοί λέξης:", self.score_word(player_input))
                end_statement = self.replace_word(player_input)
                if end_statement == 'end':
                    self.points += self.score_word(player_input)
                    print("Οι συνολικοί πόντοι σου:", self.points)
                    return end_statement
                self.points += self.score_word(player_input)
                print("Οι συνολικοί πόντοι σου:", self.points)
                break  
            self.pieces += lost_letters.copy()
            print("Η Λέξη δεν υπάρχει στο λεξικό.")


"""Οι αλγόριθμοι του υπολογιστή είναι οι mix-max-smart με default το min"""


class Computer(Player):
    def __init__(self, bag, greek7):
        super().__init__(bag, greek7)
        self.setting_choice = 'min'  

    def __repr__(self):
        return f'Computer({self.bag},{self.greek7})'

    # Επιλέγει τη μικρότερη δυνατή λέξη σε πλήθος γραμμάτων
    def min_letters(self):
        for i in range(2, 8):
            for word in permutations(self.pieces, i):  # Πρώτο correct_word 
                player_input = "".join(word)
                if self.correct_word(player_input):
                    return player_input

        return 'end' 

    # Επιλέγει τη μεγαλύτερη αποδεκτή λέξη σε πλήθος γράμματων
    def max_letters(self):
        for i in range(7, 1, -1):
            for word in permutations(self.pieces, i):
                player_input = "".join(word)
                if self.correct_word(player_input):
                    return player_input
        return 'end'

    # Επιλέγει τη μεγαλύτερη σε αξία λέξη
    def smart(self):
        max_points = -1
        max_word = 'end'
        for i in range(2, 8):
            for word in permutations(self.pieces, i):
                player_input = "".join(word)
                if self.correct_word(player_input):
                    if max_points < self.score_word(player_input):
                        max_points = self.score_word(player_input)
                        max_word = player_input
        return max_word

    # Συνάρτηση play τρέχει κάθε φορά που είναι η σειρά του Η/Υ ή καλείται στη Game στη run 
    # όταν παίζει ο παίκτης
    def play(self):
        print("Στο σακουλάκι:", self.bag.letters_sum, "γράμματα! Σειρά του Η/Υ να παίξει:")

        print("Γράμματα Η/Υ:")
        self.show_table()
        if self.setting_choice == 'min':
            word = self.min_letters()
        elif self.setting_choice == 'max':
            word = self.max_letters()
        elif self.setting_choice == 'smart':
            word = self.smart()
        if word=='end':
            print("************************************")
            print()
            print("Ο υπολογιστής δε βρήκε λέξη.")
            return 'end'

        self.points += self.score_word(word)
        print("Λέξη Η/Υ:", word)
        print("Βαθμοί λέξης:", self.score_word(word), " Συνολικοί πόντοι Η/Υ:", self.points)
        for g in word: # Αφαίρεση γραμμάτων
            self.pieces.remove(g)

        end_statement = self.replace_word(word)
        if end_statement == 'end':
            return end_statement


# 
class Game:
    def __init__(self, bag=SakClass(), greek7=set()):
        self.bag = bag
        self.greek7 = greek7
        if len(greek7) == 0:
            with io.open('greek7.txt', 'r',
                         encoding='utf-8') as file:  # Άνοιγμα αρχείου για να πάρουμε τις λέξεις.
                for line in file:
                    greek7.add(line.rstrip())
        self.human = Human(self.bag, self.greek7)
        self.computer = Computer(self.bag, self.greek7)

    def __repr__(self):
        return f'Game({self.bag},{self.greek7})'

    
    # Αρχικοποιεί τα δεδόμενα των παικτών με 0 και τις επόμενες θα καλείται η update_file (χρήση json)
    def init_file(self):
        with open("points.json", "w") as Score:
            json.dump({
                'Παίκτης': 0,
                'Η/Υ': 0
            }, Score)

    # Το αρχείο δείχνει πόσες φορές έχει κερδίσει ο παίκτης ή ο υπολογιστής.
    
    def update_file(self):
        if not os.path.exists('points.json'):
            self.init_file()
            return
        with open("points.json") as Score:
            data = json.load(Score)
            if not isinstance(data, dict):
                self.init_file()

            success_statement = [data.get('Παίκτης', -1), data.get('Η/Υ', -1)]
            if -1 in success_statement:  # Σε περίπτωση λάθους στη δομή του αρχείου, θα αρχικοποιηθεί ξανά.
                self.init_file()
                return
    #Εμφάνιση του μενού επιλογής και των στατιστικών
    def setup(self):
        main_menu = None
        while all(main_menu != val for val in ['2', '3', 'Q']):
            print()
            main_menu = input("***** SCRABBLE *****\n"
                              "--------------------\n"
                              "1: Σκορ\n"
                              "2: Ρυθμίσεις\n"
                              "3: Παιχνίδι\n"
                              "Q: Έξοδος\n"
                              "--------------------\n").upper()
            if main_menu == '1':
                with open("points.json") as file:
                    data = json.load(file)
                    print("Μπράβο! Κέρδισες τον υπολογιστή ", data['Παίκτης'], "φορές")
                    print("Εχασες απο τον υπολογιστή ", data['Η/Υ'], "φορές")
                    input("Enter για να συνεχίσεις")
        if main_menu == '3': return
        if main_menu == 'Q': exit()
        if main_menu == '2':
            dict = {1: 'min', 2: 'max', 3: 'smart'}
            difficulty = input("Διάλεξε ένα από τα επίπεδα (1,2 ή 3): 1.min, 2.max, 3.smart\n")
            while all(difficulty != val for val in ['1', '2', '3']):
                difficulty = input("Επίλεξε αριθμό από το 1 ως το 3: 1.min, 2.max, 3.smart\n")
            return dict[int(difficulty)]

    # Εκτέλεση του παιχνιδιού
    def run(self):
        self.update_file()
        while True:
            self.bag.randomize_bag()
            difficulty = self.setup()
            if difficulty != None:
                self.computer.setting_choice = difficulty
            self.human.init_table()
            self.computer.init_table()
            while True:
                end_statement = self.human.play()  # η σειρά του παίκτη

                if end_statement == 'end':
                    self.end()
                    break
                print("----------------------------")
                end_statement = self.computer.play()  # η σειρά του Η/Υ
                if end_statement == 'end':
                    self.end()
                    break
                print("----------------------------")

    # Καλείται όταν επιστρέφεται 'end'.
    def end(self):
        with open("points.json") as file:
            data = json.load(file)
        print()
        print("************************************")
        print("Οι πόντοι σου:", self.human.points)
        print("Οι πόντοι του Η/Υ:", self.computer.points)
        if self.human.points > self.computer.points:
            print("Κέρδισες τον Η/Υ!")
            data['Παίκτης'] += 1
        elif self.human.points < self.computer.points:
            print("Έχασες από τον Η/Υ!")
            data['Η/Υ'] += 1
        else:
            print("Iσοπαλία!")
        print("Μπράβο! Κέρδισες τον υπολογιστή ", data['Παίκτης'], "φορές")
        print("Εχασες απο τον υπολογιστή ", data['Η/Υ'], "φορές")
        print("************************************")

        with open("points.json", "w") as file:
            json.dump(data, file)
        input("Enter για να συνεχίσεις")
