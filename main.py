from itertools import permutations

import pandas
DataSet = pandas.read_csv("Vertical_Format.csv")
if (DataSet.columns[0] != "Tid" and DataSet.columns[1] != "items"):
    print("-----------------------Vertical Data----------------------------")
    print(DataSet)
    horizontal_DataSet = {}
    unique_ids = []
    for i in DataSet['TID_set']:
        for j in i:
            if j not in unique_ids:
                if j != ',':
                 unique_ids.append(j)

    for i in range(0,len(DataSet.values)):
        for ID in DataSet.values[i][1]:
            if ID in unique_ids:
                ID=int(ID)
                if ID in horizontal_DataSet:
                    if isinstance(horizontal_DataSet[ID], list):
                        horizontal_DataSet[ID].append(DataSet.values[i][0])
                    else:
                        horizontal_DataSet[ID] = [horizontal_DataSet[ID], DataSet.values[i][0]]
                else:
                    horizontal_DataSet[ID] = [DataSet.values[i][0]]

    DataSet = pandas.DataFrame(horizontal_DataSet.items(), columns=['TID', 'items'])
    DataSet['items'] = DataSet['items'].apply(lambda x:','.join(x))
    print("----------------------Converted To Horizontal--------------------------")
    print(DataSet)
    print("-----------------------------------------------------------------------")

minimum_support =  int(input("minimum support ??"))
minimum_confidence = float(input("minimum confidence ??"))
All_Items = []
Transactions = DataSet.values.tolist()
UniqueItems = []
Support_Items = {}
allFreqItems = {}
AllitemsConfidence = {}
All_rules = []

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
print(f"c1 : {UniqueItems}")
print(f"L1:{allFreqItems}")
print("------------------------------------------------------------------------------------------")
items = generating_item_sets(Support_Items,2)
while True :
    print(f"c{i-1}: {items}")
    freq = getFrequentItems(items)
    print(f"L{i-1} : {freq}")
    print("------------------------------------------------------------------------------------------")
    allFreqItems.update(freq)
    if len(freq)<=1:
        break

    items = generating_item_sets(freq,i)
    i+=1
for element in list(allFreqItems.keys()):
    for i in range(1,len(element)):
        for subset in permutations(element, i):
            rule = (tuple(sorted(subset)), tuple(sorted(item for item in element if item not in subset)))
            All_rules.append(rule)
print("All Frequent Items")
print(allFreqItems)
print("-------------------------------------------------------------------------------------------")
def calc_conf(item1,item2):
    sortedfreq = {}
    for i in list(allFreqItems.keys()):
        sortedfreq[tuple(sorted(i))]=allFreqItems[i]
    if (len(item1)==1):
        item1 = item1[0]
        s1=allFreqItems[item1]
    else :
        s1=sortedfreq[item1]

    if type(item1) ==tuple :
        item1=item1+item2
    else :
        item1=tuple(item1)+item2
    found= False

    s2= sortedfreq[tuple(sorted(item1))]

    confidence = (s2/s1)*100
    return confidence


stronk = {}
weak={}
for item in All_rules :
    print(f"{item[0]}---->{item[1]}: {calc_conf(item[0],item[1])}")
    if calc_conf(item[0],item[1]) >= minimum_confidence*100:
        stronk[item]=calc_conf(item[0],item[1])
    else :
        weak[item]=calc_conf(item[0], item[1])
print("------------------------------------------------------------------------------------------")
print("-----------------------------STRONG RULES--------------------------------------------------")
for item in list(stronk.keys()) :
    print(f"{item[0]}---->{item[1]}: {stronk[item]}")


def calc_lift(item1,item2):
    sortedfreq = {}
    for i in list(allFreqItems.keys()):
        sortedfreq[tuple(sorted(i))]=allFreqItems[i]
    if (len(item1)==1):
        item1 = item1[0]
        s1=allFreqItems[item1]
    else :
        s1=sortedfreq[item1]

    s1=s1/len(Transactions)

    if (len(item2) == 1):
        item2 = item2[0]
        s2 = allFreqItems[item2]
    else:
        s2=sortedfreq[item2]

    s2 = s2 / len(Transactions)




    if type(item1) ==tuple and type(item2)==tuple :
        item1=item1+item2
    else :
        item1=tuple(item1)+tuple(item2)
    found= False
    sortedfreq = {}
    for i in list(allFreqItems.keys()):
        sortedfreq[tuple(sorted(i))]=allFreqItems[i]
    s3= sortedfreq[tuple(sorted(item1))]
    s3=s3/len(Transactions)



    lift= s3/(s1*s2)
    return lift

Positive_Correlation = {}
Negative_Correlation ={}
for item in All_rules :
    if calc_lift(item[0],item[1]) > 1:
        Positive_Correlation[item]=calc_lift(item[0],item[1])
    else :
        Negative_Correlation[item]=calc_lift(item[0], item[1])

print("------------------------------------------------------------------------------------------")
print("-----------------------------POSITIVE CORRELATION--------------------------------------------------")
for item in list(Positive_Correlation.keys()) :
    print(f"{item[0]}---->{item[1]}: {Positive_Correlation[item]}")


print("------------------------------------------------------------------------------------------")
print("-----------------------------NEGATIVE CORRELATION--------------------------------------------------")
for item in list(Negative_Correlation.keys()) :
    print(f"{item[0]}---->{item[1]}: {Negative_Correlation[item]}")