import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 1500, 1000
ROAD_COLOR = (100, 100, 100)
BUILDING_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 24
ROAD_WIDTH = 40  # Width of the roads
CHARACTER_COLOR = (255, 0, 0)
CHARACTER_RADIUS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Town")

font = pygame.font.Font(None, FONT_SIZE)

character_pos = [250, 400]  # Player character

class Character:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.x = position[0]
        self.y = position[1]

    def set_position(self, position):
        self.position = position
        self.x = position[0]
        self.y = position[1]

    def set_x(self, x):
        self.position[0] = x
        self.x = x
    
    def set_y(self, y):
        self.position[1] = y
        self.y = y

    def move_x(self, dx):
        self.position[0] += dx
        self.x += dx

    def move_y(self, dy):
        self.position[1] += dy
        self.y += dy
        



def draw_road(start_pos, end_pos, name):
    pygame.draw.rect(screen, ROAD_COLOR, (*start_pos, end_pos[0] - start_pos[0], ROAD_WIDTH))
    mid_x = (start_pos[0] + end_pos[0]) // 2
    mid_y = (start_pos[1] + ROAD_WIDTH // 2)
    text_surface = font.render(name, True, TEXT_COLOR)
    screen.blit(text_surface, (mid_x - text_surface.get_width() // 2, mid_y - text_surface.get_height() // 2))

def draw_building(rect, name):
    pygame.draw.rect(screen, BUILDING_COLOR, rect)
    text_surface = font.render(name, True, TEXT_COLOR)
    screen.blit(text_surface, (rect.x + rect.width // 2 - text_surface.get_width() // 2, rect.y + rect.height // 2 - text_surface.get_height() // 2))

def draw_character(position):
    pygame.draw.circle(screen, CHARACTER_COLOR, position, CHARACTER_RADIUS)


def Capture(display,name,pos,size): # (pygame Surface, String, tuple, tuple)
    image = pygame.Surface(size)  # Create image surface
    image.blit(display,(0,0),(pos,size))  # Blit portion of the display to the image
    pygame.image.save(image,name)  # Save the image to the disk


def main():
    clock = pygame.time.Clock()
    character = Character([250, 400], CHARACTER_COLOR)
    # Draw roads
    draw_road((200, 400), (1800, 400), "Main St")      # Horizontal road
    draw_road((1000, 200), (1000, 600), "2nd Ave")     # Vertical road

    # Draw intersection
    intersection_pos = (1000, 400)
    pygame.draw.circle(screen, (0, 255, 0), intersection_pos, 10)  # Draw intersection
    text_surface = font.render("Intersection", True, TEXT_COLOR)
    screen.blit(text_surface, (intersection_pos[0] + 15, intersection_pos[1] - 10))

    # Draw buildings next to Main St without overlapping
    draw_building(pygame.Rect(250, 450, 150, 150), "House 1")  # Below Main St
    draw_building(pygame.Rect(450, 450, 150, 200), "Store")    # Below Main St
    draw_building(pygame.Rect(650, 450, 150, 250), "School")   # Below Main St

    # Move the park next to 2nd Ave
    draw_building(pygame.Rect(950, 350, 150, 150), "Park")      # Next to 2nd Ave

    # Main loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and character.x > 0:
            character.move_x(-5)
        if keys[pygame.K_RIGHT] and character.x < WIDTH:
            character.move_x(5)
        if keys[pygame.K_UP] and character.y > 0:
            character.move_y(-5)
        if keys[pygame.K_DOWN] and character.y < HEIGHT:
            character.move_y(5)
        if keys[pygame.K_1]:
            Capture(screen,"screenshot.png",(character.x-40,character.y-40),(character.x+40,character.y+40))

        print(character.x,character.y)
        # Keep character on the roads
        if character.y < 400:  
            character.y = 400
        elif character.y < 600:  
            character.y = 400
        else:  # On 2nd Ave
            character.y = max(200, min(character.y, 600))

        # Refresh screen
        screen.fill((255, 255, 255))  # Clear screen
        # Redraw roads, buildings, and character
        draw_road((200, 400), (1800, 400), "Main St")
        draw_road((1000, 200), (1000, 600), "2nd Ave")  # Vertical road
        
        pygame.draw.circle(screen, (0, 255, 0), intersection_pos, 10)  # Draw intersection
        text_surface = font.render("Intersection", True, TEXT_COLOR)
        screen.blit(text_surface, (intersection_pos[0] + 15, intersection_pos[1] - 10))

        draw_building(pygame.Rect(250, 450, 150, 150), "House 1")
        draw_building(pygame.Rect(450, 450, 150, 200), "Store")
        draw_building(pygame.Rect(650, 450, 150, 250), "School")
        draw_building(pygame.Rect(950, 350, 150, 150), "Park")  # Updated position

        draw_character([character.x, character.y])

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
