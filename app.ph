from lessons import lessons
from quiz import run_quiz

def show_lesson(lesson_id):
    lesson = lessons[lesson_id]
    print("\nLesson:", lesson["title"])

    print("\nVocabulary:")
    for word, meaning in lesson["vocab"].items():
        print(f"{word} - {meaning}")

    print("\nSample Sentences:")
    for s in lesson["sentences"]:
        print("-", s)

while True:
    print("\n=== BUSINESS ENGLISH APP ===")
    print("1. Lesson 1 - Greetings")
    print("2. Lesson 2 - Sales")
    print("3. Quiz")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        show_lesson(1)
    elif choice == "2":
        show_lesson(2)
    elif choice == "3":
        run_quiz()
    elif choice == "0":
        break
    else:
        print("Invalid choice")
