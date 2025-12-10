import pygame, random


def draw_modal(screen, victoria_img, ANCHO, ALTO, events):
    mouse_pos = pygame.mouse.get_pos()
    accion = None

    # Fondo semi-transparente
    modal_surface = pygame.Surface((ANCHO, ALTO))
    modal_surface.set_alpha(180)
    modal_surface.fill((0, 0, 0))
    screen.blit(modal_surface, (0, 0))

    # Imagen de victoria
    screen.blit(victoria_img, (ANCHO//2 - victoria_img.get_width()//2, ALTO//2 - 150))

    # Texto de victoria
    font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    text = font.render("¡Ganaste la vuelta a Colombia!", True, (255, 215, 0))
    screen.blit(text, (ANCHO//2 - text.get_width()//2, ALTO//2 + 50))

    # Botones
    button_font = pygame.font.SysFont("Comic Sans MS", 20, bold=True)
    button_width = 120
    button_height = 50
    margin = 30
    separation = 80
    total_width = button_width * 2 + separation
    start_x = (ANCHO - total_width) // 2
    y_pos = ALTO - button_height - margin

    retry_rect = pygame.Rect(start_x, y_pos, button_width, button_height)
    exit_rect  = pygame.Rect(start_x + button_width + separation, y_pos, button_width, button_height)

    # Colores y hover
    retry_color = (255, 215, 0)
    exit_color  = (200, 50, 50)
    if retry_rect.collidepoint(mouse_pos):
        retry_color = (80, 230, 80)
    if exit_rect.collidepoint(mouse_pos):
        exit_color = (230, 80, 80)

    # Dibujo en la pantalls
    pygame.draw.rect(screen, retry_color, retry_rect, border_radius=10)
    pygame.draw.rect(screen, exit_color,  exit_rect,  border_radius=10)

    retry_text = button_font.render("AGAIN", True, (255, 255, 255))
    exit_text  = button_font.render("EXIT",  True, (255, 255, 255))
    screen.blit(retry_text, retry_text.get_rect(center=retry_rect.center))
    screen.blit(exit_text,  exit_text.get_rect(center=exit_rect.center))

    # Detectar clics usando los eventos pasados
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if retry_rect.collidepoint(event.pos):
                accion = "reintentar"
            elif exit_rect.collidepoint(event.pos):
                accion = "salir"

    return accion
# funcion animacion de monedas bajando como premio
def animate_coins(screen, coins, ANCHO, ALTO):
    for coin in coins:
        coin.y += 30
        if coin.y > ALTO:
            coin.y = random.randint(-200, -50)
            coin.x = random.randint(0, ANCHO)
        pygame.draw.circle(screen, (255, 223, 0), coin.center, 10)
