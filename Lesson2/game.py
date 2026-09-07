import sys
RIDDLES = [
    ("Белый, но не сахар. Пушистый, но не птица. Нет ног, а идёт. ", "снег"),
    ("Страус может назвать себя птицей? ", "нет"),
    ("Каких камней не бывает в речке? ", "сухих"),
    ("Что можно увидеть с закрытыми глазами? ", "сон"),
    ("Висит груша — нельзя скушать. Что это? ", "лампочка"),
    ("Сколько месяцев в году имеют 28 дней? ", "все"),
]

def parse_number(text):
    if not text.isdigit():
        raise ValueError("Введено не число")
    value = int(text)
    if not (1 <= value <= 9):
        raise ValueError("Число должно быть от 1 до 9")
    return value


def check_entry(number):
    return 1 <= number <= 6


def check_riddle(answer, correct):
    return answer.lower().strip() == correct


def count_correct(answers, riddles):
    score = 0
    for answer, (question, correct) in zip(answers, riddles):
        if check_riddle(answer, correct):
            score += 1
    return score


def passed_riddles(score):
    return score >= 4


def is_win_final(number):
    return 1 <= number <= 7


def ask_number(prompt):
    while True:
        try:
            return parse_number(input(prompt))
        except ValueError as error:
            print(error)

def main():
    name = input("Как тебя зовут? ").strip()
    print(f"Привет, {name}! Пройди испытания, иначе я тебя съем.\n")

    number = ask_number("Введи число от 1 до 9: ")
    if check_entry(number):
        print("Ты прошёл дальше!\n")
    else:
        print("Не повезло. Ты проиграл!")
        sys.exit()

    print("Теперь загадки. Ответь верно хотя бы на 4 из 6.\n")
    answers = []
    for question, correct in RIDDLES:
        answer = input(question)
        answers.append(answer)
        if check_riddle(answer, correct):
            print("Правильно!")
        else:
            print(f"Неправильно! Ответ: {correct}")

    score = count_correct(answers, RIDDLES)
    if not passed_riddles(score):
        print(f"\nУвы, {name}. Загадок мало отгадано — ты проиграл!")
        sys.exit()

    print(f"\nОтлично, {name}! Осталось последнее испытание.")
    final = ask_number("Финал! Введи число от 1 до 9: ")
    if is_win_final(final):
        print(f"Поздравляю, {name}! Ты выиграл!")
    else:
        print(f"Я тебя съел, {name}!")


if __name__ == "__main__":
    main()