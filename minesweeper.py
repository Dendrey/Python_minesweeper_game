import pygame
from Const import Const # это константы в нашей программе. Все они хранятся в файле Const.py
from Globals import Globals # это глобальные переменные в нашей программе. Все они хранятся в файле Globals.py
from collections import deque 
import random

def update_mines_counter():
  mines_text = f"Mines: {Globals.current_mines_counter} / {Globals.mines_counter}"
  return mines_text

def update_timer():
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - Globals.start_time) // 1000  # Convert milliseconds to seconds
    timer_text = f"Time: {elapsed_time} sec"
    return timer_text

def OpenArea(x0, y0):
  queue = deque()
  queue.append((x0, y0))
  while len(queue) != 0:
    (x, y) = queue[0]
    queue.popleft()
    for (dx, dy) in [(1, 1), (1, 0), (1, -1),(0, 1), (0, -1),(-1, 1), (-1, 0), (-1, -1)]:
      if  (0 <= dx + x <= Globals.grid_size - 1) & (0 <= dy + y <= Globals.grid_size - 1):
        if (Globals.current_board[x + dx][y + dy] == 0) & (Globals.board[x + dx][y + dy] != 1):
          Globals.current_board[x + dx][y + dy] = Globals.board[x + dx][y + dy]
          Globals.tiles_left -= 1
          if (Globals.board[x + dx][y + dy] == 10):
            queue.append((dx + x, y + dy))

def OpenTile():
  mouse_x_coordinate = (Globals.mouse_pos[0] - Globals.x_offset) // Globals.size
  mouse_y_coordinate = (Globals.mouse_pos[1] - Globals.y_offset) // Globals.size
  if not (0 <= mouse_x_coordinate <= (Globals.grid_size - 1)) & (0 <= mouse_y_coordinate <= (Globals.grid_size - 1)):
    return
  if (Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] == 0):
    if (Globals.board[mouse_x_coordinate][mouse_y_coordinate] == 10):
      Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] = 10
      Globals.tiles_left -= 1
      OpenArea(mouse_x_coordinate, mouse_y_coordinate)
      if Globals.tiles_left == 0:
        Globals.is_won = True
    elif (Globals.board[mouse_x_coordinate][mouse_y_coordinate] == 1):
      Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] = 3 # проигрыш
      Globals.game_over = True
    else:
      Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] = Globals.board[mouse_x_coordinate][mouse_y_coordinate]
      Globals.tiles_left -= 1
      if Globals.tiles_left == 0:
        Globals.is_won = True
    

def PlaceFlag():
  mouse_x_coordinate = (Globals.mouse_pos[0] - Globals.x_offset) // Globals.size
  mouse_y_coordinate = (Globals.mouse_pos[1] - Globals.y_offset) // Globals.size
  if not (0 <= mouse_x_coordinate <= (Globals.grid_size - 1)) & (0 <= mouse_y_coordinate <= (Globals.grid_size - 1)):
    return
  if (Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] == 0) & (Globals.current_mines_counter > 0):
    Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] = 1
    Globals.current_mines_counter -= 1
  elif (Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] == 1):
    Globals.current_board[mouse_x_coordinate][mouse_y_coordinate] = 0
    Globals.current_mines_counter += 1

def EventChecker(event):   # Получение информации о нажатых клавишах и положении мыши
  if event.type == pygame.MOUSEBUTTONDOWN:
    if pygame.mouse.get_pressed(num_buttons=3)[0]:
      Globals.mouse_pos = pygame.mouse.get_pos()
      OpenTile()
    if pygame.mouse.get_pressed(num_buttons=3)[2]:
      Globals.mouse_pos = pygame.mouse.get_pos()
      PlaceFlag()
  if event.type == pygame.QUIT: # Действия при остановке программы
    Globals.running = False

def DrawTable(screen):
  screen.fill(Const.BLACK)
  Globals.screen_width, Globals.screen_height = pygame.display.get_surface().get_size()  # ширина игрового окна и высота игрового окна
  Globals.size = min(Globals.screen_height, Globals.screen_width) // (Globals.grid_size + 2)
  Globals.x_offset = (Globals.screen_width - Globals.size * Globals.grid_size)  // 2
  Globals.y_offset = (Globals.screen_height - Globals.size * Globals.grid_size) // 3 * 2
  for x in range(Globals.grid_size):
    for y in range(Globals.grid_size):
      coordinates = [Globals.size*x + Globals.x_offset, Globals.size*y + Globals.y_offset, Globals.size, Globals.size]
      switch_cases = {
        0:  [0, 0], #закрытая клетка
        1:  [2, 0],  #флаг
        10: [1, 0],  #пустое поле
        3:  [6, 0],  #взорвавшаяся бомба
        11: [0, 1],  #1
        12: [1, 1],  #2
        13: [2, 1],  #3
        14: [3, 1],  #4
        15: [4, 1],  #5
        16: [5, 1],  #6
        17: [6, 1],  #7
        18: [7, 1],  #8
      }
      tile_coord = switch_cases.get(Globals.current_board[x][y])
      view_rect = pygame.Rect(Const.tile_size * tile_coord[0], Const.tile_size * tile_coord[1],Const.tile_size,Const.tile_size)
      image = pygame.transform.scale(pygame.image.load('2000.png').convert_alpha().subsurface(view_rect), (Globals.size, Globals.size))
      screen.blit(image , coordinates)

  font = pygame.font.SysFont('Arial', Globals.size // 3 * 2)

  mines_text = update_mines_counter()
  mines_surface = font.render(mines_text, True, Const.WHITE)
  mines_rect = mines_surface.get_rect(midtop=(Globals.screen_width // 3 * 2, Globals.y_offset // 4))
  screen.blit(mines_surface, mines_rect)

  timer_text = update_timer()
  timer_surface = font.render(timer_text, True, Const.WHITE)
  timer_rect = timer_surface.get_rect(midtop=(Globals.screen_width // 3, Globals.y_offset // 4))
  screen.blit(timer_surface, timer_rect)
  
  
  pygame.display.flip()

def CreateBoard(x0 ,y0):
  Globals.tiles_left = Globals.grid_size * Globals.grid_size - Globals.mines_counter
  Globals.board = [[0 for _ in range(Globals.grid_size)] for _ in range(Globals.grid_size)]
  Globals.current_board = [[0 for _ in range(Globals.grid_size)] for _ in range(Globals.grid_size)]
  i = Globals.mines_counter
  while i > 0:
    x = random.randint(0, Globals.grid_size - 1)
    y = random.randint(0, Globals.grid_size - 1)
    if (Globals.board[x][y] == 0) & ((x0, y0) not in [(x, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x + 1, y), (x - 1, y),]) :
      Globals.board[x][y] = 1
      i -= 1
  for x in range (Globals.grid_size):
    for y in range (Globals.grid_size):
      if (Globals.board[x][y] == 0):
        Globals.board[x][y] = 10
        for dx in [-1, 0, 1]:
          for dy in [-1, 0, 1]:
            if (0 <= x+dx <= Globals.grid_size - 1) & (0 <= y+dy <= Globals.grid_size - 1):
              if Globals.board[x + dx][y + dy] == 1:
                Globals.board[x][y] += 1
  Globals.current_mines_counter = Globals.mines_counter

def FirstClickScreen():
  Globals.current_board = [[0 for _ in range(Globals.grid_size)] for _ in range(Globals.grid_size)]
  flag = True
  while flag & Globals.running:
    DrawTable(screen)
    Globals.start_time = pygame.time.get_ticks()
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
          Globals.mouse_pos = pygame.mouse.get_pos()
          mouse_x_coordinate = (Globals.mouse_pos[0] - Globals.x_offset) // Globals.size
          mouse_y_coordinate = (Globals.mouse_pos[1] - Globals.y_offset) // Globals.size
          if (0 <= mouse_x_coordinate <= (Globals.grid_size - 1)) & (0 <= mouse_y_coordinate <= (Globals.grid_size - 1)):
            CreateBoard(mouse_x_coordinate, mouse_y_coordinate)
            OpenTile()
            flag = False


            
def StartScreen(screen):
  screen.fill(Const.BLACK)
  font = pygame.font.SysFont('Arial', 40)
  text_surface = font.render("Choose Difficulty:", True, Const.WHITE)
  text_rect = text_surface.get_rect(center=(Globals.screen_width // 2, Globals.screen_height // 2 - 50))
  screen.blit(text_surface, text_rect)

  easy_button = pygame.Rect(Globals.screen_width // 2 - 100, Globals.screen_height // 2, 200, 50)
  medium_button = pygame.Rect(Globals.screen_width // 2 - 100, Globals.screen_height // 2 + 60, 200, 50)
  hard_button = pygame.Rect(Globals.screen_width // 2 - 100, Globals.screen_height // 2 + 120, 200, 50)

  pygame.draw.rect(screen, Const.GREEN, easy_button)
  pygame.draw.rect(screen, Const.YELLOW, medium_button)
  pygame.draw.rect(screen, Const.RED, hard_button)

  easy_text = font.render("Easy", True, Const.WHITE)
  easy_text_rect = easy_text.get_rect(center=easy_button.center)
  screen.blit(easy_text, easy_text_rect)

  medium_text = font.render("Medium", True, Const.WHITE)
  medium_text_rect = medium_text.get_rect(center=medium_button.center)
  screen.blit(medium_text, medium_text_rect)

  hard_text = font.render("Hard", True, Const.WHITE)
  hard_text_rect = hard_text.get_rect(center=hard_button.center)
  screen.blit(hard_text, hard_text_rect)

  pygame.display.flip()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if easy_button.collidepoint(mouse_pos):
          Globals.grid_size = 8
          Globals.mines_counter = 10
          return
        elif medium_button.collidepoint(mouse_pos):
          Globals.grid_size = 10
          Globals.mines_counter = 20
          return
        elif hard_button.collidepoint(mouse_pos):
          Globals.grid_size = 12
          Globals.mines_counter = 30
          return
        
def LoseScreen():
  # Game over screen
  screen.fill(Const.BLACK)
  font = pygame.font.SysFont('Arial', 40)
  game_over_text = font.render("Game Over", True, Const.RED)
  game_over_text_rect = game_over_text.get_rect(center=(Globals.screen_width // 2, Globals.screen_height // 2 - 50))
  screen.blit(game_over_text, game_over_text_rect)

  restart_text = font.render("Click anywhere to restart", True, Const.WHITE)
  restart_text_rect = restart_text.get_rect(center=(Globals.screen_width // 2, Globals.screen_height // 2 + 50))
  screen.blit(restart_text, restart_text_rect)

def WinScreen():
  screen.fill(Const.BLACK)
  font = pygame.font.SysFont('Arial', 40)
  game_over_text = font.render("You won", True, Const.GREEN)
  game_over_text_rect = game_over_text.get_rect(center=(Globals.screen_width // 2, Globals.screen_height // 2 - 50))
  screen.blit(game_over_text, game_over_text_rect)

  restart_text = font.render("Click anywhere to restart", True, Const.WHITE)
  restart_text_rect = restart_text.get_rect(center=(Globals.screen_width // 2, Globals.screen_height // 2 + 50))
  screen.blit(restart_text, restart_text_rect)
        

if __name__ == '__main__':
  buttons = []
  pygame.init()
  screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE) #FULLSCREEN as a variant
  font = pygame.font.SysFont('Arial', 40)
  Globals.screen_width, Globals.screen_height = pygame.display.get_surface().get_size()  # ширина игрового окна и высота игрового окна
  Globals.size = min(Globals.screen_height, Globals.screen_width) // (Globals.grid_size + 1)
  pygame.display.set_caption("Сапёр")
  while Globals.running:
    Globals.game_over = False
    StartScreen(screen)
    FirstClickScreen()
    while Globals.running & (not Globals.game_over) & (not Globals.is_won):
      DrawTable(screen)
      for event in pygame.event.get():
        EventChecker(event)
    if Globals.game_over:
      Globals.game_over = False
      LoseScreen()
    else:
      Globals.is_won = False
      WinScreen()

    pygame.display.flip()
    restart_clicked = False
    while not restart_clicked:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          restart_clicked = True
          break
