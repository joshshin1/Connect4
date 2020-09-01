import random
import sys
sys.path.append('.')

from connect4ai import AI

win = 1000000
popsize = 10
survivors = popsize - int(.8 * popsize)

board = [[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0]]

def printstats(population):
    for i in range(popsize):
        print(population[i].fitness, population[i].chromosome)
    print()

def mergesort(arr): 
    if len(arr) >1: 
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
  
        mergesort(L)
        mergesort(R) 
  
        i = j = k = 0
          
        while i < len(L) and j < len(R): 
            if L[i].fitness < R[j].fitness: 
                arr[k] = L[i] 
                i+= 1
            else: 
                arr[k] = R[j] 
                j+= 1
            k+= 1
          
        while i < len(L): 
            arr[k] = L[i] 
            i+= 1
            k+= 1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+= 1
            k+= 1

def resetboard():
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j] = 0

def mutate():
    return random.randint(0, win)    

def crossover(parent1, parent2):
    chromosome = []
    for i in range(10):
        probability = random.random()
        if probability < .4:
            chromosome.append(parent1.chromosome[i])
        elif probability < .8:
            chromosome.append(parent2.chromosome[i])
        else:
            chromosome.append(mutate())
    return AI(1, chromosome)

def play(ai1, ai2):
    while True:
        if not ai1.tie(board):
            if not ai2.finish(board):    
                ai2.blockercount[0] -= ai1.optimalMove(board)
            else:
                ai2.fitness += 1
                #ai1.fitness -= 1
                break
        else:
            ai1.fitness += .5
            ai2.fitness += .5
            break
                    
        if not ai1.tie(board):
            if not ai1.finish(board):
                ai1.blockercount[1] -= ai2.optimalMove(board)
            else:
                ai1.fitness += 1
                #ai2.fitness -= 1
                break
        else:
            ai1.fitness += .5
            ai2.fitness += .5
            break
   
def calcfitness(population):
    for i in range(popsize):
        for j in range(popsize):
            if i == j:
                continue
            population[j].color += 1
            play(population[i], population[j])
            population[j].color -= 1
            resetboard()
         
def select(population):
    mergesort(population)
    for i in range(popsize - survivors):
        population.pop(0)
    for i in range(survivors):
        population[i].fitness = 0
        
def repopulate(population):
    for i in range(popsize):
        population.append(crossover(population[i % survivors], population[(i + 1) % survivors]))
    for i in range(survivors):
        population.pop(0)

def evolve(population):
    # PLAY AI AGAINST EACH OTHER
    for i in range(10):
        calcfitness(population)
        
        print('GENERATION', i)
        printstats(population)
        
        select(population)    
        repopulate(population)
    mergesort(population)
    return population[popsize - 1]       

# CREATE RANDOM POPULATION
randpop = []
for k in range(popsize):
    randpop.append(AI(1, (mutate(), mutate(), mutate(), mutate(), mutate(), mutate(), mutate(), mutate(), mutate(), mutate())))




