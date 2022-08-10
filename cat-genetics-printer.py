# Create Cat-Objects with attributes

# %%
import random
from enum import Enum
from typing import Tuple, cast

# Rough plan: Cat has a genome
#    genome contains many chromosomes
#    chromosones come in many types
#    Y in males only
#    X once in males, twice in females (one from mother, one from father)
# Types of chromosones: Xr/b and Y = Color and Gender

# XX = Female
# XY = Male
# Xb = Black
# Xr = Red
# Genotype = Genetic Code
# Phenotype = How it looks
# (L+l)*(L+l) = LL + 2 Ll + ll


class Sex(Enum):
    X = "X"
    Y = "Y"


class CatGenomeSide:
    def __init__(self, agouti: bool, long_fur: bool, red: bool, point: bool, diluted: bool, sex: Sex):
        self.agouti = agouti
        self.long_fur = long_fur
        self.red = red
        self.point = point
        self.diluted = diluted
        self.sex = sex


class Cat:
    def __init__(self, mother: CatGenomeSide, father: CatGenomeSide):
        self.mother = mother
        self.father = father

        self.phenotype = calculate_phenotype(mother, father)


def pick_random(options):
    index = random.randrange(len(options))
    value = options[index]
    return value


def inherit_gene(mother_genes: Tuple[bool, bool], father_genes: Tuple[bool, bool]):
    mother_pick = pick_random(mother_genes)
    father_pick = pick_random(father_genes)
    return (mother_pick, father_pick)


def mate(mother: Cat, father: Cat):
    agouti_pair = inherit_gene((mother.mother.agouti, mother.father.agouti),
                               (father.mother.agouti, father.father.agouti))
    longfur_pair = inherit_gene((mother.mother.long_fur, mother.father.long_fur),
                                (father.mother.long_fur, father.father.long_fur))
    red_pair = inherit_gene((mother.mother.red, mother.father.red),
                            (father.mother.red, father.father.red))
    point_pair = inherit_gene((mother.mother.point, mother.father.point),
                              (father.mother.point, father.father.point))
    dilluted_pair = inherit_gene((mother.mother.diluted, mother.father.diluted),
                                 (father.mother.diluted, father.father.diluted))

    sex = pick_random((Sex.X, Sex.Y))

    offspring = Cat(CatGenomeSide(agouti_pair[0], longfur_pair[0], red_pair[0], point_pair[0], dilluted_pair[0], Sex.X),
                    CatGenomeSide(agouti_pair[1], longfur_pair[1], red_pair[1], point_pair[1], dilluted_pair[1], sex))
    return offspring

# %%
#   Set up rules which attribute is prefered over the other:
#   Agouti is preferred over non-agouti agouti = dominant
#   Black and red can happen at the same time True - but only on females - males have to decide. 50-50 chance!
#   Long fur can only happen if both parents have or carry long fur (rez)
#   Sex is random


def calculate_phenotype(mother: CatGenomeSide, father: CatGenomeSide):
    tags = []

    male = (father.sex == Sex.Y)
    striped = mother.agouti or father.agouti
    diluted = mother.diluted and father.diluted
    red = mother.red
    red_pure = mother.red and not diluted
    if not male:
        red_pure = (red and father.red) and not diluted
        red = red and father.red
    black_pure = not red and not diluted
    black = not red
    lucky_cat = ((mother.red and not father.red) or (
        not mother.red and father.red)) and not male
    tortie = lucky_cat and not striped and not diluted
    torbie = lucky_cat and striped and not diluted
    tortie_diluted = lucky_cat and diluted and not striped
    torbie_diluted = lucky_cat and diluted and striped
    fluffy = mother.long_fur and father.long_fur
    point = mother.point and father.point
    shorthair = not fluffy
    creme = diluted and red and not tortie_diluted and not torbie_diluted
    blue = diluted and black and not tortie_diluted and not torbie_diluted
    striped_pure = (mother.agouti or father.agouti) and not (
        torbie or torbie_diluted)

    if male:
        tags.append("male")
    else:
        tags.append('female')
    if striped_pure:
        tags.append('striped')
    if point:
        tags.append('point')
    if red_pure and not lucky_cat:
        tags.append("red")
    if black_pure and not lucky_cat:
        tags.append("black")
    if tortie:
        tags.append('tortie')
    if torbie:
        tags.append('torbie')
    if fluffy:
        tags.append('long hair')
    if shorthair:
        tags.append('shorthair')
    if blue:
        tags.append('blue')
    if creme:
        tags.append('creme')
    if tortie_diluted:
        tags.append('diluted tortie')
    if torbie_diluted:
        tags.append('diluted torbie')

    return tags


# Define how the attributes alter the look

# %%

# print kittens


cat_a = Cat(CatGenomeSide(agouti=True, long_fur=False, red=False, point=True, diluted=True, sex=Sex.X),
            CatGenomeSide(agouti=False, long_fur=True, red=True, point=False, diluted=True, sex=Sex.X))
cat_b = Cat(CatGenomeSide(agouti=False, long_fur=True, red=False, point=False, diluted=True, sex=Sex.X),
            CatGenomeSide(agouti=False, long_fur=False, red=False, point=True, diluted=False, sex=Sex.Y))

for i in range(20):
    kitten = mate(cat_a, cat_b)
    print(kitten.phenotype)


# baby = agouti =y/y -> stripeys
#        red = n/y -> red
#        black = y/n -> black
#        long_fur = n/y -> shorthair

# parent 1 n/y
# parent 2 y/n
# baby 1: n/n short
# baby 2: y/n short
# baby 3: n/y short
# baby 4: y/y longfe

# parentf = Cat(s, agouti=False, red=False, black=True, long_fur=False)
# parentm = Cat(sex="Male", agouti=True, red=True, black=False, long_fur=True)


# Reshuffle
