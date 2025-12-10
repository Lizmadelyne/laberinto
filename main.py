import pygame, random
from modal import animar_titulo, mostrar_modal_inicio
from modal_victoria import draw_modal, animate_coins
from modal_perdedor import draw_modal_derrota

pygame.init()
#inicializo pygame

fuente_cronometro = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
ANCHO, ALTO = 900, 700 # tamaño de la pantalla para el juego
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La vuelta a colombia")

# Mostrar pantalla inicial
titulo_surface, titulo_rect = animar_titulo(ventana)
mostrar_modal_inicio(ventana, titulo_surface, titulo_rect)


# Cargar imágenes
ciclistas_img= pygame.image.load("img/2ciclistas.jpg")
ciclistas_img= pygame.transform.scale(ciclistas_img,(120,120))
ciclistas_rect = ciclistas_img.get_rect(topright=(ANCHO, 0))

carrera_img = pygame.image.load("img/carrera.jpg")  #este es el jugador
carrera_img = pygame.transform.scale(carrera_img, (25, 25))

colombia_img = pygame.image.load("img/colombia.png") # esta sera la meta
colombia_img = pygame.transform.scale(colombia_img, (50, 50))

laberinto_img = pygame.image.load("img/laberinto3.png").convert_alpha() # el laberinto diseñado en word
laberinto_img= pygame.transform.scale(laberinto_img,(800, 500))
laberinto_rect = laberinto_img.get_rect(center=(ANCHO//2, ALTO//2 + 50))  

nube_img = pygame.image.load("img/nube.png").convert_alpha() # para la colision
nube_img = pygame.transform.scale(nube_img, (80, 80))  # ajusta tamaño si quieres

victoria_img = pygame.image.load("img/victoria.jpg").convert_alpha() #para el ganador
victoria_img = pygame.transform.scale(victoria_img, (120, 120))  

triste_img = pygame.image.load("img/triste.jpg") #para el perdedor
triste_img = pygame.transform.scale(triste_img, (150, 150))


# Colores
def dibujar_fondo_degradado(ventana):
    ANCHO, ALTO = ventana.get_size()

    # Colores del degradado
    color_cielo_arriba = (120, 200, 255)   # azul suave
    color_cielo_abajo = (180, 230, 255)    # azul claro 

    color_pasto_arriba = (80, 200, 80)     # verde suave (justo debajo del cielo)
    color_pasto_abajo = (40, 150, 40)      # verde más oscuro (abajo)

    for y in range(ALTO):

        # Elegir si estamos en el cielo o el pasto
        if y < ALTO // 2:
            ratio = y / (ALTO // 2)
            r = int(color_cielo_arriba[0] * (1 - ratio) + color_cielo_abajo[0] * ratio)
            g = int(color_cielo_arriba[1] * (1 - ratio) + color_cielo_abajo[1] * ratio)
            b = int(color_cielo_arriba[2] * (1 - ratio) + color_cielo_abajo[2] * ratio)
        else:
            ratio = (y - ALTO // 2) / (ALTO // 2)
            r = int(color_pasto_arriba[0] * (1 - ratio) + color_pasto_abajo[0] * ratio)
            g = int(color_pasto_arriba[1] * (1 - ratio) + color_pasto_abajo[1] * ratio)
            b = int(color_pasto_arriba[2] * (1 - ratio) + color_pasto_abajo[2] * ratio)

        pygame.draw.line(ventana, (r, g, b), (0, y), (ANCHO, y))


# Jugador
tamaño_jugador = carrera_img.get_rect()
tamaño_jugador = 40
x_jugador, y_jugador = 250, 100
velocidad = 5
jugador_rect = pygame.Rect(x_jugador, y_jugador, tamaño_jugador, tamaño_jugador)

#meta
meta_rect = colombia_img.get_rect()
meta_rect.topleft = (750, 610)  # posición en la pantalla

# Reloj y control
reloj = pygame.time.Clock()
jugando = True
cronometro_iniciado = False
cronometro_detener = False
start_time = 0

# Crear máscara del laberinto para las  colisiones
laberinto_mask = pygame.mask.from_threshold(
    laberinto_img,
    (0, 0, 0, 255),   # color exacto de la pared (negro)
    (50, 50, 50, 255) # tolerancia (para colores cercanos al negro)
)

show_modal = False
coins = [pygame.Rect(random.randint(0, ANCHO), random.randint(-200, -50), 20, 20) for _ in range(20)] # esta es la bienvenida

# logica para el videojuego
colisiones = 0
en_colision= False
accion= None
while jugando:
    events = pygame.event.get()
    for evento in events:
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()

    # Actualizamos el rect del jugador
    jugador_rect.topleft = (x_jugador, y_jugador)

    # Iniciar cronómetro al primer movimiento
    if not cronometro_iniciado and (
        teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT] or teclas[pygame.K_UP] or teclas[pygame.K_DOWN]
    ):
        start_time = pygame.time.get_ticks() #inicia el cronometro
        cronometro_iniciado = True

    anterior_x, anterior_y = x_jugador, y_jugador

    if teclas[pygame.K_LEFT]:
        x_jugador -= velocidad
    if teclas[pygame.K_RIGHT]:
        x_jugador += velocidad
    if teclas[pygame.K_UP]:
        y_jugador -= velocidad
    if teclas[pygame.K_DOWN]:
        y_jugador += velocidad

    # Actualizar rect
    jugador_rect.topleft = (x_jugador, y_jugador)

    # Máscara y colisión
    jugador_mask = pygame.mask.Mask((jugador_rect.width, jugador_rect.height), True)
    offset_x = jugador_rect.x - laberinto_rect.x
    offset_y = jugador_rect.y - laberinto_rect.y

    mostrar_oops = False
    if laberinto_mask.overlap(jugador_mask, (offset_x, offset_y)):
        mostrar_oops = True
        x_jugador, y_jugador = anterior_x, anterior_y
        jugador_rect.topleft = (x_jugador, y_jugador)
        
        if not en_colision:
            colisiones +=1
            en_colision = True
        else:
            en_colision= False
        
    #la funcion para contar las colisiones y  abrir el modal de perdedor
    if colisiones >= 20:
        accion = draw_modal_derrota(ventana, triste_img, ANCHO, ALTO)
        if accion == "reintentar":
            x_jugador, y_jugador = 250, 100
            jugador_rect.topleft = (x_jugador, y_jugador)
            colisiones = 0
            cronometro_iniciado = False
            start_time = pygame.time.get_ticks()
        elif accion == "salir":
            jugando = False


    # Meta
    if jugador_rect.colliderect(meta_rect) and not cronometro_detener:
        tiempo_total = (pygame.time.get_ticks() - start_time) / 1000
        print(f"¡Has dado la vuelta a Colombia en {tiempo_total:.2f} segundos!")
        cronometro_detener = True
        show_modal = True
           # aquí se detiene el cronómetro

    # Dibujar escena
    dibujar_fondo_degradado(ventana)
    ventana.blit(ciclistas_img, ciclistas_rect.topleft)
    ventana.blit(laberinto_img, laberinto_rect.topleft)
    ventana.blit(colombia_img, meta_rect.topleft)
    ventana.blit(carrera_img, jugador_rect.topleft)

    if mostrar_oops:
        ventana.blit(nube_img, (jugador_rect.x, jugador_rect.y - 50))

    if show_modal:
        accion = draw_modal(ventana, victoria_img, ANCHO, ALTO, events)
        animate_coins(ventana, coins, ANCHO, ALTO) 
    else:
        accion = None
    
    if accion == "reintentar": #esta funcion es para deectar el clic cuando llega a la meta y abrir el modal
        x_jugador, y_jugador = 250, 100
        jugador_rect.topleft = (x_jugador, y_jugador)
        cronometro_detener = False
        cronometro_iniciado = False
        start_time = pygame.time.get_ticks()
        colisiones = 0
        show_modal = False  # cierra el modal
    elif accion == "salir":
        jugando = False


    # Cronómetro
    if cronometro_iniciado and not cronometro_detener:
        # sigue contando
        tiempo_actual = (pygame.time.get_ticks() - start_time) / 1000
        texto_tiempo = fuente_cronometro.render(f"Tiempo: {tiempo_actual:.2f} s", True, (0, 0, 0))
        ventana.blit(texto_tiempo, (20, 20))
    elif cronometro_detener:
        texto_tiempo = fuente_cronometro.render(f"Tiempo: {tiempo_total:.2f} s", True, (0, 0, 0))
        ventana.blit(texto_tiempo, (20, 20))
        

    pygame.display.flip()
    reloj.tick(60)