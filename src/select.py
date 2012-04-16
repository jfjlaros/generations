#!/usr/bin/python

"""
Make a selection of people in a distance matrix. The distance is the number
of generations that separates them.
"""

import sys    # argv[]
import random # randint()
import argparse

maxDist = 100

def loadMatrix(handle) :
    """
    Load the content of a file into a matrix and a structure that contains the
    IDs with a pointer to the corresponding row in the matrix.

    @arg handle: Handle to an open file that contains an n*m matrix.
    @type fileName: handle

    @returns: A dictionary with the IDs pointing to the rows and an n*m matrix.
    @rtype: (list(integer), list(list(float)))
    """

    personId = []
    matrix = []
    lines = 0

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

def select(handle, distance, selectionSize, numberOfSelections) :
    """
    @arg handle:
    @arg handle:
    @arg distance:
    @arg distance:
    @arg selectionSize:
    @arg selectionSize:
    @arg numberOfSelections:
    @arg numberOfSelections:
    """

    random.seed()

    personId, matrix = loadMatrix(handle)
    #printMatrix(matrix)
    families = makeFamilies(personId, matrix, distance)
    #printFamilies(families)
    for i in range(numberOfSelections) :
        selection = pickPersons(families, selectionSize)
        for j in selection :
            print j,
        print
    #for
#select

if __name__ == "__main__" :
    """
    Main entry point.
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__.split('\n\n\n')[0],
        epilog='')

    parser.add_argument("input", metavar="INPUT_FILE",
        type=argparse.FileType('r'), help="file used as input")
    parser.add_argument("-d", dest="distance", type=int, default=1,
        help="distance in generations (%(type)s default: %(default)s)")
    parser.add_argument("-z", dest="size", type=int, default=1,
        help="selection size (%(type)s default: %(default)s)")
    parser.add_argument("-s", dest="selections", type=int, default=1,
        help="number of selections (%(type)s default: %(default)s)")

    args = parser.parse_args()

    select(args.input, args.distance, args.size, args.selections)
#if
