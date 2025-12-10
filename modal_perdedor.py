
import pygame

# Colores
AZUL = (0, 0, 250)
AZUL_CLARO = (83, 212, 255)
BLANCO_TEXTO = (255, 255, 255)
AMARILLO = (255, 215, 0)

# Fuentes
fuente_boton = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
fuente_titulo = pygame.font.SysFont("Comic Sans MS", 40, bold=True)

def draw_modal_derrota(screen, triste_img, ANCHO, ALTO):
    clock = pygame.time.Clock()
    anim_y = ALTO//2 - 200
    dy = 2

    # Botones
    boton_ancho, boton_alto = 200, 60
    boton_reintentar = pygame.Rect(ANCHO//2 - 220, ALTO - 150, boton_ancho, boton_alto)
    boton_salir = pygame.Rect(ANCHO//2 + 20, ALTO - 150, boton_ancho, boton_alto)

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reintentar.collidepoint(event.pos):
                    return "reintentar"
                if boton_salir.collidepoint(event.pos):
                    return "salir"

        # Fondo semi-transparente
        modal_surface = pygame.Surface((ANCHO, ALTO))
        modal_surface.set_alpha(180)
        modal_surface.fill((0, 0, 0))
        screen.blit(modal_surface, (0, 0))

        # Animación de la imagen triste (sube y baja)
        anim_y += dy
        if anim_y <= ALTO//2 - 220 or anim_y >= ALTO//2 - 180:
            dy *= -1
        screen.blit(triste_img, (ANCHO//2 - triste_img.get_width()//2, anim_y))

        # Texto de derrota
        text = fuente_titulo.render("¡Perdiste la vuelta a Colombia!", True, AMARILLO)
        screen.blit(text, (ANCHO//2 - text.get_width()//2, ALTO//2 + 50))

        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()

        for boton, texto in [(boton_reintentar, "REINTENTAR"), (boton_salir, "SALIR")]:
            if boton.collidepoint(mouse_pos):
                color = AZUL
                boton_inflate = boton.inflate(20, 10)
            else:
                color = AZUL_CLARO
                boton_inflate = boton

            pygame.draw.rect(screen, color, boton_inflate, border_radius=20)
            texto_boton = fuente_boton.render(texto, True, BLANCO_TEXTO)
            texto_rect = texto_boton.get_rect(center=boton_inflate.center)
            screen.blit(texto_boton, texto_rect)

        pygame.display.update()
        clock.tick(60)


