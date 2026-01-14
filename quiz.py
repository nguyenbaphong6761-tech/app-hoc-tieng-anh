def run_quiz():
    questions = {
        "Discount means?": "chiết khấu",
        "Order means?": "đơn hàng"
    }

    score = 0
    for q, a in questions.items():
        answer = input(q + " ").lower()
        if a in answer:
            score += 1

    print(f"Your score: {score}/{len(questions)}")
