# forca_pygame.py
import pygame
import sys
import random
import os

from palavras import BANCO_PALAVRAS
from jogo_forca import JogoForca
from ui.telas import TelaInicio
from ui.popup import Popup, PopupOpcoes, PopupRegras, PopupDificuldade, PopupFimDeJogo, PopupDica
from config import (
    PRETO, get_fontes, get_layout, carregar_imagem, ASSETS_DIR
)
from ui.forca import ForcaDesenhavel
from ui.sons import GerenciadorSons
from ui.intro import tocar_intro


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
    linhas = ['Desenvolvido por:', 'Amiraldo Almeida', 'Python 3 + pygame', 'Jogo da Forca - 2025', 'Objetivo:', 'Descubra a palavra secreta antes de ser enforcado!']
    popup.mostrar(tela, '', linhas, 'Pressione qualquer tecla para fechar')


def mostrar_opcoes() -> str:
    """Retorna 'fechar', 'inicio' ou 'dificuldade'."""
    popup = PopupOpcoes(int(LARGURA * 0.70), int(ALTURA * 0.85), fonte_popup, fonte_pequena_popup)
    return popup.mostrar(tela, sons)


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
    """Reproduz o video de abertura. Se nao existir ou falhar, segue direto para o menu."""
    caminho = os.path.join(ASSETS_DIR, 'video', 'intro.mp4')
    if os.path.exists(caminho):
        tocar_intro(tela, caminho, sons)

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

    def _desenhar_texto_quebrado(self, texto, fonte, cor, centro_x, y_inicial, largura_max):
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ""
        for p in palavras:
            teste = (linha_atual + " " + p).strip()
            if fonte.size(teste)[0] <= largura_max:
                linha_atual = teste
            else:
                if linha_atual: linhas.append(linha_atual)
                linha_atual = p
        if linha_atual: linhas.append(linha_atual)

        y = y_inicial
        for linha in linhas:
            txt = fonte.render(linha, True, cor)
            tela.blit(txt, (centro_x - txt.get_width() // 2, y))
            y += txt.get_height() + 5
        return y

    def _desenhar_palavra(self, jogo):
        layout = self.layout
        letras = jogo.palavra_atual()
        n = len(letras)

        # CÁLCULO À PROVA DE FALHAS: Centro fixado em 52% da tela
        centro_x = int(self.largura * 0.52)
        
        # Largura máxima que a palavra pode ter para não invadir os lados
        largura_maxima = int(self.largura * 0.40)
        
        tamanho_fonte = 72
        espaco_letras = 15 
        
        while True:
            fonte_teste = pygame.font.Font(os.path.join(ASSETS_DIR, "fonts", "Poppins-Bold.ttf"), tamanho_fonte)
            larguras = [max(fonte_teste.size(l)[0], 30) for l in letras]
            largura_total = sum(larguras) + espaco_letras * (n - 1)
            
            if largura_total <= largura_maxima:
                break
            
            tamanho_fonte -= 2
            espaco_letras = max(5, espaco_letras - 1)
            
            if tamanho_fonte < 20:
                break
        
        fonte_final = pygame.font.Font(os.path.join(ASSETS_DIR, "fonts", "Poppins-Bold.ttf"), tamanho_fonte)
        
        larguras = [max(fonte_final.size(l)[0], 30) for l in letras]
        largura_total = sum(larguras) + espaco_letras * (n - 1)
        
        # Centraliza a palavra no centro_x definido
        x_inicio = centro_x - (largura_total // 2)
        
        # Desce a palavra 40px
        y_base = layout['y_palavra'] + 40

        x = x_inicio
        for i, letra in enumerate(letras):
            if letra != '_':
                texto = fonte_final.render(letra, True, PRETO)
                tela.blit(texto, (x + (larguras[i] - texto.get_width()) // 2, y_base - texto.get_height() + 10))
            
            linha_y = y_base + 20
            pygame.draw.line(tela, PRETO, (x, linha_y), (x + larguras[i], linha_y), 4)
            x += larguras[i] + espaco_letras

    def _desenhar_hud(self, jogo, fim):
        self.btn_opcoes_hud.desenhar(self.tela)
        txt_op = self.fonte_pequena.render("Opções", True, PRETO)
        pos_x_op = self.btn_opcoes_hud.rect.left - txt_op.get_width() - 15
        pos_y_op = self.btn_opcoes_hud.rect.centery - txt_op.get_height() // 2
        tela.blit(txt_op, (pos_x_op, pos_y_op))

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
            
            # Loop Principal da Partida
            while True:
                jogo = JogoForca(BANCO_PALAVRAS, dificuldade)
                fim = False
                som_fim_tocado = False
                sair_para_menu = False
                sair_para_dificuldade = False

                while not fim:
                    tela.blit(bg_game, (0, 0))
                    layout = self.layout

                    self.forca_ui.desenhar(tela, jogo.erros)
                    self._desenhar_palavra(jogo)

                    letras_str = ' '.join(jogo.letras_usadas()) if jogo.letras_usadas() else '—'
                    texto_completo = f'Letras usadas: {letras_str}'
                    
                    self._desenhar_texto_quebrado(
                        texto_completo, self.fonte_pequena, PRETO, 
                        layout['x_textos_centro'], layout['y_letras'], layout['largura_max_texto']
                    )

                    texto_input = self.fonte_pequena.render('Digite uma letra:', True, PRETO)
                    tela.blit(texto_input, (layout['x_textos_centro'] - texto_input.get_width() // 2, layout['y_input']))

                    self._desenhar_hud(jogo, fim)
                    pygame.display.flip()

                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                            elif pygame.K_a <= evento.key <= pygame.K_z:
                                letra = chr(evento.key).upper()
                                if letra in jogo.letras_usadas():
                                    sons.tocar('erro')
                                else:
                                    acertou = jogo.tentar_letra(letra)
                                    if acertou:
                                        sons.tocar('acerto')
                                    else:
                                        sons.tocar('erro')

                        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                            if self.btn_opcoes_hud.clicado(evento):
                                # CHAMA O POPUP DE OPÇÕES E TRATA O RETORNO
                                acao_opc = mostrar_opcoes()
                                if acao_opc == 'inicio':
                                    sair_para_menu = True
                                    break
                                elif acao_opc == 'dificuldade':
                                    sair_para_dificuldade = True
                                    break
                                    
                            elif not fim and self.btn_dica.clicado(evento):
                                if jogo.pode_pedir_dica():
                                    texto_dica = jogo.pedir_dica()
                                    sons.tocar('acerto')
                                    
                                    popup_d = PopupDica(
                                        int(LARGURA * 0.6),
                                        int(ALTURA * 0.6),
                                        fonte_popup,
                                        fonte_pequena_popup,
                                        texto_dica,
                                        jogo.pode_pedir_dica()
                                    )
                                    acao_dica = popup_d.mostrar(tela)
                                    
                                    if acao_dica == 'proxima' and jogo.pode_pedir_dica():
                                        texto_dica2 = jogo.pedir_dica()
                                        popup_d2 = PopupDica(
                                            int(LARGURA * 0.6),
                                            int(ALTURA * 0.6),
                                            fonte_popup,
                                            fonte_pequena_popup,
                                            texto_dica2,
                                            False
                                        )
                                        popup_d2.mostrar(tela)
                                else:
                                    sons.tocar('erro')

                    if sair_para_menu:
                        break
                    
                    if sair_para_dificuldade:
                        popup_dif = PopupDificuldade(
                            int(LARGURA * 0.60), int(ALTURA * 0.80),
                            fonte_popup, fonte_pequena_popup
                        )
                        nova_escolha = popup_dif.mostrar(tela)
                        mapa_dificuldade = {
                            'Fácil': 'facil', 'Normal': 'normal',
                            'Difícil': 'dificil', 'Secreta': 'secreta'
                        }
                        if nova_escolha in mapa_dificuldade:
                            dificuldade = mapa_dificuldade[nova_escolha]
                            jogo = JogoForca(BANCO_PALAVRAS, dificuldade)
                            fim = False
                            som_fim_tocado = False
                            sair_para_dificuldade = False
                            continue
                        else:
                            # Se fechar o popup de dificuldade, apenas continua o jogo atual
                            sair_para_dificuldade = False

                    if jogo.venceu() or jogo.perdeu():
                        fim = True
                        if not som_fim_tocado:
                            if jogo.venceu():
                                sons.tocar('vitoria')
                            else:
                                sons.tocar('derrota')
                            som_fim_tocado = True

                # Se saiu para o menu no meio do jogo, quebra o loop da partida e volta para tela_inicio
                if sair_para_menu:
                    break 

                # Popup de Fim de Jogo (só se o jogo terminou de verdade)
                if fim:
                    popup_fim = PopupFimDeJogo(
                        int(LARGURA * 0.6), 
                        int(ALTURA * 0.75), 
                        fonte_popup, 
                        fonte_pequena_popup,
                        jogo.venceu(),
                        jogo.get_palavra()
                    )
                    escolha = popup_fim.mostrar(tela)
                    
                    if escolha == 'jogar':
                        continue
                    else:
                        break


def main() -> None:
    app = JogoForcaApp()
    app.rodar()


if __name__ == '__main__':
    main()