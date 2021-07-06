from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, QRectF
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen
from piece import Piece

# Global variables
x_global = 1
y_global = 1


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    # signal sent when there is a new click location
    clickLocationSignal = pyqtSignal(str)
    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 10000  # the timer updates ever 1 second
    counter = 10  # the number the counter will count down from
    mouse_click = False

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = [
            [0 for i in range(self.boardHeight)] for j in range(self.boardWidth)]
        self.printBoardArray()  # TODO - uncomment this method after create the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row])
                         for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        # TODO Mouse click event

        # Getting the X and Y from QPoint()
        posX = self.lastPoint.x()
        posY = self.lastPoint.y()
        x_global = int(posX/self.squareWidth())  # Assigning the repective row
        # Assigning the respective col
        y_global = int(posY/self.squareHeight())

        print(x_global)
        print(y_global)
        self.mouse_click = True

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        # start the timer with the correct speed
        self.timer.start(self.timerSpeed, self)
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            # if we do not handle an event we should pass it to the super
            super(Board, self).timerEvent(event)
            # class for handelingother wise pass it to the super class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

        if self.mouse_click == True:
            print("test")
            self.movement(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.x()) + "," + str(
            event.y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

        # TODO **Evandro**
        # Implement mouse clicking and location
        # Setting lasPoint position
        self.lastPoint = event.pos()
        print(self.lastPoint)
        self.mousePosToColRow(self)
        # event.y()
        # if event.y() < 100:
        #     self.paintEvent()
        # event.y()

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        return print("test")

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(204, 102, 0), Qt.SolidPattern))

        for row in range(0, Board.boardHeight - 1):
            for col in range(0, Board.boardWidth - 1):
                painter.save()
                # TODO set this value equal the transformation in the column direction
                colTransformation = self.squareWidth() * col
                # TODO set this value equal the transformation in the row direction
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                painter.drawRect(40, 40, self.squareWidth(),
                                 self.squareHeight())
                painter.restore()
                # painter.setPen(QPen(Qt.black, 2, Qt.SolidLine)) # TODO make board checked
                #painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                # TODO set this value equal the transformation in the column direction
                colTransformation = self.squareWidth() * col
                # TODO set this value equal the transformation in the row direction
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)

                # TODO draw some the pieces as ellipses
                # TODO choose your colour and set the painter brush to the correct colour
                radius = (self.squareWidth() * 0.35) / 2
                center = QPoint(40, 40)
                painter.drawEllipse(center, radius, radius)

                painter.restore()

    # TODO needs implementation Evandro -- Mouse Click event
    def movement(self, painter):

        test = painter

        test.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        test.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        test.translate(
            self.squareWidth() * x_global, self.squareHeight() * y_global)
        radius = (self.squareWidth() * 0.35) / 2
        center = QPoint(40, 40)
        test.drawEllipse(center, radius, radius)
