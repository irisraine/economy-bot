class Quiz:
    def __init__(self, question, answer, prize_amount=1, prize_special=None):
        self.is_active = True
        self.in_progress = True
        self.question = question
        self.answer = answer
        self.prize_amount = int(prize_amount)
        self.prize_special = prize_special

    def get_contents(self):
        return {
            "question": self.question,
            "prize_amount": self.prize_amount,
            "prize_special": self.prize_special,
        }

    def stop_quiz(self):
        self.in_progress = False

    def close_quiz(self):
        self.is_active = False
