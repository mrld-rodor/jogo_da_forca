# jogo_forca.py
import random
import string
import unicodedata


def _sem_acento(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


class JogoForca:
    def __init__(self, banco_palavras, dificuldade):
        self.dificuldade = dificuldade
        lista = banco_palavras[dificuldade]
        self.palavra_original = random.choice(list(lista.keys())).upper()
        self.dicas = list(lista[self.palavra_original])
        self.palavra_normalizada = _sem_acento(self.palavra_original)
        self.letras_normalizadas = list(self.palavra_normalizada)
        self.letras_escolhidas = set()
        self.erros = 0
        self.max_erros = 6
        self.dicas_usadas = 0
        self.max_dicas = 2

    def tentar_letra(self, letra):
        letra = _sem_acento(letra).upper()
        if letra not in string.ascii_uppercase:
            return None
        if letra in self.letras_escolhidas:
            return None
        self.letras_escolhidas.add(letra)
        if letra in self.letras_normalizadas:
            return True
        else:
            self.erros += 1
            return False

    def palavra_atual(self):
        resultado = []
        for letra_original, letra_norm in zip(self.palavra_original, self.letras_normalizadas):
            if letra_norm in self.letras_escolhidas:
                resultado.append(letra_original)
            else:
                resultado.append('_')
        return resultado

    def venceu(self):
        return all(l in self.letras_escolhidas for l in self.letras_normalizadas)

    def perdeu(self):
        return self.erros >= self.max_erros

    def finalizado(self):
        return self.venceu() or self.perdeu()

    def letras_usadas(self):
        return sorted(self.letras_escolhidas)

    def get_palavra(self):
        return self.palavra_original

    def pode_pedir_dica(self):
        if self.dicas_usadas >= self.max_dicas:
            return False
        return not self.finalizado()

    def pedir_dica(self):
        if not self.pode_pedir_dica():
            return None
        texto_dica = self.dicas[self.dicas_usadas]
        self.dicas_usadas += 1
        return texto_dica