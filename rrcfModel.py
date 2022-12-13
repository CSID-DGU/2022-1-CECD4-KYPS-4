import numpy as np
import rrcf
import csv
import time
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import colors

ftr=[3600,60,1]

num_trees = 50
tree_size = 128

forest = []

avg_codisp={}

idx=0

falldown=False

realfalldown=False

def make_tree():
    for _ in range(num_trees):
        tree = rrcf.RCTree()
        forest.append(tree)
    

def rrcfModel_run(new_node):
    
    if realfalldown==False:
        return

    # 매개변수로 노드가 들어와

    # 노드가 rrcf 모델에 계속 업데이트 됨

    # f = open('RECORD.csv', 'r', encoding='UTF8')
    # rdr = csv.reader(f)
    
    # lines = []

   

    # for line in rdr:
    #     timestr=line[1]
    #     timeSecond = sum([a*b for a,b in zip(ftr,map(int, timestr.split(':')))])
    #     line[1]=timeSecond
    #     lines.append(line) 

    now = time.localtime()
    timestr = time.strftime('%X', now)
    timeSecond = sum([a*b for a,b in zip(ftr,map(int, timestr.split(':')))])

    data=[]
    data.append(new_node)
    data.append(timeSecond)
    
    # lines.append(line_node)
    # X=np.array(lines,dtype=float)

    X=np.array(data,dtype=float)

    # sampel_size_range = (len(X)//tree_size,tree_size)

    # forest = []

    # for _ in range(num_trees):
    #     tree = rrcf.RCTree()
    #     forest.append(tree)

    # points = rrcf.shingle(lines, size=sampel_size_range)


    global idx
    global falldown
    global realfalldown
    
    for tree in forest:
        if len(tree.leaves) > tree_size:
            tree.forget_point(idx-tree_size)
                    # Insert the new point into the tree
        tree.insert_point(X, index=idx)
        # Compute codisp on the new point...
        new_codisp = tree.codisp(idx)
        # And take the average over all trees
        if not idx in avg_codisp:
            avg_codisp[idx] = 0
        avg_codisp[idx] += new_codisp / num_trees
    
    test_df = pd.Series(avg_codisp)
    isAbnormal = (avg_codisp.get(len(avg_codisp)-1)>test_df.quantile(0.9))
    if isAbnormal == True and falldown == True:
        print("real falldown!")
        # realfalldown=True

    idx=idx+1
    
    # avg_codisp={}
    # for index, point in enumerate(X):
    #     for tree in forest:
    #         # If tree is above permitted size...
    #         if len(tree.leaves) > tree_size:
    #             # Drop the oldest point (FIFO)
    #             tree.forget_point(index - tree_size)
    #         # Insert the new point into the tree
    #         tree.insert_point(point, index=index)
    #         # Compute codisp on the new point...
    #         new_codisp = tree.codisp(index)
    #         # And take the average over all trees
    #         if not index in avg_codisp:
    #             avg_codisp[index] = 0
    #         avg_codisp[index] += new_codisp / num_trees

    

    # #test_df = pd.Series(avg_codisp, index=np.arange(len(avg_codisp)))
    # test_df = pd.Series(avg_codisp)
    # print("------------")
    # print("현재값")
    # print("인덱스 : ",len(avg_codisp)-1,"값 : ",avg_codisp.get(len(avg_codisp)-1))
    # print("------------")
    # print("상위 90",'%',"기준값 : ",test_df.quantile(0.9))
    # print("결과 : ")
    # print(avg_codisp.get(len(avg_codisp)-1)>test_df.quantile(0.9))

#print(test_df.quantile(0.995), test_df.get(329))
#print(avg_codisp>avg_codisp.quantile(0.995)) 

# forest = []
# while(len(forest)<num_trees):
#     ixs=np.random.choice(len(X), size=sampel_size_range, replace=False)
#     trees=[rrcf.RCTree(X[ix], index_labels=ix) for ix in ixs]
#     forest.extend(trees)

# avg_codisp=pd.Series(0.0, index=np.arange(len(X)))
# index = np.zeros(len(X))

# threshold = avg_codisp.nlargest(n=10).min()

# for tree in forest:
#     codisp = pd.Series({leaf:tree.codisp(leaf) for leaf in tree.leaves})
#     avg_codisp[codisp.index] += codisp
#     np.add.at(index, codisp.index.values, 1)


# avg_codisp /= index

# # threshold = avg_codisp.nlargest(n=10).min()
# fig = plt.figure(figsize=(12,4))
# ax = fig.add_subplot(121, projection='3d')
# sc = ax.scatter(X[:,0], X[:,1],
#                 c=np.log(avg_codisp.sort_index().values),
#                 cmap='gnuplot2')
# plt.title('log(CoDisp)')
# ax = fig.add_subplot(122, projection='3d')
# sc = ax.scatter(X[:,0], X[:,1],
#                 linewidths=0.1, edgecolors='k',
#                 c=(avg_codisp >= threshold).astype(float),
#                 cmap='cool')
# plt.title('CoDisp above 99.5th percentile')

