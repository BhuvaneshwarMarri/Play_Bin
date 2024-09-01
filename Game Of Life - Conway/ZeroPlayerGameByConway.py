import pygame
import time
import numpy as np
COLOR_BG = (8, 8, 8)  
COLOR_GRID = (19, 19, 19)  
COLOR_DIE_NEXT = (255, 255, 255) 
COLOR_ALIVE_NEXT = (255, 27, 45)  
SIZE = 10

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    
    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT
        
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        
        if cells[row, col] == 1 or (with_progress and updated_cells[row, col] == 1):
            pygame.draw.circle(screen, color, (col*size + size//2, row*size + size//2), size//3)
        else:
            pygame.draw.circle(screen, COLOR_BG,(col*size + size//2, row*size + size//2),size//3)
    
    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((80*SIZE, 60*SIZE))
    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, SIZE)
    pygame.display.flip()
    
    running = False
    
    while True:
        new_cells = cells.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, SIZE)
                    pygame.display.update()
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                new_cells[pos[1] // SIZE, pos[0] // SIZE] = 1
                cells = new_cells
                update(screen, cells, SIZE)
                pygame.display.update()
        
        screen.fill(COLOR_GRID)
        
        if running:
            cells = update(screen, cells, SIZE, with_progress=True)
            pygame.display.update()
        
        time.sleep(0.001)

if __name__ == "__main__":
    main()
