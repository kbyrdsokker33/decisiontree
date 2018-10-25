# decision trees
1 Introduction
A decision tree is a tree-like model or graph representation that can be used to make sequential
decision problems. Decision trees are one of the most simplest and successful supervised learning
techniques which results in decision trees being one of the most commonly used methods in the
field of artificial intelligence. Supervised learning is a type of machine learning feedback that gives
the agent (decision tree in this case) a collection of input-output examples so then the decision
tree can use a function to correctly map those input values to the output values. By doing this
continued mapping, the decision tree should be able to learn how to generalize these values well,
so that when novel examples come, it will be able to predict their output values correctly. Since
a decision tree is creating this graph of values that helps the user make decisions like Should I go
to this restaurant? or Should I go play soccer, they ultimately work much better with data that is
discrete. This is because we have to have each value to represent a specific node on the tree. Each
value of the nodes of the trees are called attributes (examples of attributes for the soccer example
above could be Outlook, Humidity, Field Condition, or Temperature). The decision tree passes in
a vector or dictionary of these attributes and their values into its function. One of the goals of a
decision tree is to reach/find a decision in the most efficient and effective way possible. This usually
results in having small tree sizes very desirable. To achieve this, the decision tree tries to find the
most informative attribute and add it to the tree first. To find the most informative attribute the
decision tree calculates the entropy and information gain of each attribute. Entropy is the amount
of variability in a current set, so set will have an entropy of 0 when all its members are in the same
class (for the soccer example, if the Outlook attribute had a value that was rain and rain always
gave the output of no for whether or not to play soccer, then this set would have an entropy of 0).
The equation for entropy of an entire set is:
Entropy(S) = -Pos * log2(Pos) - Neg * log2(Neg)
Where S is the set, Pos is the number of positive outputs in current set, and Neg is the number
of negative outputs in entire set. Note: I also use Gini and MisClassification Index to find impurity of a set. Once we calculate entropy we can calculate the information gain
for an attribute which is given by the equation:

Gain(attribute) = Entropy(S) - *Entropy(examples when attribute value is positive) - *En-
tropy(examples when attribute value is negative).

The attribute that gives us the largest information gain is the one that is added to the tree
first. The decision tree continues to calculate these values until it has formed the best possible tree.


2 Details
I implemented this decision tree program by first providing the user with a menu asking what
type of data they would like to display a decision tree for. As stated in the introduction, there are
three options: binary data, tennis data, and voting data. Based on the answer to this question, I
specified what the target attribute is and what the possible values for the target attribute are.
I implemented a DecisionTree class and DecisionTreeNode class to accomplish my goal. The
initializer for the DecisionTree class sets the values for the examples to be looked at, the target
attribute, possible values of the target attribute, and the list of possible attributes. The Decision-
TreeNode class also initializes the examples so that are being focused on, in addition, it contains
properties such as whether the current node is a leaf, what level in the tree the current node is at,
the best attribute that the node will be labeled, and the label of the decision (for example: yes or
no or + or -). The DecisionTreeNode class also has an addBranch method that adds a node to a
list of the branches of the tree.

In the DecisionTree Class, I implemented a method to divide the examples provided to the
class into the training set and the testing set. I do this by asking the user what percentage of the
set they would like to use for the training set. Based on the answer to this question, I randomly
pick instances from the set of examples to be added to the training set. Whatever examples are
left become the testing set.
When I call train, this constructs the decision tree. The basis of my recursive algorithm
includes this:

I first create my node by passing in the current dictionary of examples into my Decision-
TreeNode class. Then, I constructed my base cases which sees if all the examples have the same
type of decision. If the answer is yes, then I label my current node as that decision and return
the node. Additionally, I check if my list containing all of my attributes is empty , and if it is,
then I label my node by finding the most common decision in the set of examples, and return
the node. If the algorithm has passed my base cases then I have it find the best attribute in
the dictionary of examples. I calculate the best attribute in my bestAttribute method where
I call the method infoGain. InfoGain calculates the information gain on a current attribute by
calculating the entropy of a set and its subsets (by using the equation described in the Introduc-
tion) and then applies the entropy values it gets to the information gain equation (also described
in Introduction). Additionally, in infoGain, I made sure to handle if some attributes had missing
values in the data sets. Missing values were represented by a ? in my sets, to compensate for
this I created a generateMissingInfo method which replaced the missing values in my dictionary
examples to reflect the distribution of values for that attribute in the current set of examples. To
reflect the distribution I substituted the missing values with the value that was most common in
my examples for that given attribute.

After my best attribute was found, I set my nodes decision property to be that said attribute.
I then iterated over the possible values of the current attribute and found a subset of dictionar-
ies that contained the attribute and value. Finally I recursively called of decisionTree in my
node.addBranch method, which allowed us to continue to construct my tree.
Once I have the decision tree constructed using the training data, I test how much this tree
generalizes to the examples in the testing data. I did this by writing a method that recursively
finds the decision that would be given for each example in the testing set. I then compare the
decision returned from the tree to what the expected output specified by the example is. I keep
track of how many examples were classified correctly, and output statistics to the user at the end.


3 Results
To analyze how the performance is affected by the size of the training set, I ran the program five
times on the data set summarizing voting outcomes with training set percentages ranging from 30-
80. I recorded the statistic for what percentage of the examples in the testing set were classified
correctly using the decision tree built from the training set. The results are summarized in the
table shown below.
Average percentage of testing set classified correctly: 30 percent training set: 88.786 40 percent
training set: 86.588 50 percent training set: 88.348 60 percent training set: 88.276 70 percent
training set: 89.312 80 percent training set: 89.884
What is interesting about these results is that a higher percentage of examples contained in the
training set did not necessarily correlate with a higher percentage of examples classified correctly.
This could be because the size of the voting data is excessively large in the first place.

4 Conclusions
Overall, my decision tree implementation was successful in analyzing the examples given to it and
creating a decision tree that generalized to the testing set around 90 percent of the time. In general,
decision trees are bad at handling examples with missing data. I handled this problem by filling
in the missing data with values that reflected the distribution of the overall set of examples. There
are several other modifications that I could have made to improve my performance slightly. With
my current implementation, I did not control for the branching factor of the decision tree. I
could have controlled the amount of examples allowed in a particular node when splitting. For
both my binary data and my tennis data, the resulting decision trees were simple and easy to
understand. However, with my voting data, the decision tree was large and difficult to understand.
This is another weakness of decision trees. In this case, it quickly produces decisions, but it is
difficult for humans to understand how that decision was made.
