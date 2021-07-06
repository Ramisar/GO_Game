
from PyQt5.QtWidgets import QAction, QDockWidget, QFrame, QGridLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from board import Board
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtGui
from functools import partial

class ScoreBoard(QDockWidget):
    ''' base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.board = Board(self)
        self.initUI()
        
    def initUI(self):
        '''initiates ScoreBoard UI'''
        
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets. Added Grid Layout
        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout()
        self.mainWidget.setLayout(self.mainLayout)

        # Added the New Button
        self.button_newGame = QPushButton("New Game")
        self.button_newGame.setFixedWidth(120)
        self.button_newGame.setFixedHeight(100)
        self.button_newGame.setStatusTip("Start a New Game.")
        self.button_newGame.clicked.connect(
            partial(self.on_click, self.button_newGame))
        self.button_newGame.setIcon(QIcon(QPixmap("./icons/new_game2.png")))

        # Added the Pass button
        self.button_pass = QPushButton("Pass")
        self.button_pass.setFixedWidth(100)
        self.button_pass.setFixedHeight(100)
        self.button_pass.setShortcut("Space")
        self.button_pass.setStatusTip(
            "Pass your turn! A player can pass twice before ending game.")
        self.button_pass.clicked.connect(self.on_click)

        # create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time Remaining: ")
        self.label_piecescaptured1 = QLabel("Pieces Captured: ")
        self.label_piecescaptured2 = QLabel("Pieces Captured: ")
        self.label_player1 = QLabel("Player 1")
        self.label_player2 = QLabel("Player 2")

        # Labels Font
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.label_player1.setFont(myFont)
        self.label_player2.setFont(myFont)
        self.label_player1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player2.setAlignment(QtCore.Qt.AlignCenter)

        # Setting boxes styles
        self.label_timeRemaining.setFrameStyle(
            QFrame.Panel | QFrame.Sunken)
        self.label_piecescaptured1.setFrameStyle(
            QFrame.Panel | QFrame.Sunken)
        self.label_piecescaptured2.setFrameStyle(
            QFrame.Panel | QFrame.Sunken)
        self.label_clickLocation.setFrameStyle(
            QFrame.Panel | QFrame.Sunken)
        self.label_timeRemaining.setLineWidth(3)
        self.label_piecescaptured1.setLineWidth(3)
        self.label_piecescaptured2.setLineWidth(3)
        self.label_clickLocation.setLineWidth(3)

        # Adding buttons to ScoreBoard
        self.mainLayout.addWidget(self.button_newGame, 0, 0, 0, 1)
        self.mainLayout.addWidget(self.button_pass, 0, 1, 0, 1)
        self.mainLayout.addWidget(self.label_player1, 0, 2)
        self.mainLayout.addWidget(self.label_player2, 0, 3)
        self.mainLayout.addWidget(
            self.label_piecescaptured1, 1, 2)  # TODO Pieces Captured
        self.mainLayout.addWidget(
            self.label_piecescaptured2, 1, 3)  # TODO Pieces Captured
        self.mainLayout.addWidget(self.label_clickLocation, 2, 3)
        self.mainLayout.addWidget(self.label_timeRemaining, 2, 2)
        self.setWidget(self.mainWidget)
        self.show()

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''


    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    # checks to make sure that the following slot is receiving an argument of the type 'int'
    @pyqtSlot(str)
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        print('slot '+update)
        # self.redraw()

    # TODO still needs to implement the counter for captured pieces
    @pyqtSlot(int)
    def setPiecesCaptured(self, piecesCaptured):
        '''Updates the number of pieces captured'''
        update = "Pieces Captured: " + int(piecesCaptured)
        self.label_piecescaptured1.setText(update)

    def on_click(self, btn):
        # TODO Implement Pass movement and New Game

        if btn == self.button_newGame:
            message = QMessageBox.question(
                self, 'New Game', 'Starting a New Game will erase the actually game. Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            # TODO Implement New Game option
            if message == QMessageBox.Yes:
                self.board.resetGame()

            else:
                pass

            print("New Game Event")
        else:
            message = QMessageBox.question(
                self, 'Pass Movement', 'Are you sure that you want to pass your turn?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            # TODO Implement Pass option
            if message == QMessageBox.Yes:
                print("Pass")

            else:
                pass

            print("Pass event.")


