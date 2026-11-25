# Configurações globais do jogo (cores, fontes, dimensões)
import pygame

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 200, 0)
CINZA_CLARO = (240, 240, 240)

# Fontes (padrão, pode ser ajustado conforme necessidade)
def get_fontes():
    pygame.font.init()
    fonte = pygame.font.SysFont('arial', 72)
    fonte_pequena = pygame.font.SysFont('arial', 48)
    fonte_popup = pygame.font.SysFont('arial', 48)
    fonte_pequena_popup = pygame.font.SysFont('arial', 32)
    return fonte, fonte_pequena, fonte_popup, fonte_pequena_popup

# Dimensões padrão de botões, popups, etc.
BOTAO_OPCOES = (260, 80)
BOTAO_MENU = (220, 60)
POPUP_CREDITOS = (1000, 500)
POPUP_OPCOES = (500, 220)


def get_layout(largura, altura):
    """Retorna medidas proporcionais à resolução atual."""
    margem = int(largura * 0.03)             # 3% da largura (~57px em 1920)
    largura_botao = int(largura * 0.14)      # 14% (~268px)
    altura_botao = int(altura * 0.075)       # 7,5% (~81px)
    
    return {
        'margem': margem,
        'largura_botao': largura_botao,
        'altura_botao': altura_botao,
        'espaco_lista': int(altura * 0.065), # ~70px entre dificuldades
        'y_titulo': int(altura * 0.07),      # ~75px
        'y_subtitulo': int(altura * 0.16),   # ~173px
        'espaco_secao': int(altura * 0.04),   # ~43px entre zonas verticais
        'y_forca': int(altura * 0.55),        # ~594px, topo da forca
    }