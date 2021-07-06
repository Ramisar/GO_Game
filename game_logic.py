class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game


'''Checking if Piece has Liberty(s) or not
    def liberty(self)

IF  & piece.position % 7 == 0
    & piece.position + 1 == False | null
    & piece.position + 7 == False | null
    & piece.position -7  == False | null
    Then:
    Return False

ELIF    & piece.position % 7 == 6
        & piece.position -1  == False | null
        & piece.position + 7 == False | null
        & piece.position -7  == False | null
        Then:
        Return False

ELIF    & piece.position -1  == False | null
        & piece.position +1  == False | null
        & piece.position + 7 == False | null
        & piece.position -7  == False | null
        Then:
        Return False

'''

'''Capturing pieces
    def capture(self)

IF  piece.liberty() == False 
    & piece.position -1     == oponent.piece | null
    & piece.position + 1    == oponent.piece | null
    & piece.position + 7    == oponent.piece | null
    & piece.position -7     == oponent.piece | null
    Then:
    piece.isCaptured()
'''

'''





'''


