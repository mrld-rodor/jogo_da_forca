import pygame
import sys

class Popup:
    def __init__(self, largura, altura, fonte_titulo, fonte_texto, cor_fundo, cor_borda, cor_texto):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = fonte_titulo
        self.fonte_texto = fonte_texto
        self.cor_fundo = cor_fundo
        self.cor_borda = cor_borda
        self.cor_texto = cor_texto

    def mostrar(self, tela, titulo, linhas, instrucoes=None):
        popup_x = (tela.get_width() - self.largura) // 2
        popup_y = (tela.get_height() - self.altura) // 2
        popup = pygame.Surface((self.largura, self.altura))
        popup.fill(self.cor_fundo)
        pygame.draw.rect(popup, self.cor_borda, (0, 0, self.largura, self.altura), 4)
        y = 40
        t = self.fonte_titulo.render(titulo, True, self.cor_texto)
        popup.blit(t, (self.largura//2 - t.get_width()//2, y))
        y += 50
        for linha in linhas:
            l = self.fonte_texto.render(linha, True, self.cor_texto)
            popup.blit(l, (self.largura//2 - l.get_width()//2, y))
            y += 40
        if instrucoes:
            i = self.fonte_texto.render(instrucoes, True, self.cor_texto)
            popup.blit(i, (self.largura//2 - i.get_width()//2, self.altura - 60))
        tela.blit(popup, (popup_x, popup_y))
        pygame.display.flip()
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN or evento.type == pygame.QUIT:
                    esperando = False
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

class PopupOpcoes:
    def __init__(self, largura, altura, fonte, cor_fundo, cor_borda, cor_texto, cor_botao, cor_botao_texto):
        self.largura = largura
        self.altura = altura
        self.fonte = fonte
        self.cor_fundo = cor_fundo
        self.cor_borda = cor_borda
        self.cor_texto = cor_texto
        self.cor_botao = cor_botao
        self.cor_botao_texto = cor_botao_texto

    def mostrar(self, tela, sons):
        popup_x = (tela.get_width() - self.largura) // 2
        popup_y = (tela.get_height() - self.altura) // 2
        
        selecionado = 0
        # 0: Vol Efeitos, 1: Mudo Efeitos, 2: Vol Música, 3: Mudo Música, 4: Fechar
        
        esperando = True
        while esperando:
            popup = pygame.Surface((self.largura, self.altura))
            popup.fill(self.cor_fundo)
            pygame.draw.rect(popup, self.cor_borda, (0, 0, self.largura, self.altura), 4)
            
            titulo = self.fonte.render('Opções de Áudio', True, self.cor_texto)
            popup.blit(titulo, (self.largura//2 - titulo.get_width()//2, 20))
            
            # Renderiza as linhas de opções
            y = 80
            espacamento = 45
            
            # 0: Volume Efeitos
            txt_vol_ef = self.fonte.render(f"Volume Efeitos: {int(sons.volume_efeitos * 100)}%", True, self.cor_texto)
            popup.blit(txt_vol_ef, (30, y))
            self._desenhar_slider(popup, 300, y, sons.volume_efeitos, selecionado == 0)
            y += espacamento
            
            # 1: Mudo Efeitos
            txt_mudo_ef = self.fonte.render("Mutar Efeitos Sonoros", True, self.cor_texto)
            popup.blit(txt_mudo_ef, (30, y))
            self._desenhar_checkbox(popup, 300, y, sons.mudo_efeitos, selecionado == 1)
            y += espacamento
            
            # 2: Volume Música
            txt_vol_mus = self.fonte.render(f"Volume Música: {int(sons.volume_musica * 100)}%", True, self.cor_texto)
            popup.blit(txt_vol_mus, (30, y))
            self._desenhar_slider(popup, 300, y, sons.volume_musica, selecionado == 2)
            y += espacamento
            
            # 3: Mudo Música
            txt_mudo_mus = self.fonte.render("Mutar Música de Fundo", True, self.cor_texto)
            popup.blit(txt_mudo_mus, (30, y))
            self._desenhar_checkbox(popup, 300, y, sons.mudo_musica, selecionado == 3)
            y += espacamento + 10
            
            # 4: Fechar
            cor_fechar = self.cor_botao if selecionado == 4 else (180, 180, 180)
            rect_fechar = pygame.Rect((self.largura - 200)//2, y, 200, 40)
            pygame.draw.rect(popup, cor_fechar, rect_fechar, border_radius=8)
            txt_fechar = self.fonte.render("Fechar", True, self.cor_botao_texto if selecionado == 4 else (0,0,0))
            popup.blit(txt_fechar, (rect_fechar.x + (rect_fechar.width-txt_fechar.get_width())//2, rect_fechar.y + (rect_fechar.height-txt_fechar.get_height())//2))
            
            tela.blit(popup, (popup_x, popup_y))
            pygame.display.flip()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        selecionado = (selecionado - 1) % 5
                    elif evento.key == pygame.K_DOWN:
                        selecionado = (selecionado + 1) % 5
                    elif evento.key == pygame.K_ESCAPE or evento.key == pygame.K_SPACE:
                        return None
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if selecionado == 1:
                            sons.mudo_efeitos = not sons.mudo_efeitos
                        elif selecionado == 3:
                            sons.mudo_musica = not sons.mudo_musica
                            sons.atualizar_volumes()
                        elif selecionado == 4:
                            return None
                    elif evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        passo = -0.05 if evento.key == pygame.K_LEFT else 0.05
                        if selecionado == 0 and not sons.mudo_efeitos:
                            sons.volume_efeitos = max(0.0, min(1.0, sons.volume_efeitos + passo))
                        elif selecionado == 2 and not sons.mudo_musica:
                            sons.volume_musica = max(0.0, min(1.0, sons.volume_musica + passo))
                            sons.atualizar_volumes()
                            
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = evento.pos[0] - popup_x, evento.pos[1] - popup_y
                    if 300 <= mx <= 500:
                        # Checa cliques nas barras de volume (Y aproximado)
                        if 70 <= my <= 90: # Slider Efeitos
                            sons.volume_efeitos = max(0.0, min(1.0, (mx - 300) / 200))
                        elif 160 <= my <= 180: # Slider Música
                            sons.volume_musica = max(0.0, min(1.0, (mx - 300) / 200))
                            sons.atualizar_volumes()

    def _desenhar_slider(self, surf, x, y, valor, selecionado):
        largura_barra = 200
        altura_barra = 10
        # Fundo da barra
        pygame.draw.rect(surf, (200, 200, 200), (x, y + 5, largura_barra, altura_barra), border_radius=5)
        # Preenchimento
        largura_preenchida = int(largura_barra * valor)
        pygame.draw.rect(surf, (0, 150, 255) if not selecionado else (0, 200, 255), (x, y + 5, largura_preenchida, altura_barra), border_radius=5)
        # Bolinha
        pygame.draw.circle(surf, (0, 100, 200), (x + largura_preenchida, y + 10), 8 if selecionado else 6)

    def _desenhar_checkbox(self, surf, x, y, marcado, selecionado):
        rect = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(surf, (200, 200, 200), rect, border_radius=4)
        pygame.draw.rect(surf, (0, 150, 255) if not selecionado else (0, 200, 255), rect, 2 if selecionado else 1, border_radius=4)
        if marcado:
            pygame.draw.line(surf, (0, 100, 200), (x+4, y+10), (x+8, y+15), 3)
            pygame.draw.line(surf, (0, 100, 200), (x+8, y+15), (x+16, y+4), 3)  