#!/usr/bin/python

"""
@requires: sys
@requires: random
"""

import sys    # argv[]
import random # randint()

maxDist = 100

def loadMatrix(fileName) :
    """
    Load the content of a file into a matrix and a structure that contains the
    IDs with a pointer to the corresponding row in the matrix.

    @arg fileName: Name of a file that contains an n*m matrix.
    @type fileName: string

    @returns: A dictionary with the IDs pointing to the rows and an n*m matrix.
    @rtype: (list(integer), list(list(float)))
    """

    personId = []
    matrix = []
    lines = 0

    handle = open(fileName, "r")

    line = handle.readline()
    line = handle.readline()
    while line :
        personId.append(int(line.split('\t')[0]))
        matrix.append([])
        for i in line[:-1].split('\t')[1:] :
            if i :
                matrix[lines].append(float(i))
            else :
                matrix[lines].append(0)
        #for
        line = handle.readline()
        lines += 1
    #while

    handle.close()

    return personId, matrix
#loadMatrix

def printMatrix(matrix) :
    """
    Print the content of a matrix and the number of rows in the matrix.

    @arg matrix: An n*m matrix.
    @type matrix: list(list(float))
    """

    for i in matrix :
        for j in i :
            print "%3i" % int(j),
        print
    #for
    print "rows: %i\n" % len(matrix)
#printMatrix

def makeFamilies(personId, matrix, distance) :
    """
    Convert a matrix and a list of persons to a dictionary of families. Use 
    the distance parameter to determine whether two people are placed in the
    same family.

    @arg personId: List of person IDs.
    @type personId: list(integer)
    @arg matrix: Matrix with distances between people.
    @type matrix: list(list(float))
    @arg distance: Distance to determine whether two people are related.
    @type distance: integer

    @returns: Dictionary of people and their families.
    @rtype: dict(list(integer))
    """

    families = {}

    for i in range(len(personId)) :
        families[personId[i]] = [personId[i]]
        for j in range(len(personId)) :
            element = matrix[i][j]
            if element != 0 and element != maxDist and element <= distance :
                families[personId[i]].append(personId[j])
        #for
    #for

    return families
#makeFamilies

def printFamilies(families) :
    """
    Print the families dictionary.

    @arg families: Dictionary of people and their families.
    @type families: dict(list(integer))
    """

    for i in families.keys() :
        print "%i: %s" % (i, str(families[i]))
    print
#printFamilies

def pickPersons(families, number) :
    """
    Randomly select a number of persons from the families dictionary, if a
    person is selected, the family of this person is purged from the
    dictionary.

    @arg families: Dictionary of people and their families.
    @type families: dict(list(integer))
    @arg number: Number of people to select.
    @type number: integer

    @returns: A list of person IDs.
    @rtype: list(integer)
    """

    myFamilies = dict(families)
    selection = []

    #printFamilies(myFamilies)
    for i in range(number) :
        pick = myFamilies.keys()[random.randint(0, len(myFamilies.keys()) - 1)]
        selection.append(pick)
        for j in myFamilies[pick] :
            if not len(myFamilies.keys()) :
                print "Error: Families depleted, exiting."
                sys.exit(1)
            #if
            if myFamilies.has_key(j) : # A family member can already be removed
                myFamilies.pop(j)      # by removing a remote family member.
        #print pick
        #printFamilies(myFamilies)
    #for

    return selection
#pickPersons

if __name__ == "__main__" :
    fileName = sys.argv[1]
    distance = int(sys.argv[2])
    selectionSize = int(sys.argv[3])
    numberOfSelections = int(sys.argv[4])
    
    random.seed()
    
    personId, matrix = loadMatrix(fileName)
    #printMatrix(matrix)
    families = makeFamilies(personId, matrix, distance)
    #printFamilies(families)
    for i in range(numberOfSelections) :
        selection = pickPersons(families, selectionSize)
        for j in selection :
            print j,
        print
    #for
#if
