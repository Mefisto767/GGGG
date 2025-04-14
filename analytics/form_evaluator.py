import random

# Простая оценка формы — можно будет заменить на API или исторические данные
def evaluate_team_form(draft):
    # Пока что просто случайно варьируем форму от 20 до 40
    return sum(random.randint(4, 8) for _ in draft)
