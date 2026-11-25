import pygame
import sys
import random
from palavras import palavra_facil, palavra_normal, palavra_dificil, palavra_secreta
from jogo_forca import JogoForca
from ui.telas import TelaInicio
from ui.popup import Popup, PopupOpcoes
from config import BRANCO, PRETO, VERMELHO, VERDE, get_fontes, get_layout
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

# Classe para gerenciar a exibição da forca e gerenciador de sons
forca_ui = ForcaDesenhavel(LARGURA, ALTURA)
sons = GerenciadorSons()
sons.iniciar_musica() # Inicia a música de fundo gerada sinteticamente


def mostrar_creditos() -> None:
    """Exibe o popup de créditos do jogo."""
    popup = Popup(1000, 500, fonte_pequena_popup, fonte_pequena_popup, (240,240,240), PRETO, PRETO)
    linhas = [
        'Desenvolvido por:',
        'Amiraldo Almeida',
        'Python 3 + pygame',
        'Jogo da Forca - 2025',
        'Objetivo:',
        'Descubra a palavra secreta antes de ser enforcado!'
    ]
    popup.mostrar(tela, '', linhas, 'Pressione qualquer tecla para fechar')


def mostrar_opcoes() -> None:
    """Exibe o popup de opções de áudio e retorna quando fechado."""
    popup = PopupOpcoes(600, 420, fonte_pequena_popup, (240,240,240), PRETO, PRETO, PRETO, BRANCO)
    popup.mostrar(tela, sons)


def tela_inicio() -> list:
    """Exibe a tela inicial e retorna a lista de palavras escolhida pelo usuário."""
    selecionado = 0
    opcoes = [
        ("Fácil", palavra_facil),
        ("Normal", palavra_normal),
        ("Difícil", palavra_dificil),
        ("Secreta", palavra_secreta)
    ]
    nomes_opcoes = [nome for nome, _ in opcoes]
    tela_inicio_ui = TelaInicio(LARGURA, ALTURA, fonte, fonte_pequena, BRANCO, PRETO, VERDE, VERMELHO, BRANCO)
    layout = get_layout(LARGURA, ALTURA)
    botao_sair = pygame.Rect(layout['margem'], ALTURA - layout['margem'] - layout['altura_botao'], layout['largura_botao'], layout['altura_botao'])
    botao_creditos = pygame.Rect(LARGURA - layout['margem'] - layout['largura_botao'], ALTURA - layout['margem'] - layout['altura_botao'], layout['largura_botao'], layout['altura_botao'])
    
    while True:
        tela_inicio_ui.desenhar(tela, nomes_opcoes, selecionado, botao_creditos, botao_sair, layout)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    return opcoes[selecionado][1]
                elif evento.key == pygame.K_c:
                    mostrar_creditos()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_creditos.collidepoint(evento.pos):
                    mostrar_creditos()
                if botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()


def tela_abertura() -> None:
    """Exibe a tela de abertura com efeito animado."""
    tempo_inicial = pygame.time.get_ticks()
    duracao_efeito = 2200  # 2.2 segundos de efeito
    duracao_titulo = 1200  # 1.2 segundos mostrando o título completo
    rodando = True
    efeito_finalizado = False
    titulo_str = 'Jogo da Forca'
    letras_titulo = list(titulo_str)
    letras_mostradas = 0
    tempo_letra = 80  # ms entre cada letra
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
            letras_mostradas = min(len(letras_titulo), int(tempo_atual/tempo_letra))
            titulo = ''.join(letras_titulo[:letras_mostradas])
            texto = fonte.render(titulo, True, VERMELHO)
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - texto.get_height()//2))
        else:
            if not efeito_finalizado:
                efeito_finalizado = True
                tempo_titulo = pygame.time.get_ticks()
            texto = fonte.render(titulo_str, True, VERMELHO)
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - texto.get_height()//2))
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
    """Classe principal do aplicativo Jogo da Forca (Pygame)."""
    def __init__(self) -> None:
        self.tela = tela
        self.largura = LARGURA
        self.altura = ALTURA
        self.fonte = fonte
        self.fonte_pequena = fonte_pequena
        self.forca_ui = forca_ui

    def rodar(self) -> None:
        """Executa o loop principal do jogo da forca."""
        tela_abertura()
        while True:
            lista_palavra = tela_inicio()
            jogo = JogoForca(lista_palavra)
            fim = False
            mensagem = ''
            aviso = ''
            mostrar_popup = False
            som_fim_tocado = False
            
            while True:
                self.tela.fill(BRANCO)
                layout = get_layout(self.largura, self.altura)

                # Zona 1: palavra
                palavra_mostrar = ' '.join(jogo.palavra_atual())
                texto_palavra = self.fonte.render(palavra_mostrar, True, PRETO)
                y = layout['y_titulo']
                self.tela.blit(texto_palavra, (self.largura//2 - texto_palavra.get_width()//2, y))

                # Zona 2: letras usadas
                y += texto_palavra.get_height() + layout['espaco_secao']
                letras_str = ' '.join(jogo.letras_usadas()) if jogo.letras_usadas() else '—'
                texto_usadas = self.fonte_pequena.render(f'Letras usadas: {letras_str}', True, PRETO)
                self.tela.blit(texto_usadas, (self.largura//2 - texto_usadas.get_width()//2, y))

                # Zona 3: "Digite uma letra" + aviso
                y += texto_usadas.get_height() + layout['espaco_secao']
                if not fim:
                    texto_input = self.fonte_pequena.render('Digite uma letra:', True, PRETO)
                    self.tela.blit(texto_input, (self.largura//2 - texto_input.get_width()//2, y))
                    y += texto_input.get_height() + (layout['espaco_secao'] // 2)
                    if aviso:
                        texto_aviso = self.fonte_pequena.render(aviso, True, VERMELHO)
                        self.tela.blit(texto_aviso, (self.largura//2 - texto_aviso.get_width()//2, y))

                # Zona 4: forca
                self.forca_ui.desenhar(self.tela, jogo.erros)

                # Zona 5: mensagem de fim + reinício
                if jogo.venceu():
                    mensagem = 'Parabéns! Você venceu!'
                    if not som_fim_tocado:
                        sons.tocar('vitoria')
                        som_fim_tocado = True
                    fim = True
                elif jogo.perdeu():
                    mensagem = f'Você perdeu! Palavra: {jogo.get_palavra()}'
                    if not som_fim_tocado:
                        sons.tocar('derrota')
                        som_fim_tocado = True
                    fim = True
                
                if fim:
                    texto_msg = self.fonte_pequena.render(mensagem, True, VERDE if jogo.venceu() else VERMELHO)
                    self.tela.blit(texto_msg, (self.largura//2 - texto_msg.get_width()//2, self.altura - 200))
                    
                    texto_reiniciar = self.fonte_pequena.render('Pressione R para jogar novamente ou ESC para sair', True, PRETO)
                    self.tela.blit(texto_reiniciar, (self.largura//2 - texto_reiniciar.get_width()//2, self.altura - 120))

                # Botão Opções (canto superior direito)
                botao_opcoes = pygame.Rect(self.largura - 380, 30, 320, 80)
                pygame.draw.rect(self.tela, PRETO, botao_opcoes, border_radius=16)
                txt_opcoes = self.fonte_pequena.render('Opções (Espaço)', True, BRANCO)
                self.tela.blit(txt_opcoes, (botao_opcoes.x + (botao_opcoes.width-txt_opcoes.get_width())//2, botao_opcoes.y + (botao_opcoes.height-txt_opcoes.get_height())//2))

                pygame.display.flip()
                
                if mostrar_popup:
                    mostrar_opcoes()
                    mostrar_popup = False

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if not fim:
                            if evento.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                            elif evento.key == pygame.K_SPACE:
                                mostrar_popup = True
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
                            if evento.key == pygame.K_r:
                                jogo = JogoForca(lista_palavra)
                                fim = False
                                mensagem = ''
                                aviso = ''
                                som_fim_tocado = False
                            elif evento.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if botao_opcoes.collidepoint(evento.pos):
                            mostrar_popup = True


def main() -> None:
    """Função principal: instancia e executa o app do Jogo da Forca."""
    app = JogoForcaApp()
    app.rodar()


if __name__ == '__main__':
    main()