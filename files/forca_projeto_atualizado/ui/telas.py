# ui/telas.py
import pygame
from config import carregar_imagem

class BotaoMenu:
    """Botão com imagem e estados normal/hover/pressed."""
    def __init__(self, rect, img_normal, img_hover, img_pressed, texto,
                 fonte, cor_texto=(0, 0, 0), cor_sombra=(255, 255, 255)):
        self.rect = rect
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.img_pressed = img_pressed
        self.texto = texto
        self.fonte = fonte
        self.cor_texto = cor_texto
        self.cor_sombra = cor_sombra

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            img = self.img_pressed if mouse_pressed else self.img_hover
        else:
            img = self.img_normal

        tela.blit(img, self.rect)

        # Texto com sombra (offset) para combinar com o estilo
        txt_sombra = self.fonte.render(self.texto, True, self.cor_sombra)
        txt = self.fonte.render(self.texto, True, self.cor_texto)
        cx = self.rect.x + (self.rect.width - txt.get_width()) // 2
        cy = self.rect.y + (self.rect.height - txt.get_height()) // 2
        tela.blit(txt_sombra, (cx + 2, cy + 2))
        tela.blit(txt, (cx, cy))

    def clicado(self, evento):
        return (evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
                and self.rect.collidepoint(evento.pos))


class TelaInicio:
    """Tela inicial com temática de caderno."""

    def __init__(self, largura, altura, fonte_pequena):
        self.largura = largura
        self.altura = altura
        self.fonte = fonte_pequena

        # ---------------- Carregar assets ----------------
        # Fundo
        self.bg = carregar_imagem('backgrounds/bg_menu.png', (largura, altura))

        # Painel do caderno (ocupa ~85% da tela)
        painel_w = int(largura * 0.85)
        painel_h = int(altura * 0.85)
        self.painel = carregar_imagem('ui/panel_large.png', (painel_w, painel_h))
        self.painel_rect = self.painel.get_rect(center=(largura // 2, altura // 2))

        # Lombada (faixa central do caderno)
        self.lombada = carregar_imagem('ui/panel_spine.png', (60, painel_h))
        self.lombada_rect = self.lombada.get_rect(
            midleft=(self.painel_rect.centerx - 30, self.painel_rect.centery)
        )

        # Logo no canto superior esquerdo do painel
        self.logo = carregar_imagem('ui/logo_forca.png', (int(painel_w * 0.42), int(painel_h * 0.18)))
        self.logo_pos = (self.painel_rect.x + int(painel_w * 0.05),
                         self.painel_rect.y + int(painel_h * 0.08))

        # Forca (estágio 3 para dar um visual simpático)
        self.forca = carregar_imagem('hangman/stage_3.png', (int(painel_w * 0.28), int(painel_h * 0.45)))
        self.forca_pos = (self.painel_rect.x + int(painel_w * 0.08),
                          self.painel_rect.y + int(painel_h * 0.35))

        # Lápis e borracha decorativos
        self.pencil = carregar_imagem('decor/pencil.png', (int(painel_w * 0.18), int(painel_h * 0.25)))
        self.pencil_pos = (self.painel_rect.right - int(painel_w * 0.14),
                           self.painel_rect.y - int(painel_h * 0.06))

        self.eraser = carregar_imagem('decor/eraser.png', (int(painel_w * 0.10), int(painel_h * 0.14)))
        self.eraser_pos = (self.painel_rect.right - int(painel_w * 0.18),
                           self.painel_rect.bottom - int(painel_h * 0.05))

        # ---------------- Botões ----------------
        # Largura e altura dos botões do menu
        btn_w = int(painel_w * 0.32)
        btn_h = int(painel_h * 0.13)

        # Posição X: centro da metade direita do painel
        btn_x = self.painel_rect.centerx + int(painel_w * 0.06)
        # Posição Y inicial
        btn_y_start = self.painel_rect.y + int(painel_h * 0.25)
        espaco = int(painel_h * 0.17)

        # Botão JOGAR (amarelo)
        rect_jogar = pygame.Rect(btn_x, btn_y_start, btn_w, btn_h)
        self.btn_jogar = BotaoMenu(
            rect_jogar,
            carregar_imagem('buttons/btn_yellow_normal.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_yellow_hover.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_yellow_pressed.png', (btn_w, btn_h)),
            "JOGAR", self.fonte, cor_texto=(0, 0, 0), cor_sombra=(255, 255, 255)
        )

        # Botão OPÇÕES (branco)
        rect_opcoes = pygame.Rect(btn_x, btn_y_start + espaco, btn_w, btn_h)
        self.btn_opcoes = BotaoMenu(
            rect_opcoes,
            carregar_imagem('buttons/btn_white_normal.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_white_hover.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_white_pressed.png', (btn_w, btn_h)),
            "Opções", self.fonte, cor_texto=(0, 0, 0), cor_sombra=(255, 255, 255)
        )

        # Botão REGRAS (branco) — substitui o antigo Ranking
        rect_regras = pygame.Rect(btn_x, btn_y_start + 2 * espaco, btn_w, btn_h)
        self.btn_regras = BotaoMenu(
            rect_regras,
            carregar_imagem('buttons/btn_white_normal.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_white_hover.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_white_pressed.png', (btn_w, btn_h)),
            "Regras", self.fonte, cor_texto=(0, 0, 0), cor_sombra=(255, 255, 255)
)

        # Botão SAIR (rosa)
        rect_sair = pygame.Rect(btn_x, btn_y_start + 3 * espaco, btn_w, btn_h)
        self.btn_sair = BotaoMenu(
            rect_sair,
            carregar_imagem('buttons/btn_pink_normal.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_pink_hover.png', (btn_w, btn_h)),
            carregar_imagem('buttons/btn_pink_pressed.png', (btn_w, btn_h)),
            "Sair", self.fonte, cor_texto=(255, 255, 255), cor_sombra=(0, 0, 0)
        )

        self.botoes = [self.btn_jogar, self.btn_opcoes, self.btn_regras, self.btn_sair]

    # ------------------------------------------------------------
    def desenhar(self, tela):
        """Desenha toda a tela inicial."""
        # Fundo
        tela.blit(self.bg, (0, 0))

        # Painel do caderno
        tela.blit(self.painel, self.painel_rect)

        # Lombada
        tela.blit(self.lombada, self.lombada_rect)

        # Logo
        tela.blit(self.logo, self.logo_pos)

        # Forca
        tela.blit(self.forca, self.forca_pos)

        # Decorações
        tela.blit(self.pencil, self.pencil_pos)
        tela.blit(self.eraser, self.eraser_pos)

        # Botões
        for botao in self.botoes:
            botao.desenhar(tela)

    # ------------------------------------------------------------
    def processar_evento(self, evento):
        """
        Verifica cliques nos botões.
        Retorna uma string com a ação: 'jogar', 'opcoes', 'ranking', 'sair' ou None.
        """
        if self.btn_jogar.clicado(evento):
            return 'jogar'
        if self.btn_opcoes.clicado(evento):
            return 'opcoes'
        if self.btn_regras.clicado(evento):
            return 'regras'
        if self.btn_sair.clicado(evento):
            return 'sair'
        return None