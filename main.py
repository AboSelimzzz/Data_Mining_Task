import pandas

minimum_support =   2

DataSet = pandas.read_csv("WannyData.csv")
All_Items = []
Transactions = DataSet.values.tolist()
UniqueItems = []
Support_Items = {}
allFreqItems = {}

for i in range(len(DataSet.values)):
    Transactions[i] = Transactions[i][1]

for i in range(len(DataSet.values)):
    All_Items += str.split(Transactions[i], ',')


for i in All_Items:
    if not (i in UniqueItems):
        UniqueItems.append(i)


for eachitem in UniqueItems:
    support = 0
    for i in Transactions:
        if i.find(eachitem) != -1:
            support = support + 1

    Support_Items[eachitem] = support

Support_Items = {key: value for key, value in Support_Items.items() if value >= minimum_support}

allFreqItems.update(Support_Items)

def generating_item_sets(frequent_item_set, k_level):
    if k_level == 2:
        candidates = []
        for i, value in enumerate(frequent_item_set):
            for j, value2 in enumerate(frequent_item_set):
                if j > i:
                    each_candidate = []
                    each_candidate.append(value)
                    each_candidate.append(value2)
                    candidates.append(each_candidate)
        return candidates
    else:
        candidates = list(frequent_item_set.keys())
        tmp = []
        for i in range(len(candidates)):
            for j in range( i+1,len(candidates)):
                if candidates[i][0:k_level-2] == candidates[j][0:k_level-2]:
                    each_candidate = []
                    for k in candidates[i]:
                        each_candidate.append(k)
                    each_candidate.append(candidates[j][-1])
                    tmp.append(each_candidate)




        return tmp
def getFrequentItems(candidates):
    freqItems={}
    for candidate in candidates :
        support = 0
        for transaction in Transactions :
            for item in candidate :
                if transaction.find(item)==-1:
                    break
                if item==candidate[-1]:
                   support+=1
        if support >= minimum_support:
            freqItems[tuple(candidate)] = support
    return freqItems


i=3
items = generating_item_sets(Support_Items,2)
while True :
    freq = getFrequentItems(items)
    allFreqItems.update(freq)
    if len(freq)<=1:
        break

    items = generating_item_sets(freq,i)
    i+=1



print(allFreqItems)
