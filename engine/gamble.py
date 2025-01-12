import random
from collections import Counter


class SlotMachine:
    BETS = {
        'low': 5,
        'high': 8
    }
    REEL = {
        'low': (['frog_green'] * 3 + ['frog_orange'] * 2 + ['frog_white']),
        'high': (['gold'] * 1 + ['cart'] * 2 + ['star'] * 3 + ['horseshoe'] * 4 + ['moonshine'] * 5 +
            ['frog_green'] * 16 + ['frog_orange'] * 8 + ['frog_white'] * 4)
    }
    WINNING_OUTCOMES_PREDEFINED = {
        "three_gold": {'probability_range': (0, 0.01), 'reel': ['gold'] * 3},
        "three_cart": {'probability_range': (0.01, 0.03), 'reel': ['cart'] * 3},
        "three_star": {'probability_range': (0.03, 0.055), 'reel': ['star'] * 3},
        "three_horseshoe": {'probability_range': (0.055, 0.08), 'reel': ['horseshoe'] * 3},
        "three_moonshine": {'probability_range': (0.08, 0.15), 'reel': ['moonshine'] * 3},
        "two_gold": {'probability_range': (0.15, 0.3), 'reel': ['gold'] * 2},
        "one_gold": {'probability_range': (0.3, 1.0), 'reel': ['gold'] * 1},
    }
    NEAR_WINNING_OUTCOMES_PREDEFINED = {
        "cart": {'probability_range': (0, 0.15), 'reel': ['cart'] * 2},
        "star": {'probability_range': (0.15, 0.40), 'reel': ['star'] * 2},
        "horseshoe": {'probability_range': (0.40, 0.60), 'reel': ['horseshoe'] * 2},
        "moonshine": {'probability_range': (0.60, 0.75), 'reel': ['moonshine'] * 2},
        "frog": {'probability_range': (0.75, 1.0),
                 'reel': [random.choice(['frog_green', 'frog_orange', 'frog_white'])] * 2},
    }
    THRESHOLD_FOR_PREDEFINED_WINNING = 0.25
    THRESHOLD_FOR_PREDEFINED_NEAR_WINNING = 0.15
    WINNINGS = {
        "three_gold": 300,
        "three_cart": 100,
        "three_star": 75,
        "three_horseshoe": 50,
        "three_moonshine": 40,
        "two_gold": 25,
        "three_frogs_white": 25,
        "three_frogs_orange": 20,
        "three_frogs_green": 10,
        "three_frogs_all_colors": 15,
        "one_gold": 10,
    }

    def __init__(self, player):
        self.player = player
        self.bet = None
        self.reels = []
        self.winning = 0

    def place_bet(self, bet):
        self.bet = bet

    def reel(self):
        return random.choice(self.REEL[self.bet])

    def spin(self):
        central_line = []

        if self.bet == 'high':
            roll_for_predefined_winning = random.random()
            is_predefined_winning = roll_for_predefined_winning < self.THRESHOLD_FOR_PREDEFINED_WINNING
            if is_predefined_winning:
                roll_for_predefined_winning_type = random.random()
                for outcome in self.WINNING_OUTCOMES_PREDEFINED.values():
                    lower_bound, upper_bound = outcome['probability_range']
                    if lower_bound <= roll_for_predefined_winning_type < upper_bound:
                        central_line = outcome['reel']
                        break
            else:
                roll_for_predefined_near_winning = random.random()
                is_predefined_near_winning = roll_for_predefined_near_winning < self.THRESHOLD_FOR_PREDEFINED_NEAR_WINNING
                if is_predefined_near_winning:
                    roll_for_predefined_near_winning_type = random.random()
                    for outcome in self.NEAR_WINNING_OUTCOMES_PREDEFINED.values():
                        lower_bound, upper_bound = outcome['probability_range']
                        if lower_bound <= roll_for_predefined_near_winning_type < upper_bound:
                            central_line = outcome['reel']
                            break
        if central_line:
            if len(central_line) == 2:
                central_line.append(self.reel())
            elif len(central_line) == 1:
                central_line += [self.reel() for _ in range(2)]
            random.shuffle(central_line)
            self.reels.append([self.reel() for _ in range(3)])
            self.reels.append(central_line)
            self.reels.append([self.reel() for _ in range(3)])
        else:
            self.reels = [[self.reel() for _ in range(3)] for _ in range(3)]

    def calculate_winnings(self, reels):
        central_line = reels[1]
        counts = {symbol: central_line.count(symbol) for symbol in set(central_line)}

        if self.bet == "high":
            if counts.get("gold", 0) == 3:
                return self.WINNINGS["three_gold"]
            elif counts.get("cart", 0) == 3:
                return self.WINNINGS["three_cart"]
            elif counts.get("star", 0) == 3:
                return self.WINNINGS["three_star"]
            elif counts.get("horseshoe", 0) == 3:
                return self.WINNINGS["three_horseshoe"]
            elif counts.get("moonshine", 0) == 3:
                return self.WINNINGS["three_moonshine"]
            elif counts.get("gold", 0) == 2:
                return self.WINNINGS["two_gold"]
            elif counts.get("gold", 0) == 1:
                return self.WINNINGS["one_gold"]
        if counts.get("frog_green", 0) == 3:
            return self.WINNINGS["three_frogs_green"]
        elif counts.get("frog_white", 0) == 3:
            return self.WINNINGS["three_frogs_white"]
        elif counts.get("frog_orange", 0) == 3:
            return self.WINNINGS["three_frogs_orange"]
        elif counts.get("frog_green", 0) == 1 and counts.get("frog_orange", 0) == 1 and counts.get("frog_white", 0) == 1:
            return self.WINNINGS["three_frogs_all_colors"]
        return 0

    def draw(self):
        pass

    def play(self):
        self.reels = [] #убрать после тестов
        self.spin()
        self.winning = self.calculate_winnings(self.reels)

        # print("Slot Machine Result:")
        # for row in self.reels:
        #     print(" | ".join(row))
        #
        # if self.winning > 0:
        #     print(f"Congratulations! You won {self.winning} credits!")
        # else:
        #     print("No luck this time! Try again.")
        return self.winning


class Roulette:
    COLORS = {
        0: 'green', 1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red', 6: 'black',
        7: 'red', 8: 'black', 9: 'red', 10: 'black', 11: 'black', 12: 'red',
        13: 'black', 14: 'red', 15: 'black', 16: 'red', 17: 'black', 18: 'red',
        19: 'red', 20: 'black', 21: 'red', 22: 'black', 23: 'red', 24: 'black',
        25: 'red', 26: 'black', 27: 'red', 28: 'black', 29: 'black', 30: 'red',
        31: 'black', 32: 'red', 33: 'black', 34: 'red', 35: 'black', 36: 'red'
    }
    MULTIPLIERS = {
        "straight": 36,
        "color": 2, "even_odd": 2, "high_low": 2,
        "dozen": 3, "row": 3,
        "sixline": 6
    }
    DOZEN_RANGES = {
        1: range(1, 13),
        2: range(13, 25),
        3: range(25, 37)
    }
    ROW_MODULO = {
        1: 1,
        2: 2,
        3: 0
    }
    SIXLINE_RANGES = {
        1: range(1, 7),
        2: range(7, 13),
        3: range(13, 19),
        4: range(19, 25),
        5: range(25, 31),
        6: range(31, 37)
    }
    LOW_RANGE = range(1, 19)
    HIGH_RANGE = range(19, 37)
    EVEN_NUMBERS = [i for i in range(1, 37) if i % 2 == 0]
    ODD_NUMBERS = [i for i in range(1, 37) if i % 2 != 0]

    def __init__(self, player):
        self.player = player
        self.numbers = list(range(0, 37))
        self.bets = []
        self.result = None

    def place_bet(self, category, value, amount):
        self.bets.append({"category": category, "value": value, "amount": amount})

    def overall_bet(self):
        return sum(bet["amount"] for bet in self.bets)

    def spin(self):
        self.result = random.choice(self.numbers)

    def calculate_payout(self):
        payout = {
            "total_winnings": 0,
            "winning_bets": []
        }

        for bet in self.bets:
            winnings = self._calculate_individual_payout(bet)
            if winnings > 0:
                payout["total_winnings"] += winnings
                payout["winning_bets"].append({
                    "category": bet["category"],
                    "value": bet["value"],
                    "amount": bet["amount"],
                    "winnings": winnings
                })
        return payout

    def _calculate_individual_payout(self, bet):
        category = bet["category"]
        value = bet["value"]
        amount = bet["amount"]

        if category == "straight":
            return amount * self.MULTIPLIERS["straight"] if self.result == value else 0
        if category == "color":
            return amount * self.MULTIPLIERS["color"] if self.COLORS[self.result] == value else 0
        if category == "even_odd":
            if value == "even" and self.result in self.EVEN_NUMBERS:
                return amount * self.MULTIPLIERS["even_odd"]
            if value == "odd" and self.result in self.ODD_NUMBERS:
                return amount * self.MULTIPLIERS["even_odd"]
        if category == "high_low":
            if value == "high" and self.result in self.HIGH_RANGE:
                return amount * self.MULTIPLIERS["high_low"]
            if value == "low" and self.result in self.LOW_RANGE:
                return amount * self.MULTIPLIERS["high_low"]
        if category == "dozen":
            return amount * self.MULTIPLIERS["dozen"] if self.result in self.DOZEN_RANGES.get(value) else 0
        if category == "row":
            return amount * self.MULTIPLIERS["row"] if self.result % 3 == self.ROW_MODULO.get(value) else 0
        if category == "sixline":
            return amount * self.MULTIPLIERS["sixline"] if self.result in self.SIXLINE_RANGES.get(value) else 0
        return 0

class Yahtzee:
    WINNING_COMBINATIONS = {
            "yahtzee": 25,
            "four-of-a-kind": 3,
            "full-house": 2,
            "three-of-a-kind": 1.5,
            "small-straight": 5,
            "large-straight": 10
        }

    def __init__(self, player):
        self.player = player
        self.bet = 0
        self.dice = [0] * 5
        self.reroll_indexes = []
        self.winning_combination = None
        self.winnings = 0


    def place_bet(self, amount):
        self.bet = amount

    def roll_dice(self):
        self.dice = [random.randint(1, 6) for _ in range(5)]
        return self.dice

    def set_reroll(self, index):
        self.reroll_indexes.append(index)

    def reroll_dice(self):
        for i in self.reroll_indexes:
            self.dice[i] = random.randint(1, 6)
        return self.dice

    def check_winning_combinations(self):
        counts = Counter(self.dice)
        unique_values = sorted(counts.keys())
        counts_values = list(counts.values())

        if 5 in counts_values:
            self.winning_combination = "yahtzee"

        elif 4 in counts_values:
            self.winning_combination = "four-of-a-kind"

        elif 3 in counts_values:
            self.winning_combination = "three-of-a-kind"

        elif sorted(counts_values) == [2, 3]:
            self.winning_combination = "full-house"

        elif any(all(x in unique_values for x in straight) for straight in [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]):
            self.winning_combination = "small-straight"

        elif unique_values == [1, 2, 3, 4, 5] or unique_values == [2, 3, 4, 5, 6]:
            self.winning_combination = "large-straight"

    def calculate_winnings(self):
        self.winnings = int(self.bet * self.WINNING_COMBINATIONS[self.winning_combination])
