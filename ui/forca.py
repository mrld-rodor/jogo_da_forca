# ui/forca.py
import pygame
from config import carregar_imagem

class ForcaDesenhavel:
    """Desenha a forca usando os estágios em PNG do projeto."""

    def __init__(self, largura, altura, altura_alvo=None):
        self.largura = largura
        self.altura = altura
        self.altura_alvo = altura_alvo or int(altura * 0.42)

        # Carrega os 7 estágios (0 a 6 erros)
        self.estagios = []
        for i in range(7):
            img = carregar_imagem(f'hangman/stage_{i}.png')
            # Redimensiona mantendo proporção para a altura alvo
            proporcao = img.get_width() / img.get_height()
            nova_largura = int(self.altura_alvo * proporcao)
            img = pygame.transform.smoothscale(img, (nova_largura, self.altura_alvo))
            self.estagios.append(img)

        # Centraliza no eixo X e Y conforme configuração
        self.rect = self.estagios[0].get_rect()

    def definir_centro(self, cx, cy):
        """Define o centro da forca na tela."""
        self.rect = self.estagios[0].get_rect(center=(cx, cy))

    def desenhar(self, tela, erros):
        """Desenha o estágio correspondente ao número de erros (0 a 6)."""
        erros = max(0, min(6, erros))
        tela.blit(self.estagios[erros], self.rect)