from useful_data_structures.tree import Tree
from useful_data_structures.probe_hash_map import ProbeHashMap


class SuffixTree(Tree):
    class _Node():
        __slots__ = '_value', '_parent', '_children', '_marker', '_length'

        def __init__(self, value, parent, length=0):
            """Inizializes the node that represents the information associated with the suffix tree."""
            self._value = value
            self._parent = parent
            self._children = ProbeHashMap(cap=26)  # in order to have a lookup table for english characters
            self._marker = set()
            self._length = length

    class Position(Tree.Position):

        __slots__ = '_container', '_node'

        def __init__(self, container, node):
            """Inizializes the position that contains the node and a reference to the suffix three it belongs to."""
            self._container = container
            self._node = node

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    __slots__ = '_strings', '_root'

    #la creazione ha complessita len(strings)* la stringa più lunga, nel caso sia solo una o(n^2) (la stringa più lunga è il suffisso più lungo)
    def __init__(self, strings):
        """Initialize the Suffix Tree with a list of strings passed as input """
        self._strings = strings
        self._root = self._make_position(self._Node([0, 0, 0], None))
        for stringNumber, string in enumerate(strings):
            self._addString(string, stringNumber + 1)

    def _validate(self, p):
        """It checks if the input position is valid for that Suffix tree and if it is, it returns the associated node, otherwise it raises an exception."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """From the input node create a position associating the Suffix tree"""
        return self.Position(self, node) if node is not None else None

    def root(self):
        """Returns the root of the associated Suffix Tree"""
        return self._root

    def _addString(self, string, stringNumber):
        """The method adds all the suffixes of a string to the Suffix Tree"""
        for i in range(1, len(string) + 1):
            self._addSuffix([stringNumber, len(string) - i, len(string)])

    #Il peso è dato dalla chiamata ricorsiva che viene effettuata al massino la lunghezza del suffisso ipotizzando che ad ogni nodo si abbia 
    # un unica lettera come stringa
    def _addSuffix(self, suffix, p=None):
        """Given in input a suffix the method adds properly this last one to the Suffix Tree"""
        suffix_string = self._compactToString(suffix)
        if p is None:
            p = self.root()
        pnode = self._validate(p)
        children = pnode._children
        if not self.is_root(p):
            pstring = self._compactToString(pnode._value)
            marker = pnode._marker

        #caso in cui ci si ritrova nella radice oppure la stringa nel nodo è contenuta nella suffisso da inserire --> faccio una chiamata ricorsiva
        if self.is_root(p) or suffix_string.startswith(pstring):
            mismatch = 0
            if not self.is_root(p):
                mismatch = self._num_match(suffix, pnode._value)
                p._node._marker.add(suffix[0])
            try:
                child = self._validate(children[suffix_string[mismatch]])
            except:
                child = None
            suffix[1] = mismatch + suffix[1]
            if child is None:
                node = self._Node(suffix, p, self.getNodeDepth(p) + (suffix[2] - suffix[1]))
                node._marker.add(suffix[0])
                tempKey = self._strings[suffix[0] - 1][suffix[1]:suffix[1] + 1]
                if tempKey == '':
                    tempKey = '$'
                if not self.is_root(p):
                    marker.add(suffix[0])
                    if len(p._node._children) == 0:
                        endss_node = self._Node(
                            [suffix[0], len(self._strings[suffix[0] - 1]), len(self._strings[suffix[0] - 1])], p,
                            self.getNodeDepth(p))
                        endss_node._marker.add(suffix[0])
                        children["$"] = self._make_position(endss_node)
                children[tempKey] = self._make_position(node)
            else:
                self._addSuffix(suffix, self._make_position(child))
        else:
        #caso in cui vi è un mismatch tra la stringa nel nodo e il suffisso da inserire oppure 
        # il suffisso da inserire è contenuto nella stringa del nodo --> creo un nodo intermedio a cui attacco le due stringhe (una potrebbe essere il carattere di fine stringa)
            mismatch = self._num_match(suffix, pnode._value)

            gpnode = self._validate(pnode._parent)
            parent_node = self._Node([pnode._value[0], pnode._value[1], pnode._value[1] + mismatch],
                                     self._make_position(gpnode), pnode._length - (len(pstring) - mismatch))

            gpnode._children[pstring[0]] = self._make_position(parent_node)
            parent_node._marker.update(marker)
            parent_node._marker.add(suffix[0])
            pnode._value[1] = pnode._value[1] + mismatch
            pnode._parent = self._make_position(parent_node)

            if pstring.startswith(suffix_string):
                endss_node = self._Node([suffix[0], suffix[2], suffix[2]], self._make_position(parent_node),
                                        self.getNodeDepth(self._make_position(parent_node)))
                parent_node._children["$"] = self._make_position(endss_node)
            else:
                endss_node = self._Node([suffix[0], suffix[1] + mismatch, suffix[2]], self._make_position(parent_node),
                                        len(self._compactToString(suffix)) + gpnode._length)
                parent_node._children[suffix_string[mismatch]] = self._make_position(endss_node)

            parent_node._children[self._compactToString(pnode._value)[0:1]] = p
            endss_node._marker = set({suffix[0]})

    def _compactToString(self, compact):
        """From the compact form of a string [string index, start index, end index], returns the explicitly string """
        if compact[0] == 0:
            return ""
        return self._strings[compact[0] - 1][compact[1]:compact[2]]

    def _num_match(self, substringC, nodestringC):
        """The method returns the number of matched characters between two strings"""
        substring = self._compactToString(substringC)
        nodestring = self._compactToString(nodestringC)

        countMatch = 0
        if len(substring) >= len(nodestring):
            for i in range(0, len(nodestring)):
                if substring[i] == nodestring[i]:
                    countMatch += 1
                else:
                    break
        else:

            for i in range(0, len(substring)):
                if (substring[i] == nodestring[i]):
                    countMatch += 1
                else:
                    break
        return countMatch

    # ------------------------INTERFACE METHODS--------------------
    
    #o(1)
    def getNodeLabel(self, p):
        """The method takes in input a position and returns the information, the string, associated to it"""
        node = self._validate(p)
        return self._compactToString(node._value)

    #o(lunghezza della sottostringa in p)
    def pathString(self, p):
        """The method takes in input a position and returns the information, the string, representative of the path from the root to the same position"""
        node = self._validate(p)
        str = ''
        while node is not self._validate(self.root()):
            str = self._compactToString(node._value) + str
            node = self._validate(node._parent)
        return str

    #o(1) il parametro length definisce la lunghezza dalla radice fino alla sottostringa corrente
    def getNodeDepth(self, p):
        """ It returns the length of substring associated to the path from the root to the position in input"""
        node = self._validate(p)
        return node._length

    #o(1)
    def getNodeMark(self, p):
        """It returns the mark of the position"""
        node = self._validate(p)
        return node._marker

    #controllo se è presente un figlio nella hashmap con chiave s[0], se presente ritorno la position solo se soddisfa la condizione o(s) (ammortizzato?!)
    def child(self, p, s):
        """ If exists it returns the position of the child that contain or is contained in the input string"""
        parent_node = self._validate(p)
        try:
            position = parent_node._children[s[0]]
        except:
            return None
        node_string = self.getNodeLabel(position)
        if node_string.startswith(s) or s.startswith(node_string):
            return position
        return None
