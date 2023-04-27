from collections import Counter


allergy_dict = {
    "dairy": ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'sour cream', 'custard', 'evaporated milk', 'condensed milk', 'buttermilk', 'ice cream', 'pudding'],
    "tree-nuts": ['almonds', 'brazil nuts', 'cashews', 'chestnuts', 'filberts', 'hazelnuts', 'hickory nuts', 'macademia', 'pecans', 'pistachios', 'walnuts', 'ginkgo'],
    "soy-bean": ['soybean', 'soy flour', 'soy drink', 'tofu', 'tempeh', 'soy yogurt', 'soy bread', 'soy sauce'],
    "shell-fish": ['crab', 'crayfish', 'lobster', 'shrimp', 'prawns', 'scallops', 'squid', 'mussels', 'snails', 'clams', 'oysters', 'octopus'],
    "fish": ['abalone', 'anchovy', 'arctic char', 'barracuda', 'barramundi', 'bass', 'bass blue gill', 'bass sea', 'bass lake', 'bass striped', 'bass drum', 'black sea bass', 'bluefish', 'bluenose', 'bullhead', 'butterfish', 'capelin', 'carp', 'catfish', 'caviar', 'chilean seabass', 'chub', 'clam', 'cobia', 'cod', 'conch', 'corvina', 'crab', 'crayfish', 'croaker', 'cusk', 'dab', 'drum', 'eel', 'escolar', 'flounder', 'gray sole', 'greater amberjack', 'grenadier', 'grouper', 'haddock', 'hake', 'halfmoon fish', 'halibut', 'harvest fish', 'herring', 'imitation crab', 'jellyfish', 'lingcod', 'lobster', 'mackerel atlantic', 'mackerel spanish', 'mahi mahi', 'marlin', 'monkfish', 'mullet', 'muskellunge', 'mussels', 'ocean pout', 'octopus', 'opah', 'opaleye', 'orange roughy', 'oyster', 'pangasius', 'parrotfish', 'perch', 'perch ocean', 'pickerel', 'pike', 'pilchards', 'plaice', 'pomfret', 'pompano', 'pollock', 'porgy', 'red porgy', 'red snapper', 'rockfish', 'rosefish', 'sablefish', 'salmon atlantic', 'salmon chinook', 'salmon sockeye', 'sanddabs', 'sardine', 'scab', 'scallops', 'scrod', 'scup', 'sea beam', 'sea urchin', 'seatrout', 'shad', 'shark', 'sheepshead fish', 'shrimp', 'skate', 'smelt spearfish', 'snail', 'sole', 'squid', 'striped bass', 'sturgeon', 'sucker', 'sunfish', 'swai', 'swordfish', 'tatoaba', 'tilapia', 'tilefish', 'trout rainbow', 'trout sea', 'trout steelhead', 'tuna albacore', 'tuna bigeye', 'tuna blackfin', 'tuna bluefin', 'tuna tongol', 'tuna yellowfin', 'tuna', 'turbot', 'wahoo', 'walleye', 'weakfish', 'white seabass', 'whitefish', 'whiting', 'wolfish atlantic', 'wreckfish', 'yellowtail'],
    "egg": ["albumin",    "apovitellin",    "cholesterol-free egg substitute",    "dried egg solids",    "egg",    "egg wash",    "eggnog",    "fat substitutes",    "globulin",    "livetin",    "lysozyme",    "mayonnaise",    "meringue",    "ovalbumin",    "ovoglobulin",    "ovomucin",    "ovomucoid",    "ovotransferrin",    "ovovitelia",    "ovovitellin",    "powdered eggs",    "silici albuminate",    "simplesse",    "surimi",    "trailblazer",    "vitellin",    "whole egg",    "dried egg",    "egg white",    "egg yolk",    "egg solids",    "meringue powder"],
    "sesame": ['benne', 'gingelly', 'gomasio', 'sesame flour', 'sesame oil', 'sesame paste', 'sesame salt', 'sesame seed', 'sesamol', 'sesemolina', 'sesamum indicum', 'sim sim', 'tahini, tahina, tehina', 'til', 'benne seed', 'benniseed', 'sesamum', 'sesame salt', 'gingelly oil'],
    "peanut": ['arachic oil', 'arachis', 'arachis hypogaea', 'artificial nuts', 'beer nuts', 'boiled peanuts', 'peanut oil', 'crushed nuts', 'earth nuts', 'goober peas', 'ground nuts', 'hydrolyzed peanut protein', 'mandelonas', 'mixed nuts', 'monkey nuts', 'nu nuts flavored nuts', 'nut pieces', 'nutmeat', 'peanuts', 'peanut flour', 'peanut paste', 'peanut sauce', 'spanish peanuts', 'virginia peanuts', 'crushed peanuts', 'ground peanuts', 'peanut butter', 'peanut butter chips', 'peanut butter morsels', 'peanut syrup'],
    "wheat": ['white flour',
              'bulgur',
              'cereal extract',
              'couscous',
              'cracker meal',
              'einkorn',
              'emmer – also known as farro',
              'farina',
              'farro',
              'flour',
              'freekeh, frikeh, farik',
              'fu',
              'gluten',
              'hydrolyzed wheat protein',
              'kamut ',
              'malt, malt extract',
              'matzo ',
              'noodles ',
              'seitan',
              'semolina',
              'spelt',
              'tabbouleh',
              'triticale',
              'triticum',
              'wheat',
              'wheatgrass',
              'wheat flour',
              'bread crumbs',
              'whole wheat',
              'wheat berries',
              'wheat bran',
              'whole wheat bread',
              'whole wheat flour',
              'wheat germ',
              'wheat germ oil',
              'wheat protein isolate',
              'wheat starch',
              'wheat sprouts',
              'sprouted wheat',
              'matzo meal',
              'khorasan wheat',
              'matzoh',
              'matzah',
              'matza',
              'pasta',
              'wheat gluten',
              'vital gluten',
              'vital wheat gluten',
              'fu',
              'all-purpose',
              'atta',
              'bread',
              'bromated',
              'cake',
              'durum',
              'einkorn',
              'emmer',
              'enriched',
              'farina',
              'graham',
              'high gluten',
              'instant pastry',
              'kamut',
              'maida',
              'semolina',
              'soft wheat',
              'spelt',
              'steel ground flour',
              'stone flour',
              'triticale',
              'triticum',
              'unbleached flour',
              'white flour',
              'whole wheat'],


}


def check_allergies(ingredients):
    allergies = []
    for allergen, allergen_ingredients in allergy_dict.items():
        for ingredient in allergen_ingredients:
            if ingredient in ingredients.lower():
                allergies.append(allergen)
                break
    # print(allergies)
    return allergies


# check_allergies("CHEDDAR CHEESE AGED OVER 100 DAYS (CULTURED UNPASTEURIZED MILK, SALT, ENZYMES), WATER, WHEY, CREAM, TOMATO FLAKES, BASIL, LACTIC ACID. benne")
def get_top_three(micros):
    new_mapping = {}
    for key in micros:
        value = micros[key]["value"]
        unit = micros[key]["unit"]
        if unit == "mg":
            new_mapping[key] = value
        elif unit == "µg":
            new_mapping[key] = value / 1000
        elif unit == "iu":
            if key == "Vitamin A":
                new_mapping[key] = value * 0.00333
            elif key == "Vitamin D":
                value = value * 0.04
    c = Counter(new_mapping)

    most_common = c.most_common(3)

    my_keys = [key for key, val in most_common]

    return my_keys