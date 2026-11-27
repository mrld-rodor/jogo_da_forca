# config.py
import os
import sys
import pygame


def resource_path(*partes):
    """Caminho de um recurso, tanto a correr via Python como dentro do executavel (PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *partes)


BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = resource_path("forca_assets")

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
    margem_esq = int(largura * 0.12)
    margem_dir = int(largura * 0.08)
    margem_topo = int(altura * 0.12)
    margem_base = int(altura * 0.12)
    
    margem_icones = 60 
    x_icones = largura - margem_dir - margem_icones
    
    # AQUI ESTÁ A CORREÇÃO: Centraliza a palavra no espaço entre a forca e o HUD
    # A forca ocupa até ~40% da tela, o HUD fica nos 90%. O centro lógico é 65% da tela.
    x_textos_centro = int(largura * 0.65)
    
    return {
        # --- ZONA ESQUERDA (FORCA) ---
        'x_forca_centro': margem_esq + int(largura * 0.18),
        'y_forca_centro': int(altura * 0.65), 
        'altura_forca': int(altura * 0.45), 
        
        # --- ZONA DIREITA (TEXTOS) ---
        'x_textos_centro': x_textos_centro,  # AGORA CENTRALIZADO EM 65% DA TELA
        
        # Y dos textos
        'y_palavra': int(altura * 0.32), 
        'y_letras': int(altura * 0.55),
        'y_input': int(altura * 0.75),
        
        # Limites para a palavra não vazar para os lados
        'limite_palavra_esq': margem_esq + int((largura - margem_esq - margem_dir) * 0.30),
        'limite_palavra_dir': x_icones - 120,
        
        # --- HUD ---
        'hud_x_dir': x_icones,
        'hud_y_topo': margem_topo + margem_icones,
        'hud_y_base': altura - margem_base - margem_icones,
        
        # --- LARGURA MÁXIMA DE TEXTO (Para quebra de linha) ---
        'largura_max_texto': int(largura * 0.45)
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