"""Exemplo pygame: menu principal usando os assets.  pip install pygame"""
import pygame, sys
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Forca")
clock = pygame.time.Clock()
img = lambda p: pygame.image.load(p).convert_alpha()
font = pygame.font.Font("fonts/Poppins-Bold.ttf", 30)

bg   = img("backgrounds/bg_menu.png")
logo = pygame.transform.smoothscale(img("ui/logo_forca.png"), (450, 125))
hero = img("hangman/stage_4.png")
pencil = pygame.transform.smoothscale(img("decor/pencil.png"), (400, 120))

class Button:
    def __init__(self, text, color, center, action):
        self.text, self.action = text, action
        self.s = {st: img(f"buttons/btn_{color}_{st}.png") for st in ("normal", "hover", "pressed")}
        self.rect = self.s["normal"].get_rect(center=center)
        self.down = False
    def draw(self, surf, mouse):
        st = "pressed" if self.down else "hover" if self.rect.collidepoint(mouse) else "normal"
        surf.blit(self.s[st], self.rect)
        label = font.render(self.text, True, (10, 10, 10))
        dy = 4 if st == "pressed" else -2
        surf.blit(label, label.get_rect(center=(self.rect.centerx, self.rect.centery + dy)))
    def event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos): self.down = True
        if e.type == pygame.MOUSEBUTTONUP:
            if self.down and self.rect.collidepoint(e.pos): self.action()
            self.down = False

# página direita do caderno ≈ x 640..1190
cx = 915
buttons = [
    Button("JOGAR",   "yellow", (cx, 230), lambda: print("jogar")),
    Button("Opções",  "white",  (cx, 340), lambda: print("opções")),
    Button("Ranking", "white",  (cx, 450), lambda: print("ranking")),
    Button("Sair",    "pink",   (cx, 560), lambda: (pygame.quit(), sys.exit())),
]
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        for b in buttons: b.event(e)
    mouse = pygame.mouse.get_pos()
    screen.blit(bg, (0, 0))
    screen.blit(logo, logo.get_rect(center=(365, 190)))
    screen.blit(pygame.transform.smoothscale(hero, (260, 260)), (235, 300))
    screen.blit(pygame.transform.rotate(pencil, -38), (930, 0))
    for b in buttons: b.draw(screen, mouse)
    pygame.display.flip(); clock.tick(60)
