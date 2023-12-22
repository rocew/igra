import pygame
import random
pygame.init()

WIDTH = 800
HEIGHT = 600
CARD_SIZE = 100
GAP = 10
ROWS = 4
COLS = 4

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Создание шрифта
font = pygame.font.SysFont(None, 48)

# Загрузка изображений
images = []
for i in range(1, 9):
    image = pygame.image.load(f"images/{i}.png")
    image = pygame.transform.scale(image, (CARD_SIZE, CARD_SIZE))
    images.append(image)

# Создание списка с парами картинок
images = [pygame.image.load("images/1.png"), pygame.image.load("images/2.png"), pygame.image.load("images/3.png"), pygame.image.load("images/4.png"),pygame.image.load("images/5.png"),pygame.image.load("images/6.png"),pygame.image.load("images/7.png"),pygame.image.load("images/8.png")]
image_pairs = images * 2
random.shuffle(image_pairs)

# Создание игрового поля
grid = []
for row in range(ROWS):
    new_row = []
    for col in range(COLS):
        if image_pairs:
            image = image_pairs.pop()
            rect = pygame.Rect(col * (CARD_SIZE + GAP), row * (CARD_SIZE + GAP), CARD_SIZE, CARD_SIZE)
            card = {"image": image, "rect": rect, "visible": False, "matched": False}
            new_row.append(card)
    grid.append(new_row)

# Функция для проверки совпадения карт
def check_match(first_card, second_card):
    if first_card["image"] == second_card["image"]:
        first_card["matched"] = True
        second_card["matched"] = True

# функции отрисовки карты
def draw_card(card):
    if card["visible"]:
        if "image" in card and "rect" in card:
            scaled_image = pygame.transform.smoothscale(card["image"], (CARD_SIZE, CARD_SIZE))
            screen.blit(scaled_image, card["rect"])
    else:
        pygame.draw.rect(screen, GRAY, card["rect"])



# Создание переменных состояния игры
first_card = None
second_card = None
matched_pairs = 0
game_over = False

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            for row in grid:
                for card in row:
                    if card["rect"].collidepoint(x, y) and not card["visible"]:
                        card["visible"] = True
                        if first_card is None:
                            first_card = card
                        elif second_card is None:
                            second_card = card
                            if first_card["image"] == second_card["image"]:
                                first_card = None
                                second_card = None
                                matched_pairs += 1
                                if matched_pairs == 8:
                                    game_over = True
                            else:
                                pygame.time.wait(1000)
                                first_card["visible"] = False
                                second_card["visible"] = False
                                first_card = None
                                second_card = None

    screen.fill(BLACK)

    for row in grid:
        for card in row:
            if not card["visible"]:
                pygame.draw.rect(screen, GRAY, card["rect"])
            else:
                draw_card(card)

    # Отрисовка текста
    text = font.render(f"Pairs Matched: {matched_pairs}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    if game_over:
        text = font.render("Game Over!", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

# Завершение игры
pygame.quit()




