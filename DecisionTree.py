"""
Allison Ryder and Kendell Byrd--Decision Tree Project

DecisionTree Class- defines all the properties and methods/functions to run program, ask for user input, generate a decision tree, and output the tree and statistics

"""

from DecisionTreeNode import *
from math import *
import sys 
import ast
from random import *


class DecisionTree(object):

  def __init__(self, examples, targetAttribute, target_values, attributes):
      self.root=None
      self.target_values = target_values
      self.targetAttribute = targetAttribute
      self.examples = examples
      self.testSet = []
      self.trainSet = []
      self.attributes = attributes
      self.attributeValuesDict={}
  """
  getTrainTestSet--asks and gets user input about what precentage of the same it wants to train and what precentage it wants to test

  """
  def getTrainTestSet(self):
	sizeTraining = raw_input("What percentage of the examples do you want to use as the training set? (0-100): ")
    	while True:
	    try:
	 	sizeTraining = int(sizeTraining)
		break
	    except ValueError:
		print "Invalid: Please enter an integer from 0 to 100!"
		sizeTraining = raw_input("What percentage of the examples do you want to use as the training set? (0-100) ")
    	while sizeTraining < 0 or sizeTraining > 100:
		print "Invalid: Please enter an integer from 0 to 100!"
		sizeTraining = raw_input("What percentage of the examples do you want to use as the training set? (0-100) ")
    
    	sizeTesting = 100-sizeTraining
    	numTraining = int(len(self.examples)*(float(sizeTraining)/100))
    	numTesting = len(self.examples)-numTraining
    
	examplesCopy = self.examples[:]
	
   	for x in range(numTraining):
		random = randrange(len(examplesCopy))
		self.trainSet.append(examplesCopy[random])
		examplesCopy.pop(random)
    	self.testSet = examplesCopy

    	print
    	print "Train Set", self.trainSet
    	print 
    	print "Test Set", self.testSet
    	print
  """
  train-- First calls getAttributeValues() to compute a dictionary of all the values for each attribute in the examples then trains trainset by calling descisionTree method
  """

  def train(self):
     self.getAttributeValues()
     self.decisionTree(self.trainSet, 0)

  """ 
  test--method that evaluates our decision tree algorithm by using the testing set to see how well it generalized given our training set decision tree. This method outputs statistics about how well the decision tree generalized.
  """

  def test(self):
     if len(self.testSet) == 0:
	return
     print "\n~~TESTING TREE~~"
     numCorrect = 0
     for item in self.testSet:
	print 
	decision = self.getDecision(item, self.root)
	print "Decision returned: ", decision
	print "Correct decision for example: ", item[self.targetAttribute]
        if decision == item[self.targetAttribute]:
		numCorrect += 1

     percent = float(numCorrect)/len(self.testSet) * 100

     print "\n--------Statistics---------\n"
     print "Number of examples in training set: ", len(self.trainSet)
     print "Number of examples in testing set: ", len(self.testSet)
     print "Number of examples classified correctly: ", numCorrect
     print ("\nPercentage classified correctly: %.2f" %(percent))

   
  """
   getDecision-takes in a dictionary entry in the test set examples and the nodes of the current decision trees(made by training set) to figure out a decision of the examples of the test set based on the training set decision tree
  """
  def getDecision(self,item,node):
	if node.leaf:
		return node.label
	nodeAttr = node.decision
	#print nodeAttr
	itemAnswer = item[nodeAttr]
	for branch in node.branch:
		if branch[1] == itemAnswer:
			return self.getDecision(item, branch[0])
	
  """
    decisionTree--Main decision tree function that creates the decision tree based on dictionary of examples passed in. Additionally, iteration is a parameter passed in so we can keep track how many times recursion is happening 
  """
  def decisionTree(self, examples, iteration):

    node=DecisionTreeNode(examples)
    node.level = iteration
    if self.targetAttribute in attributes:
        attributes.remove(self.targetAttribute)
    if iteration==0:
      self.root = node

    allFirstAttr= True
    for x in range(len(examples)):
        if examples[x][self.targetAttribute]==self.target_values[1]:  
          allFirstAttr = False
    if allFirstAttr:
        node.label = self.target_values[0]
        node.leaf = True
        return node
    allSecondAttr = True
    print examples

    for x in range(len(examples)):
        if examples[x][self.targetAttribute] == self.target_values[0]:
            allSecondAttr = False
    if allSecondAttr:
        node.label = self.target_values[1]
        node.leaf = True
        return node
    
    if len(attributes)==0:
        node.label = self.getMostCommon(examples)
        node.leaf = True
        return node


    bestA=self.bestAttribute(examples, attributes)
    node.decision=bestA
    values=self.attributeValuesDict[bestA]
    print values
    attributes.remove(bestA)
    #print bestA
    for v in values:
        subset=self.getSubset(examples,bestA,v)
        if len(subset) != 0:
            node.addBranch(self.decisionTree(subset, iteration+1), v)
    
    return node

  """
  getMostCommon--takes in the dictionaries of examples to determine which decision value is most common in the current data set
  """
  def getMostCommon(self, examples):
        numFirstValue = 0
        numSecondValue = 0
        for x in range(len(examples)):
          if examples[x][self.targetAttribute] == self.target_values[0]:
            numFirstValue += 1
          elif examples[x][self.targetAttribute]==self.target_values[1]:
            numSecondValue += 1
        if numFirstValue > numSecondValue:
            return self.target_values[0]
        else:
            return self.target_values[1]

  """
  entropy--takes in the dictionaries of examples and calculates the entropy of the set

  """
  def entropy(self, examples):
         
	 if len(examples) == 0:
	    return 0
         numFirstValue=0
         numSecondValue=0
         for x in range(len(examples)):
           print examples[x]
           if examples[x][self.targetAttribute]==self.target_values[0]:
             numFirstValue+=1
           else:
             numSecondValue+=1
         posProportion=float(numFirstValue)/len(examples)
         negProportion=float(numSecondValue)/len(examples)

         if posProportion == 0.0 or negProportion == 0.0:
		return 0
	 entropy = (-1)*posProportion*log(posProportion,2)-negProportion*log(negProportion,2)
         return entropy
  

  def gini(self, examples):
      if len(examples) ==0:
          return 0
      numFirstValue=0
      numSecondValue=0
      for i in range(len(examples)):
          if examples[i][self.targetAttribute]==self.target_values[0]:
              numFirstValue+=1
          else:
              numSecondValue+=1
      posProportion=float(numFirstValue)/len(examples)
      negProportion=float(numSecondValue)/len(examples)

      gini=1-(posProportion)-(negProportion)
      return gini

  def misClass(self, examples):
      if len(examples) == 0:
          return 0
      numFirstValue=0
      numSecondValue=0
      for i in range(len(examples)):
          if examples[i][self.targetAttribute]==self.target_values[0]:
              numFirstValue+=1
          else:
              numSecondValue+=1

      posProportion=float(numFirstValue)/len(examples)
      negProportion=float(numSecondValue)/len(examples)

      err=1-max(posProportion, negProportion)

      return err
  """
  bestAttribute--returns the best attribute based on the one with the highest info gain
  Parameters: examples dictionary and list of attributes

  """
  def bestAttribute(self, examples,attributes):
         gain_list=[]
         for i in range(len(attributes)):
                gain_list.append(self.infoGain(examples, attributes[i]))
         bestGainIndex = gain_list.index(max(gain_list))
         #print "GAIN LIST: ", gain_list
         return attributes[bestGainIndex]
  """
  generateMissingInfo--Replaces attribute values that are missing with the value that is common in current set of dictionaries for that given attribute

  Parameters: examples dictionaries, the current attribute, and list of values of current attribute
  """
  def generateMissingInfo(self, examples, attribute, values): 
	
        copy_values=values[:]
        count=[]
        for i in range(len(copy_values)):
            count.append(0)

        for x in range(len(examples)):
          for j in range(len(copy_values)):
            if examples[x][attribute] == copy_values[j]:
                count[j]+=1

        index=count.index(max(count))
        value = copy_values[index]

	for x in range(len(examples)):
		if examples[x][attribute] == "?":
			examples[x][attribute] = value


  """
  infoGain--calculates the information gain of a current attribute in the dictionary of examples 
  Parameters: Dictionaries of examples, current attribute
  """
  def infoGain(self,examples, attribute):

        gain = self.entropy(examples) 
        values=self.attributeValuesDict[attribute]
	if '?' in values:
		self.attributeValuesDict[attribute].remove('?')
		self.generateMissingInfo(examples, attribute, values)
        for v in range(len(values)):
            subset = self.getSubset(examples, attribute, values[v])
            gain -= (float(len(subset)))/len(examples)*self.entropy(subset)
        return gain
        
  """
  getSubset--Given a value, attribute, and data set, getSubset constructs a list  of dictionaries that contain that attribute and value

  Parameters: examples, current attribute, and value of attribute
  """
  def getSubset(self, examples, attribute, v):
        subset = []
        for x in range(len(examples)):
            if examples[x][attribute] == v:
                subset.append(examples[x])
        return subset
  """
  getAttributeValues--calculates the attribute values of all the attributes in the given data set and stores each attribute and a list of its values in a dictionary
  """
  def getAttributeValues(self):
        dic={}
        for attr in self.examples[0].keys():
            attr_values=[]
            for i in range(len(examples)):
              if self.examples[i][attr] not in attr_values:
                attr_values.append(self.examples[i][attr]) 
            dic[attr]=attr_values
        self.attributeValuesDict=dic

  """
  printTree--prints out or decision tree
  Parameters-A decision tree node (typically root)
  """
  def printTree(self,node):
      space = (node.level)*"\t"
      if node.decision != None:
        print space, "Attribute:", node.decision
      space = (node.level+1)*"\t"
      for i in node.branch:
          if i[0].leaf:
              print space, "Value:", i[1], "DECISION:", i[0].label 
          if not i[0].leaf:
	    print space, "Value:", i[1]
            self.printTree(i[0])

 

  
if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        print "Usage: python DecisionTree.py filename.txt"
        exit(1)
    filename = sys.argv[1]
    print "Using file:", filename
    """

    print
    print "~~~~~ Welcome to the decision tree program!!! ~~~~~"
    print

    print "What type of decision tree would you like to see?"
    print "\t(1) binary data"
    print "\t(2) tennis data"
    print "\t(3) voting data"
    choice = raw_input("Please enter the number of your choice: ")
    while choice != "1" and choice != "2" and choice != "3":
	print "That's not a valid choice!"
	choice = raw_input("Please enter the number of your choice: ")

    if choice == "1":
	filename = "binaryDataA.py"
	targetAttr = "out"
	target_values = ["+","-"]
    elif choice == "2":
	filename = "tennisData.py"
	targetAttr = "play"
	target_values = ["+","-"]
    elif choice == "3":
	filename = "votingData.py"
	targetAttr = "party"
	target_values = ["democrat","republican"]

    f = open(filename, "r")
    examples = []

    for line in f:
        line = line.rstrip()
        line = ast.literal_eval(line)
        examples.append(line)
    attributes=[]
    attributes=examples[0].keys()

    dtree=DecisionTree(examples, targetAttr, target_values, attributes)
    dtree.getTrainTestSet()
    dtree.train()
    dtree.test()

    print "\n---------Decision Tree Result-----------\n"
    dtree.printTree(dtree.root)
    print 

    

