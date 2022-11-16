def printTable(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            #print with width 5
            print("{:30}".format(str(table[i][j])), end=" ")
           
        print("")