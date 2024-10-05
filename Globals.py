import pygame
class Globals:
  running = True
  screen_width = 0
  screen_height = 0
  size = 0
  x_offset = 0
  y_offset = 0
  mouse_pos = (0,0)
  grid_size = 10
  board = []
  current_board = []
  mines_counter = 40
  current_mines_counter = 0
  start_time = pygame.time.get_ticks()
  game_over = False
  tiles_left = 0
  is_won = False