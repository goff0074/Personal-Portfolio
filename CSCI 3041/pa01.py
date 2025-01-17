def find_closest(filename):
    with open(filename, 'r') as fp:
        namBalDic = {}
        closestBal = float('inf')
        closestName = []
        fp.readline()
        for line in fp:
            name,balance,accNum = line.strip().split(',')
            namBalDic[name] = float(balance)
        for name1, balance1 in namBalDic.items():
            for name2, balance2 in namBalDic.items():
                if name1 != name2:
                    currentBal = abs(balance1 - balance2)
                    if currentBal < closestBal:
                        closestBal = currentBal
                        closestName = [name1, name2]
        return closestName
            
if __name__ =='__main__':
    print(find_closest('bank1.csv'))