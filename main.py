import pandas

minimum_support = 3

DataSet = pandas.read_csv("Horizontal_Format.csv")
All_Items = []
Transactions = DataSet.values.tolist()
UniqueItems = []
Support_Items = {}

for i in range(len(DataSet.values)):
    Transactions[i] = Transactions[i][1]

for i in range(len(DataSet.values)):
    All_Items += str.split(Transactions[i], ',')

for i in All_Items:
    if i not in UniqueItems:
        UniqueItems += i

for element in UniqueItems:
    support = 0
    for i in Transactions:
        for j in i:
            if j == element:
                support += 1
                break
    Support_Items[element] = support

Support_Items = {key: value for key, value in Support_Items.items() if value >= minimum_support}


def generating_item_sets(frequent_item_set, k_level):
    candidates = []
    if k_level == 2:
        for i, value in enumerate(frequent_item_set):
            for j, value2 in enumerate(frequent_item_set):
                if j > i:
                    each_candidate = []
                    each_candidate.append(value)
                    each_candidate.append(value2)
                    candidates.append(each_candidate)
        return candidates
    else:
        tmp = []
        for i in range(len(candidates)):
            for j in range(len(candidates)):
                Done = 1
                if j > i:
                    for index in range(k_level - 2):
                        if candidates[i][index] != candidates[j][index]:
                            Done = 0
                            break

                        if Done:
                            each_candidate = []
                            for k in candidates[i]:
                                each_candidate.append(k)
                            each_candidate.append(candidates[j][-1])
                            tmp.append(each_candidate)
        return tmp


