import pygame

# Initialize the pygame font
pygame.font.init()

# Total window
screen = pygame.display.set_mode((500, 600))

# Title and Icon 
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
img = pygame.image.load('icon.png')
pygame.display.set_icon(img)

x = 0
y = 0
dif = 500 / 9
val = 0

# Default Sudoku Board.
grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)

def get_cord(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif

# Highlight the cell selected
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7) 

# Function to draw required lines for making Sudoku grid		 
def draw():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    
    for i in range(10):
        thick = 7 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)	 


# Fill value entered in cell	 
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15)) 

# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570)) 

def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
    screen.blit(text1, (20, 570)) 

# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val or m[it][j] == val:
            return False
    it = i // 3
    jt = j // 3
    for x in range(it * 3, it * 3 + 3):
        for y in range(jt * 3, jt * 3 + 3):
            if m[x][y] == val:
                return False
    return True

# Solves the sudoku board using Backtracking Algorithm with sets
def solve_with_sets(grid):
    row_sets = [set(range(1, 10)) for _ in range(9)]
    col_sets = [set(range(1, 10)) for _ in range(9)]
    box_sets = [set(range(1, 10)) for _ in range(9)]
    stack = []  #stack
    
    # Initialize sets based on the grid
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                val = grid[r][c]
                row_sets[r].discard(val)
                col_sets[c].discard(val)
                box_sets[(r // 3) * 3 + (c // 3)].discard(val)

    # Backtracking
    def backtrack():
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    # Get available values
                    available = row_sets[r] & col_sets[c] & box_sets[(r // 3) * 3 + (c // 3)]
                    for val in available:
                        grid[r][c] = val
                        row_sets[r].discard(val)
                        col_sets[c].discard(val)
                        box_sets[(r // 3) * 3 + (c // 3)].discard(val)
                        stack.append((r, c, val))  # Keep track of choices
                        
                        if backtrack():
                            return True
                        
                        # If we reach here, we need to backtrack
                        grid[r][c] = 0
                        row_sets[r].add(val)
                        col_sets[c].add(val)
                        box_sets[(r // 3) * 3 + (c // 3)].add(val)
                        stack.pop()
                    return False
        return True  # Solved if no empty cell is found

    # Start backtracking
    if backtrack():
        return True
    else:
        return False

# Display instruction for the game
def instruction():
    text1 = font2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))	 
    screen.blit(text2, (20, 540))

# Display options when solved
def result():
    text1 = font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
    screen.blit(text1, (20, 570)) 

run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0

# The loop that keeps the window running
while run:
    # White color background
    screen.fill((255, 255, 255))
    
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                val = event.key - pygame.K_0  # Convert key to its number
            if event.key == pygame.K_RETURN:
                flag2 = 1
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                grid = [[0] * 9 for _ in range(9)]  # Clear the Sudoku board
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                ]
    if flag2 == 1:
        if not solve_with_sets(grid):
            error = 1
        else:
            rs = 1
        flag2 = 0

    if val != 0:
        draw_val(val)
        if valid(grid, int(x), int(y), val):
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            raise_error2() 
        val = 0

    if error == 1:
        raise_error1() 
    if rs == 1:
        result()	 
    draw() 
    if flag1 == 1:
        draw_box()	 
    instruction() 

    # Update window
    pygame.display.update() 

# Quit pygame window 
pygame.quit()
