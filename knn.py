import json as js
import operator
import time
start = time.time()

def similarity(testIngredients, trainingIngredients):
    testSet = set(testIngredients)
    trainingSet = set(trainingIngredients)
    score = float(len(testSet&trainingSet))/float(len(testSet|trainingSet))
    return score

with open('../input/train.json') as training_data_file:
    training_data = js.load(training_data_file)
with open('../input/test.json') as test_data_file:
    test_data = js.load(test_data_file)
    
n_training = len(training_data)
n_test = len(test_data)

file_out = open('knnResults.csv','w')
file_out.write('id,cuisine\n')

n_k = 20
for t in range(n_test):
    id = str(test_data[t]['id'])
    simScores = dict()
    cuisineCounts = dict()
    
    for i in range(n_training):
        ss = similarity(test_data[t]['ingredients'], training_data[i]['ingredients'])
        simScores[str(i)] = ss
    sortedSs = sorted(simScores.items(), key=operator.itemgetter(1), reverse=True)

    for k in range(n_k):
        nearestIndex = int(sortedSs.pop(0)[0])
        nearestCuisine = str(training_data[nearestIndex]['cuisine'])
        cuisineCounts[nearestCuisine] = cuisineCounts.get(nearestCuisine, 0) + 1
    sortedCc = sorted(cuisineCounts.items(), key=operator.itemgetter(1), reverse=True)
    predictedCuisine = sortedCc.pop(0)[0]

    file_out.write(id)
    file_out.write(',')
    file_out.write(predictedCuisine)
    file_out.write('\n')
file_out.close()

print("runtime:", time.time()-start, "seconds")
