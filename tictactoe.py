import pygame

PLAYER_1_HAND = 'X'
PLAYER_2_HAND = 'O'
rootW = 300
rootH = 300
squareW = int(rootW/3)
squareH = int(rootH/3)
FONT_SIZE = squareW+squareH-5

class Board:
    def __init__(self) -> None:
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]

    def get(self,row,col):
        if(row >= 0 and row < 3 and col >= 0 and col < 3):
            return self.board[row][col]
        return None

    def set(self,row,col,c):
        if(row >= 0 and row < 3 and col >= 0 and col < 3):
            self.board[row][col] = c

    def isFull(self):
        for i in range(0,3):
            for j in range(0,3):
                if self.board[i][j] == ' ':
                    return False
        return True

    def clear(self):
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]


class TicTacToeGame:
    def __init__(self) -> None:
        #Pygame initialized here!
        pygame.init()
        screen = pygame.display.set_mode((rootW,rootH))
        pygame.display.set_caption('Tic-Tac-Toe')
        self.board = Board()
        self.isP1Turn = True
        self.isRunning = True
        self.gameSurface = screen

    def isP1Turn(self) -> bool:
        return self.isP1Turn

    def reset(self):
        self.board.clear()
        self.isRunning = True

    def move(self,row:int,col:int) -> bool:
        if(row >= 0 and row < 3 and col >= 0 and col < 3 and (self.board.get(row,col) == ' ')):
            if self.isP1Turn:
                self.board.set(row,col,PLAYER_1_HAND)
            else:
                self.board.set(row,col,PLAYER_2_HAND)
            return True
        return False

    #This function checks for a win based on which player turn it is.
    #Returns a tuple indicating if there wasAWin, the (x,y) tuple indicating
    #the starting x and y coordinates to draw the strike-through line, and
    #the (x,y) tuple indicating the ending x and y coordinates to draw the
    #strike-through line, in the respective order.
    def check4Win(self):
        playerHand = PLAYER_1_HAND if self.isP1Turn else PLAYER_2_HAND
        for i in range(0,8):
            if i == 0:
                if self.board.get(0,0) == playerHand and self.board.get(1,0) == playerHand and self.board.get(2,0) == playerHand:
                    return (True,(squareW/2,0),(squareW/2,rootH))
            elif i == 1:
                if self.board.get(0,1) == playerHand and self.board.get(1,1) == playerHand and self.board.get(2,1) == playerHand:
                    return (True,((squareW*2)-(squareW/2),0),((squareW*2)-(squareW/2),rootH))
            elif i == 2:
                if self.board.get(0,2) == playerHand and self.board.get(1,2) == playerHand and self.board.get(2,2) == playerHand:
                    return (True,((squareW*3)-(squareW/2),0),((squareW*3)-(squareW/2),rootH))
            elif i == 3:
                if self.board.get(0,0) == playerHand and self.board.get(0,1) == playerHand and self.board.get(0,2) == playerHand:
                    return (True,(0,squareH/2),(rootW,squareH/2))
            elif i == 4:
                if self.board.get(1,0) == playerHand and self.board.get(1,1) == playerHand and self.board.get(1,2) == playerHand:
                    return (True,(0,(squareH*2)-(squareH/2)),(rootW,(squareH*2)-(squareH/2)))
            elif i == 5:
                if self.board.get(2,0) == playerHand and self.board.get(2,1) == playerHand and self.board.get(2,2) == playerHand:
                    return (True,(0,(squareH*3)-(squareH/2)),(rootW,(squareH*3)-(squareH/2)))
            elif i == 6:
                if self.board.get(0,0) == playerHand and self.board.get(1,1) == playerHand and self.board.get(2,2) == playerHand:
                    return (True,(0,0),(rootW,rootH))
            else:
                if self.board.get(2,0) == playerHand and self.board.get(1,1) == playerHand and self.board.get(0,2) == playerHand:
                    return (True,(0,rootH),(rootW,0))
                
        return (False,None,None)

    #This function defines the entry point, or game loop, for the game.
    def gameloop(self):
        while True:
            boardPos = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    winResult = None
                    if self.isRunning:
                        #Get location player wants to move
                        boardPos = (event.pos[0]//squareW, event.pos[1]//squareH) #Map mouse coordinates to position on board
                        #Move there
                        if self.move(boardPos[1],boardPos[0]):
                            #check for win
                            winResult = self.check4Win()
                            #if (win) stop running and return player
                            if winResult[0]:
                                self.isRunning = False
                                winner = "X" if self.isP1Turn else "O"
                                print(f"{winner} won!")
                            #else if board is full stop running and return draw
                            elif self.board.isFull():
                                self.isRunning = False
                                self.isP1Turn = True
                                print("It's a draw!")
                            #else repeat for other player
                            else:
                                self.isP1Turn = not self.isP1Turn
                    else:
                        self.reset()
                    self.drawBoard(winResult)

    def drawBoard(self,winResult=None):
        #Set background color to white
        self.gameSurface.fill('white')
        #Draw the 2 horizontal and 2 vertical cross lines (4 total) that make up the board
        pygame.draw.line(self.gameSurface,'black',(squareW,0),(squareW,rootH),width=3)
        pygame.draw.line(self.gameSurface,'black',(squareW*2,0),(squareW*2,rootH),width=3)
        pygame.draw.line(self.gameSurface,'black',(0,squareH),(rootW,squareH),width=3)
        pygame.draw.line(self.gameSurface,'black',(0,squareH*2),(rootW,squareH*2),width=3)
        #Set font size
        font = pygame.font.Font(None, FONT_SIZE)
        #Offsets used to align text within the board square
        xOffset = 3
        yOffset = 9 
        #Draw each player hand as is in the board at their respective locations
        for i in range(0,3):
            for j in range(0,3):
                if self.board.get(i,j) == 'X':
                    text = font.render('X',True,'red')
                    self.gameSurface.blit(text,(j*squareW-xOffset,i*squareH-yOffset))
                elif self.board.get(i,j) == 'O':
                    text = font.render('O',True,'blue')
                    self.gameSurface.blit(text,(j*squareW-xOffset,i*squareH-yOffset))
                                
        #If their was a win draw strike-through line over the winning sequence
        if winResult != None and winResult[0]:
            pygame.draw.line(self.gameSurface,'green',winResult[1],winResult[2],width=6)

        pygame.display.update()     #Update display

def main():
    game = TicTacToeGame()
    game.drawBoard()

    game.gameloop()

if __name__ == "__main__":
    main()