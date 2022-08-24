from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
import sys
import random


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("Cursach.ui", self)
        self.setWindowTitle("BleckJack")
        self.setWindowIcon(QIcon("iconca.png"))


        # Define our widgets
        self.dealerCard1 = self.findChild(QLabel, "dealerCard1")
        self.dealerCard2 = self.findChild(QLabel, "dealerCard2")
        self.dealerCard3 = self.findChild(QLabel, "dealerCard3")
        self.dealerCard4 = self.findChild(QLabel, "dealerCard4")
        self.dealerCard5 = self.findChild(QLabel, "dealerCard5")

        self.playerCard1 = self.findChild(QLabel, "playerCard1")
        self.playerCard2 = self.findChild(QLabel, "playerCard2")
        self.playerCard3 = self.findChild(QLabel, "playerCard3")
        self.playerCard4 = self.findChild(QLabel, "playerCard4")
        self.playerCard5 = self.findChild(QLabel, "playerCard5")

        self.dealerlabel = self.findChild(QLabel, "dlabel")
        self.playerlabel = self.findChild(QLabel, "plabel")
        self.result_label = self.findChild(QLabel, "labe_fo_result")

        self.Shuffle_Btn = self.findChild(QPushButton, "Deal_card_button")
        self.Hit_me_Btn = self.findChild(QPushButton, "Hit_me_button")
        self.Stand_Btn = self.findChild(QPushButton, "stand_button")

        # Click Button
        self.Shuffle_Btn.clicked.connect(self.shuffle)
        self.Hit_me_Btn.clicked.connect(self.playerHit)
        #self.Stand_Btn.clicked.connect(self.dealerHit)
        self.Stand_Btn.clicked.connect(self.stand)
        
        # Shuffle deck
        self.shuffle()
        # Show the app
        self.show() 
    
    def stand(self):
        self.Hit_me_Btn.setEnabled(False)
        self.Stand_Btn.setEnabled(False)

        self.player_total = 0
        self.dealer_total = 0

        for score in self.player_score:
            self.player_total += score
        
        for score in self.dealer_score:
            self.dealer_total += score

        if self.dealer_total >= 17:
            # Check for bust
            if self.dealer_total > 21:
                QMessageBox.about(self, "PLayer Wins!" , f"Player wins! Dealer has: {self.dealer_total}  Player has: {self.player_total}!!")
            elif self.dealer_total == self.player_total:
                QMessageBox.about(self, "Tie!" , f"No one wins! Dealer has: {self.dealer_total}  Player has: {self.player_total}!!")
            elif self.dealer_total > self.player_total:
                QMessageBox.about(self, "Dealer Wins!" , f"Dealer wins! Dealer has: {self.dealer_total}  Player has: {self.player_total}!!")
            elif len(self.dealer_score) == 5:
                 QMessageBox.about(self, "Dealer wins!" , f"Dealer has 5 card")
            else:
                QMessageBox.about(self, "PLayer Wins!" , f"Player wins! Dealer has: {self.dealer_total}  Player has: {self.player_total}!!")
        else:
            self.dealerHit()
            self.stand()
        
    def check(self, player):
        # Keep track our score
        self.player_total = 0
        self.dealer_total = 0

        if player == "dealer":
            if len(self.dealer_score) == 2:
                if self.dealer_score[0] + self.dealer_score[1] == 21:
                    self.blackjack_status["dealer"] = "yes"
            else:
                for score in self.dealer_score:
                    self.dealer_total += score
                if self.dealer_total == 21:
                    self.blackjack_status["dealer"] = "yes"
                elif self.dealer_total > 21:
                    for card_num, card in enumerate(self.dealer_score):
                        if card == 11:
                            self.dealer_score[card_num] = 1

                            # Update totals
                            self.dealer_total = 0
                            for score in self.dealer_score:
                                self.dealer_total += score

                            # Chack for  win/bust
                            if self.dealer_total > 21:
                                self.blackjack_status["dealer"] = "bust"
                    else:
                        # Check for win/bust
                        if self.dealer_total == 21:
                            self.blackjack_status["dealer"] = "yes"
                        elif self.dealer_total > 21:
                            self.blackjack_status["dealer"] = "bust"
                        elif len(self.dealer_score) == 5:
                            self.blackjack_status["dealer"] = "5card"


                    
        if player == "player":
            if len(self.player_score) == 2:
                if self.player_score[0] + self.player_score[1] == 21:
                    self.blackjack_status["player"] = "yes"
            else:
                for score in self.player_score:
                    self.player_total += score
                if self.player_total == 21:
                    self.blackjack_status["player"] = "yes"
                elif self.player_total > 21:
                    for card_num, card in enumerate(self.player_score):
                        if card == 11:
                            self.player_score[card_num] = 1

                            # Update totals
                            self.player_total = 0
                            for score in self.player_score:
                                self.player_total += score

                            # Chack for  win/bust
                            if self.player_total > 21:
                                self.blackjack_status["player"] = "bust"
                    else:
                        # Check for win/bust
                        if self.player_total == 21:
                            self.blackjack_status["player"] = "yes"
                        elif self.player_total > 21:
                                self.blackjack_status["player"] = "bust"
                        elif len(self.player_score) == 5:
                            self.blackjack_status["player"] = "5card"

                    #self.blackjack_status["player"] = "bust"
                    self.dealerlabel.setText(f"Dealer; Dealer score: {self.dealer_total}")
                    self.playerlabel.setText(f"Player; Player score: {self.player_total}")



        # Check for blackjack                 
        if len(self.player_score) == 2 and len(self.dealer_score) == 2:
            # Check for tie
            if self.blackjack_status["dealer"] == "yes" and self.blackjack_status["player"] == "yes":
                QMessageBox.about(self, "Tie!" , "BlackJack!!")
                self.Hit_me_Btn.setEnabled(False)
                self.Stand_Btn.setEnabled(False)
            # Check for dealer wins
            elif self.blackjack_status["dealer"] == "yes":
                QMessageBox.about(self, "Dealer Wins!" , "BlackJack!!")
                self.Hit_me_Btn.setEnabled(False)
                self.Stand_Btn.setEnabled(False)
            # Check for player wins
            elif self.blackjack_status["player"] == "yes":
                QMessageBox.about(self, "PLayer Wins!" , "BlackJack!!")
                self.Hit_me_Btn.setEnabled(False)
                self.Stand_Btn.setEnabled(False)
        
        else:
            if self.blackjack_status["player"] == "bust":
                QMessageBox.about(self, "PLayer lose!" , "Bust!!")
                self.Hit_me_Btn.setEnabled(False)
                self.Stand_Btn.setEnabled(False)
            elif self.blackjack_status["dealer"] == "bust":
                QMessageBox.about(self, "Deler lose!" , "Bust!!")
                self.Hit_me_Btn.setEnabled(False)
                self.Stand_Btn.setEnabled(False)
            elif self.blackjack_status["player"] == "5card":
                QMessageBox.about(self, "Player wins!" , "Player has 5 card")
                self.Hit_me_Btn.setEnabled(False)
                self.Stand_Btn.setEnabled(False)

    def shuffle(self):
        # Dict to track blackjack status
        self.blackjack_status = {"dealer":"no", "player":"no"}

        # Enable btns
        self.Hit_me_Btn.setEnabled(True)
        self.Stand_Btn.setEnabled(True)


        # Reset card images
        pixmap = QPixmap("cards/green.png")
        self.dealerCard1.setPixmap(pixmap)
        self.dealerCard2.setPixmap(pixmap)
        self.dealerCard3.setPixmap(pixmap)
        self.dealerCard4.setPixmap(pixmap)
        self.dealerCard5.setPixmap(pixmap)

        self.playerCard1.setPixmap(pixmap)
        self.playerCard2.setPixmap(pixmap)
        self.playerCard3.setPixmap(pixmap)
        self.playerCard4.setPixmap(pixmap)
        self.playerCard5.setPixmap(pixmap)

        # Define our deck
        suits = ["diamonds", "clubs", "hearts", "spades"]
        values = range(2, 15)
        #11 - Jack, 12 - Queen, 13 - King, 14 - Ace

        # Create Deck
        self.deck = []

        for suit in suits:
            for value in values:
                self.deck.append(f"{value}_of_{suit}")
        
        # Create Our Players
        self.dealer = []
        self.player = []
        self.dealer_score = []
        self.player_score = []
        self.playerSpot = 0
        self.dealerSpot = 0

        self.dealerHit()
        self.dealerHit()
        self.playerHit()
        self.playerHit()

    
    def dealerHit(self):
        if self.dealerSpot <= 5:
            try:
                # Grab a random card for dealer
                card1 = random.choice(self.deck)
                # Remove That card from the deck
                self.deck.remove(card1)
                # Add that card to dealer list
                self.dealer.append(card1)

                # Add card to dealer score
                self.dcard = int(card1.split("_", 1)[0])
                if self.dcard == 14:
                    self.dealer_score.append(11)
                elif self.dcard == 13 or self.dcard == 12 or self.dcard == 11:
                    self.dealer_score.append(10)
                else:
                    self.dealer_score.append(self.dcard)


                # Output card on screen
                pixmap1 = QPixmap(f"cards/{card1}.png")

                if self.dealerSpot == 0:
                    self.dealerCard1.setPixmap(pixmap1) 
                    self.dealerSpot += 1

                elif self.dealerSpot == 1:
                    self.dealerCard2.setPixmap(pixmap1) 
                    self.dealerSpot += 1

                elif self.dealerSpot == 2:
                    self.dealerCard3.setPixmap(pixmap1) 
                    self.dealerSpot += 1

                elif self.dealerSpot == 3:
                    self.dealerCard4.setPixmap(pixmap1) 
                    self.dealerSpot += 1

                elif self.dealerSpot == 4:
                    self.dealerCard5.setPixmap(pixmap1) 
                    self.dealerSpot += 1
                
                    
                #self.setWindowTitle(f"{len(self.deck)} cards left in a deck")
            except:
                self.setWindowTitle("Game Over")
            
            self.check("dealer")

    def playerHit(self):
        if self.playerSpot <= 5:
            try:
                # Grab a random card for dealer
                card1 = random.choice(self.deck)
                # Remove That card from the deck
                self.deck.remove(card1)
                # Add that card to dealer list
                self.dealer.append(card1)
                
                # Add card to player score
                self.pcard = int(card1.split("_", 1)[0])
                if self.pcard == 14:
                    self.player_score.append(11)
                elif self.pcard == 13 or self.pcard == 12 or self.pcard == 11:
                    self.player_score.append(10)
                else:
                    self.player_score.append(self.pcard)

                # Output card on screen
                pixmap1 = QPixmap(f"cards/{card1}.png")

                if self.playerSpot == 0:
                    self.playerCard1.setPixmap(pixmap1) 
                    self.playerSpot += 1

                elif self.playerSpot == 1:
                    self.playerCard2.setPixmap(pixmap1) 
                    self.playerSpot += 1

                elif self.playerSpot == 2:
                    self.playerCard3.setPixmap(pixmap1) 
                    self.playerSpot += 1

                elif self.playerSpot == 3:
                    self.playerCard4.setPixmap(pixmap1) 
                    self.playerSpot += 1

                elif self.playerSpot == 4:
                    self.playerCard5.setPixmap(pixmap1) 
                    self.playerSpot += 1
                
                self.dealer_total = 0
                self.player_total = 0

                for score in self.dealer_score:
                    if self.dealer_total <= 21:
                        self.dealer_total += score
                    elif self.dealer_total > 21:
                        for card_num, card in enumerate(self.dealer_score):
                            if card == 11:
                                self.dealer_score[card_num] = 1
                                self.dealerlabel.setText(f"Dealer; Dealer score: {self.dealer_total}")
                    
                
                for score in self.player_score:
                    if self.player_total <= 21:
                        self.player_total += score
                    elif self.player_score > 21:
                        for card_num, card in enumerate(self.player_score):
                            if card == 11:
                                self.player_score[card_num] = 1
                            self.playerlabel.setText(f"Player; Player score: {self.player_total}")
                    

                self.dealerlabel.setText(f"Dealer; Dealer score: {self.dealer_total}")
                self.playerlabel.setText(f"Player; Player score: {self.player_total}")
                self.setWindowTitle(f"{len(self.deck)} cards left in a deck")
            except:
                self.setWindowTitle("Game Over")
            
            self.check("player")

        
    
# Initialize the app 
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()