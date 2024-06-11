class Moves:
    def __init__(self):
        self.moves = {}
    def rook_moves(self):
        rook_movesx,rook_movesy = [],[]
        for x in range(-7,8):
            rook_movesx.append([x,0])
            rook_movesy.append([0,x])
        self.moves["r"] = [rook_movesx,rook_movesy]
    def bishop_moves(self):
        bishop_moves1 = []
        for x in range(-7,8):
            bishop_moves1.append([x,x])
        self.moves["b"] = [bishop_moves1]
    def king_moves(self):
        king_moves1 = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
        self.moves["k"] = king_moves1
        
class Positions():
    def __init__(self):
        self.positions = positions
        self.current_positions = current_positions
    def search(self):
        for position in self.current_positions:
            position.search()
class Position():
    moves = {}
    def __init__(self,fen,depth):
        self.fen = fen
        self.array = []
        self.parents = []
        self.children = []
        self.depth = depth
    def convert_fen(self):
        fen_list = list(self.fen.split("/"))
        for row in fen_list:
            row_list = []
            for piece in row:
                try:
                    row_list = ["0" for x in range(int(piece))]
                except ValueError:
                    row_list.append(piece)
            self.array.append(row_list)
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
    def search(self):
        moves = []
        for x in range(8):
            for y in range(8):
                if self.empty(self.array[x][y]) == False:
                    new_moves = self.search_piece(self.array[x][y])
                    for move in new_moves:
                        moves.append(move)
    def square_name(self,square):
        x = {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
        name = f"{x[square[0]]}{square[1]+1}"
        return name
    def check(self):
        if self.array.count("k") + self.array.count("K") == 2:
            return False
        
        
        
                        
    
                
pos = Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
pos.convert_fen()
print(pos.array)
print(pos.capital("3"))
rook = Moves()
rook.rook_moves()
rook.bishop_moves()
rook.king_moves()

print(rook.moves)
print(pos.square_name([3,3]))