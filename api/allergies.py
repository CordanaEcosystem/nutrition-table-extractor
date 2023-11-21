from collections import Counter
import re
others={
    "dairy":['milk']
}
allergy_dict = {
    "dairy": [ 'cheese', 'yogurt', 'butter', 'cream', 'sour cream', 'custard', 'evaporated milk', 'condensed milk', 'buttermilk', 'ice cream', 'pudding'],
    "tree-nuts": ['almonds', 'brazil nuts', 'cashews', 'chestnuts', 'filberts', 'hazelnuts', 'hickory nuts', 'macademia', 'pecans', 'pistachios', 'walnuts', 'ginkgo'],
    "soy-bean": ['soybean', 'soy flour', 'soy drink', 'tofu', 'tempeh', 'soy yogurt', 'soy bread', 'soy sauce'],
    "shell-fish": ['crab', 'crayfish', 'lobster', 'shrimp', 'prawns', 'scallops', 'squid', 'mussels', 'snails', 'clams', 'oysters', 'octopus'],
    "fish":  ["abalone",
    "anchovy",
    "arctic char",
    "barracuda",
    "barramundi",
    "bass",
    "bass blue gill",
    "bass sea",
    "bass lake",
    "bass striped",
    "bass drum",
    "black sea bass",
    "bluefish",
    "bluenose",
    "bullhead",
    "butterfish",
    "capelin",
    "carp",
    "catfish",
    "caviar",
    "chilean seabass",
    "chub",
    "clam",
    "cobia",
    "cod",
    "conch",
    "corvina",
    "croaker",
    "cusk",
    "dab",
    "drum",
    "eel",
    "escolar",
    "flounder",
    "gray sole",
    "greater amberjack",
    "grenadier",
    "grouper",
    "haddock",
    "hake",
    "halfmoon fish",
    "halibut",
    "harvest fish",
    "herring",
    "imitation crab",
    "jellyfish",
    "lingcod",
    "mackerel atlantic",
    "mackerel spanish",
    "mahi mahi",
    "marlin",
    "monkfish",
    "mullet",
    "muskellunge",
    "ocean pout",
    "opah",
    "opaleye",
    "orange roughy",
    "oyster",
    "pangasius",
    "parrotfish",
    "perch",
    "perch ocean",
    "pickerel",
    "pike",
    "pilchards",
    "plaice",
    "pomfret",
    "pompano",
    "pollock",
    "porgy",
    "red porgy",
    "red snapper",
    "rockfish",
    "rosefish",
    "sablefish",
    "salmon atlantic",
    "salmon chinook",
    "salmon sockeye",
    "sanddabs",
    "sardine",
    "scab",
    "scrod",
    "scup",
    "sea beam",
    "sea urchin",
    "seatrout",
    "shad",
    "shark",
    "sheepshead fish",
    "skate",
    "smelt spearfish",
    "snail",
    "sole",
    "striped bass",
    "sturgeon",
    "sucker",
    "sunfish",
    "swai",
    "swordfish",
    "tatoaba",
    "tilapia",
    "tilefish",
    "trout rainbow",
    "trout sea",
    "trout steelhead",
    "tuna albacore",
    "tuna bigeye",
    "tuna blackfin",
    "tuna bluefin",
    "tuna tongol",
    "tuna yellowfin",
    "tuna",
    "turbot",
    "wahoo",
    "walleye",
    "weakfish",
    "white seabass",
    "whitefish",
    "whiting",
    "wolfish atlantic",
    "wreckfish",
    "yellowtail"
],

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
            regex = r"\b" + re.escape(ingredient) + r"\b"
            matches = re.finditer(regex, ingredients.lower())
            for match in matches:
                start_index = match.start()
                end_index = match.end()
                
                # Find the prefix word
                prefix_start_index = ingredients.rfind(' ', 0, start_index-2) + 1
                prefix_word = ingredients[prefix_start_index:start_index].strip()
                # print(match,prefix_word)
                # Check if the neighboring words indicate exclusion
                if (prefix_word.lower() == 'no' or prefix_word.lower() == 'without'):
                    continue
                # print(allergen)
                allergies.append(allergen)
                break
    unique_allergies = list(set(allergies))
    return unique_allergies



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
Dv_values={
    "Calcium": {"amount": 1300, "unit": "mg"},
    "Magnesium": {"amount": 420, "unit": "mg"},
    "Manganese": {"amount": 2.3, "unit": "mg"},
    "Phosphorous": {"amount": 1250, "unit": "mg"},
    "Potassium": {"amount": 4700, "unit": "mg"},
    "Vitamin C": {"amount": 90, "unit": "mg"},
    "Vitamin D": {"amount": 800, "unit": "IU"},
    "Vitamin K": {"amount": 120, "unit": "µg"},
    "Vitamin B-7": {"amount": 30, "unit": "µg"},
    "Chloride": {"amount": 2300, "unit": "mg"},
    "Chromium": {"amount": 35, "unit": "µg"},
    "Copper": {"amount": 900, "unit": "µg"},
    "Vitamin B-9": {"amount": 400, "unit": "µg"},
    "Molybdenum": {"amount": 45, "unit": "µg"},
    "Vitamin B-3": {"amount": 16, "unit": "mg"},
    "Vitamin B-5": {"amount": 5, "unit": "mg"},
    "Vitamin B-2": {"amount": 1.3, "unit": "mg"},
    "Selenium": {"amount": 55, "unit": "µg"},
    "Sodium": {"amount": 2300, "unit": "mg"},
    "Vitamin B-1": {"amount": 1.2, "unit": "mg"},
    "Vitamin A": {"amount": 3000, "unit": "IU"},
    "Vitamin B-12": {"amount": 2.4, "unit": "µg"},
    "Vitamin E": {"amount": 15, "unit": "mg"},
    "Zinc": {"amount": 11, "unit": "mg"},
    "Iodine": {"amount": 150, "unit": "µg"},
    "Iron": {"amount": 18, "unit": "mg"},
    "Vitamin B-6": {"amount": 1.7, "unit": "mg"}
}
