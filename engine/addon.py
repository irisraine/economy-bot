import engine.config as config
import engine.sql as sql
import engine.utils as utils


class QuizManager:
    def __init__(self):
        self.current_quiz = None

    def create_quiz(self):
        self.current_quiz = Quiz()

    def start_quiz(self, question, answer, prize_amount, prize_special=None):
        self.current_quiz.setup(question, answer, prize_amount, prize_special)
        sql.set_quiz_statistics(increment=True)

    def get_status(self):
        if not self.current_quiz or not self.current_quiz.is_started or not self.current_quiz.is_active():
            return "no_available_quiz"
        elif self.current_quiz.in_progress():
            return "in_progress"
        else:
            return "finished"

    def close_quiz(self):
        self.current_quiz = None

    def reward_winner(self, quiz_winner):
        sql.set_user_balance(quiz_winner, self.current_quiz.prize_amount)
        sql.set_quiz_statistics(prize_amount=self.current_quiz.prize_amount)


class Quiz:
    def __init__(self):
        self.__start_time = None
        self.__question = None
        self.__answer = None
        self.__prize_amount = None
        self.__prize_special = None
        self.__is_started = False

    def setup(self, question, answer, prize_amount, prize_special):
        self.__start_time = utils.get_timestamp()
        self.__question = question
        self.__answer = answer
        self.__prize_amount = int(prize_amount)
        self.__prize_special = prize_special
        self.__is_started = True

    @property
    def question(self):
        return self.__question

    @property
    def answer(self):
        return self.__answer

    @property
    def prize_amount(self):
        return self.__prize_amount

    @property
    def prize_special(self):
        return self.__prize_special

    @property
    def is_started(self):
        return self.__is_started

    def in_progress(self):
        return utils.get_timestamp() - self.__start_time < config.QUIZ_ROUND_TIME

    def is_active(self):
        return utils.get_timestamp() - self.__start_time < config.QUIZ_ACTIVE_TIME
