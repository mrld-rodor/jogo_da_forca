# config.py
import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "forca_assets")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 200, 0)
CINZA_CLARO = (240, 240, 240)
CINZA_MEDIO = (200, 200, 200)

def get_fontes():
    pygame.font.init()
    fonte_path = os.path.join(ASSETS_DIR, "fonts", "Poppins-Bold.ttf")
    if not os.path.exists(fonte_path):
        return (pygame.font.SysFont("arial", 72), pygame.font.SysFont("arial", 48),
                pygame.font.SysFont("arial", 48), pygame.font.SysFont("arial", 32))
    return (pygame.font.Font(fonte_path, 72), pygame.font.Font(fonte_path, 48),
            pygame.font.Font(fonte_path, 48), pygame.font.Font(fonte_path, 32))

def get_layout(largura, altura):
    # Margens da área branca do caderno
    margem_esq = int(largura * 0.12) 
    margem_dir = int(largura * 0.08) 
    margem_topo = int(altura * 0.12) 
    margem_base = int(altura * 0.12) 
    
    area_util_w = largura - margem_esq - margem_dir
    area_util_h = altura - margem_topo - margem_base
    
    # Âncora fixa da direita
    ancora_x_dir = largura - margem_dir - 40 
    
    return {
        # --- ZONA ESQUERDA (FORCA) ---
        # Movida um pouco mais para a esquerda e para baixo
        'x_forca_centro': margem_esq + int(area_util_w * 0.20),
        'y_forca_centro': margem_topo + int(area_util_h * 0.60),
        'altura_forca': int(area_util_h * 0.55),
        
        # --- ZONA DIREITA (TEXTOS) ---
        # A palavra sobe um pouco e os textos ficam mais próximos
        'x_textos_centro': margem_esq + int(area_util_w * 0.68),
        'y_palavra': margem_topo + int(area_util_h * 0.15),
        'y_letras': margem_topo + int(area_util_h * 0.45),
        'y_input': margem_topo + int(area_util_h * 0.62),
        'y_aviso': margem_topo + int(area_util_h * 0.72),
        
        # Limites para a palavra não vazar
        'x_palavra_min': margem_esq + int(area_util_w * 0.45),
        'x_palavra_max': largura - margem_dir - 40,
        
        # --- HUD (Alinhado à direita) ---
        'hud_x_dir': ancora_x_dir,
        'hud_y_topo': margem_topo + 40,
        'hud_y_base': altura - margem_base - 50,
    }

def carregar_imagem(rel_path, escala=None):
    caminho = os.path.join(ASSETS_DIR, rel_path)
    try:
        img = pygame.image.load(caminho).convert_alpha()
    except pygame.error as e:
        print(f"[AVISO] Não foi possível carregar {caminho}: {e}")
        img = pygame.Surface((50, 50), pygame.SRCALPHA)
        img.fill((255, 0, 255, 128))
    if escala:
        img = pygame.transform.smoothscale(img, escala)
    return img