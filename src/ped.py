#!/usr/bin/python

"""
@requires: sys
"""

import sys

class Individual() :
    """
    """

    def __init__(self, thisId, paternalId, maternalId, dnaId) :
        """
        Initialise the instance variables.

        @arg thisId      : Id of this individual.
        @type thisId     : char
        @arg paternalId  : Id of the father of this individual.
        @type paternalId : char
        @arg maternalId  : Id of the mother of this individual.
        @type maternalId : char
        @arg dnaId       : Id of the DNA sample of this individual.
        @type dnaId      : char
        """

        self.thisId = int(thisId)
        """ Id of this individual. """

        self.paternalId = int(paternalId)
        """ Id of the father of this individual. """

        self.maternalId = int(maternalId)
        """ Id of the mother of this individual. """

        self.dnaId = 0
        """ Id of the DNA sample of this individual. """

        if not dnaId == "NA" :
            self.dnaId = int(dnaId)

        self.link = None
        """ Link to the parent object. """

        self.flag = False
        """ General purpose flag. """
    #__init__

    def depth(self) :
        """
        Return the number of steps from this node to the root of the tree.
        """
    
        numberOfSteps = 0
        thisIndividual = self
    
        while thisIndividual != thisIndividual.link :
            thisIndividual = thisIndividual.link
            numberOfSteps += 1
        #while
    
        return numberOfSteps - 1
    #depth
    
    def flagPath(self) :
        """
        Flag the path from this node to the root of the tree.
        """
    
        thisIndividual = self
    
        while thisIndividual != thisIndividual.link :
            thisIndividual.flag = True
            thisIndividual = thisIndividual.link
        #while
    #flagPath
    
    def searchFlag(self) :
        """
        Count the number of steps until we encounter a flag.

        The flag is disabled to let the clearPath() function know where the
        common ancestor is.

        @returns: The number of steps from this node to the common ancestor.
        @rtype  : integer
        """
    
        numberOfSteps = 0
        thisIndividual = self
        
        while thisIndividual != thisIndividual.link :
            if thisIndividual.flag :
                thisIndividual.flag = False
                return numberOfSteps
            #if
            thisIndividual = thisIndividual.link
            numberOfSteps += 1
        #while
    #searchFlag
    
    def clearPath(self) :
        """
        Remove the flags on the path that was made by the flagPath() function.
        If a disabled flag is found, we have found the common ancestor and 
        memorise the number of steps that were taken so far.

        @returns: The number of steps from this node to the common ancestor.
        @rtype  : integer
        """
    
        numberOfSteps = 0
        depth = 0
        thisIndividual = self
        
        while thisIndividual != thisIndividual.link :
            if not thisIndividual.flag :
                depth = numberOfSteps
            thisIndividual.flag = False
            thisIndividual = thisIndividual.link
            numberOfSteps += 1
        #while
    
        return depth
    #clearPath
#Individual

def distance(person, id1, id2) :
    """
    Calculate the distance between two individuals.

    @arg person  : Dictionary of Individual instances, indexed by id.
    @type person : dictionary
    @arg     id1 : Id of a person.
    @type    id1 : integer
    @arg     id2 : Id of a person.
    @type    id2 : integer
    """

    person[id1].flagPath()
    return person[id2].searchFlag() + person[id1].clearPath()
#distance

if __name__ == "__main__" :
    person = {}
    root = Individual(0, 0, 0, 0)
    person[0] = root

    handle = open(sys.argv[1], 'r')
    line = handle.readline()
    while line :
        data = line[:-1].split(',') # Ignore the last character ('\n').
        thisIndividual = Individual(data[1], data[2], data[3], data[4])
        person[int(data[1])] = thisIndividual
        line = handle.readline()
    #while
    handle.close()

    # Construct the tree.
    for i in person.keys() :
        person[i].link = person[person[i].paternalId]

    # Print the matrix.
    print 0,
    for i in person.keys() :
        if person[i].dnaId :
            print person[i].dnaId, 
    print
    for i in person.keys() :
        if person[i].dnaId :
            print person[i].dnaId, 
            for j in person.keys() :
                if person[j].dnaId :
                    print distance(person, person[i].thisId, person[j].thisId),
            print
        #if
#if
