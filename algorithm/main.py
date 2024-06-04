import random
import matplotlib.pyplot as plt

# константы генетического алгоритма
ONE_MAX_LENGTH = 100  # длина хромосомы
GENERATION_SIZE = 100 # количество особей одного поколения (кол-во детей, кол-во взрослых, кол-во пожилых)
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.1  # вероятность мутации
MAX_GENERATIONS = 100  # максимальное количество поколений

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

class FitnessMax(): # значение приспособленности особи
    def __init__(self):
        self.values = [0]

class Individual(list): # представление каждой особи в популяции (список из 0 и 1)
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()

def oneMaxFitness(individual): # вычисление приспособленности отдельной особи
    return sum(individual), # кортеж

def individualCreator(): # создания отдельного индивидуума
    return Individual([random.randint(0, 1) for i in range(ONE_MAX_LENGTH)])

def populationCreator(n=0): # создание начальной популяции
    return list([individualCreator() for i in range(n)])

adultsPopulation = populationCreator(n=GENERATION_SIZE) # формирование начальной популяции со взрослыми особями
olderPopulation = populationCreator(n=GENERATION_SIZE) # формирование начальной популяции с пожилыми особями
generationCounter = 0 # счетчик поколений

fitnessValues = list(map(oneMaxFitness, adultsPopulation)) # приспособленность каждой взрослой особи в текущей популяции

for individual, fitnessValue in zip(adultsPopulation, fitnessValues): # присваивание значения функции приспособленности для каждой особи
    individual.fitness.values = fitnessValue

maxFitnessValues = [] # вспомогательный список для хранения лучшей приспособленности в каждом текущем поколении
meanFitnessValues = [] # вспомогательный список для хранения средней приспособленности в каждом текущем поколении

def clone(value): # клонирование отдельного индивидуума
    ind = Individual(value[:])
    ind.fitness.values[0] = value.fitness.values[0]
    return ind

def selection(generation, g_len): # отбор лучших взрослых особей
    offspring = [] # новый список с выбранными наилучшими особями
    for n in range(g_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = random.randint(0, g_len - 1), random.randint(0, g_len - 1), random.randint(0, g_len - 1)

        offspring.append(max([generation[i1], generation[i2], generation[i3]], key=lambda ind: ind.fitness.values[0]))

    return offspring

def cxOnePoint(child1, child2): # одноточечное скрещивание
    s = random.randint(2, len(child1) - 3) # создаем точку разрыва
    child1[s:], child2[s:] = child2[s:], child1[s:] # меняем части хромосом

def mutFlipBit(mutant, indpb=0.01): # мутация
    for indx in range(len(mutant)):
        if random.random() < indpb:
            mutant[indx] = 0 if mutant[indx] == 1 else 1 # инверсия бита (если равен 1, то меняем на 0, иначе 1)

fitnessValues = [individual.fitness.values[0] for individual in adultsPopulation] # список значений функции приспособленности

while max(fitnessValues) < ONE_MAX_LENGTH and generationCounter < MAX_GENERATIONS:
    generationCounter += 1
    childrenPopulation = selection(adultsPopulation, len(adultsPopulation)) # отбираем лучших особей
    childrenPopulation = list(map(clone, childrenPopulation)) # клонируем особи, чтобы не было повторений

    for child1, child2 in zip(childrenPopulation[::2], childrenPopulation[1::2]): # выполняем скрещивание
        if random.random() < P_CROSSOVER:
            cxOnePoint(child1, child2) # образование потомков

    for mutant in childrenPopulation: # мутация
        if random.random() < P_MUTATION:
            mutFlipBit(mutant, indpb=1.0 / ONE_MAX_LENGTH)

    freshFitnessValues = list(map(oneMaxFitness, childrenPopulation)) # обновление функции приспособленности для новой популяции
    for individual, fitnessValue in zip(childrenPopulation, freshFitnessValues):
        individual.fitness.values = fitnessValue # записываем значения приспособленности для каждой новой особи

    olderPopulation[:] = adultsPopulation # обновляем список популяции пожилых особей
    adultsPopulation[:] = childrenPopulation # обновляем список популяции взрослых особей

    fitnessValues = [ind.fitness.values[0] for ind in adultsPopulation] # список всех значений приспособленности для новой популяции

    maxFitness = max(fitnessValues) # особь с максимальной приспособленностью
    meanFitness = sum(fitnessValues) / len(adultsPopulation) # средняя приспособленность популяции
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
    print(f"Поколение {generationCounter}: Макс приспособ. = {maxFitness}, Средняя приспособ.= {meanFitness}")
    best_index = fitnessValues.index(max(fitnessValues)) # индекс лучшего индивидуума
    print("Лучший индивидуум = ", *adultsPopulation[best_index], "\n")

plt.plot(maxFitnessValues, color='blueviolet')
plt.plot(meanFitnessValues, color='lawngreen')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.title('Зависимость максимальной и средней приспособленности от поколения')
plt.show()