# ui/popup.py
import pygame
from config import carregar_imagem, PRETO, BRANCO

# -----------------------------------------------------------------
# CLASSE BASE POPUP
# -----------------------------------------------------------------
class Popup:
    def __init__(self, largura, altura, fonte, fonte_pequena,
                 cor_fundo, cor_texto, cor_borda=None):
        self.largura = largura
        self.altura = altura
        self.fonte = fonte
        self.fonte_pequena = fonte_pequena
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.cor_borda = cor_borda

    def mostrar(self, tela, titulo, linhas, rodape):
        overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        rodando = True

        while rodando:
            tela.blit(overlay, (0, 0))
            rect = pygame.Rect(0, 0, self.largura, self.altura)
            rect.center = tela.get_rect().center
            pygame.draw.rect(tela, self.cor_fundo, rect, border_radius=16)
            if self.cor_borda:
                pygame.draw.rect(tela, self.cor_borda, rect, width=4, border_radius=16)

            y = rect.y + 30
            if titulo:
                txt = self.fonte.render(titulo, True, self.cor_texto)
                tela.blit(txt, (rect.centerx - txt.get_width() // 2, y))
                y += txt.get_height() + 20

            for linha in linhas:
                txt = self.fonte_pequena.render(linha, True, self.cor_texto)
                tela.blit(txt, (rect.centerx - txt.get_width() // 2, y))
                y += txt.get_height() + 8

            txt_rodape = self.fonte_pequena.render(rodape, True, self.cor_texto)
            tela.blit(txt_rodape,
                      (rect.centerx - txt_rodape.get_width() // 2,
                       rect.bottom - txt_rodape.get_height() - 20))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys; sys.exit()
                if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    rodando = False


# -----------------------------------------------------------------
# COMPONENTE: SLIDER
# -----------------------------------------------------------------
class Slider:
    def __init__(self, rect, valor_inicial=1.0):
        self.rect = rect
        self.valor = max(0.0, min(1.0, valor_inicial))
        self.arrastando = False
        self.radius = rect.height // 2

        self.img_bg = None
        self.img_fill = None
        self.img_knob_norm = None
        self.img_knob_press = None

    def definir_imagens(self, img_bg, img_fill, img_knob_norm, img_knob_press):
        self.img_bg = img_bg
        self.img_fill = img_fill
        self.img_knob_norm = img_knob_norm
        self.img_knob_press = img_knob_press

    def _knob_center(self):
        return (self.rect.x + int(self.rect.width * self.valor),
                self.rect.centery)

    def desenhar(self, tela):
        if self.img_bg:
            tela.blit(self.img_bg, self.rect)
        else:
            pygame.draw.rect(tela, (220, 220, 220), self.rect, border_radius=self.radius)

        largura_fill = int(self.rect.width * self.valor)
        if largura_fill > 0:
            if self.img_fill:
                fill_img = pygame.transform.smoothscale(self.img_fill, (self.rect.width, self.rect.height))
                tela.blit(fill_img, self.rect, area=pygame.Rect(0, 0, largura_fill, self.rect.height))
            else:
                pygame.draw.rect(tela, (100, 200, 100),
                                 (self.rect.x, self.rect.y, largura_fill, self.rect.height),
                                 border_radius=self.radius)

        knob_img = self.img_knob_press if self.arrastando else self.img_knob_norm
        if knob_img:
            kx, ky = self._knob_center()
            tela.blit(knob_img, (kx - knob_img.get_width() // 2,
                                 ky - knob_img.get_height() // 2))

    def processar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            area_clique = self.rect.inflate(0, 20)
            if area_clique.collidepoint(evento.pos):
                self.arrastando = True
                self._atualizar_por_mouse(evento.pos[0])
                return True
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.arrastando:
                self.arrastando = False
                return True
        elif evento.type == pygame.MOUSEMOTION and self.arrastando:
            self._atualizar_por_mouse(evento.pos[0])
            return True
        return False

    def _atualizar_por_mouse(self, mouse_x):
        x_rel = mouse_x - self.rect.x
        self.valor = max(0.0, min(1.0, x_rel / self.rect.width))


# -----------------------------------------------------------------
# POPUP: OPÇÕES DE ÁUDIO (com botões 144x144)
# -----------------------------------------------------------------
class PopupOpcoes:
    def __init__(self, largura, altura, fonte_titulo, fonte_texto):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = fonte_titulo
        self.fonte_texto = fonte_texto

        self.painel = carregar_imagem('ui/panel_medium.png', (largura, altura))

        # Botões 144x144
        self.btn_fechar_size = (144, 144)
        self.img_fechar_norm = carregar_imagem('buttons/btn_round_close_normal.png', self.btn_fechar_size)
        self.img_fechar_press = carregar_imagem('buttons/btn_round_close_pressed.png', self.btn_fechar_size)
        self.btn_fechar_rect = None

        # Sliders
        bar_w = int(largura * 0.55) # Ligeiramente mais estreito para caber com botões grandes
        bar_h = 30
        self.slider_musica = Slider(pygame.Rect(0, 0, bar_w, bar_h))
        self.slider_efeitos = Slider(pygame.Rect(0, 0, bar_w, bar_h))

        img_bg = carregar_imagem('ui/bar_bg.png', (bar_w, bar_h))
        img_fill = carregar_imagem('ui/bar_fill.png', (bar_w, bar_h))
        
        # Knob do slider (um pouco maior também)
        knob_size = (48, 48)
        img_knob_norm = carregar_imagem('buttons/btn_round_sound_normal.png', knob_size)
        img_knob_press = carregar_imagem('buttons/btn_round_sound_pressed.png', knob_size)
        for s in (self.slider_musica, self.slider_efeitos):
            s.definir_imagens(img_bg, img_fill, img_knob_norm, img_knob_press)

        # Botões de mute (144x144)
        self.img_mute_on = carregar_imagem('buttons/btn_round_mute_normal.png', self.btn_fechar_size)
        self.img_mute_off = carregar_imagem('buttons/btn_round_sound_normal.png', self.btn_fechar_size)

        self.btn_mute_musica_rect = None
        self.btn_mute_efeitos_rect = None

        self._vol_musica_antes = 1.0
        self._vol_efeitos_antes = 1.0

    def mostrar(self, tela, sons):
        overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        rodando = True

        self.slider_musica.valor = sons.get_volume_musica()
        self.slider_efeitos.valor = sons.get_volume_efeitos()

        while rodando:
            tela.blit(overlay, (0, 0))
            rect = self.painel.get_rect(center=tela.get_rect().center)
            tela.blit(self.painel, rect)

            # Botão fechar (canto superior direito)
            bw, bh = self.btn_fechar_size
            margem = 20
            self.btn_fechar_rect = pygame.Rect(rect.right - bw - margem, rect.top + margem, bw, bh)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            img_fechar = (self.img_fechar_press if self.btn_fechar_rect.collidepoint(mouse_pos) and mouse_pressed else self.img_fechar_norm)
            tela.blit(img_fechar, self.btn_fechar_rect)

            # Título
            txt_titulo = self.fonte_titulo.render("Opções de Áudio", True, PRETO)
            tela.blit(txt_titulo, (rect.centerx - txt_titulo.get_width() // 2, rect.y + 40))

            # Layout dos sliders
            slider_x = rect.centerx - self.slider_musica.rect.width // 2
            slider_y_musica = rect.y + int(rect.height * 0.30)
            slider_y_efeitos = rect.y + int(rect.height * 0.60)

            self.slider_musica.rect.topleft = (slider_x, slider_y_musica)
            self.slider_efeitos.rect.topleft = (slider_x, slider_y_efeitos)

            lbl_musica = self.fonte_texto.render("Música", True, PRETO)
            tela.blit(lbl_musica, (slider_x, slider_y_musica - 40))
            lbl_efeitos = self.fonte_texto.render("Efeitos Sonoros", True, PRETO)
            tela.blit(lbl_efeitos, (slider_x, slider_y_efeitos - 40))

            txt_mus = self.fonte_texto.render(f"{int(self.slider_musica.valor * 100)}%", True, PRETO)
            tela.blit(txt_mus, (slider_x + self.slider_musica.rect.width + 20, slider_y_musica - 8))
            txt_ef = self.fonte_texto.render(f"{int(self.slider_efeitos.valor * 100)}%", True, PRETO)
            tela.blit(txt_ef, (slider_x + self.slider_efeitos.rect.width + 20, slider_y_efeitos - 8))

            self.slider_musica.desenhar(tela)
            self.slider_efeitos.desenhar(tela)

            # Botões Mute (alinhados à esquerda, simétricos aos sliders)
            icone_w, icone_h = self.img_mute_on.get_size()
            self.btn_mute_musica_rect = pygame.Rect(slider_x - icone_w - 30, slider_y_musica + (self.slider_musica.rect.height - icone_h) // 2, icone_w, icone_h)
            self.btn_mute_efeitos_rect = pygame.Rect(slider_x - icone_w - 30, slider_y_efeitos + (self.slider_efeitos.rect.height - icone_h) // 2, icone_w, icone_h)

            img_mute_mus = self.img_mute_on if self.slider_musica.valor == 0 else self.img_mute_off
            img_mute_ef = self.img_mute_on if self.slider_efeitos.valor == 0 else self.img_mute_off
            tela.blit(img_mute_mus, self.btn_mute_musica_rect)
            tela.blit(img_mute_ef, self.btn_mute_efeitos_rect)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys; sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.btn_fechar_rect.collidepoint(evento.pos):
                        rodando = False
                        break
                    if self.btn_mute_musica_rect.collidepoint(evento.pos):
                        if self.slider_musica.valor > 0:
                            self._vol_musica_antes = self.slider_musica.valor
                            self.slider_musica.valor = 0.0
                        else:
                            self.slider_musica.valor = self._vol_musica_antes or 0.5
                        sons.set_volume_musica(self.slider_musica.valor)

                    if self.btn_mute_efeitos_rect.collidepoint(evento.pos):
                        if self.slider_efeitos.valor > 0:
                            self._vol_efeitos_antes = self.slider_efeitos.valor
                            self.slider_efeitos.valor = 0.0
                        else:
                            self.slider_efeitos.valor = self._vol_efeitos_antes or 0.5
                        sons.set_volume_efeitos(self.slider_efeitos.valor)

                if self.slider_musica.processar_evento(evento):
                    sons.set_volume_musica(self.slider_musica.valor)
                if self.slider_efeitos.processar_evento(evento):
                    sons.set_volume_efeitos(self.slider_efeitos.valor)


# -----------------------------------------------------------------
# POPUP: REGRAS (com botão fechar 144x144)
# -----------------------------------------------------------------
class PopupRegras:
    def __init__(self, largura, altura, fonte_titulo, fonte_texto):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = fonte_titulo
        self.fonte_texto = fonte_texto
        self.painel = carregar_imagem('ui/panel_large.png', (largura, altura))

        btn_w, btn_h = 144, 144
        self.btn_fechar_size = (btn_w, btn_h)
        self.img_fechar_norm = carregar_imagem('buttons/btn_round_close_normal.png', (btn_w, btn_h))
        self.img_fechar_press = carregar_imagem('buttons/btn_round_close_pressed.png', (btn_w, btn_h))
        self.btn_fechar_rect = None

    def _quebrar_texto(self, texto, fonte, largura_max):
        palavras = texto.split()
        linhas = []
        linha_atual = ""
        for p in palavras:
            teste = (linha_atual + " " + p).strip()
            if fonte.size(teste)[0] <= largura_max:
                linha_atual = teste
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = p
        if linha_atual:
            linhas.append(linha_atual)
        return linhas

    def mostrar(self, tela):
        overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        rodando = True

        regras = [
            ("Como jogar:", True),
            ("• Descubra a palavra secreta antes de ser enforcado.", False),
            ("• Você tem até 6 erros permitidos.", False),
            ("• Digite uma letra por vez usando o teclado.", False),
            ("• Letras corretas aparecem na palavra.", False),
            ("• Letras erradas desenham o boneco na forca.", False),
            ("• Pressione Espaço durante a partida para abrir opções.", False),
            ("• Pressione R após o fim para jogar novamente.", False),
            ("", False),
            ("Dicas:", True),
            ("• Durante a partida você pode pedir até 2 dicas.", False),
            ("• Cada dica revela uma letra da palavra secreta.", False),
            ("• As dicas são limitadas: use com sabedoria!", False),
            ("", False),
            ("Boa sorte e divirta-se!", True),
        ]

        while rodando:
            tela.blit(overlay, (0, 0))
            rect = self.painel.get_rect(center=tela.get_rect().center)
            tela.blit(self.painel, rect)

            bw, bh = self.btn_fechar_size
            margem = 20
            self.btn_fechar_rect = pygame.Rect(rect.right - bw - margem, rect.top + margem, bw, bh)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if (self.btn_fechar_rect.collidepoint(mouse_pos) and mouse_pressed):
                img_fechar = self.img_fechar_press
            else:
                img_fechar = self.img_fechar_norm
            tela.blit(img_fechar, self.btn_fechar_rect)

            margem_texto = 60
            x_texto = rect.x + margem_texto
            largura_texto = rect.width - 2 * margem_texto
            y = rect.y + 50

            for item, destaque in regras:
                if item == "":
                    y += 12
                    continue
                fonte = self.fonte_titulo if destaque else self.fonte_texto
                cor = PRETO
                for linha in self._quebrar_texto(item, fonte, largura_texto):
                    txt = fonte.render(linha, True, cor)
                    tela.blit(txt, (x_texto, y))
                    y += txt.get_height() + 4

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys; sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.btn_fechar_rect and self.btn_fechar_rect.collidepoint(evento.pos):
                        rodando = False


# -----------------------------------------------------------------
# POPUP: DIFICULDADE (com botão fechar 144x144)
# -----------------------------------------------------------------
class PopupDificuldade:
    def __init__(self, largura, altura, fonte_titulo, fonte_botao):
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = fonte_titulo
        self.fonte_botao = fonte_botao

        self.painel = carregar_imagem('ui/panel_medium.png', (largura, altura))
        self.titulo = "Escolha a Dificuldade"

        btn_w, btn_h = 144, 144
        self.btn_fechar_size = (btn_w, btn_h)
        self.img_fechar_norm = carregar_imagem('buttons/btn_round_close_normal.png', (btn_w, btn_h))
        self.img_fechar_press = carregar_imagem('buttons/btn_round_close_pressed.png', (btn_w, btn_h))
        self.btn_fechar_rect = None

        self.opcoes = [
            ("Fácil",   "green",  (255, 255, 255)),
            ("Normal",  "white",  (0, 0, 0)),
            ("Difícil", "pink",   (255, 255, 255)),
            ("Secreta", "white",  (0, 0, 0)),
        ]

        btn_largura = int(largura * 0.7)
        btn_altura = int(altura * 0.15)
        espaco = int(altura * 0.05)
        self.btn_largura = btn_largura
        self.btn_altura = btn_altura
        self.espaco = espaco

        self.imagens_botoes = {}
        for cor in set(c for _, c, _ in self.opcoes):
            self.imagens_botoes[cor] = {
                'normal':  carregar_imagem(f'buttons/btn_{cor}_normal.png',  (btn_largura, btn_altura)),
                'hover':   carregar_imagem(f'buttons/btn_{cor}_hover.png',   (btn_largura, btn_altura)),
                'pressed': carregar_imagem(f'buttons/btn_{cor}_pressed.png', (btn_largura, btn_altura)),
            }

        self.rects_botoes = []

    def mostrar(self, tela, sons=None):
        overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        rodando = True
        escolha = None

        while rodando:
            tela.blit(overlay, (0, 0))
            rect = self.painel.get_rect(center=tela.get_rect().center)
            tela.blit(self.painel, rect)

            bw, bh = self.btn_fechar_size
            margem = 20
            self.btn_fechar_rect = pygame.Rect(rect.right - bw - margem, rect.top + margem, bw, bh)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            img_fechar = (self.img_fechar_press if self.btn_fechar_rect.collidepoint(mouse_pos) and mouse_pressed else self.img_fechar_norm)
            tela.blit(img_fechar, self.btn_fechar_rect)

            txt_titulo = self.fonte_titulo.render(self.titulo, True, PRETO)
            tela.blit(txt_titulo, (rect.centerx - txt_titulo.get_width() // 2, rect.y + int(rect.height * 0.08)))

            self.rects_botoes = []
            total_altura = (len(self.opcoes) * self.btn_altura + (len(self.opcoes) - 1) * self.espaco)
            y_inicial = rect.y + (rect.height - total_altura) // 2 + int(rect.height * 0.05)

            for i, (nome, cor, cor_texto) in enumerate(self.opcoes):
                bx = rect.centerx - self.btn_largura // 2
                by = y_inicial + i * (self.btn_altura + self.espaco)
                rect_botao = pygame.Rect(bx, by, self.btn_largura, self.btn_altura)
                self.rects_botoes.append(rect_botao)

                imgs = self.imagens_botoes[cor]
                if rect_botao.collidepoint(mouse_pos):
                    img = imgs['pressed'] if mouse_pressed else imgs['hover']
                else:
                    img = imgs['normal']
                tela.blit(img, rect_botao)

                txt = self.fonte_botao.render(nome, True, cor_texto)
                tela.blit(txt, (rect_botao.centerx - txt.get_width() // 2, rect_botao.centery - txt.get_height() // 2))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    import sys; sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.btn_fechar_rect and self.btn_fechar_rect.collidepoint(evento.pos):
                        rodando = False
                        break
                    for i, rect_botao in enumerate(self.rects_botoes):
                        if rect_botao.collidepoint(evento.pos):
                            escolha = self.opcoes[i][0]
                            rodando = False
                            break

        return escolha