import sys

riddles = [
    ("Белый, но не сахар. Пушистый, но не птица. Нет ног, а идёт. ", "снег"),
    ("Страус может назвать себя птицей? ", "нет"),
    ("Каких камней не бывает в речке? ", "сухих"),
    ("Что можно увидеть с закрытыми глазами? ", "сон"),
    ("Висит груша — нельзя скушать. Что это? ", "лампочка"),
    ("Сколько месяцев в году имеют 28 дней? ", "все"),
]

name = input("Как тебя зовут? ").strip()
print(f"Привет, {name}! Пройди испытания, иначе я тебя съем.\n")

number = input("Введи число от 1 до 9: ")
while not number.isdigit() or not (1 <= int(number) <= 9):
    number = input("Нужно число от 1 до 9: ")
if int(number) <= 6:
    print("Ты прошёл дальше!\n")
else:
    print("Не повезло. Ты проиграл!")
    sys.exit()

print("Теперь загадки. Ответь верно хотя бы на 4 из 6.\n")
score = 0
for question, correct in riddles:
    answer = input(question).lower().strip()
    if answer == correct:
        print("Правильно!")
        score += 1
    else:
        print(f"Неправильно! Ответ: {correct}")

if score < 4:
    print(f"\nУвы, {name}. Загадок мало отгадано — ты проиграл!")
    sys.exit()

print(f"\nОтлично, {name}! Осталось последнее испытание.")
final = input("Финал! Введи число от 1 до 9: ")
while not final.isdigit() or not (1 <= int(final) <= 9):
    final = input("Нужно число от 1 до 9: ")
if int(final) <= 7:
    print(f"Поздравляю, {name}! Ты выиграл!")
else:
    print(f"Я тебя съел, {name}!")