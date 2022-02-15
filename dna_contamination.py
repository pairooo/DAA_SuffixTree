

from suffix_tree import SuffixTree
from useful_data_structures.heap_priority_queue import HeapPriorityQueue


class DNAContamination:
    __slots__ = '_string', '_stringStree', '_contaminants', '_threshold'

    def __init__(self, s, l):
        """The constructor creates a DNAContamination object initializing it with the string to be checked and the threshold value for which a contaminant is valid"""
        self._string = s
        self._stringStree = SuffixTree([self._string])
        self._threshold = l
        self._contaminants = HeapPriorityQueue()

    def addContaminant(self, c):
        """Adds a contaminant to the set of contaminants, associating the degree of contamination."""
        self._contaminants.add(-1 * self._contaminantDegree(c), c)

    #o(k*logn)
    def getContaminants(self, k):
        """Return k contaminants with the highest degree of contamination"""
        list = dict()
        for i in range(min(k, len(self._contaminants))):
            key, value = self._contaminants.remove_min()
            list[value] = -1 * key

        for key, value in list.items():
            self._contaminants.add(-1 * value, key)
        return list.keys()

    #o(len(c)*len(stringa del suffix tree ))
    def _contaminantDegree(self, c):
        """Returns the degree of contamination of a contaminanant, represented as a string"""
        lista = []
        for i in range(len(c) - (self._threshold - 1)):
            substring = c[i:]
            #calcolo di quanti caratteri matcho da i in poi
            currentMatches = self._stringMatch(substring)
            if currentMatches >= self._threshold:
                currentValue = [i, i + currentMatches]
                toBeInsert = True
                if len(lista) != 0:
                    previuosValue = lista[-1]
                    #se la stringa corrente da dover inserire è sottostringa dell' ultima appena inserita allora non la inserisco
                    if currentValue[1] == previuosValue[1] and previuosValue[0] < currentValue[0]:
                        toBeInsert = False

                if toBeInsert:
                    lista.append(currentValue)
        return len(lista)

    #o(len(stringa del suffix tree )) nel caso peggiore in cui scendo in tutti i nodi e il suffisso più lungo è l' intera stringa
    def _stringMatch(self, string):
        """Returns the total number of matches made by a string with the SuffixTree associated with the DNAContamiantion object. """
        node = self._stringStree.root()
        string += '$'
        counterMatch = 0
        # controllo se una e sottostringa di uno dei figlio o viceversa
        childNode = self._stringStree.child(node, string[counterMatch])
        while childNode is not None:
            nodeString = self._stringStree.getNodeLabel(childNode)

            for car in nodeString:
                if string[counterMatch] == car:
                    counterMatch += 1
                else:
                    return counterMatch
            childNode = self._stringStree.child(childNode, string[counterMatch])
        return counterMatch
