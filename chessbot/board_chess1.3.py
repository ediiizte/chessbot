import pygame

size = (800, 800)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Position:
    col1 = (20,20,20)
    col2 = (240,240,240)
    def __init__(self,fen,scrn_size):
        self.fen = fen
        self.scrn_size = scrn_size
        self.board = []
        self.moves = {}
        self.squares = pygame.sprite.Group()
        self.pieces = []

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
    def piece_type(self,piece_letter):
        convert = {"r":"rook","k":"king","q":"queen","n":"knight","p":"pawn","b":"bishop"}
        return convert[piece_letter.lower()]
    def setup_board_pieces(self):
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != "0":
                    self.create_piece(x,y,False,self.scrn_size,self.square_type(x,y),self.piece_type(self.board[x][y]))
    def create_piece(self,x,y,moved,scrn_size,colour,ID):
        piece1 = None
        ID2 = ID.lower()
        match ID2:
            case "rook":
                piece1 = Rook(x,y,self,moved,scrn_size,colour,ID)
        match ID2:
            case "bishop":
                piece1 = Bishop(x,y,self,moved,scrn_size,colour,ID)
        match ID2:
            case "knight":
                piece1 = Knight(x,y,self,moved,scrn_size,colour,ID)
        match ID2:
            case "king":
                piece1 = King(x,y,self,moved,scrn_size,colour,ID)
        match ID2:
            case "queen":
                piece1 = Queen(x,y,self,moved,scrn_size,colour,ID)
        match ID2:
            case "pawn":
                piece1 = Pawn(x,y,self,moved,scrn_size,colour,ID)
        piece1.update_img_coord()
        self.pieces.append(piece1)
        piece1.image()

    def display_pieces(self):
        for piece in self.pieces:
            piece.draw()
    def get_closest_piece(self):
        mouse_coord = pygame.mouse.get_pos()
        min_dist = []
        for piece in self.pieces:
            coord2 = (piece.img_x,piece.img_y)
            dist = self.distance(mouse_coord,coord2)
            min_dist.append(dist)
        min_piece_index = min_dist.index(min(min_dist))
        return self.pieces[min_piece_index]
        return None
    def distance(self,coord1,coord2):
        return ((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2)**0.5
    def mouse_click(self):
        return pygame.mouse.get_pressed()[0]
    def click_piece(self):
        if self.check_for_clicked_piece() == None and self.mouse_click() == True:
            piece_clicked = self.get_closest_piece()
            if piece_clicked != None:
                piece_clicked.clicked = True
                piece_clicked.click()
    def check_for_clicked_piece(self):
        for piece in self.pieces:
            if piece.clicked == True:
                return piece
        return None
    def move_clicked_piece(self):
        piece = self.check_for_clicked_piece()
        if piece != None:
            piece.click()

            
class Piece:
    def __init__(self,x,y,position,moved,scrn_size,colour,ID):
        self.scrn_size = scrn_size
        self.ID = ID
        self.colour = colour
        self.img = ""
        self.x = x
        self.y = y
        self.og_xy = (self.x,self.y)
        self.img_x = 0
        self.img_y = 0
        self.position = position
        self.moved = moved
        self.moves = []
        self.clicked = False
    def update_img_coord(self):
        self.img_x = (self.y)*self.scrn_size/8
        self.img_y = (self.x)*self.scrn_size/8
    def image(self):
        self.img = pygame.image.load(f"{self.colour}_{self.ID}.png")
        self.img = pygame.transform.scale(self.img,(self.scrn_size/8,self.scrn_size/8))
    def draw(self):
        try:
            screen.blit(self.img,(self.img_x,self.img_y))
        except:
            TypeError
    def index_check(self,move):
        if -1 < self.x + move[0] < 8 and -1 < self.y + move[1] < 8:
            return True
    def same_piece_check(self,move):
        square = self.position.board[self.x+move[0]][self.y+move[1]]
        if self.position.empty(square) == False and self.position.capital(square) == self.colour:
            self.moves.pop(move)
                
    def quick_move_check(self):
        for move in self.moves:
            if self.index_check(move) == False or self.same_piece_check(move) == True:
                self.moves.pop(move)
    def click(self):
        if self.position.mouse_click() == True:
            self.img_x,self.img_y = pygame.mouse.get_pos()[0]-0.5*self.scrn_size/8,pygame.mouse.get_pos()[1]-0.5*self.scrn_size/8
        else:
            self.clicked = False
            self.img_x = self.find_closest_square(self.img_x)
            self.img_y = self.find_closest_square(self.img_y)
            self.take_piece()
            self.update_coord()
    def coord_direction(self,coord):
        value = abs(coord%(self.scrn_size/8))
        if value > 50:
            direction = "up"
        else:
            direction = "down"
        return direction,value
    def find_closest_square(self,coord):
        direction,value = self.coord_direction(coord)
        if direction == "down":
            coord -= value
        else:
            coord += (100-value)
        return coord
    def update_coord(self):
        print(self.x,self.y)
        self.x,self.y = int(self.img_y*8/self.scrn_size),int(self.img_x*8/self.scrn_size)
        if self.x > 7 or self.x < 0 or 0 > self.y or self.y > 7:
            print(1)
            print("x",self.x,"y",self.y)
            self.x,self.y = self.og_xy[0],self.og_xy[1]
            print(self.x,self.y)
            self.update_img_coord()
        else:
            self.og_xy = (self.x,self.y)
        self.promote()
    def take_piece(self):
        for piece in self.position.pieces:
            if (piece.img_x,piece.img_y) == (self.img_x,self.img_y) and piece.colour != self.colour:
                self.position.pieces.remove(piece)
    def promote(self):
        if self.ID == "pawn":
            if self.colour == "white" and self.x == 0 or self.colour == "black" and self.x == 7:
                self.position.create_piece(self.x,self.y,self.moved,self.scrn_size,self.colour,"queen")
                self.position.pieces.remove(self)
            
class Rook(Piece):
    x_moves = [[-7, 0], [-6, 0], [-5, 0], [-4, 0], [-3, 0], [-2, 0], [-1, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]]
    y_moves = [[0, -7], [0, -6], [0, -5], [0, -4], [0, -3], [0, -2], [0, -1], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]]
    def __init__(self,x,y,position,moved,scrn_size,colour,ID):
        super().__init__(x,y,position,moved,scrn_size,colour,ID)
class Knight(Piece):
    moves = [[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1],[-2,1],[-1,2]]
    def __init__(self,x,y,position,moved,scrn_size,colour,ID):
        super().__init__(x,y,position,moved,scrn_size,colour,ID)
class King(Piece):
    moves = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
    def __init__(self,x,y,position,moved,scrn_size,colour,ID):
        super().__init__(x,y,position,moved,scrn_size,colour,ID)
class Queen(Piece):
    def __init__(self,x,y,position,moved,scrn_size,colour,ID):
        super().__init__(x,y,position,moved,scrn_size,colour,ID)
class Bishop(Piece):
    positive_moves1 = [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]
    positive_moves2 = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]]
    def __init__(self,x,y,position,moved,scrn_size,colour,ID):
        super().__init__(x,y,position,moved,scrn_size,colour,ID)
class Pawn(Piece):
    moves = [[-1,1],[1,1],[1,0],[2,0]]
    def __init__(self,x,y,position,moved,scrn_size,colour,ID):
        super().__init__(x,y,position,moved,scrn_size,colour,ID)
 
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
current = Position(start_fen,800)
current.get_board()
current.setup_board_pieces()
current.create_group(size[0])
# knight = Knight(2,2,current,False,800,"white","knight")
# knight.same_piece_check([1,2])
# knight.image()
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
    current.click_piece()
    current.move_clicked_piece()
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    # --- Drawing code should go here
    current.draw_squares(screen)
#     knight.draw()
    current.display_pieces()
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()