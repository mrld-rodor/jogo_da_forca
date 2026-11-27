#intro.py

# ui/intro.py
"""Reproduz o video de abertura (intro.mp4) com som, usando PyAV."""
import sys
import pygame


def _carregar_audio(caminho):
    """Descodifica a faixa de audio do video para um pygame Sound (ou None)."""
    import av
    try:
        contentor = av.open(caminho)
    except Exception:
        return None
    try:
        faixa = next((s for s in contentor.streams if s.type == "audio"), None)
        if faixa is None:
            return None
        resampler = av.AudioResampler(format="s16", layout="stereo", rate=44100)
        blocos = []
        for frame in contentor.decode(faixa):
            for f in resampler.resample(frame):
                blocos.append(f.to_ndarray().tobytes())
        for f in resampler.resample(None):
            blocos.append(f.to_ndarray().tobytes())
        if not blocos:
            return None
        return pygame.mixer.Sound(buffer=b"".join(blocos))
    except Exception as e:
        print(f"[AVISO] Nao foi possivel carregar o audio da intro: {e}")
        return None
    finally:
        contentor.close()


def tocar_intro(tela, caminho, sons=None) -> bool:
    """Toca o video em ecra cheio, mantendo a proporcao. Qualquer tecla ou clique salta.

    Devolve True se o video foi reproduzido (ou saltado) e False se nao foi possivel
    reproduzi-lo, caso em que o jogo deve seguir diretamente para o menu.
    """
    try:
        import av
        contentor = av.open(caminho)
    except Exception as e:
        print(f"[AVISO] Intro indisponivel ({caminho}): {e}")
        return False

    largura, altura = tela.get_size()
    musica_volume_original = None
    som_intro = None
    try:
        video = contentor.streams.video[0]
        video.thread_type = "AUTO"
        escala = min(largura / video.codec_context.width, altura / video.codec_context.height)
        lw = max(2, int(video.codec_context.width * escala) // 2 * 2)
        lh = max(2, int(video.codec_context.height * escala) // 2 * 2)
        pos = ((largura - lw) // 2, (altura - lh) // 2)

        # Audio (se houver mixer ativo)
        if pygame.mixer.get_init():
            som_intro = _carregar_audio(caminho)

        # Silencia a musica de fundo durante a intro
        if sons is not None and getattr(sons, "musica", None) is not None:
            musica_volume_original = 0.0 if sons.mudo_musica else sons.volume_musica
            sons.musica.set_volume(0.0)

        tela.fill((0, 0, 0))
        pygame.display.flip()
        relogio = pygame.time.Clock()
        inicio = pygame.time.get_ticks()
        if som_intro is not None:
            som_intro.play()

        for frame in contentor.decode(video):
            if frame.pts is None:
                continue
            t_frame = float(frame.pts * video.time_base)

            # Espera pelo momento certo, ou salta o frame se estiver atrasado
            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                        return True
                agora = (pygame.time.get_ticks() - inicio) / 1000.0
                if agora >= t_frame:
                    break
                pygame.time.wait(2)
            if agora - t_frame > 0.15:
                continue  # atrasado: descarta

            rgb = frame.reformat(width=lw, height=lh, format="rgb24").to_ndarray()
            superficie = pygame.image.frombuffer(rgb.tobytes(), (lw, lh), "RGB")
            tela.blit(superficie, pos)
            pygame.display.flip()
            relogio.tick(120)
        return True
    except Exception as e:
        print(f"[AVISO] Erro ao reproduzir a intro: {e}")
        return False
    finally:
        try:
            if som_intro is not None:
                som_intro.fadeout(200)
            if sons is not None and musica_volume_original is not None:
                sons.musica.set_volume(musica_volume_original)
            contentor.close()
        except Exception:
            pass
        tela.fill((0, 0, 0))
        pygame.display.flip()