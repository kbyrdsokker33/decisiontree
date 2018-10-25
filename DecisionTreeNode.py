class DecisionTreeNode(object):

    def __init__(self, examples):
        self.examples=examples
	self.level = 0
        self.branch=[]
        self.label = None
        self.leaf = False
        self.decision=None
        self.parent=None

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def getExamples(self):
        return self.examples

    def getAttribute(self):
        return self.attribute

    def setAttribute(self, attribute):
        self.attribute=attribute

    def getParent(self):
        return self.parent 

    def isLeaf(self):
        return self.leaf

    def getLabel(self):
        return self.label

    def setLeaf(self):
        self.leaf = True

    def setLabel(self, label):
        self.label = label
    
    def setLevel(self, level):
	self.level = level

    def getLevel(self):
	return self.level

    def addBranch(self, node, value):
        self.branch.append((node,value))

    def getBranches(self):
        return self.branch

