import pygame
import os
import json

DATA_PATH = os.path.join("data", "users.json")

def load_users():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([], f)
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_PATH, "w") as f:
        json.dump(users, f, indent=4)

def show_scores_window(users):
    pygame.init()
    score_screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Scores par niveau")
    font = pygame.font.Font(None, 28)

    running = True
    while running:
        score_screen.fill((20, 20, 20))
        title = font.render("Scores des joueurs (nombre de coups)", True, (255, 255, 255))
        score_screen.blit(title, (50, 20))

        for i, user in enumerate(users):
            name = user["name"]
            scores = user.get("scores", {})
            text = f"{name} - Niv 1: {scores.get('1', '-')} | Niv 2: {scores.get('2', '-')} | Niv 3: {scores.get('3', '-')}"
            line = font.render(text, True, (200, 200, 200))
            score_screen.blit(line, (20, 60 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

def display_menu():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Utilisateur Menu - Auto Sokoban")
    font = pygame.font.Font(None, 36)

    users = load_users()
    input_text = ""
    selected_user = None
    create_mode = False

    input_box = pygame.Rect(200, 100, 200, 40)
    create_button = pygame.Rect(100, 300, 150, 45)
    scores_button = pygame.Rect(350, 300, 150, 45)

    running = True
    while running:
        screen.fill((30, 30, 30))

        title = font.render("Sélection ou création de joueur", True, (255, 255, 255))
        screen.blit(title, (100, 30))

        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        input_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(input_surface, (input_box.x + 10, input_box.y + 5))

        pygame.draw.rect(screen, (0, 128, 0), create_button)
        screen.blit(font.render("Créer", True, (255, 255, 255)), (create_button.x + 30, create_button.y + 10))

        pygame.draw.rect(screen, (0, 100, 100), scores_button)
        screen.blit(font.render("Voir scores", True, (255, 255, 255)), (scores_button.x + 10, scores_button.y + 5))

        for i, user in enumerate(users):
            user_surface = font.render(user["name"], True, (200, 200, 200))
            screen.blit(user_surface, (20, 150 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            elif event.type == pygame.KEYDOWN:
                if create_mode:
                    if event.key == pygame.K_RETURN and input_text.strip():
                        name = input_text.strip()
                        if not any(u["name"] == name for u in users):
                            users.append({"name": name, "scores": {"1": None, "2": None, "3": None}})
                            save_users(users)
                        selected_user = name
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    create_mode = True

                elif create_button.collidepoint(event.pos):
                    if input_text.strip():
                        name = input_text.strip()
                        if not any(u["name"] == name for u in users):
                            users.append({"name": name, "scores": {"1": None, "2": None, "3": None}})
                            save_users(users)
                        selected_user = name
                        running = False

                elif scores_button.collidepoint(event.pos):
                    show_scores_window(users)

        pygame.display.flip()

    pygame.quit()
    return selected_user
