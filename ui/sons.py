# ui/sons.py
import os
import sys
import pygame
import math
import array


def _iniciar_mixer():
    """Tenta iniciar o audio com varios drivers. Devolve True se conseguiu.

    No Windows o driver por defeito (WASAPI) falha em alguns PCs
    ("WASAPI can't initialize audio client"), por isso tentamos alternativas.
    """
    drivers = [None]
    if sys.platform == "win32":
        drivers += ["directsound", "winmm"]

    for driver in drivers:
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
            if driver:
                os.environ["SDL_AUDIODRIVER"] = driver
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            return True
        except pygame.error as e:
            print(f"[AVISO] Audio indisponivel com driver {driver or 'padrao'}: {e}")
    return False


class GerenciadorSons:
    def __init__(self):
        self.volume_musica = 0.5
        self.volume_efeitos = 0.7
        self.mudo_musica = False
        self.mudo_efeitos = False
        self.efeitos = {}
        self.musica = None
        # Se nao houver audio, o jogo continua a funcionar sem som.
        self.ativo = _iniciar_mixer()
        if self.ativo:
            self._gerar_sons()
        else:
            print("[AVISO] O jogo vai correr sem som.")

    def _gerar_tom(self, frequencia, duracao_ms, volume=0.5):
        """Gera uma nota simples (estéreo)."""
        taxa = 44100
        n_amostras = int(taxa * (duracao_ms / 1000.0))
        amostras = array.array('h')
        for i in range(n_amostras):
            t = i / taxa
            # Envelope para evitar cliques
            env = math.exp(-3 * t) if duracao_ms < 200 else 1.0
            val = int(32767 * volume * env * math.sin(2 * math.pi * frequencia * t))
            amostras.append(val)  # L
            amostras.append(val)  # R
        return pygame.mixer.Sound(buffer=amostras.tobytes())

    def _gerar_sons(self):
        # Efeitos
        self.efeitos['acerto'] = self._gerar_tom(880, 80, self.volume_efeitos)
        self.efeitos['erro'] = self._gerar_tom(220, 120, self.volume_efeitos)
        self.efeitos['vitoria'] = self._gerar_tom(1046, 250, self.volume_efeitos)
        self.efeitos['derrota'] = self._gerar_tom(130, 300, self.volume_efeitos)

    def iniciar_musica(self):
        """Gera uma melodia simples em loop."""
        if not self.ativo:
            return
        taxa = 44100
        # Melodia: Dó, Mi, Sol, Mi (frequências em Hz)
        notas = [261.63, 329.63, 392.00, 329.63]
        duracao_nota_ms = 250
        amostras = array.array('h')

        for freq in notas:
            n_amostras = int(taxa * (duracao_nota_ms / 1000.0))
            for i in range(n_amostras):
                t = i / taxa
                # Envelope suave para a nota
                env = math.exp(-2 * t) if i > n_amostras - 1000 else 1.0
                val = int(32767 * self.volume_musica * 0.3 * env * math.sin(2 * math.pi * freq * t))
                amostras.append(val)
                amostras.append(val)

        self.musica = pygame.mixer.Sound(buffer=amostras.tobytes())
        self.musica.set_volume(0.0 if self.mudo_musica else self.volume_musica)
        self.musica.play(loops=-1)

    def tocar(self, nome_som):
        if self.ativo and nome_som in self.efeitos and not self.mudo_efeitos:
            self.efeitos[nome_som].play()

    # ------------------------------------------------------------------
    def set_volume_musica(self, volume):
        self.volume_musica = max(0.0, min(1.0, volume))
        self.mudo_musica = (self.volume_musica == 0.0)
        if self.musica:
            self.musica.set_volume(0.0 if self.mudo_musica else self.volume_musica)

    def set_volume_efeitos(self, volume):
        self.volume_efeitos = max(0.0, min(1.0, volume))
        self.mudo_efeitos = (self.volume_efeitos == 0.0)
        for som in self.efeitos.values():
            som.set_volume(0.0 if self.mudo_efeitos else self.volume_efeitos)

    def get_volume_musica(self):
        return self.volume_musica

    def get_volume_efeitos(self):
        return self.volume_efeitos