import pygame

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Font Showcase")
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
bahnschrift_font = pygame.font.SysFont("bahnschrift", 50)
consolas_font = pygame.font.SysFont("consolas", 50)
impact_font = pygame.font.SysFont("impact", 50)
agencyfb_font = pygame.font.SysFont("agencyfb", 50)
lucidaconsole_font = pygame.font.SysFont("lucidaconsole", 50)
franklingothicmedium_font = pygame.font.SysFont("franklingothicmedium", 50)
stencil_font = pygame.font.SysFont("stencil", 50)
haettenschweiler_font = pygame.font.SysFont("haettenschweiler", 50)
ocraextended_font = pygame.font.SysFont("ocraextended", 50)  # Note: This might not be available on all systems
segoeuiblack_font = pygame.font.SysFont("segoeuiblack", 50)

# Render text
texts = [
    bahnschrift_font.render("Bahnschrift Font", True, white),
    consolas_font.render("Consolas Font", True, white),
    impact_font.render("Impact Font", True, white),
    agencyfb_font.render("Agency FB Font", True, white),
    lucidaconsole_font.render("Lucida Console Font", True, white),
    franklingothicmedium_font.render("Franklin Gothic Medium Font", True, white),
    stencil_font.render("Stencil Font", True, white),
    haettenschweiler_font.render("Haettenschweiler Font", True, white),
    ocraextended_font.render("OCR A Extended Font", True, white),
    segoeuiblack_font.render("Segoe UI Black Font", True, white),
]

# Display text on the screen
screen.fill(black)  # Set background to black
y = 50
for text in texts:
    screen.blit(text, (50, y))
    y += 60  # Increment Y position for each font

pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


