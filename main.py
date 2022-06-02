import random
import pygame



pygame.font.init()

# global variables

col = 10  # 10 kolom
row = 20  # 20 baris
s_width = 800
s_height = 750
play_width = 300
play_height = 600
block_size = 30  # size blok

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

filepath = 'highscore.txt'
fontpath = '/Users/Windows/PycharmProjects/TUBES PBO FINISH/arcade.ttf'
fontpath_comic = '/Users/Windows/PycharmProjects/TUBES PBO FINISH/COMIC.ttf'

# Bentuk Tetris (dibentuk dalmam array)

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# index menunjukan bentuk tetris
shapes = [S, Z, I, O, J, L, T]
# warna untuk setiap tetris
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# class untuk setiap piece


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # memilih warna dari list
        self.rotation = 0  # memilih rotasi sesuai index


# Grid
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]  # grid untuk warna dalam tuples

    # dictionary untuk locked_position
    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[
                    (x, y)]  # untuk mendapatkan value warna (r,g,b) dari  locked_positions dictionary menggunakan key (x,y)
                grid[y][x] = color  #  grid position ke warna

    return grid


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]  # mendapatkan posisi saat rotasi yang di inginkan

    for i, line in enumerate(shape_format):  # i memberikan index dan line memberikan string
        row = list(line)  # membuat list char dari string
        for j, column in enumerate(row):  # j memberikan index dari char dan column memberikan char
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # offset menurut dari input yang diberikan dengan . dan nol

    return positions


# cek posisi valid atau tidak
def valid_space(piece, grid):
    # membuat  2D list dari semua kemungkinan (x,y)
    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
    # menghapus sub lists dan menaruh (x,y) dalam satu list agar lebih gampang di cari
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


# cek apakah piece keluar dari board/grid
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# memilih piece secara random
def get_shape():
    return Piece(5, 0, random.choice(shapes))


# mengeluar text di tengah
def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size, bold=False, italic=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


# untuk grid dalam game
def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # gray line dalam grid horizontal
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            # gray line dalam grid vertikal
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


# clear row ketika penuh
def clear_rows(grid, locked):
    # cek row dan shift kebawah
    increment = 0
    for i in range(len(grid) - 1, -1, -1):      # cek grid secara mundur
        grid_row = grid[i]                      # row terakhir
        if (0, 0, 0) not in grid_row:           # jika tidak ada blok yang kosong
            increment += 1
            index = i                           # row index will be constant
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)]          # delete every locked element in the bottom row
                except ValueError:
                    continue

    if increment > 0:
        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:                       # jika nilai y diatas index yang di remove maka turunkan posisi ke bawah
                new_key = (x, y + increment)
                locked[new_key] = locked.pop(key)

    return increment


# membuat piece
def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next Piece', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (start_x + j*block_size, start_y + i*block_size, block_size, block_size), 0)

    surface.blit(label, (start_x, start_y - 30))

    # pygame.display.update()



def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.Font(fontpath_comic, 65, bold=True)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 30))

    # skor skarang
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Score   ' + str(score) , 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    surface.blit(label, (start_x, start_y + 200))

    # highskor
    label_hi = font.render('Highscore   ' + str(last_score), 1, (255, 255, 255))

    start_x_hi = top_left_x - 240
    start_y_hi = top_left_y + 200

    surface.blit(label_hi, (start_x_hi + 20, start_y_hi + 200))

    # membuat konten dalam
    for i in range(row):
        for j in range(col):
            # membuat rectangle shape
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # membuat vertical dan horizontal grid lines
    draw_grid(surface)

    # membuat border kotak dalam grid permainan
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)

    # pygame.display.update()


# mengupdate file highscore
def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))


# membaca file untuk skor
def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()        # membaca semua line lalu masukan ke list
        score = int(lines[0].strip())   # remove \n

    return score


def main(window):
    locked_positions = {}
    create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score()

    while run:
        # buat new grid secar konstan dikarenakan locked pos ganti"
        grid = create_grid(locked_positions)

        # tambah time sejak terakhir tick() ke fall_time
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        clock.tick()  # updates clock

        if level_time/1000 > 5:    # naik diff tiap 10 detik
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                # cek piece apakah sudah di bawah atau collide dengan piece lain
                # lock posisi dan buat piece baru
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # geser x position ke kiri
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # gesr x position ke kanan
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # geser shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        piece_pos = convert_shape_format(current_piece)

        # draw  piece ke dalam grid dengan memberikan warna di lokasi piece
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:  # jika piece ke locked
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color       # add key dan value ke dalam dictionary
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10    # increment skor 10 tiap clear
            update_score(score)

            if last_score < score:
                last_score = score

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle('Game Over', 40, (255, 255, 255), window)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()


def main_menu(window):
    run = True
    while run:
        draw_text_middle('Tekan tombol untuk memulai', 50, (255, 255, 255), window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                main(window)

    pygame.quit()


if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('TetrisPBO')

    main_menu(win)  # start game
