from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, QRectF
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    # signal sent when there is a new click location
    clickLocationSignal = pyqtSignal(str)
    boardWidth = 7  
    boardHeight = 7  
    timerSpeed = 10000  # the timer updates ever 1 second
    counter = 10  # the number the counter will count down from

    x_global = 0  # col
    y_global = 0  # row

    player1 = True # True: Player1 _ False: Player2

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
        self.printBoardArray()  # Printing Board

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row])
                         for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

        # Getting the X and Y from QPoint()
        posX = self.lastPoint.x()
        posY = self.lastPoint.y()

        # Assigning the repective row
        self.x_global = int(posX / self.squareWidth())
       
        # Assigning the respective col
        self.y_global = int(posY / self.squareHeight())

        # Assigning click position to player
        self.tryMove(self.y_global, self.x_global)

        # Printing board updated.
        self.printBoardArray()

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts the game'''
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
        self.drawBoardSquares(painter) # Painting the board
        self.drawPieces(painter)    # Drawing the pieces

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.x()) + "," + str(
            event.y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        
        self.clickLocationSignal.emit(clickLoc)

        # Setting lasPoint position
        self.lastPoint = event.pos()
        print(self.lastPoint)
        self.mousePosToColRow(self)
        
        self.update()

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(204, 102, 0), Qt.SolidPattern))

        for row in range(0, Board.boardHeight - 1):
            for col in range(0, Board.boardWidth - 1):
                painter.save()
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)
                painter.drawRect(40, 40, self.squareWidth(),
                                 self.squareHeight())
                painter.restore()

    def drawPieces(self, painter):
        '''draw the pieces on the board'''

        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):

                if self.boardArray[row][col] == 1:
                    painter.setPen(QPen(Qt.transparent, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                elif self.boardArray[row][col] == 2:
                    painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                else:
                    painter.setPen(QPen(Qt.transparent, 2, Qt.SolidLine))
                    painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))

                painter.save()
                colTransformation = self.squareWidth() * col
                rowTransformation = self.squareHeight() * row
                painter.translate(colTransformation, rowTransformation)

                radius = (self.squareWidth() * 0.65) / 2
                center = QPoint(40, 40)
                painter.drawEllipse(center, radius, radius)

                painter.restore()

    def playerNumber(self):
        'Returning players number'
        if self.player1:
            return 1
        else:
            return 2

    def finish_turn(self):
        'Returns opposite of boolean player1, allowing us to swap between players'
        return not self.player1

    def resetGame(self):
        '''Reseting the game, removing pieces from board'''
        painter = QPainter(self)
        self.boardArray = [
            [0 for i in range(self.boardHeight)] for j in range(self.boardWidth)]
        self.drawPieces(painter)
        self.update()

    # Board Movement methods
    def hasLiberty(self, col, row):
        'checking if piece has liberty around'
        # Loading list with all avaliable on the board
        liberties = self.withinBoardRange(col, row)
        liberty_count = len(liberties)
        # Iterate with the list without jumping elements.
        for index in reversed(liberties):
            if index == 1 or index == 2:
                liberties.remove(index)
                liberty_count -= 1

        # print("Liberties " + str(liberty_count))

        return liberty_count

    def withinBoardRange(self, row, col):
        'Checking nearby positions of given piece'
        neighbors = []

        # Top position
        if row - 1 >= 0:
            neighbors.append(self.boardArray[row - 1][col])
            # print("up")

        # Right position
        if col + 1 < self.boardWidth - 1:
            neighbors.append(self.boardArray[row][col + 1])
            # print("right")

        # Lower position
        if row + 1 < self.boardHeight - 1:
            neighbors.append(self.boardArray[row + 1][col])
            # print("down")

        # Left position
        if col - 1 >= 0:
            neighbors.append(self.boardArray[row][col - 1])
            # print("left")

        return neighbors

    #TODO NotWorking - The method was designed to map all the enemies pieces around a given position
    '''def enemiesAround(self, row, col):
        enemy = 0

        if self.playerNumber() == 1:
            enemy = 2

        if self.playerNumber() == 2:
            enemy = 1

        group = []

        if row - 1 >= 0 and self.boardArray[row - 1][col] == enemy and self.hasLiberty(col, row - 1) == 1:
            group.append(self.boardArray[row - 1][col])
            self.enemiesAround(row - 1, col)

        if col + 1 < self.boardWidth - 1 and self.boardArray[row][col + 1] == enemy and self.hasLiberty(col + 1,
                                                                                                        row) == 1:
            group.append(self.boardArray[row][col + 1])
            self.enemiesAround(row, col + 1)

        if row + 1 < self.boardHeight - 1 and self.boardArray[row + 1][col] == enemy and self.hasLiberty(col,
                                                                                                         row - 1) == 1:
            group.append(self.boardArray[row + 1][col])
            self.enemiesAround(row + 1, col)

        if self.boardArray[row][col-1] == enemy and self.hasLiberty(col-1,row) == 1:
            
            group.append(self.boardArray[row][col -1])
            self.enemiesAround(row, col -1)

            for i in group:
                group[i] = 0, 0

        return group
    '''

    #TODO NotWotking - The method was designed to map all the opponents pieces
    '''def ListsOfOpponentLocations(self, col, row):
        top_list = []
        right_list = []
        lower_list = []
        left_list = []
    
        top_liberties = 0
        right_liberties = 0
        lower_liberties = 0
        left_liberties = 0
    
        if row - 1 >= 0:
            top_list = self.withinBoardRange(row-1, col)
            top_liberties = self.hasLiberty(row - 1, col)
            print("top_list", top_list)
            print("top_liberties", top_liberties)
    
        if col + 1 < self.boardWidth:
            right_list = self.withinBoardRange(row, col+1)
            right_liberties = self.hasLiberty(row, col + 1)
            print("right_list", right_list)
            print("right_liberties", right_liberties)
    
        if row + 1 < self.boardHeight:
            lower_list = self.withinBoardRange(row + 1, col)
            lower_liberties = self.hasLiberty(row + 1, col)
            print("lower_list", lower_list)
            print("lower_liberties", lower_liberties)
    
        if col - 1 >= 0:
            left_list = self.withinBoardRange(row, col-1)
            left_liberties = self.hasLiberty(row, col-1)
            print("left_list", left_list)
            print("left_liberties", left_liberties)
    '''

    def isEmpty(self, row, col):
        'Checking if position is valid to place a piece'
        if self.boardArray[row][col] == 0:
            return True
        else:
            return False

    # Couple of methods which should have been implemented here are missing
    def tryMove(self, row, col):
        '''tries to move a piece'''
        # Checking if position is empty.
        if self.isEmpty(row, col) == True and self.suicideMovement(row, col) == False:
            
            #Printing current number of liberties
            #print("Current Piece Liberties: ", self.hasLiberty(row, col))
            
            self.boardArray[self.y_global][self.x_global] = self.playerNumber()
            self.player1 = self.finish_turn()
        else:
            # TODO Change Status Message
            print("piece can't be placed")

    # TODO NotWorking - Capture method
    '''def captureMovement(self, row, col):
        'captures piece if the same is surround by opponent'
        pass
    '''
    # TODO NotWorking - KO movement 
    '''def koMovement(self, row, col):
        'Keeping track of previous movements and avoiding infinite plays'
        pass
    '''
    def suicideMovement(self, row, col):
        'Checking for suicide movements'
        suicide_list = self.withinBoardRange(row, col)
        surrounding = len(suicide_list)

        # Checking empty positions around
        if self.hasLiberty(row, col) == 0:
            for positions in suicide_list:
                if positions is not self.playerNumber():
                    surrounding -= 1
        
        if surrounding == 0:
            return True
        else:
            return False
