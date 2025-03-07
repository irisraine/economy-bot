import random
import io
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import engine.casino.config as config


class SlotMachine:
    REEL = {
        'low': (['frog_green'] * 5 + ['frog_orange'] * 4 + ['frog_white'] * 3),
        'high': (['gold'] * 1 + ['cart'] * 2 + ['star'] * 3 + ['horseshoe'] * 4 + ['moonshine'] * 5 +
                 ['frog_green'] * 10 + ['frog_orange'] * 8 + ['frog_white'] * 6)
    }
    PREDEFINED_OUTCOMES = {
        'winning': {
            ('cart', 'cart', 'cart'): (0, 0.01),
            ('star', 'star', 'star'): (0.01, 0.02),
            ('horseshoe', 'horseshoe', 'horseshoe'): (0.02, 0.035),
            ('moonshine', 'moonshine', 'moonshine'): (0.035, 0.1),
            ('frog_white', 'frog_white', 'frog_white'): (0.1, 0.2),
            ('frog_orange', 'frog_orange', 'frog_orange'): (0.2, 0.35),
            ('gold', 'gold'): (0.35, 0.5),
            ('frog_green', 'frog_green', 'frog_green'): (0.5, 0.7),
            ('gold',): (0.7, 1.0)
        },
        'near_winning': {
            ('cart', 'cart'): (0, 0.1),
            ('star', 'star'): (0.1, 0.25),
            ('horseshoe', 'horseshoe'): (0.25, 0.4),
            ('moonshine', 'moonshine'): (0.4, 0.6),
            ('frog_white', 'frog_white'): (0.6, 0.7),
            ('frog_orange', 'frog_orange'): (0.7, 0.8),
            ('frog_green', 'frog_green'): (0.8, 1.0),
        }
    }
    THRESHOLDS_FOR_PREDEFINED_OUTCOMES = {
        'winning': 0.3,
        'near_winning': 0.5,
    }

    def __init__(self, player):
        self.__player = player
        self.__bet_type = None
        self.__reels = []
        self.__payout = 0
        self.__image = None

    @property
    def player(self):
        return self.__player

    @property
    def bet(self):
        return config.SLOT_MACHINE_BET_AMOUNTS[self.__bet_type]

    @property
    def reels(self):
        return self.__reels

    @property
    def payout(self):
        return self.__payout

    def __reel(self):
        return random.choice(self.REEL[self.__bet_type])

    def __spin(self):
        central_line = []
        if self.__bet_type == 'high':
            roll_for_category = random.random()
            predefined_outcome = None
            if roll_for_category < self.THRESHOLDS_FOR_PREDEFINED_OUTCOMES['winning']:
                predefined_outcome = 'winning'
            elif roll_for_category < self.THRESHOLDS_FOR_PREDEFINED_OUTCOMES['near_winning']:
                predefined_outcome = 'near_winning'
            if predefined_outcome:
                roll_for_type = random.random()
                for reel, probability_range in self.PREDEFINED_OUTCOMES[predefined_outcome].items():
                    lower_bound, upper_bound = probability_range
                    if lower_bound <= roll_for_type < upper_bound:
                        central_line.extend(reel)
                        break
        if central_line:
            while len(central_line) < 3:
                central_line.append(self.__reel())
            random.shuffle(central_line)
            self.__reels = [
                [self.__reel() for _ in range(3)],
                central_line,
                [self.__reel() for _ in range(3)],
            ]
        else:
            self.__reels = [[self.__reel() for _ in range(3)] for _ in range(3)]

    def __calculate_payout(self, reels):
        central_line = reels[1]
        symbol_counts = {symbol: central_line.count(symbol) for symbol in set(central_line)}
        for symbol, payouts in config.SLOT_MACHINE_PAYOUT_AMOUNTS.items():
            count = symbol_counts.get(symbol, 0)
            if count in payouts:
                self.__payout = payouts[count]
                return

    def place_bet(self, bet_type):
        self.__bet_type = bet_type

    def play(self):
        self.__spin()
        self.__calculate_payout(self.__reels)

    def draw(self):
        slot_machine_frame = Image.open(config.SLOT_MACHINE_FRAME)
        payline = Image.open(config.SLOT_MACHINE_PAYLINE)
        symbols = {
            key: Image.open(config.SLOT_MACHINE_REEL_SYMBOLS[key]["image"])
            for key in config.SLOT_MACHINE_REEL_SYMBOLS
        }
        grid = Image.new("RGBA", config.SLOT_MACHINE_DIMENSIONS["grid_size"], (0, 0, 0, 0))
        for row in range(3):
            for col in range(3):
                symbol_position = config.SLOT_MACHINE_DIMENSIONS["symbol_positions"][row][col]
                grid.paste(symbols[self.__reels[row][col]], symbol_position)
        slot_machine_frame.paste(grid, config.SLOT_MACHINE_DIMENSIONS["grid_offset"], grid)
        slot_machine_frame.paste(payline, config.SLOT_MACHINE_DIMENSIONS["payline_offset"], payline)
        self.__image = io.BytesIO()
        slot_machine_frame.save(self.__image, format='JPEG')
        return self.__image.getvalue()


class Roulette:
    NUMBERS = list(range(0, 37))
    COLORS = {
        0: 'green', 1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red', 6: 'black',
        7: 'red', 8: 'black', 9: 'red', 10: 'black', 11: 'black', 12: 'red',
        13: 'black', 14: 'red', 15: 'black', 16: 'red', 17: 'black', 18: 'red',
        19: 'red', 20: 'black', 21: 'red', 22: 'black', 23: 'red', 24: 'black',
        25: 'red', 26: 'black', 27: 'red', 28: 'black', 29: 'black', 30: 'red',
        31: 'black', 32: 'red', 33: 'black', 34: 'red', 35: 'black', 36: 'red'
    }
    LOW_RANGE = range(1, 19)
    HIGH_RANGE = range(19, 37)
    EVEN_NUMBERS = [i for i in range(1, 37) if i % 2 == 0]
    ODD_NUMBERS = [i for i in range(1, 37) if i % 2 != 0]
    DOZEN_RANGES = {
        1: range(1, 13),
        2: range(13, 25),
        3: range(25, 37)
    }
    ROW_RANGES = {
        1: [i for i in range(1, 37, 3)],
        2: [i for i in range(2, 37, 3)],
        3: [i for i in range(3, 37, 3)]
    }
    SIXLINE_RANGES = {
        1: range(1, 7),
        2: range(7, 13),
        3: range(13, 19),
        4: range(19, 25),
        5: range(25, 31),
        6: range(31, 37)
    }

    def __init__(self, player):
        self.__player = player
        self.__bets = []
        self.__sector = {
            'number': None,
            'color': ""
        }
        self.__winnings = {
            'total_payout': 0,
            'winning_bets': []
        }
        self.__images = {
            'table': None,
            'wheel': None
        }

    @property
    def player(self):
        return self.__player

    @property
    def bets(self):
        return self.__bets

    @property
    def sector(self):
        return self.__sector

    @property
    def winnings(self):
        return self.__winnings

    def __spin(self):
        number = random.choice(self.NUMBERS)
        self.__sector = {'number': number, 'color': self.COLORS[number]}

    def __calculate_payout(self):
        for bet in self.__bets:
            single_payout = self.__calculate_individual_payout(bet)
            if single_payout > 0:
                self.__winnings["total_payout"] += single_payout
                self.__winnings["winning_bets"].append({
                    "category": bet["category"],
                    "value": bet["value"],
                    "amount": bet["amount"],
                    "winnings": single_payout
                })

    def __calculate_individual_payout(self, bet):
        category, value, amount = bet["category"], bet["value"], bet["amount"]
        number, color = self.__sector['number'], self.__sector['color']

        conditions = {
            "straight": lambda: number == value,
            "color": lambda: color == value,
            "even_odd": lambda: (value == "even" and number in self.EVEN_NUMBERS) or
                                (value == "odd" and number in self.ODD_NUMBERS),
            "high_low": lambda: (value == "high" and number in self.HIGH_RANGE) or
                                (value == "low" and number in self.LOW_RANGE),
            "dozen": lambda: number in self.DOZEN_RANGES.get(value),
            "row": lambda: number in self.ROW_RANGES.get(value),
            "sixline": lambda: number in self.SIXLINE_RANGES.get(value)
        }
        if conditions[category]():
            return amount * config.ROULETTE_PAYOUT_MULTIPLIERS[category]
        return 0

    def place_bet(self, category, value, amount):
        for bet in self.__bets:
            if bet["category"] == category and bet["value"] == value:
                bet["amount"] = amount
                return
        self.__bets.append({"category": category, "value": value, "amount": amount})

    def overall_bet(self):
        return sum(bet["amount"] for bet in self.__bets)

    def play(self):
        self.__spin()
        self.__calculate_payout()

    def draw(self, image_type):
        if image_type == "table":
            roulette_table = Image.open(config.ROULETTE_TABLE)
            chip = Image.open(config.ROULETTE_CHIP)
            font = ImageFont.truetype(config.ROULETTE_CHIP_FONT, 20)
            for bet in self.__bets:
                category, value, amount = bet["category"], bet["value"], bet["amount"]
                chip_with_bet_amount = chip.copy()
                draw = ImageDraw.Draw(chip_with_bet_amount)
                bet_amount = str(amount)
                bet_amount_position = config.ROULETTE_DIMENSIONS["bet_amount"][len(bet_amount)]
                draw.text(bet_amount_position, bet_amount, fill="white", font=font)
                chip_position = config.ROULETTE_DIMENSIONS['chip'].get(category).get(value)
                roulette_table.paste(chip_with_bet_amount, chip_position, chip_with_bet_amount)
            self.__images['table'] = io.BytesIO()
            roulette_table.save(self.__images['table'], format='JPEG')
            return self.__images['table'].getvalue()

        if image_type == "wheel":
            roulette_wheel = Image.open(config.ROULETTE_WHEEL)
            ball = Image.open(config.ROULETTE_BALL)
            position = config.ROULETTE_DIMENSIONS['ball'][self.__sector['number']]
            roulette_wheel.paste(ball, position, ball)
            self.__images['wheel'] = io.BytesIO()
            roulette_wheel.save(self.__images['wheel'], format='JPEG')
            return self.__images['wheel'].getvalue()


class Yahtzee:
    def __init__(self, player):
        self.__player = player
        self.__bet = 0
        self.__roll_outcome = {
            'dice': [0] * 5,
            'winning_combination': ""
        }
        self.__reroll_indexes = []
        self.__payout = 0
        self.__image = None

    @property
    def player(self):
        return self.__player

    @property
    def bet(self):
        return self.__bet

    @property
    def reroll_indexes(self):
        return self.__reroll_indexes

    @property
    def roll_outcome(self):
        return self.__roll_outcome

    @property
    def payout(self):
        return self.__payout

    def __roll_dice(self):
        if not self.__reroll_indexes:
            self.__roll_outcome['dice'] = [random.randint(1, 6) for _ in range(5)]
        else:
            for i in self.__reroll_indexes:
                self.__roll_outcome['dice'][i] = random.randint(1, 6)

    def __calculate_payout(self):
        counts = Counter(self.__roll_outcome['dice'])
        unique_values = sorted(counts.keys())
        counts_values = list(counts.values())
        conditions = {
            "yahtzee": lambda: 5 in counts_values,
            "four_of_a_kind": lambda: 4 in counts_values,
            "full_house": lambda: sorted(counts_values) == [2, 3],
            "large_straight": lambda: unique_values == [1, 2, 3, 4, 5] or unique_values == [2, 3, 4, 5, 6],
            "small_straight": lambda: any(all(x in unique_values for x in straight)
                                          for straight in [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])
        }
        for combination, condition in conditions.items():
            if condition():
                self.__roll_outcome['winning_combination'] = combination
                self.__payout = round(self.bet * config.YAHTZEE_PAYOUT_MULTIPLIERS[combination])
                break

    def place_bet(self, bet):
        self.__bet = bet

    def set_reroll(self, index):
        self.__reroll_indexes.append(index)

    def play(self):
        self.__roll_dice()
        self.__calculate_payout()

    def draw(self):
        yahtzee_table = Image.open(config.YAHTZEE_TABLE)
        dice_images = [Image.open(config.YAHTZEE_DICE[i]) for i in range(1, 7)]
        for i, die in enumerate(self.__roll_outcome['dice']):
            die_image = dice_images[die - 1]
            die_position = config.YAHTZEE_DIMENSIONS['dice_positions'][i]
            yahtzee_table.paste(die_image, die_position, die_image)
        self.__image = io.BytesIO()
        yahtzee_table.save(self.__image, format='JPEG')
        return self.__image.getvalue()
