import random
import matplotlib.pyplot as plt

# константы генетического алгоритма
ONE_MAX_LENGTH = 100  # длина хромосомы
GENERATION_SIZE = 200  # количество особей одного поколения (кол-во детей, кол-во взрослых, кол-во пожилых)
GENDER_SIZE = 100  # количество особей одного пола в поколении
MALE_GENDER = 'Man'
FEMALE_GENDER = 'Woman'
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.1  # вероятность мутации
P_IMPACT = 0.8  # вероятность положительного влияния на детских особей в период воспитания
P_SELECTION = 0.6  # вероятность попадания особи в список дважды при турнирном отборе
MAX_GENERATIONS = 100  # максимальное количество поколений

RANDOM_SEED = 5
random.seed(RANDOM_SEED)


class FitnessMax():  # значение приспособленности особи
    def __init__(self):
        self.values = [0]


class Individual(list):  # представление каждой особи в популяции (список из 0 и 1)
    def __init__(self, *args, gender):
        super().__init__(*args)
        self.fitness = FitnessMax()
        self.gender = gender


def oneMaxFitness(individual):  # вычисление приспособленности отдельной особи
    return sum(individual),  # кортеж


def individualCreator(gender):  # создания отдельного индивидуума
    return Individual([random.randint(0, 1) for i in range(ONE_MAX_LENGTH)], gender=gender)


def populationCreator(gender, n=0):  # создание начальной популяции
    return list([individualCreator(gender) for i in range(n)])


menAdultsPopulation = populationCreator(MALE_GENDER, n=GENDER_SIZE)  # начальное поколение взрослых мужских особей
womenAdultsPopulation = populationCreator(FEMALE_GENDER, n=GENDER_SIZE)  # начальное поколение взрослых женских особей

menAndWomenAdultsPopulation = menAdultsPopulation + womenAdultsPopulation  # начальное поколения взрослых мужских и
# женских особей
menAndWomenOlderPopulation = menAndWomenAdultsPopulation  # начальное поколение пожилых мужских и женских особей
generationCounter = 0  # счетчик поколений

fitnessValues = list(
    map(oneMaxFitness, menAndWomenAdultsPopulation))  # приспособленность каждой взрослой особи в текущей популяции

for individual, fitnessValue in zip(menAndWomenAdultsPopulation,
                                    fitnessValues):  # присваивание значения функции приспособленности для каждой особи
    individual.fitness.values = fitnessValue

maxFitnessValues = []  # вспомогательный список для хранения лучшей приспособленности в каждом текущем поколении
meanFitnessValues = []  # вспомогательный список для хранения средней приспособленности в каждом текущем поколении


def clone(value):  # клонирование отдельного индивидуума
    ind = Individual(value[:], gender='')
    ind.fitness.values[0] = value.fitness.values[0]
    ind.gender = value.gender
    return ind


def selection(generation, g_len):  # отбор лучших взрослых особей
    offspring = []  # новый список с выбранными наилучшими особями
    for n in range(g_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = random.randint(0, g_len - 1), random.randint(0, g_len - 1), random.randint(0, g_len - 1)

        offspring.append(max([generation[i1], generation[i2], generation[i3]], key=lambda ind: ind.fitness.values[0]))
        if random.random() < P_SELECTION:
            offspring.append(
                max([generation[i1], generation[i2], generation[i3]], key=lambda ind: ind.fitness.values[0]))
    return offspring


def cxOnePoint(child1, child2):  # одноточечное скрещивание
    s = random.randint(2, len(child1) - 3)  # создаем точку разрыва
    child1[s:], child2[s:] = child2[s:], child1[s:]  # меняем части хромосом
    child1.gender = MALE_GENDER
    child2.gender = FEMALE_GENDER


def mutFlipBit(mutant, indpb=0.01):  # мутация
    for indx in range(len(mutant)):
        if random.random() < indpb:
            mutant[indx] = 0 if mutant[indx] == 1 else 1  # инверсия бита (если равен 1, то меняем на 0, иначе 1)

def socialImpact(child, indpb=0.01):  # инверсия бита (если равен 0, то меняем на 1)
    for index in range(len(child)):
        if random.random() < indpb:
            if child[index] == 0:
                child[index] = 1


fitnessValues = [individual.fitness.values[0] for individual in
                 menAndWomenAdultsPopulation]  # список значений функции приспособленности

while max(fitnessValues) < ONE_MAX_LENGTH and generationCounter < MAX_GENERATIONS:
    generationCounter += 1
    half = len(menAndWomenAdultsPopulation) // 2  # для среза списка особей на половины
    menChildrenPopulation = selection(menAndWomenAdultsPopulation[:half],
                                      len(menAndWomenAdultsPopulation[:half]))  # отбираем лучших мужских особей
    womenChildrenPopulation = selection(menAndWomenAdultsPopulation[half:],
                                        len(menAndWomenAdultsPopulation[half:]))  # отбираем лучших женских особей
    menChildrenPopulation = list(
        map(clone, menChildrenPopulation))  # клонируем мужские особи, чтобы не было повторений
    womenChildrenPopulation = list(
        map(clone, womenChildrenPopulation))  # клонируем женские особи, чтобы не было повторений

    fitnessValuesMen = [ind.fitness.values[0] for ind in
                        menChildrenPopulation]
    fitnessValuesWomen = [ind.fitness.values[0] for ind in
                          womenChildrenPopulation]
    menPopulationCounter = len(menChildrenPopulation) - 100
    womenPopulationCounter = len(womenChildrenPopulation) - 100
    for i in range(0, menPopulationCounter):
        minFitnessMen = fitnessValuesMen.index(min(fitnessValuesMen))
        del fitnessValuesMen[minFitnessMen]
        del menChildrenPopulation[minFitnessMen]
    for j in range(0, womenPopulationCounter):
        minFitnessWomen = fitnessValuesWomen.index(min(fitnessValuesWomen))
        del fitnessValuesWomen[minFitnessWomen]
        del womenChildrenPopulation[minFitnessWomen]

    menAndWomenChildrenPopulation = menChildrenPopulation + womenChildrenPopulation  # объединяем списки отобранных
    # мужских и женских особей

    for child1, child2 in zip(menAndWomenChildrenPopulation[:half],
                              menAndWomenChildrenPopulation[half:]):  # выполняем скрещивание
        if random.random() < P_CROSSOVER:
            cxOnePoint(child1, child2)  # образование потомков

    for mutant in menAndWomenChildrenPopulation:  # мутация
        if random.random() < P_MUTATION:
            mutFlipBit(mutant, indpb=1.0 / ONE_MAX_LENGTH)

    for child in menAndWomenChildrenPopulation:  # положительное влияние на детских особей в период воспитания
        if random.random() < P_IMPACT:
            socialImpact(child, indpb=1.0 / ONE_MAX_LENGTH)

    freshFitnessValues = list(
        map(oneMaxFitness, menAndWomenChildrenPopulation))  # обновление функции приспособленности для новой популяции
    for individual, fitnessValue in zip(menAndWomenChildrenPopulation, freshFitnessValues):
        individual.fitness.values = fitnessValue  # записываем значения приспособленности для каждой новой особи

    menAndWomenOlderPopulation[:] = menAndWomenAdultsPopulation  # обновляем список популяции пожилых особей
    menAndWomenAdultsPopulation[:] = menAndWomenChildrenPopulation  # обновляем список популяции взрослых особей

    fitnessValues = [ind.fitness.values[0] for ind in
                     menAndWomenAdultsPopulation]  # список всех значений приспособленности для новой популяции
    genderValues = [ind.gender for ind in menAndWomenAdultsPopulation]  # список всех полов для новой популяции

    maxFitness = max(fitnessValues)  # особь с максимальной приспособленностью
    meanFitness = sum(fitnessValues) / len(menAndWomenAdultsPopulation)  # средняя приспособленность популяции
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
    print(f"Поколение {generationCounter}: Макс приспособ. = {maxFitness}, Средняя приспособ.= {meanFitness}")

    best_index = fitnessValues.index(max(fitnessValues))  # индекс лучшего индивидуума
    best_gender = genderValues[best_index]  # пол лучшей особи
    print("Лучший индивидуум = ", *menAndWomenAdultsPopulation[best_index])
    print("Пол лучшего индивидуума: ", best_gender, "\n")

    fitnessMinMen = fitnessValues[:100]  # список детских мужских особей
    fitnessMinWomen = fitnessValues[100:]  # список детских женских особей
    for i in range(0, 5):  # гибель 15 особей с наименьшей целевой функцией мужского пола
        minFitnessIndexMen = fitnessMinMen.index(min(fitnessMinMen))  # индекс особи с наименьшей целевой функцией
        del fitnessMinMen[minFitnessIndexMen]  # удаление особи из списка
        del menAndWomenAdultsPopulation[minFitnessIndexMen]  # удаление особи из списка
    for j in range(0, 5):  # гибель 15 особей с наименьшей целевой функцией женского пола
        minFitnessIndexWomen = fitnessMinWomen.index(min(fitnessMinWomen))  # индекс особи с наименьшей целевой функцией
        del fitnessMinWomen[minFitnessIndexWomen]  # удаление особи из списка
        minFitnessIndexWomen = minFitnessIndexWomen + 95
        del menAndWomenAdultsPopulation[minFitnessIndexWomen]  # удаление особи из списка

    for s in range(0, 5):  # случайная смертность 5 детских особей мужского пола
        indexMen = random.randint(0, 89)
        del menAndWomenAdultsPopulation[indexMen]
    for s in range(0, 5):  # случайная смертность 5 детских особей женского пола
        indexWomen = random.randint(89, 179)
        del menAndWomenAdultsPopulation[indexWomen]

plt.plot(maxFitnessValues, color='blueviolet')
plt.plot(meanFitnessValues, color='lawngreen')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.title('Зависимость максимальной и средней приспособленности от поколения')
plt.show()
