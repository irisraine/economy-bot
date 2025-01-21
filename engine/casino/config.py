CASINO_ENTRANCE = "assets/casino/casino_entrance.jpg"
CASINO_FRAUD_BAN = "assets/casino/casino_fraud_ban.jpg"
CASINO_WRONG_PLAYER = "assets/casino/casino_wrong_player.jpg"

SEPARATOR_CONFIRM = "assets/casino/separator_confirm.png"
SEPARATOR_ERROR = "assets/casino/separator_error.png"

ROULETTE = "assets/casino/roulette.jpg"
ROULETTE_TABLE = "assets/casino/roulette_table.jpg"
ROULETTE_CHIP = "assets/casino/roulette_chip.png"
ROULETTE_WHEEL = "assets/casino/roulette_wheel.jpg"
ROULETTE_BALL = "assets/casino/roulette_ball.png"
ROULETTE_DIMENSIONS = {
    "chip": {
        "straight": {
            0: (20, 150),
            1: (72, 218), 2: (72, 150), 3: (72, 82), 4: (122, 218), 5: (122, 150), 6: (122, 82),
            7: (172, 218), 8: (172, 150), 9: (172, 82), 10: (222, 218), 11: (222, 150), 12: (222, 82),
            13: (272, 218), 14: (272, 150), 15: (272, 82), 16: (322, 218), 17: (322, 150), 18: (322, 82),
            19: (372, 218), 20: (372, 150), 21: (372, 82), 22: (422, 218), 23: (422, 150), 24: (422, 82),
            25: (472, 218), 26: (472, 150), 27: (472, 82), 28: (522, 218), 29: (522, 150), 30: (522, 82),
            31: (572, 218), 32: (572, 150), 33: (572, 82), 34: (622, 218), 35: (622, 150), 36: (622, 82)
        },
        "color": {
            "red": (297, 332),
            "black": (397, 332)
        },
        "even_odd": {
            "even": (197, 332),
            "odd": (497, 332)
        },
        "high_low": {
            "high": (597, 332),
            "low": (97, 332)
        },
        "dozen": {
            1: (145, 279), 2: (345, 279), 3: (545, 279)
        },
        "row": {
            1: (672, 218), 2: (672, 150), 3: (672, 82)
        },
        "sixline": {
            1: (97, 252), 2: (197, 252), 3: (297, 252), 4: (397, 252), 5: (497, 252), 6: (597, 252)
        },
    },
    "ball": {
        0: (384, 64),
        32: (408, 66), 15: (431, 72), 19: (452, 83), 4: (469, 97), 21: (486, 114), 2: (501, 132),
        25: (510, 153), 17: (517, 175), 34: (519, 199), 6: (517, 221), 27: (514, 244), 13: (504, 265),
        36: (493, 285), 11: (478, 303), 30: (459, 317), 8: (440, 328), 23: (419, 336), 10: (396, 341),
        5: (373, 341), 24: (350, 336), 16: (329, 329), 33: (309, 317), 1: (292, 302), 20: (276, 284),
        14: (264, 265), 31: (255, 245), 9: (251, 222), 22: (250, 198), 18: (252, 175), 29: (259, 153),
        7: (270, 132), 28: (282, 112), 12: (299, 97), 35: (318, 83), 3: (339, 75), 26: (361, 67)
    },
    "bet_amount": {
        1: (15, 10),
        2: (10, 10),
    }
}
ROULETTE_PAYOUT_MULTIPLIERS = {
    "straight": 36,
    "color": 2, "even_odd": 2, "high_low": 2,
    "dozen": 3, "row": 3,
    "sixline": 6
}

SLOT_MACHINE = "assets/casino/slot_machine.jpg"
SLOT_MACHINE_FRAME = "assets/casino/slot_machine_frame.jpg"
SLOT_MACHINE_REEL_SYMBOLS = {
    "gold": {
        "image": "assets/casino/slot_machine_reel_gold.png",
        "emoji": "<:gold:1327365509359997039>"
    },
    "cart": {
        "image": "assets/casino/slot_machine_reel_cart.png",
        "emoji": "<:cart:1327365671218057307>"
    },
    "star": {
        "image": "assets/casino/slot_machine_reel_star.png",
        "emoji": "<:str:1327365588535742666>"
    },
    "horseshoe": {
        "image": "assets/casino/slot_machine_reel_horseshoe.png",
        "emoji": "<:horseshoe:1327365621259829349>"
    },
    "moonshine": {
        "image": "assets/casino/slot_machine_reel_moonshine.png",
        "emoji": "<:moonshine:1327365697906544751>"
    },
    "frog_green": {
        "image": "assets/casino/slot_machine_reel_frog_green.png",
        "emoji": "<:1frg:1286272480083836970>"},
    "frog_orange": {
        "image": "assets/casino/slot_machine_reel_frog_orange.png",
        "emoji": "<:2frg:1327365446361415791>"},
    "frog_white": {
        "image": "assets/casino/slot_machine_reel_frog_white.png",
        "emoji": "<:3frg:1327365491781799978>"
    },
}
SLOT_MACHINE_PAYLINE = "assets/casino/slot_machine_payline.png"
SLOT_MACHINE_DIMENSIONS = {
    "grid_size": (312, 161),
    "symbol_positions": {
        0: [(0, -27), (122, -27), (248, -27)],
        1: [(0, 47), (122, 47), (248, 47)],
        2: [(0, 121), (122, 121), (248, 121)]
    },
    "grid_offset": (240, 110),
    "payline_offset": (220, 185)
}
SLOT_MACHINE_BET_AMOUNTS = {
    "low": 3,
    "high": 8
}
SLOT_MACHINE_PAYOUT_AMOUNTS = {
    "gold": {3: 300, 2: 20, 1: 8},
    "cart": {3: 200},
    "star": {3: 100},
    "horseshoe": {3: 50},
    "moonshine": {3: 25},
    "frog_white": {3: 18},
    "frog_orange": {3: 12},
    "frog_green": {3: 10},
}

YAHTZEE = "assets/casino/yahtzee.jpg"
YAHTZEE_TABLE = "assets/casino/yahtzee_table.jpg"
YAHTZEE_DICE = {
    1: "assets/casino/yahtzee_dice_1.png",
    2: "assets/casino/yahtzee_dice_2.png",
    3: "assets/casino/yahtzee_dice_3.png",
    4: "assets/casino/yahtzee_dice_4.png",
    5: "assets/casino/yahtzee_dice_5.png",
    6: "assets/casino/yahtzee_dice_6.png",
}
YAHTZEE_DIMENSIONS = {
    "dice_positions": [(150, 121), (250, 121), (350, 121), (450, 121), (550, 121)]
}
YAHTZEE_PAYOUT_MULTIPLIERS = {
    "small_straight": 1.5,
    "full_house": 2,
    "four_of_a_kind": 2.5,
    "large_straight": 4,
    "yahtzee": 10
}
