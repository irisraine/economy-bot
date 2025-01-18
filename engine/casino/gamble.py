import random
import io
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import engine.casino.config as config


class SlotMachine:
    REEL = {
        'low': (['frog_green'] * 3 + ['frog_orange'] * 2 + ['frog_white']),
        'high': (['gold'] * 1 + ['cart'] * 2 + ['star'] * 3 + ['horseshoe'] * 4 + ['moonshine'] * 5 +
            ['frog_green'] * 16 + ['frog_orange'] * 8 + ['frog_white'] * 4)
    }
    PREDEFINED_OUTCOMES = {
        'winning': {
            'three_gold': {
                'probability_range': (0, 0.01),
                'reel': ['gold'] * 3
            },
            'three_cart': {
                'probability_range': (0.01, 0.03),
                'reel': ['cart'] * 3
            },
            'three_star': {
                'probability_range': (0.03, 0.055),
                'reel': ['star'] * 3
            },
            'three_horseshoe': {
                'probability_range': (0.055, 0.08),
                'reel': ['horseshoe'] * 3
            },
            'three_moonshine': {
                'probability_range': (0.08, 0.15),
                'reel': ['moonshine'] * 3
            },
            'two_gold': {
                'probability_range': (0.15, 0.3),
                'reel': ['gold'] * 2
            },
            'one_gold': {
                'probability_range': (0.3, 1.0),
                'reel': ['gold'] * 1
            },
        },
        'near_winning': {
            'cart': {
                'probability_range': (0, 0.15),
                'reel': ['cart'] * 2
            },
            'star': {
                'probability_range': (0.15, 0.40),
                'reel': ['star'] * 2
            },
            'horseshoe': {
                'probability_range': (0.40, 0.60),
                'reel': ['horseshoe'] * 2
            },
            'moonshine': {
                'probability_range': (0.60, 0.75),
                'reel': ['moonshine'] * 2
            },
            'frog': {
                'probability_range': (0.75, 1.0),
                'reel': [random.choice(['frog_green', 'frog_orange', 'frog_white'])] * 2
            },
        }
    }
    THRESHOLDS_FOR_PREDEFINED_OUTCOMES = {
        'winning': 0.2,
        'near_winning': 0.4,
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
            predefined_outcome = None
            roll_for_predefined_outcome_category = random.random()
            if roll_for_predefined_outcome_category < self.THRESHOLDS_FOR_PREDEFINED_OUTCOMES['winning']:
                predefined_outcome = 'winning'
            elif roll_for_predefined_outcome_category < self.THRESHOLDS_FOR_PREDEFINED_OUTCOMES['near_winning']:
                predefined_outcome = 'near_winning'
            if predefined_outcome:
                roll_for_predefined_outcome_type = random.random()
                for outcome in self.PREDEFINED_OUTCOMES[predefined_outcome].values():
                    lower_bound, upper_bound = outcome['probability_range']
                    if lower_bound <= roll_for_predefined_outcome_type < upper_bound:
                        central_line = outcome['reel'][:]
                        break
        if central_line:
            if len(central_line) == 2:
                central_line.append(self.__reel())
            elif len(central_line) == 1:
                central_line.extend([self.__reel() for _ in range(2)])
            random.shuffle(central_line)
            self.__reels.append([self.__reel() for _ in range(3)])
            self.__reels.append(central_line)
            self.__reels.append([self.__reel() for _ in range(3)])
        else:
            self.__reels = [[self.__reel() for _ in range(3)] for _ in range(3)]

    def __calculate_payout(self, reels):
        central_line = reels[1]
        counts = {symbol: central_line.count(symbol) for symbol in set(central_line)}

        if self.__bet_type == "high":
            if counts.get("gold", 0) == 3:
                return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_gold"]
            elif counts.get("cart", 0) == 3:
                return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_cart"]
            elif counts.get("star", 0) == 3:
                return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_star"]
            elif counts.get("horseshoe", 0) == 3:
                return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_horseshoe"]
            elif counts.get("moonshine", 0) == 3:
                return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_moonshine"]
            elif counts.get("gold", 0) == 2:
                return config.SLOT_MACHINE_PAYOUT_AMOUNTS["two_gold"]
            elif counts.get("gold", 0) == 1:
                return config.SLOT_MACHINE_PAYOUT_AMOUNTS["one_gold"]
        if counts.get("frog_green", 0) == 3:
            return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_frogs_green"][self.__bet_type]
        elif counts.get("frog_white", 0) == 3:
            return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_frogs_white"][self.__bet_type]
        elif counts.get("frog_orange", 0) == 3:
            return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_frogs_orange"][self.__bet_type]
        elif counts.get("frog_green", 0) == 1 and counts.get("frog_orange", 0) == 1 and counts.get("frog_white", 0) == 1:
            return config.SLOT_MACHINE_PAYOUT_AMOUNTS["three_frogs_all_colors"][self.__bet_type]
        return 0

    def place_bet(self, bet_type):
        self.__bet_type = bet_type

    def play(self):
        self.__spin()
        self.__payout = self.__calculate_payout(self.__reels)

    def draw(self):
        slot_size = config.SLOT_MACHINE_DIMENSIONS["slot_size"]
        grid_width = config.SLOT_MACHINE_DIMENSIONS["grid_size"]["width"]
        grid_height = config.SLOT_MACHINE_DIMENSIONS["grid_size"]["height"]
        horizontal_margin = config.SLOT_MACHINE_DIMENSIONS["margin"]["horizontal"]
        left_margin = config.SLOT_MACHINE_DIMENSIONS["margin"]["left"]
        right_margin = config.SLOT_MACHINE_DIMENSIONS["margin"]["right"]
        crop_top = config.SLOT_MACHINE_DIMENSIONS["crop"]["top"]
        crop_bottom = config.SLOT_MACHINE_DIMENSIONS["crop"]["bottom"]
        grid_x_offset = config.SLOT_MACHINE_DIMENSIONS["grid_offset"]["x"]
        grid_y_offset = config.SLOT_MACHINE_DIMENSIONS["grid_offset"]["y"]
        payline_x_offset = config.SLOT_MACHINE_DIMENSIONS["payline_offset"]["x"]
        payline_y_offset = config.SLOT_MACHINE_DIMENSIONS["payline_offset"]["y"]

        slot_machine_bg = Image.open(config.SLOT_MACHINE_REELS_BLANK)
        payline = Image.open(config.SLOT_MACHINE_PAYLINE)
        symbols = {
            key: Image.open(config.SLOT_MACHINE_REEL_SYMBOLS[key]["image"])
            for key in config.SLOT_MACHINE_REEL_SYMBOLS
        }
        grid = Image.new("RGBA", (grid_width, grid_height), (0, 0, 0, 0))
        for row in range(3):
            for col in range(3):
                x_offset = col * slot_size + (left_margin if col == 1 else left_margin + right_margin if col == 2 else 0)
                y_offset = row * (slot_size + horizontal_margin)
                grid.paste(symbols[self.__reels[row][col]], (x_offset, y_offset))
        cropped_grid = grid.crop((0, crop_top, grid_width, grid_height - crop_bottom))
        slot_machine_bg.paste(cropped_grid, (grid_x_offset, grid_y_offset), cropped_grid)
        slot_machine_bg.paste(payline, (payline_x_offset, payline_y_offset), payline)
        self.__image = io.BytesIO()
        slot_machine_bg.save(self.__image, format='JPEG')
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
            'table': None, 'wheel': None
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

        if category == "straight":
            return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["straight"] if self.__sector['number'] == value else 0
        if category == "color":
            return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["color"] if self.__sector['color'] == value else 0
        if category == "even_odd":
            if value == "even" and self.__sector['number'] in self.EVEN_NUMBERS:
                return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["even_odd"]
            if value == "odd" and self.__sector['number'] in self.ODD_NUMBERS:
                return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["even_odd"]
        if category == "high_low":
            if value == "high" and self.__sector['number'] in self.HIGH_RANGE:
                return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["high_low"]
            if value == "low" and self.__sector['number'] in self.LOW_RANGE:
                return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["high_low"]
        if category == "dozen":
            return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["dozen"] if self.__sector['number'] in self.DOZEN_RANGES.get(value) else 0
        if category == "row":
            return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["row"] if self.__sector['number'] % 3 == self.ROW_MODULO.get(value) else 0
        if category == "sixline":
            return amount * config.ROULETTE_PAYOUT_MULTIPLIERS["sixline"] if self.__sector['number'] in self.SIXLINE_RANGES.get(value) else 0
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
            table = Image.open(config.ROULETTE_TABLE)
            chip = Image.open(config.ROULETTE_CHIP)
            font = ImageFont.truetype("arial.ttf", 20)
            for bet in self.__bets:
                category, value, amount = bet["category"], bet["value"], bet["amount"]
                chip_with_text = chip.copy()
                draw = ImageDraw.Draw(chip_with_text)
                text = str(amount)
                text_width = int(draw.textlength(text, font))
                text_height = font.size
                text_x = (chip_with_text.width - text_width) // 2
                text_y = (chip_with_text.height - text_height) // 2
                draw.text((text_x - 1, text_y - 1), text, fill="white", font=font)
                chip_x_position, chip_y_position = config.ROULETTE_CHIP_POSITIONS.get(category).get(value)
                table.paste(chip_with_text, (chip_x_position, chip_y_position), chip_with_text)
            self.__images['table'] = io.BytesIO()
            table.save(self.__images['table'], format='JPEG')
            return self.__images['table'].getvalue()

        if image_type == "wheel":
            wheel = Image.open(config.ROULETTE_WHEEL)
            ball = Image.open(config.ROULETTE_BALL)
            position = config.ROULETTE_BALL_POSITIONS[self.__sector['number']]
            wheel.paste(ball, position, ball)
            self.__images['wheel'] = io.BytesIO()
            wheel.save(self.__images['wheel'], format='JPEG')
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

        if 5 in counts_values:
            self.__roll_outcome['winning_combination'] = "yahtzee"
        elif 4 in counts_values:
            self.__roll_outcome['winning_combination'] = "four_of_a_kind"
        elif sorted(counts_values) == [2, 3]:
            self.__roll_outcome['winning_combination'] = "full_house"
        elif 3 in counts_values:
            self.__roll_outcome['winning_combination'] = "three_of_a_kind"
        elif unique_values == [1, 2, 3, 4, 5] or unique_values == [2, 3, 4, 5, 6]:
            self.__roll_outcome['winning_combination'] = "large_straight"
        elif any(all(x in unique_values for x in straight) for straight in [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]):
            self.__roll_outcome['winning_combination'] = "small_straight"

        if self.__roll_outcome['winning_combination']:
            self.__payout = int(self.bet * config.YAHTZEE_PAYOUT_MULTIPLIERS[self.__roll_outcome['winning_combination']])

    def place_bet(self, bet):
        self.__bet = bet

    def set_reroll(self, index):
        self.__reroll_indexes.append(index)

    def play(self):
        self.__roll_dice()
        self.__calculate_payout()

    def draw(self):
        table = Image.open(config.YAHTZEE_TABLE)
        table_width, table_height = table.size

        dice_images = [Image.open(config.YAHTZEE_DICE[i]) for i in range(1, 7)]
        dice_size, _ = dice_images[0].size

        total_dice_width = len(self.__roll_outcome['dice']) * dice_size
        start_x = (table_width - total_dice_width) // 2
        start_y = (table_height - dice_size) // 2

        for i, die in enumerate(self.__roll_outcome['dice']):
            x_offset = start_x + i * dice_size
            y_offset = start_y
            die_image = dice_images[die - 1]
            table.paste(die_image, (x_offset, y_offset), die_image)

        self.__image = io.BytesIO()
        table.save(self.__image, format='JPEG')
        return self.__image.getvalue()
