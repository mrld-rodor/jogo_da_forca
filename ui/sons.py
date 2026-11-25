import pygame
import numpy as np

class GerenciadorSons:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error:
            print("Aviso: Sistema de áudio não encontrado. O jogo rodará sem som.")
            self.ativo = False
            return
            
        self.ativo = True
        self.mudo_efeitos = False
        self.mudo_musica = False
        
        # Volumes iniciais (0.0 a 1.0)
        self.volume_efeitos = 0.5
        self.volume_musica = 0.3
        
        self.sons = {}
        self._gerar_sons()
        self._gerar_musica()

    def _criar_som(self, frequencias, duracao, volume=0.3, tipo='senoide'):
        sample_rate = 44100
        n_samples = int(sample_rate * duracao)
        t = np.linspace(0, duracao, n_samples, False)
        
        onda = np.zeros(n_samples)
        for freq in frequencias:
            if tipo == 'senoide':
                onda += np.sin(freq * t * 2 * np.pi)
            elif tipo == 'quadrada':
                onda += np.sign(np.sin(freq * t * 2 * np.pi))
                
        onda /= len(frequencias)
        
        envelope = np.ones(n_samples)
        fade_samples = int(sample_rate * 0.05)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        onda *= envelope
        
        onda_int = (onda * 32767 * volume).astype(np.int16)
        array_estereo = np.column_stack((onda_int, onda_int))
        
        return pygame.sndarray.make_sound(array_estereo)

    def _gerar_sons(self):
        self.sons['acerto'] = self._criar_som([523.25, 659.25], 0.1, volume=0.2, tipo='senoide')
        self.sons['erro'] = self._criar_som([196.00, 130.81], 0.25, volume=0.3, tipo='quadrada')
        self.sons['vitoria'] = self._criar_som([523.25, 659.25, 783.99, 1046.50], 0.6, volume=0.3, tipo='senoide')
        self.sons['derrota'] = self._criar_som([130.81, 155.56, 196.00], 0.8, volume=0.3, tipo='quadrada')

    def _gerar_musica(self):
        """Gera uma pequena melodia em loop para o fundo."""
        sample_rate = 44100
        # Uma sequência de notas simples (Dó, Mi, Sol, Dó oitava acima, Sol, Mi)
        notas_freq = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63]
        duracao_nota = 0.3
        n_samples_nota = int(sample_rate * duracao_nota)
        
        onda_total = np.array([])
        t_nota = np.linspace(0, duracao_nota, n_samples_nota, False)
        
        for freq in notas_freq:
            nota = np.sin(freq * t_nota * 2 * np.pi)
            # Envelope para não estalar
            envelope = np.ones(n_samples_nota)
            fade = int(sample_rate * 0.02)
            envelope[:fade] = np.linspace(0, 1, fade)
            envelope[-fade:] = np.linspace(1, 0, fade)
            onda_total = np.concatenate((onda_total, nota * envelope))
            
        onda_int = (onda_total * 32767 * 0.2).astype(np.int16)
        array_estereo = np.column_stack((onda_int, onda_int))
        
        self.musica_fundo = pygame.sndarray.make_sound(array_estereo)
        self.musica_fundo.set_volume(self.volume_musica)

    def iniciar_musica(self):
        if self.ativo and not self.mudo_musica:
            pygame.mixer.Channel(1).play(self.musica_fundo, loops=-1)

    def atualizar_volumes(self):
        """Aplica os volumes atuais."""
        if not self.ativo: return
        if self.mudo_musica:
            pygame.mixer.Channel(1).set_volume(0)
        else:
            pygame.mixer.Channel(1).set_volume(self.volume_musica)

    def tocar(self, nome):
        if self.ativo and not self.mudo_efeitos and nome in self.sons:
            self.sons[nome].set_volume(self.volume_efeitos)
            self.sons[nome].play()