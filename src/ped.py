#!/usr/bin/python

"""
@requires: sys
"""

import sys

defaultDepth = 100

class Individual() :
    """
    Class for nodes that have a pointer to their direct ancestor.
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
        Flag the path from this node to the root of the tree to make the
        searchFlag() function able to figure out what the lowest common
        ancestor is.
        """
    
        thisIndividual = self
    
        while thisIndividual != thisIndividual.link :
            thisIndividual.flag = True
            thisIndividual = thisIndividual.link
        #while
    #flagPath
    
    def searchFlag(self) :
        """
        Count the number of steps until we encounter a flag, set by the
        flagPath() function.

        The flag is disabled to let the clearPath() function know where the
        lowest common ancestor is.

        @returns: The number of steps from this node to the lowest common
            ancestor.
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

        return defaultDepth / 2
    #searchFlag
    
    def clearPath(self) :
        """
        Remove the flags on the path that was made by the flagPath() function.
        If a disabled flag is found, we have found the lowest common ancestor
        and memorise the number of steps that were taken so far.

        @returns: The number of steps from this node to the lowest common
            ancestor.
        @rtype  : integer
        """
    
        numberOfSteps = 0
        depth = defaultDepth / 2
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

        - Mark the path from individual 1 to the root.
        - Count the number of steps to the path when walking from individual 2
          to the root.
            - Undo the marking at the lowest common ancestor.
        - Count the number of marked nodes when walking from individual 2 to
          the root again.
            - Remove the rest of the markings.
        - Add the two numbers.

    @arg person  : Dictionary of Individual instances, indexed by id.
    @type person : dictionary
    @arg id1     : Id of a person.
    @type id1    : integer
    @arg id2     : Id of a person.
    @type id2    : integer
    """

    person[id1].flagPath()
    return person[id2].searchFlag() + person[id1].clearPath()
#distance

if __name__ == "__main__" :
    person = {}                   # A dictionary for the data.
    root = Individual(0, 0, 0, 0) # A root node for the tree.
    person[0] = root              # Add the root to the dictionary.

    # Parse the input file and store the data in a dictionary.
    handle = open(sys.argv[1], 'r')
    line = handle.readline()
    while line :
        data = line[:-1].split(',') # Ignore the last character ('\n').
        person[int(data[1])] = Individual(data[1], data[2], data[3], data[4])
        line = handle.readline()
    #while
    handle.close()

    # Construct the tree.
    for i in person.keys() :
        person[i].link = person[person[i].paternalId]

    # Filter out everything without a dnaId.
    for i in person.keys() :
        if not person[i].dnaId :
            person.pop(i)

    # Print the matrix.
    print "0\t",                        # Just a filler for (0,0).
    for i in person.keys()[:-1] :       # Print the first line of id's.
        print "%i\t" % person[i].dnaId,
    print person[person.keys()[-1]].dnaId

    for i in person.keys() :            # Print the content of the matrix.
        print "%i\t" % person[i].dnaId, # Print the first column of id's.
        for j in person.keys()[:-1] :
            print "%i\t" % distance(
                person, person[i].thisId, person[j].thisId),
        print distance(person, person[i].thisId, 
            person[person.keys()[-1]].thisId)
    #for
#if
