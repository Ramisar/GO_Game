from PyQt5.QtWidgets import QAction, QCheckBox, QDesktopWidget, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from board import Board
from score_board import ScoreBoard
from PyQt5.QtGui import QIcon


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        # Adding main menu
        mainMenu = self.menuBar()
        menu = mainMenu.addMenu("Menu")
        helpMenu = mainMenu.addMenu("Help")

        # View Menu
        viewMenu = mainMenu.addMenu("View")

        # Adding icons to menu
        newGame = QAction(QIcon("./icons/new_game2.png"), "New Game", self)
        quit = QAction(QIcon("./icons/exit.png"), "Quit", self)
        about = QAction(QIcon("./icons/about_us.png"), "About us", self)
        rules = QAction(QIcon("./icons/rules.png"), "Rules", self)
        self.scoreWindow = QAction("Score Board", checkable=True)

        # Setting shortcuts for buttons
        newGame.setShortcut("Ctrl+N")
        quit.setShortcut("Ctrl+Q")
        rules.setShortcut("Ctrl+H")
        self.scoreWindow.setShortcut("Ctrl+1")

        # Setting instructions to user
        newGame.setStatusTip("Start a New Game.")
        quit.setStatusTip("Exit application.")
        about.setStatusTip("Meet our project group.")
        rules.setStatusTip("Basic rules for Go board game.")
        self.scoreWindow.setStatusTip("Enable/Disable the Score Board.")

        # Connecting buttons to methods
        newGame.triggered.connect(self.new_game)
        quit.triggered.connect(self.close)
        about.triggered.connect(self.about)
        rules.triggered.connect(self.rules)
        self.scoreWindow.toggled.connect(self.score_window)

        # CheckBox - Setting default value to True
        self.scoreWindow.setChecked(True)

        # Adding buttons to top menu
        menu.addAction(newGame)
        menu.addAction(quit)
        helpMenu.addAction(rules)
        helpMenu.addAction(about)
        viewMenu.addAction(self.scoreWindow)

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.TopDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        # Adding title,icon, position and size for MainWindow
        self.resize(700, 700)
        self.center()
        self.setWindowTitle("Go BoardGame_Project")
        self.setWindowIcon(QIcon("./icons/app_icon.png"))
        self.show()

        # Adding Status menu
        self.statusBar().showMessage("Go Board Game.")

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def new_game(self):
        message = QMessageBox.question(
            self, 'New Game', 'Starting a New Game will erase the actually game. Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # TODO Implement New Game option
        if message == QMessageBox.Yes:
            self.board.resetGame()
        else:
            pass


    def closeEvent(self, event):
        '''Printing exit event message to user'''
        message = QMessageBox.question(
            self, 'Exit', 'Do you really want to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Dealing with user's choice
        if message == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def about(self):
        '''Setting the about_us message box'''
        # Adding tittle, text and displaying icon
        msg = QMessageBox()
        msg.setWindowTitle("About us")
        msg.setText("GO Project - Evandro and Gavin \n\n This project was based on the game Go, the strategy chinese board game, and was created using Python and the library PyQt5 to implement it. \n The objective of this project was to recreate the game itself and implement user's UI, allowing the same to be able to access all the main functions. Unfortunatelly, we couldn't finish all the features and game's rules, leaving the project unfinished.")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def rules(self):
        '''Setting the rules message box'''
        # Adding tittle, text and displaying icon
        message = QMessageBox()
        message.setText("The Rules \n\n  A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces (called stones), one taking the black stones, the other taking white. The main object of the game is to use your stones to form territories by surrounding vacant areas of the board. It is also possible to capture your opponent's stones by completely surrounding them. \n\n Players take turns, placing one of their stones on a vacant point at each turn, with Black playing first. Note that stones are placed on the intersections of the lines rather than in the squares and once played stones are not moved. However they may be captured, in which case they are removed from the board, and kept by the capturing player as prisoners. \n\n For more deatails, please access: https://www.britgo.org/intro/intro2.html")
        message.setIcon(QMessageBox.Question)
        message.setWindowTitle("Rules")
        message.exec()

    def score_window(self):
        if self.scoreWindow.isChecked() == True:
            self.getScoreBoard().show()
        else:
            self.getScoreBoard().close()
