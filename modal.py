import pygame

# Inicializar f
pygame.init()

# Colores
ANCHO, ALTO = 900, 700
AZUL_CIELO = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO =(255,0,0)
AZUL_CLARO = (83,212, 255)
GRIS_TEXTO = (0,0,0)
ROSA = (245, 22, 107)
AZUL_TITULO = (32, 23, 198)

pygame.mixer.init()
sonido_modal = pygame.mixer.Sound("sonidos/coin-op_shenanigans.ogg")  
sonido_modal.play()
sonido_modal.play(-1)  # se repite en loop

# Fuentes
fuente_boton = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
fuente_juega = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
fuente_titulo = pygame.font.SysFont("Comic Sans MS", 60, bold=True)

#cargar ciclista
ciclomontañista_img = pygame.image.load("img/ciclomontañista.jpg")
ciclomontañista_img = pygame.transform.scale(ciclomontañista_img, (200, 200))
ciclom_x = (ANCHO - ciclomontañista_img.get_width()) // 2
ciclom_y = (ALTO - ciclomontañista_img.get_height()) // 2

#funcion para el titulo

def animar_titulo(screen):
    clock = pygame.time.Clock()
    texto = "Vuelta a Colombia"
   
    titulo_surface = fuente_titulo.render(texto, True, AZUL_TITULO)
    titulo_rect = titulo_surface.get_rect(center=(ANCHO//2, -100))

    final_y= 100
    
    animando = True

    while animando:
        screen.fill(AMARILLO, rect=(0, 0, ANCHO, ALTO // 3))
        screen.fill(AZUL_CIELO, rect=(0, ALTO // 3, ANCHO, ALTO // 3))
        screen.fill(ROJO, rect=(0, 2 * (ALTO // 3), ANCHO, ALTO // 3))
        screen.blit(ciclomontañista_img, (ciclom_x, ciclom_y))

        if titulo_rect.y < final_y:
            titulo_rect.y +=5
        else:
            animando = False

        screen.blit(titulo_surface, titulo_rect)
        pygame.display.update()
        clock.tick(60)

    return titulo_surface, titulo_rect     


#funcion de la animacion juega
def mostrar_modal_inicio(screen, titulo_surface, titulo_rect):
    clock = pygame.time.Clock()
    texto_juega = fuente_juega.render("JUEGA", True, BLANCO)
    x, y = 100, 100
    dx, dy = 3, 2

    boton_ancho, boton_alto = 250, 60
    boton_x = (ANCHO - boton_ancho) // 2
    boton_y = ALTO - 120

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                boton_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
                if boton_rect.collidepoint(mouse_pos):
                    esperando = False

        # Fondo
        screen.fill(AMARILLO, rect=(0, 0, ANCHO, ALTO // 3))
        screen.fill(AZUL_CIELO, rect=(0, ALTO // 3, ANCHO, ALTO // 3))
        screen.fill(ROJO, rect=(0, 2 * (ALTO // 3), ANCHO, ALTO // 3))
        screen.blit(ciclomontañista_img, (ciclom_x, ciclom_y))
          
        screen.blit(titulo_surface, titulo_rect)

    

        # Animar texto "JUEGA"
        x += dx
        y += dy
        if x <= 0 or x + texto_juega.get_width() >= ANCHO:
            dx *= -1
        if y <= 0 or y + texto_juega.get_height() >= ALTO:
            dy *= -1
        screen.blit(texto_juega, (x, y))

        # Botón
        mouse_pos = pygame.mouse.get_pos()
        boton_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
        if boton_rect.collidepoint(mouse_pos):
            color = AZUL_CLARO
            boton_rect = boton_rect.inflate(20, 10)  # versión segura
        else:
            color = BLANCO

        pygame.draw.rect(screen, color, boton_rect, border_radius=30)
        texto_boton = fuente_boton.render("INICIAR", True, GRIS_TEXTO)
        texto_rect = texto_boton.get_rect(center=boton_rect.center)
        screen.blit(texto_boton, texto_rect)

        pygame.display.update()
        clock.tick(60)
        