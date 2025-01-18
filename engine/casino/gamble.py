import random
import io
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import engine.casino.config as config


class SlotMachine:
    BET_AMOUNTS = {
        'low': 4,
        'high': 8
    }
    PAYOUT_AMOUNTS = {
        'three_gold': 300,
        'three_cart': 100,
        'three_star': 75,
        'three_horseshoe': 50,
        'three_moonshine': 40,
        'two_gold': 25,
        'three_frogs_white': {'low': 20, 'high': 25},
        'three_frogs_orange': {'low': 15, 'high': 20},
        'three_frogs_green': {'low': 7, 'high': 12},
        'three_frogs_all_colors': {'low': 10, 'high': 15},
        'one_gold': 10,
    }
    REEL = {
        'low': (['frog_green'] * 3 + ['frog_orange'] * 2 + ['frog_white']),
        'high': (['gold'] * 1 + ['cart'] * 2 + ['star'] * 3 + ['horseshoe'] * 4 + ['moonshine'] * 5 +
            ['frog_green'] * 16 + ['frog_orange'] * 8 + ['frog_white'] * 4)
    }
    PREDEFINED_OUTCOMES = {
        'winning': {
            'three_gold': {'probability_range': (0, 0.01), 'reel': ['gold'] * 3},
            'three_cart': {'probability_range': (0.01, 0.03), 'reel': ['cart'] * 3},
            'three_star': {'probability_range': (0.03, 0.055), 'reel': ['star'] * 3},
            'three_horseshoe': {'probability_range': (0.055, 0.08), 'reel': ['horseshoe'] * 3},
            'three_moonshine': {'probability_range': (0.08, 0.15), 'reel': ['moonshine'] * 3},
            'two_gold': {'probability_range': (0.15, 0.3), 'reel': ['gold'] * 2},
            'one_gold': {'probability_range': (0.3, 1.0), 'reel': ['gold'] * 1},
        },
        'near_winning': {
            'cart': {'probability_range': (0, 0.15), 'reel': ['cart'] * 2},
            'star': {'probability_range': (0.15, 0.40), 'reel': ['star'] * 2},
            'horseshoe': {'probability_range': (0.40, 0.60), 'reel': ['horseshoe'] * 2},
            'moonshine': {'probability_range': (0.60, 0.75), 'reel': ['moonshine'] * 2},
            'frog': {'probability_range': (0.75, 1.0),'reel': [random.choice(['frog_green', 'frog_orange', 'frog_white'])] * 2},
        }
    }
    THRESHOLDS_FOR_PREDEFINED_OUTCOMES = {
        'winning': 0.25,
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
        return self.BET_AMOUNTS[self.__bet_type]

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
                return self.PAYOUT_AMOUNTS["three_gold"]
            elif counts.get("cart", 0) == 3:
                return self.PAYOUT_AMOUNTS["three_cart"]
            elif counts.get("star", 0) == 3:
                return self.PAYOUT_AMOUNTS["three_star"]
            elif counts.get("horseshoe", 0) == 3:
                return self.PAYOUT_AMOUNTS["three_horseshoe"]
            elif counts.get("moonshine", 0) == 3:
                return self.PAYOUT_AMOUNTS["three_moonshine"]
            elif counts.get("gold", 0) == 2:
                return self.PAYOUT_AMOUNTS["two_gold"]
            elif counts.get("gold", 0) == 1:
                return self.PAYOUT_AMOUNTS["one_gold"]
        if counts.get("frog_green", 0) == 3:
            return self.PAYOUT_AMOUNTS["three_frogs_green"][self.__bet_type]
        elif counts.get("frog_white", 0) == 3:
            return self.PAYOUT_AMOUNTS["three_frogs_white"][self.__bet_type]
        elif counts.get("frog_orange", 0) == 3:
            return self.PAYOUT_AMOUNTS["three_frogs_orange"][self.__bet_type]
        elif counts.get("frog_green", 0) == 1 and counts.get("frog_orange", 0) == 1 and counts.get("frog_white", 0) == 1:
            return self.PAYOUT_AMOUNTS["three_frogs_all_colors"][self.__bet_type]
        return 0

    def place_bet(self, bet_type):
        self.__bet_type = bet_type

    def play(self):
        self.__spin()
        self.__payout = self.__calculate_payout(self.__reels)

    def draw(self):
        slot_size = 64
        horizontal_margin = 10
        left_margin, right_margin = 58, 62
        crop_top, crop_bottom = 27, 24
        grid_x_offset, grid_y_offset = 240, 110
        payline_x_offset, payline_y_offset = 220, 185

        slot_machine_bg = Image.open(config.SLOT_MACHINE_REELS_BLANK)
        payline = Image.open(config.SLOT_MACHINE_PAYLINE)
        symbols = {
            "gold": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["gold"]["image"]),
            "cart": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["cart"]["image"]),
            "star": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["star"]["image"]),
            "horseshoe": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["horseshoe"]["image"]),
            "moonshine": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["moonshine"]["image"]),
            "frog_green": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["frog_green"]["image"]),
            "frog_orange": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["frog_orange"]["image"]),
            "frog_white": Image.open(config.SLOT_MACHINE_REEL_SYMBOLS["frog_white"]["image"]),
        }

        temp_grid_width = slot_size * 3 + left_margin + right_margin
        temp_grid_height = slot_size * 3 + horizontal_margin * 2
        temp_grid = Image.new("RGBA", (temp_grid_width, temp_grid_height), (0, 0, 0, 0))

        for row in range(3):
            for col in range(3):
                x_offset = col * slot_size + (left_margin if col == 1 else (left_margin + right_margin if col == 2 else 0))
                y_offset = row * (slot_size + horizontal_margin)
                temp_grid.paste(symbols[self.__reels[row][col]], (x_offset, y_offset))

        cropped_grid = temp_grid.crop((0, crop_top, temp_grid_width, temp_grid_height - crop_bottom))
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
    PAYOUT_MULTIPLIERS = {
        "straight": 36,
        "color": 2, "even_odd": 2, "high_low": 2,
        "dozen": 3, "row": 3,
        "sixline": 6
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
            return amount * self.PAYOUT_MULTIPLIERS["straight"] if self.__sector['number'] == value else 0
        if category == "color":
            return amount * self.PAYOUT_MULTIPLIERS["color"] if self.__sector['color'] == value else 0
        if category == "even_odd":
            if value == "even" and self.__sector['number'] in self.EVEN_NUMBERS:
                return amount * self.PAYOUT_MULTIPLIERS["even_odd"]
            if value == "odd" and self.__sector['number'] in self.ODD_NUMBERS:
                return amount * self.PAYOUT_MULTIPLIERS["even_odd"]
        if category == "high_low":
            if value == "high" and self.__sector['number'] in self.HIGH_RANGE:
                return amount * self.PAYOUT_MULTIPLIERS["high_low"]
            if value == "low" and self.__sector['number'] in self.LOW_RANGE:
                return amount * self.PAYOUT_MULTIPLIERS["high_low"]
        if category == "dozen":
            return amount * self.PAYOUT_MULTIPLIERS["dozen"] if self.__sector['number'] in self.DOZEN_RANGES.get(value) else 0
        if category == "row":
            return amount * self.PAYOUT_MULTIPLIERS["row"] if self.__sector['number'] % 3 == self.ROW_MODULO.get(value) else 0
        if category == "sixline":
            return amount * self.PAYOUT_MULTIPLIERS["sixline"] if self.__sector['number'] in self.SIXLINE_RANGES.get(value) else 0
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
            zero_x_position, zero_y_position = 20, 150
            first_line_x_position = 72
            line_x_offset = 50
            rows_x_position = 672
            first_row_y_position, second_row_y_position, third_row_y_position = 218, 150, 82
            dozen_x_position, dozen_y_position = 145, 279
            dozen_x_offset = 200
            binary_x_position, binary_y_position = 97, 332
            binary_x_offset = 100
            sixline_x_position, sixline_y_position = 97, 252
            sixline_x_offset = 100
            chip_positions = {
                "straight":
                    {
                        i: (
                            first_line_x_position + ((i - 1) // 3) * line_x_offset,
                            [first_row_y_position, second_row_y_position, third_row_y_position][(i - 1) % 3]
                        ) for i in range(1, 37)
                    } | {0: (zero_x_position, zero_y_position)},
                "color":
                    {
                        "red": (binary_x_position + binary_x_offset * 2, binary_y_position),
                        "black": (binary_x_position + binary_x_offset * 3, binary_y_position)
                    },
                "even_odd":
                    {
                        "even": (binary_x_position + binary_x_offset, binary_y_position),
                        "odd": (binary_x_position + binary_x_offset * 4, binary_y_position)
                    },
                "high_low":
                    {
                        "high": (binary_x_position + binary_x_offset * 5, binary_y_position),
                        "low": (binary_x_position, binary_y_position)
                    },
                "dozen":
                    {
                        i: (dozen_x_position + (i - 1) * dozen_x_offset, dozen_y_position) for i in range(1, 4)
                    },
                "row":
                    {
                        i: (
                            rows_x_position,
                            [first_row_y_position, second_row_y_position, third_row_y_position][i - 1]
                        ) for i in range(1, 4)
                    },
                "sixline":
                    {i: (sixline_x_position + (i - 1) * sixline_x_offset, sixline_y_position) for i in range(1, 7)},
            }
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
                chip_x_position, chip_y_position = chip_positions.get(category).get(value)
                table.paste(chip_with_text, (chip_x_position, chip_y_position), chip_with_text)
            self.__images['table'] = io.BytesIO()
            table.save(self.__images['table'], format='JPEG')
            return self.__images['table'].getvalue()

        if image_type == "wheel":
            ball_positions = {
                0: (384, 64),
                32: (408, 66), 15: (431, 72), 19: (452, 83), 4: (469, 97), 21: (486, 114), 2: (501, 132),
                25: (510, 153), 17: (517, 175), 34: (519, 199), 6: (517, 221), 27: (514, 244), 13: (504, 265),
                36: (493, 285), 11: (478, 303), 30: (459, 317), 8: (440, 328), 23: (419, 336), 10: (396, 341),
                5: (373, 341), 24: (350, 336), 16: (329, 329), 33: (309, 317), 1: (292, 302), 20: (276, 284),
                14: (264, 265), 31: (255, 245), 9: (251, 222), 22: (250, 198), 18: (252, 175), 29: (259, 153),
                7: (270, 132), 28: (282, 112), 12: (299, 97), 35: (318, 83), 3: (339, 75), 26: (361, 67)
            }
            wheel = Image.open(config.ROULETTE_WHEEL)
            ball = Image.open(config.ROULETTE_BALL)
            position = ball_positions[self.__sector['number']]
            wheel.paste(ball, position, ball)
            self.__images['wheel'] = io.BytesIO()
            wheel.save(self.__images['wheel'], format='JPEG')
            return self.__images['wheel'].getvalue()


class Yahtzee:
    PAYOUT_MULTIPLIERS = {
        "three-of-a-kind": 1.5,
        "full-house": 2,
        "four-of-a-kind": 3,
        "small-straight": 5,
        "large-straight": 15,
        "yahtzee": 50
    }

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
            self.__roll_outcome['winning_combination'] = "four-of-a-kind"
        elif sorted(counts_values) == [2, 3]:
            self.__roll_outcome['winning_combination'] = "full-house"
        elif 3 in counts_values:
            self.__roll_outcome['winning_combination'] = "three-of-a-kind"
        elif unique_values == [1, 2, 3, 4, 5] or unique_values == [2, 3, 4, 5, 6]:
            self.__roll_outcome['winning_combination'] = "large-straight"
        elif any(all(x in unique_values for x in straight) for straight in [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]):
            self.__roll_outcome['winning_combination'] = "small-straight"

        if self.__roll_outcome['winning_combination']:
            self.__payout = int(self.bet * self.PAYOUT_MULTIPLIERS[self.__roll_outcome['winning_combination']])

    def place_bet(self, bet):
        self.__bet = bet

    def set_reroll(self, index):
        self.__reroll_indexes.append(index)

    def play(self):
        self.__roll_dice()
        self.__calculate_payout()

    def draw(self):
        desk = Image.open(config.YAHTZEE_TABLE)
        desk_width, desk_height = desk.size

        dice_images = [Image.open(config.YAHTZEE_DICE[i]) for i in range(1, 7)]
        dice_size, _ = dice_images[0].size

        total_dice_width = len(self.__roll_outcome['dice']) * dice_size
        start_x = (desk_width - total_dice_width) // 2
        start_y = (desk_height - dice_size) // 2

        for i, die in enumerate(self.__roll_outcome['dice']):
            x_offset = start_x + i * dice_size
            y_offset = start_y
            die_image = dice_images[die - 1]
            desk.paste(die_image, (x_offset, y_offset), die_image)

        self.__image = io.BytesIO()
        desk.save(self.__image, format='JPEG')
        return self.__image.getvalue()
