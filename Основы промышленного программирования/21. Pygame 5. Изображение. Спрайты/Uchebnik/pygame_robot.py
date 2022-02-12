import os
import sys
import pygame


def load_image(path, colorkey=None):
    full_path = os.path.join('data', path)
    # ксли файл не существует, то выходим
    if not os.path.exists(full_path):
        print(f"Файл с изображением '{full_path}' не найден")
        sys.exit()
    im = pygame.image.load(full_path)

    if colorkey is not None:
        im = im.convert()
        if colorkey == -1:
            colorkey = im.get_at((0, 0))
        im.set_colorkey(colorkey)
    else:
        im = im.convert_alpha()
    return im


def main():
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Шаблон")
    screen.fill('white')
    image = load_image('robot.png')
    image1 = pygame.transform.scale(image, (200, 100))
    image2 = pygame.transform.scale(image, (100, 200))
    image3 = pygame.transform.scale(image, (200, 200))
    screen.blit(image1, (100, 200))
    screen.blit(image2, (100, 250))
    screen.blit(image3, (200, 50))
    running = True
    while running:
        # цикл приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.blit(image, event.pos)
        # отрисовка и изменение св-в объектов
        pygame.display.flip()  # обновление экрана
    pygame.quit()


if __name__ == '__main__':
    main()
