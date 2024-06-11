import pygame

size = (800, 800)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Position:
    col1 = (30,220,30)
    col2 = (50,120,20)
    def __init__(self,fen):
        self.fen = fen
        self.board = []
        self.moves = {}
        self.squares = pygame.sprite.Group()

    def get_board(self):
        fen_list = list(self.fen.split("/"))
        for row in fen_list:
            row_list = []
            for piece in row:
                try:
                    row_list = ["0" for x in range(int(piece))]
                except ValueError:
                    row_list.append(piece)
            self.board.append(row_list)
    def capital(self,string):
            if string.lower() == string:
                return False
            else:
                return True
    def empty(self,square):
        if square == "0":
            return True
        else:
            return False
    def square_type(self,x,y):
        print(x,y)
        print(self.board[x][y])
        square = self.board[x][y]
        if self.empty(square) == True:
            return "empty"
        elif self.capital(square) == False:
            return "black"
        else:
            return "white"
    def colour(self,col):
        if col == Position.col1:
         return Position.col2
        else:
            return Position.col1
    def create_group(self,screen_length):
        col = Position.col1
        for x in range(8):
            col = self.colour(col)
            x_val = (x+0.5)*screen_length/8
            for y in range(8):
                y_val = (y+0.5)*screen_length/8
                col = self.colour(col)
                square = Square(x_val,y_val,screen_length/8,col)
                square.group(self.squares)
    def draw_squares(self,screen):
        self.squares.draw(screen)
    def create_piece(self,piece,x,y):
        match piece:
            case "rook":
                piece1 = Rook(x,y,self.board)
        match piece:
            case "bishop":
                piece1 = Bishop(x,y,self.board)
        match piece:
            case "knight":
                piece1 = Knight(x,y,self.board)
        match piece:
            case "king":
                piece1 = King(x,y,self.board)
        match piece:
            case "queen":
                piece1 = Queen(x,y,self.board)
        match piece:
            case "pawn":
                piece1 = Pawn(x,y,self.board)
class Piece_moves:
    def __init__(self,square_size):
        self.square_size = square_size/8
        self.knight_moves = None
        self.rook_moves = None
        self.pawn_moves = None
        self.king_moves = None
        self.queen_moves = []
        self.rook_moves = None
        self.knight_img = pygame.image.load("white_knight.png")
        self.knight_img = pygame.transform.scale(self.knight_img,(self.square_size,self.square_size))
    def knight(self):
        self.knight_moves = [[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1],[-2,1],[-1,2]]
    def king(self):
        self.king_moves = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
    def bishop(self):
        moves = []
        for x in range(-7,8):
            moves.append([x,x])
        self.bishop_moves = moves
    def pawn(self):
        self.pawn_moves = [[-1,1],[1,1],[1,0],[2,0]]
    def queen(self):
        self.queen_moves.append(self.bishop_moves)
        self.queen_moves.append(self.rook_moves)
    def rook(self):
        moves = []
        movesup = []
        movesacross = []
        for i in range(-7,8):
            movesup.append([0,i])
            movesacross.append([i,0])
        for travel1 in movesup:
            moves.append(travel1)
        for travel2 in movesacross:
            moves.append(travel2)
        self.rook_moves = moves
        
            
class Piece:
    def __init__(self,x,y,board,player,moved,obj):
        self.x = x
        self.y = y
        self.board = board
        self.player = player
        self.moved = moved
        self.moves = []
        self.moves_obj = obj
class Rook(Piece):
    def __init__(self,x,y,board,player):
        super().__init__(x,y,board,player)
    def output_moves(self):
        moves = copy.deepcopy(obj.rook_moves)
class Knight(Piece):
    def __init__(self,x,y,board,player,moved,obj):
        super().__init__(x,y,board,player,moved,obj)
    def check_moves(self):
        for move in self.moves_obj.knight_moves:
            if -1 < int(self.x + move[0]) < 8 and -1 < self.y + move[1] < 8:
                print(move)
                if self.board.square_type(self.x+move[0],self.y+move[1]) != self.player:
                    self.moves.append(move)
    def draw(self):
        screen.blit(self.moves_obj.knight_img,(self.x,self.y))
class King(Piece):
    def __init__(self,x,y,board,player):
        super().__init__(x,y,board,player)
class Queen(Piece):
    def __init__(self,x,y,board,player):
        super().__init__(x,y,board,player)
class Bishop(Piece):
    def __init__(self,x,y,board,player):
        super().__init__(x,y,board,player)
class Pawn(Piece):
    def __init__(self,x,y,board,player):
        super().__init__(x,y,board,player)
def setup_moves(square_size):
    obj = Piece_moves(square_size)
    obj.knight()
    obj.pawn()
    obj.bishop()
    obj.king()
    obj.queen()
    obj.rook()
    return obj
obj = setup_moves(size[0])
            

 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]

screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")

class Square(pygame.sprite.Sprite):

    def __init__(self,x,y,length,colour):
        super().__init__()
        self.x,self.y = x,y
        self.length = length
        self.image = pygame.Surface((self.length, self.length))
        self.colour = colour
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    def group(self, group):
        group.add(self)

start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
current = Position(start_fen)
current.get_board()
current.create_group(size[0])
knight = Knight(0,0,current,"white",False,obj)
# class of chess board drawing
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    # --- Drawing code should go here
    current.draw_squares(screen)
    knight.draw()
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()