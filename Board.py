import pygame
from Server import GameServer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

square_size = 20
padding     = 1

class Board():
    """Game of life Board, it must be initilized with
       the height and width desired"""
    def __init__(self,width,height):
        self.width  = width
        self.height = height
        total_square_size = square_size + padding
        self.size   = (height * total_square_size,width * total_square_size)
        self.screen = pygame.display.set_mode(self.size)
        self.keep_playing = True

        self.board_state = [False] * self.width * self.height

        game_server = GameServer(lambda x: self.patch(x))
        game_server.start_server()

    def patch(self,x):
        self.board_state = x
    
    def __setattr__(self, name, value):
        if (name == "board_state"):
            orig_val = value
            try:
                if isinstance(value,str):
                    value = value.split(',')
                value = list(map(lambda x: bool(int(x)),value))
                
            except Exception as e:
                print("Error trying to process ",orig_val)
                return
            self.__dict__[name] = value
            self.draw_state(self.__dict__[name])
        else:
            self.__dict__[name] = value

    def draw_state(self,alive_list):
        if len(alive_list) < self.height * self.width:
            print("Error: missing elements in alive list")
            return

        self.screen.fill(BLACK)
        al = alive_list.copy()
        al.reverse()

        for i in range(1, self.size[0], square_size + 1):
            for j in range(1, self.size[1], square_size + 1):
                if not al.pop():
                    pygame.draw.rect(self.screen, WHITE, [i, j, square_size, square_size], 0)
        pygame.display.flip()

    def end_game(self):
        self.keep_playing = False

    def game_loop(self):
        pygame.init()
        pygame.display.set_caption("Conway Game of Life")
        self.draw_state(self.board_state)
        while self.keep_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.keep_playing = False
