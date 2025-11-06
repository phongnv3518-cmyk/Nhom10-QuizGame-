import csv


def load_questions(file_path):
    """Đọc câu hỏi từ file CSV

    File CSV yêu cầu có header: question,A,B,C,D,answer
    Trả về list các dict: {"question": str, "options": [A,B,C,D], "answer": str}
    """
    questions = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append({
                "question": row["question"],
                "options": [row.get("A", ""), row.get("B", ""), row.get("C", ""), row.get("D", "")],
                "answer": row["answer"]
            })
    return questions


def check_answer(user_answer, correct_answer):
    """Kiểm tra đáp án: so sánh không phân biệt hoa thường và bỏ khoảng trắng thừa"""
    if user_answer is None or correct_answer is None:
        return False
    return user_answer.strip().lower() == correct_answer.strip().lower()
