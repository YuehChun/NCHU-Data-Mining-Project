from sklearn.externals.six import StringIO  
from sklearn.feature_extraction import DictVectorizer
import pydot 
from sklearn import tree
with open(fname) as f:
    content = f.readlines()
f = open('./Temp.data', 'r')
data = f.read()
# samples = [dict(enumerate(sample)) for sample in data]
# print samples

# turn list of dicts into a numpy array
# vect = DictVectorizer(sparse=False)
# X = vect.fit_transform(samples)
# print data


f = open('./temp.target', 'r')
target = f.read()



clf = tree.DecisionTreeClassifier()
clf = clf.fit(data, target)
# dot_data = StringIO() 
# tree.export_graphviz(clf, out_file=dot_data) 
# graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
# graph.write_pdf("Temp.pdf") 