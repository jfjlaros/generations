#!/usr/bin/python

import random # randint()
import sys    # argv[]

maxDist = 100

def pickPersons(allPerons, relationMatrix, number) :
    """
    Select a random subset out of a set.

    @arg allPersons: A set of persons.
    @type allPersons: dict
    @arg number: The size of the subset.
    @type number: integer

    @returns: A random subset of allPersons.
    @rtype: list
    """

    myPersons = dict(allPersons)
    selection = []

    for i in range(number) :
        pick = myPersons.keys()[random.randint(0, len(myPersons.keys()) - 1)]
        selection.append(pick)
        purge = myPersons.pop(pick)
        for j in relationMatrix[purge] :
            print j
    #for

    return selection
#pickPersons

def loadMatrix(fileName) :
    """
    """

    personId = {}
    matrix = []
    lines = 0

    handle = open(fileName, "r")

    line = handle.readline()
    for i in line[2:-1].split('\t') :
        personId[i] = lines
        lines += 1
    #for

    lines = 0
    line = handle.readline()
    while line :
        matrix.append([])
        for i in line[:-1].split('\t')[1:] :
            matrix[lines].append(i)
        line = handle.readline()
        lines += 1
    #while

    handle.close()

    for i in matrix :
        for j in i :
            print "%3i" % int(j),
        print
    #for

    return personId, len(matrix)
#loadMatrix

if __name__ == "__main__" :
    random.seed()
    
    allPersons, matrix = loadMatrix(sys.argv[1])
    print pickPersons(allPersons, matrix, 2)
#if
