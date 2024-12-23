

class Move():
    def __init__(self, color, piece, origin, destination):
        self.color = color
        self.piece = piece
        self.origin = origin
        self.destination = destination

    def __str__(self) -> str:
        return f"Move : {color} moves {piece} from {origin} to {destination}"