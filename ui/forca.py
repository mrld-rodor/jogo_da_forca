import pygame
import math
from config import PRETO

class ForcaDesenhavel:
    """Classe para desenhar a forca e o boneco com animações progressivas."""
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.erros_anteriores = 0
        self.tempo_inicio_animacao = 0
        self.duracao_animacao = 400  # Tempo em milissegundos para desenhar cada parte

    def _desenhar_linha_progressiva(self, tela, inicio, fim, progresso, espessura):
        """Desenha uma linha do ponto inicial ao final, baseado no progresso (0.0 a 1.0)"""
        if progresso >= 1.0:
            pygame.draw.line(tela, PRETO, inicio, fim, espessura)
        elif progresso > 0.0:
            # Interpolação linear para achar o ponto atual
            x_atual = inicio[0] + (fim[0] - inicio[0]) * progresso
            y_atual = inicio[1] + (fim[1] - inicio[1]) * progresso
            pygame.draw.line(tela, PRETO, inicio, (x_atual, y_atual), espessura)

    def _desenhar_circulo_progressivo(self, tela, centro, raio, progresso, espessura):
        """Desenha um círculo/arco progressivamente usando pygame.draw.arc"""
        if progresso >= 1.0:
            pygame.draw.circle(tela, PRETO, centro, raio, espessura)
        elif progresso > 0.0:
            # O pygame.draw.arc desenha de 0 a 2*pi (em radianos). 
            # Começamos em pi/2 (topo) e giramos no sentido horário.
            rect = pygame.Rect(centro[0] - raio, centro[1] - raio, raio * 2, raio * 2)
            angulo_fim = math.pi/2 - (math.pi * 2 * progresso)
            # O pygame desenha no sentido anti-horário por padrão, então invertemos
            pygame.draw.arc(tela, PRETO, rect, angulo_fim, math.pi/2, espessura)

    def desenhar(self, tela, erros):
        # Detecção de novo erro para iniciar a animação
        if erros > self.erros_anteriores:
            self.tempo_inicio_animacao = pygame.time.get_ticks()
            self.erros_anteriores = erros
        elif erros < self.erros_anteriores:
            # Se o jogo reiniciou (erros voltaram para 0), reseta a animação
            self.erros_anteriores = erros
            self.tempo_inicio_animacao = 0

        # Calcula o progresso (0.0 a 1.0) da animação atual
        tempo_decorrido = pygame.time.get_ticks() - self.tempo_inicio_animacao
        progresso = min(1.0, tempo_decorrido / self.duracao_animacao)
        
        # Se for o início do jogo, progresso é 1.0 (não tem animação pendente)
        if self.tempo_inicio_animacao == 0:
            progresso = 1.0

        base_x = (self.largura // 2) - 100
        base_y = self.altura - 250
        altura_forca = 200
        largura_forca = 100
        
        # Base e madeira (desenhados de uma vez, são o cenário)
        pygame.draw.line(tela, PRETO, (base_x, base_y), (base_x + largura_forca, base_y), 6)
        pygame.draw.line(tela, PRETO, (base_x + largura_forca//2, base_y), (base_x + largura_forca//2, base_y - altura_forca), 6)
        pygame.draw.line(tela, PRETO, (base_x + largura_forca//2, base_y - altura_forca), (base_x + largura_forca + 30, base_y - altura_forca), 6)
        pygame.draw.line(tela, PRETO, (base_x + largura_forca + 30, base_y - altura_forca), (base_x + largura_forca + 30, base_y - altura_forca + 30), 6)
        
        # Elementos do boneco (animados)
        # Cabeça (1 erro)
        if erros > 0:
            p = progresso if erros == 1 else 1.0
            self._desenhar_circulo_progressivo(tela, (base_x + largura_forca + 30, base_y - altura_forca + 60), 20, p, 4)
        
        # Tronco (2 erros)
        if erros > 1:
            p = progresso if erros == 2 else 1.0
            self._desenhar_linha_progressiva(tela, 
                (base_x + largura_forca + 30, base_y - altura_forca + 80), 
                (base_x + largura_forca + 30, base_y - altura_forca + 140), 
                p, 4)
        
        # Braço esquerdo (3 erros)
        if erros > 2:
            p = progresso if erros == 3 else 1.0
            self._desenhar_linha_progressiva(tela, 
                (base_x + largura_forca + 30, base_y - altura_forca + 90), 
                (base_x + largura_forca + 5, base_y - altura_forca + 110), 
                p, 4)
        
        # Braço direito (4 erros)
        if erros > 3:
            p = progresso if erros == 4 else 1.0
            self._desenhar_linha_progressiva(tela, 
                (base_x + largura_forca + 30, base_y - altura_forca + 90), 
                (base_x + largura_forca + 55, base_y - altura_forca + 110), 
                p, 4)
        
        # Perna esquerda (5 erros)
        if erros > 4:
            p = progresso if erros == 5 else 1.0
            self._desenhar_linha_progressiva(tela, 
                (base_x + largura_forca + 30, base_y - altura_forca + 140), 
                (base_x + largura_forca + 5, base_y - altura_forca + 180), 
                p, 4)
        
        # Perna direita (6 erros)
        if erros > 5:
            p = progresso if erros == 6 else 1.0
            self._desenhar_linha_progressiva(tela, 
                (base_x + largura_forca + 30, base_y - altura_forca + 140), 
                (base_x + largura_forca + 55, base_y - altura_forca + 180), 
                p, 4)