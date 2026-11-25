# forca_pygame.py
import pygame
import sys
import random
import os

from palavras import BANCO_PALAVRAS
from jogo_forca import JogoForca
from ui.telas import TelaInicio
from ui.popup import Popup, PopupOpcoes, PopupRegras, PopupDificuldade
from config import (
    BRANCO, PRETO, VERMELHO, VERDE, CINZA_MEDIO,
    get_fontes, get_layout, carregar_imagem
)
from ui.efeitos import gradiente_animado, efeito_flashes
from ui.forca import ForcaDesenhavel
from ui.sons import GerenciadorSons

pygame.init()
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h
flags = pygame.FULLSCREEN

tela = pygame.display.set_mode((LARGURA, ALTURA), flags)
pygame.display.set_caption('Jogo da Forca - Pygame')
fonte, fonte_pequena, fonte_popup, fonte_pequena_popup = get_fontes()

bg_game = carregar_imagem('backgrounds/bg_game.png', (LARGURA, ALTURA))

layout = get_layout(LARGURA, ALTURA)
forca_ui = ForcaDesenhavel(LARGURA, ALTURA, altura_alvo=layout['altura_forca'])
forca_ui.definir_centro(layout['x_forca_centro'], layout['y_forca_centro'])

sons = GerenciadorSons()
sons.iniciar_musica()


class BotaoIcone:
    def __init__(self, centro, tamanho, icon_path):
        self.centro = centro
        self.tamanho = tamanho
        self.img_icon = carregar_imagem(icon_path, tamanho)
        self.raio = max(tamanho) // 2 + 10
        self.rect = pygame.Rect(0, 0, *tamanho)
        self.rect.center = centro
        self.cor_hover = (255, 255, 200, 160)
        self.cor_press = (255, 220, 120, 220)

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        hover = self.rect.collidepoint(mouse_pos)

        if hover:
            surf = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
            cor = self.cor_press if mouse_pressed else self.cor_hover
            pygame.draw.circle(surf, cor, (self.raio, self.raio), self.raio)
            tela.blit(surf, (self.rect.centerx - self.raio, self.rect.centery - self.raio))

        tela.blit(self.img_icon, self.rect)

    def clicado(self, evento):
        return (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.rect.collidepoint(evento.pos))


def mostrar_creditos() -> None:
    popup = Popup(1000, 500, fonte_pequena_popup, fonte_pequena_popup, (240, 240, 240), PRETO, PRETO)
    linhas = [
        'Desenvolvido por:', 'Amiraldo Almeida',
        'Python 3 + pygame', 'Jogo da Forca - 2025',
        'Objetivo:', 'Descubra a palavra secreta antes de ser enforcado!'
    ]
    popup.mostrar(tela, '', linhas, 'Pressione qualquer tecla para fechar')


def mostrar_opcoes() -> None:
    popup = PopupOpcoes(int(LARGURA * 0.70), int(ALTURA * 0.85), fonte_popup, fonte_pequena_popup)
    popup.mostrar(tela, sons)


def tela_inicio() -> str:
    tela_inicio_ui = TelaInicio(LARGURA, ALTURA, fonte_pequena)
    mapa_dificuldade = {'Fácil': 'facil', 'Normal': 'normal', 'Difícil': 'dificil', 'Secreta': 'secreta'}

    while True:
        tela_inicio_ui.desenhar(tela)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            acao = tela_inicio_ui.processar_evento(evento)

            if acao == 'jogar':
                popup_dif = PopupDificuldade(int(LARGURA * 0.60), int(ALTURA * 0.80), fonte_popup, fonte_pequena_popup)
                escolha = popup_dif.mostrar(tela)
                if escolha in mapa_dificuldade:
                    return mapa_dificuldade[escolha]
            elif acao == 'opcoes':
                mostrar_opcoes()
            elif acao == 'regras':
                popup_regras = PopupRegras(int(LARGURA * 0.75), int(ALTURA * 0.75), fonte_popup, fonte_pequena_popup)
                popup_regras.mostrar(tela)
            elif acao == 'sair':
                pygame.quit()
                sys.exit()


def tela_abertura() -> None:
    tempo_inicial = pygame.time.get_ticks()
    duracao_efeito = 2200
    duracao_titulo = 1200
    rodando = True
    efeito_finalizado = False
    titulo_str = 'Jogo da Forca'
    letras_titulo = list(titulo_str)
    letras_mostradas = 0
    tempo_letra = 80
    flashes = []
    grad_y = 0
    while rodando:
        gradiente_animado(tela, LARGURA, ALTURA, grad_y)
        grad_y += 2
        tempo_atual = pygame.time.get_ticks() - tempo_inicial
        if random.random() < 0.08:
            flashes.append((random.randint(0, LARGURA), random.randint(0, ALTURA), random.randint(32, 64)))
        flashes = efeito_flashes(tela, flashes)
        if tempo_atual < duracao_efeito:
            letras_mostradas = min(len(letras_titulo), int(tempo_atual / tempo_letra))
            titulo = ''.join(letras_titulo[:letras_mostradas])
            texto = fonte.render(titulo, True, VERMELHO)
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
        else:
            if not efeito_finalizado:
                efeito_finalizado = True
                tempo_titulo = pygame.time.get_ticks()
            texto = fonte.render(titulo_str, True, VERMELHO)
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
            if pygame.time.get_ticks() - tempo_titulo > duracao_titulo:
                rodando = False
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                rodando = False


class JogoForcaApp:
    def __init__(self) -> None:
        self.tela = tela
        self.largura = LARGURA
        self.altura = ALTURA
        self.fonte = fonte
        self.fonte_pequena = fonte_pequena
        self.forca_ui = forca_ui
        self.layout = layout

        tamanho_icone = (70, 70) 
        x_hud = self.layout['hud_x_dir'] 
        
        self.btn_dica = BotaoIcone(
            centro=(x_hud, self.layout['hud_y_base']),
            tamanho=tamanho_icone,
            icon_path=os.path.join('icons', 'icon_hint.png')
        )
        self.btn_opcoes_hud = BotaoIcone(
            centro=(x_hud, self.layout['hud_y_topo']),
            tamanho=tamanho_icone,
            icon_path=os.path.join('icons', 'icon_gear.png')
        )

    def _desenhar_palavra(self, jogo):
        layout = self.layout
        letras = jogo.palavra_atual()
        n = len(letras)

        # --- LÓGICA DE REDIMENSIONAMENTO INTELIGENTE ---
        # Define o espaço máximo que a palavra pode ocupar (do meio da tela até a borda direita)
        largura_maxima = layout['x_palavra_max'] - layout['x_palavra_min']
        
        # Tenta usar o tamanho de fonte padrão (72)
        tamanho_fonte = 72
        espaco_letras = 20
        
        while True:
            fonte_teste = pygame.font.Font(os.path.join(os.path.dirname(__file__), "forca_assets", "fonts", "Poppins-Bold.ttf"), tamanho_fonte)
            larguras = [max(fonte_teste.size(l)[0], 40) for l in letras]
            largura_total = sum(larguras) + espaco_letras * (n - 1)
            
            # Se couber no espaço máximo, paramos
            if largura_total <= largura_maxima:
                break
            
            # Se não couber, diminuímos a fonte e o espaçamento
            tamanho_fonte -= 4
            espaco_letras = max(5, espaco_letras - 2)
            
            # Limite de segurança para não ficar ilegível
            if tamanho_fonte < 24:
                break
        
        fonte_final = pygame.font.Font(os.path.join(os.path.dirname(__file__), "forca_assets", "fonts", "Poppins-Bold.ttf"), tamanho_fonte)
        
        # Recalcula com a fonte final
        larguras = [max(fonte_final.size(l)[0], 30) for l in letras]
        largura_total = sum(larguras) + espaco_letras * (n - 1)
        
        # CENTRALIZAÇÃO EXATA: 
        # O centro será o próprio centro da zona de texto, limitado para não invadir o botão de opções.
        x_inicio = layout['x_textos_centro'] - largura_total // 2
        y_base = layout['y_palavra']

        x = x_inicio
        for i, letra in enumerate(letras):
            # Desenha a letra se já foi descoberta
            if letra != '_':
                texto = fonte_final.render(letra, True, PRETO)
                tela.blit(texto, (x + (larguras[i] - texto.get_width()) // 2, y_base - texto.get_height() + 10))
            
            # Desenha o traço
            linha_y = y_base + 20
            pygame.draw.line(tela, PRETO, (x, linha_y), (x + larguras[i], linha_y), 4)
            x += larguras[i] + espaco_letras

    def _desenhar_hud(self, jogo, fim):
        # 1. Botão de Opções (Topo Direito)
        self.btn_opcoes_hud.desenhar(self.tela)
        txt_op = self.fonte_pequena.render("Opções", True, PRETO)
        
        pos_x_op = self.btn_opcoes_hud.rect.left - txt_op.get_width() - 15
        pos_y_op = self.btn_opcoes_hud.rect.centery - txt_op.get_height() // 2
        tela.blit(txt_op, (pos_x_op, pos_y_op))

        # 2. Botão de Dica (Base Direita)
        if not fim:
            self.btn_dica.desenhar(self.tela)
            
            txt_dica = self.fonte_pequena.render("Dica", True, PRETO)
            txt_contador = self.fonte_pequena.render(f'{jogo.dicas_usadas}/{jogo.max_dicas}', True, PRETO)
            
            pos_x_dica = self.btn_dica.rect.left - txt_dica.get_width() - 15
            pos_x_cont = self.btn_dica.rect.left - txt_contador.get_width() - 15
            
            centro_y = self.btn_dica.rect.centery
            
            tela.blit(txt_dica, (pos_x_dica, centro_y - txt_dica.get_height() - 2))
            tela.blit(txt_contador, (pos_x_cont, centro_y + 2))

    def rodar(self) -> None:
        tela_abertura()
        while True:
            dificuldade = tela_inicio()
            jogo = JogoForca(BANCO_PALAVRAS, dificuldade)
            fim = False
            aviso = ''
            som_fim_tocado = False

            while True:
                tela.blit(bg_game, (0, 0))
                layout = self.layout

                self.forca_ui.desenhar(tela, jogo.erros)
                self._desenhar_palavra(jogo)

                letras_str = ' '.join(jogo.letras_usadas()) if jogo.letras_usadas() else '—'
                texto_usadas = self.fonte_pequena.render(f'Letras usadas: {letras_str}', True, PRETO)
                tela.blit(texto_usadas, (layout['x_textos_centro'] - texto_usadas.get_width() // 2, layout['y_letras']))

                if not fim:
                    texto_input = self.fonte_pequena.render('Digite uma letra:', True, PRETO)
                    tela.blit(texto_input, (layout['x_textos_centro'] - texto_input.get_width() // 2, layout['y_input']))
                    
                    if aviso:
                        texto_aviso = self.fonte_pequena.render(aviso, True, VERMELHO)
                        tela.blit(texto_aviso, (layout['x_textos_centro'] - texto_aviso.get_width() // 2, layout['y_aviso']))

                if jogo.venceu():
                    if not som_fim_tocado:
                        sons.tocar('vitoria')
                        som_fim_tocado = True
                    fim = True
                elif jogo.perdeu():
                    if not som_fim_tocado:
                        sons.tocar('derrota')
                        som_fim_tocado = True
                    fim = True

                if fim:
                    msg = 'Parabéns! Você venceu!' if jogo.venceu() else f'Você perdeu! Palavra: {jogo.get_palavra()}'
                    cor_msg = VERDE if jogo.venceu() else VERMELHO
                    txt_msg = self.fonte_pequena.render(msg, True, cor_msg)
                    tela.blit(txt_msg, (layout['x_textos_centro'] - txt_msg.get_width() // 2, layout['y_input']))
                    
                    txt_restart = self.fonte_pequena.render('Clique para jogar novamente', True, PRETO)
                    tela.blit(txt_restart, (layout['x_textos_centro'] - txt_restart.get_width() // 2, layout['y_aviso']))

                self._desenhar_hud(jogo, fim)
                pygame.display.flip()

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if evento.type == pygame.KEYDOWN:
                        if not fim:
                            if evento.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                            elif pygame.K_a <= evento.key <= pygame.K_z:
                                letra = chr(evento.key).upper()
                                if letra in jogo.letras_usadas():
                                    aviso = f'A letra "{letra}" já foi usada!'
                                    sons.tocar('erro')
                                else:
                                    acertou = jogo.tentar_letra(letra)
                                    aviso = ''
                                    if acertou:
                                        sons.tocar('acerto')
                                    else:
                                        sons.tocar('erro')
                        else:
                            if evento.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()

                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        if self.btn_opcoes_hud.clicado(evento):
                            mostrar_opcoes()
                        elif not fim and self.btn_dica.clicado(evento):
                            texto_dica = jogo.pedir_dica()
                            if texto_dica is None:
                                aviso = 'Você já usou todas as dicas!'
                                sons.tocar('erro')
                            else:
                                aviso = f'Dica: {texto_dica}'
                                sons.tocar('acerto')
                        elif fim and self._clicou_reiniciar(evento):
                            jogo = JogoForca(BANCO_PALAVRAS, dificuldade)
                            fim = False
                            aviso = ''
                            som_fim_tocado = False

    def _clicou_reiniciar(self, evento):
        rect_reiniciar = pygame.Rect(self.layout['x_textos_centro'] - 300, self.layout['y_aviso'] - 20, 600, 60)
        return rect_reiniciar.collidepoint(evento.pos)


def main() -> None:
    app = JogoForcaApp()
    app.rodar()


if __name__ == '__main__':
    main()