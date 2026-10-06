import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mascota Virtual IPET 249 - Steve Programador")

# Reloj de FPS
reloj = pygame.time.Clock()

# Paleta de Colores Institucionales y Complementarios
BORDO = (128, 0, 32)
AMARILLO = (255, 215, 0)
ROJO = (220, 20, 60)
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS_OSCURO = (40, 40, 40)
PIEL = (220, 160, 120)
MARRON = (100, 60, 30)
AZUL_JEAN = (40, 60, 120)
VERDE = (50, 205, 50)

# Variables de Estado de la Mascota (0 a 100)
bateria = 100.0   # Carga de Café / Batería
codigo = 100.0    # Nivel de Código / Ánimo
salud = 100.0     # Limpieza de Bugs / Salud

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 22, bold=True)
fuente_texto = pygame.font.SysFont("Arial", 16)
fuente_estado = pygame.font.SysFont("Arial", 18, bold=True)

def dibujar_escudo(x, y):
    """Dibuja el escudo institucional del IPET 249."""
    pygame.draw.polygon(pantalla, AMARILLO, [(x, y), (x + 70, y), (x + 70, y + 60), (x + 35, y + 85), (x, y + 60)])
    pygame.draw.polygon(pantalla, BORDO, [(x, y), (x + 70, y), (x + 70, y + 60), (x + 35, y + 85), (x, y + 60)], 3)
    
    # Texto del escudo
    texto_escudo = fuente_texto.render("249", True, BORDO)
    pantalla.blit(texto_escudo, (x + 20, y + 30))

def dibujar_steve(x, y, estado):
    """Dibuja a Steve de Minecraft con accesorios y ropa del IPET 249."""
    # Cabeza (80x80)
    pygame.draw.rect(pantalla, PIEL, (x, y, 80, 80))
    # Cabello
    pygame.draw.rect(pantalla, MARRON, (x, y, 80, 20))
    pygame.draw.rect(pantalla, MARRON, (x, y + 20, 15, 20))
    pygame.draw.rect(pantalla, MARRON, (x + 65, y + 20, 15, 20))

    # Ojos y Expresión según estado
    if estado == "cansado":
        # Ojos adormilados / entornados
        pygame.draw.rect(pantalla, NEGRO, (x + 15, y + 45, 15, 4))
        pygame.draw.rect(pantalla, NEGRO, (x + 50, y + 45, 15, 4))
    elif estado == "bugs":
        # Ojos desorbitados (error)
        pygame.draw.rect(pantalla, ROJO, (x + 15, y + 40, 15, 10))
        pygame.draw.rect(pantalla, ROJO, (x + 50, y + 40, 15, 10))
    else:
        # Ojos normales (Steve feliz/programando)
        pygame.draw.rect(pantalla, BLANCO, (x + 15, y + 40, 15, 10))
        pygame.draw.rect(pantalla, AZUL_JEAN, (x + 22, y + 40, 8, 10))
        pygame.draw.rect(pantalla, BLANCO, (x + 50, y + 40, 15, 10))
        pygame.draw.rect(pantalla, AZUL_JEAN, (x + 57, y + 40, 8, 10))

    # Nariz / Boca
    pygame.draw.rect(pantalla, MARRON, (x + 32, y + 52, 16, 8))
    
    # Anteojos de Programador
    pygame.draw.rect(pantalla, NEGRO, (x + 10, y + 36, 25, 18), 2)
    pygame.draw.rect(pantalla, NEGRO, (x + 45, y + 36, 25, 18), 2)
    pygame.draw.line(pantalla, NEGRO, (x + 35, y + 42), (x + 45, y + 42), 2)

    # Auriculares Gaming Institucionales (Bordó y Amarillo)
    pygame.draw.rect(pantalla, BORDO, (x - 10, y + 25, 12, 35))
    pygame.draw.rect(pantalla, BORDO, (x + 78, y + 25, 12, 35))
    pygame.draw.arc(pantalla, BORDO, (x - 8, y - 10, 96, 40), 0, 3.14, 5)
    pygame.draw.rect(pantalla, AMARILLO, (x - 6, y + 35, 4, 15))
    pygame.draw.rect(pantalla, AMARILLO, (x + 82, y + 35, 4, 15))

    # Cuerpo / Remera del IPET 249 (Bordó con franja Amarilla)
    pygame.draw.rect(pantalla, BORDO, (x - 20, y + 80, 120, 100))
    pygame.draw.rect(pantalla, AMARILLO, (x - 20, y + 120, 120, 15))
    
    # Escudo bordado en el pecho
    pygame.draw.rect(pantalla, AMARILLO, (x + 60, y + 90, 18, 22))
    
    # Brazos
    pygame.draw.rect(pantalla, PIEL, (x - 45, y + 80, 25, 80))
    pygame.draw.rect(pantalla, PIEL, (x + 100, y + 80, 25, 80))

    # Pantalones Jean
    pygame.draw.rect(pantalla, AZUL_JEAN, (x - 20, y + 180, 120, 80))

def dibujar_barra(x, y, ancho, alto, valor, color, etiqueta):
    """Dibuja las barras de estado dinámicas."""
    # Fondo de la barra
    pygame.draw.rect(pantalla, GRIS_OSCURO, (x, y, ancho, alto), border_radius=5)
    # Porcentaje actual
    ancho_actual = int((valor / 100.0) * ancho)
    if ancho_actual > 0:
        pygame.draw.rect(pantalla, color, (x, y, ancho_actual, alto), border_radius=5)
    # Borde
    pygame.draw.rect(pantalla, BLANCO, (x, y, ancho, alto), 2, border_radius=5)
    # Texto
    texto = fuente_texto.render(f"{etiqueta}: {int(valor)}%", True, BLANCO)
    pantalla.blit(texto, (x, y - 22))

# Ciclo principal del juego
ejecutando = True
mensaje_accion = "¡Usa las teclas [C], [P] o [B] para interactuar!"

while ejecutando:
    # 1. Gestión de Desgaste Temporal
    bateria = max(0.0, bateria - 0.03)
    codigo = max(0.0, codigo - 0.02)
    salud = max(0.0, salud - 0.015)

    # 2. Eventos de Teclado y Botones
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_c:  # Tomar café / Recargar batería
                bateria = min(100.0, bateria + 25.0)
                mensaje_accion = "¡Steve tomó un Café de Sistemas! (+25% Batería)"
            elif evento.key == pygame.K_p:  # Programar
                codigo = min(100.0, codigo + 20.0)
                mensaje_accion = "¡Steve programó un script en Python! (+20% Código)"
            elif evento.key == pygame.K_b:  # Depurar / Limpiar Bugs
                salud = min(100.0, salud + 30.0)
                mensaje_accion = "¡Steve eliminó los Bugs del sistema! (+30% Salud)"

    # 3. Determinación de Estado Visual
    if bateria < 30.0:
        estado_mascota = "cansado"
        estado_texto = "Estado: ¡Sin Batería / Cansado!"
    elif salud < 30.0:
        estado_mascota = "bugs"
        estado_texto = "Estado: ¡Sistemas infectados con BUGS!"
    else:
        estado_mascota = "feliz"
        estado_texto = "Estado: Programando a full (OK)"

    # 4. Renderizado Visual
    pantalla.fill(BORDO)  # Fondo institucional bordó

    # Marco de la interfaz
    pygame.draw.rect(pantalla, GRIS_OSCURO, (20, 20, 760, 560), border_radius=10)
    pygame.draw.rect(pantalla, AMARILLO, (25, 25, 750, 550), 3, border_radius=10)

    # Encabezado e Identidad Institucional
    dibujar_escudo(45, 40)
    titulo_1 = fuente_titulo.render("IPET 249 - Nicolás Copérnico", True, AMARILLO)
    titulo_2 = fuente_texto.render("Especialidad: Informática | Mascota Virtual: Steve Copérnico", True, BLANCO)
    pantalla.blit(titulo_1, (130, 45))
    pantalla.blit(titulo_2, (130, 75))

    # Dibujar la Mascota
    dibujar_steve(360, 200, estado_mascota)

    # Barras de Estado (Bloque 2)
    dibujar_barra(50, 480, 200, 20, bateria, AMARILLO, "Carga / Batería (C)")
    dibujar_barra(300, 480, 200, 20, codigo, VERDE, "Nivel de Código (P)")
    dibujar_barra(550, 480, 200, 20, salud, ROJO, "Limpia de Bugs (B)")

    # Estado y Mensajes de Control
    txt_estado = fuente_estado.render(estado_texto, True, AMARILLO)
    txt_instrucciones = fuente_texto.render("[C] Tomar Café  |  [P] Programar  |  [B] Limpiar Bugs", True, BLANCO)
    txt_feedback = fuente_texto.render(mensaje_accion, True, BLANCO)

    pantalla.blit(txt_estado, (260, 150))
    pantalla.blit(txt_instrucciones, (230, 525))
    pantalla.blit(txt_feedback, (200, 550))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
