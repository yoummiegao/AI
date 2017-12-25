# show A star searching method implementation in python
# feng

import numpy as np
class State:
    def __init__(self,state,dFlag = None,parent = None,sfN = None,sfN_Mis = None,sgN = 0):
        self.state = state
        self.direction = ['left','right','up','down']
        if dFlag:
            self.direction.remove(dFlag)
        self.symbol = ' '
        self.answer = np.array([[1,2,3],[4,self.symbol,5],[6,7,9]])
        self.parent = parent
        self.fN = sfN
        self.fN_Mis = sfN_Mis
        self.gN = sgN
    def showInfo(self):
        # for i in range(3):
        #     for j in range(3):
        #         print(self.state[i, j])
        #         print(' ')
        #     print("\n")
        print(self.state)
        print('->')
        return
    def calManhatton(self):
        manDistance = 0
        for element in self.answer.flat:
            if element != self.symbol:
                rowF,colF = np.where(self.answer == element)
                rowC,colC = np.where(self.state == element)
                manDistance = manDistance + abs(rowF - rowC) + abs(colF - colC)
        return manDistance
    def calMisplacedTile(self):
        calDistance = 0
        for element in self.answer.flat:
            if element != self.symbol:
                positionF = np.where(self.answer == element)
                positionC = np.where(self.state == element)
                if (positionC != positionF):
                    calDistance = calDistance + 1
        return calDistance
    def calfN(self):
        self.fN = self.calManhatton() + self.gN
    def calfN_Mis(self):
        self.fN_Mis = self.calMisplacedTile() + self.gN
    def getEmptyPos(self):
        postion = np.where(self.state == self.symbol)
        return postion
    def gSubStates(self,sMethd = 0):
        if not self.direction:
            return []
        subStates = []
        boarder_d, board_w = np.shape(self.state)
        row, col = self.getEmptyPos()
        if row == 0:
            self.direction.remove('up')
        elif row == boarder_d - 1:
            self.direction.remove('down')
        if col == 0:
            self.direction.remove('left')
        elif col == board_w - 1 :
            self.direction.remove('right')

        if 'left' in self.direction:
            s = self.state.copy()
            temp = s[row,col-1]
            s[row,col-1]=s[row,col]
            s[row,col] = temp
            new_S = State(s,'right',self,None,None,self.gN+1)
            if(sMethd == 0):
                new_S.calfN()
            elif(sMethd == 1):
                new_S.calfN_Mis()
            #new_S.calfN()
            subStates.append(new_S)
        if 'right'in self.direction:
            s = self.state.copy()
            temp = s[row,col + 1]
            s[row,col + 1] = s[row,col]
            s[row,col] = temp
            new_S = State(s,'left',self,None,None,self.gN+1)
            if (sMethd == 0):
                new_S.calfN()
            elif (sMethd == 1):
                new_S.calfN_Mis()
            #new_S.calfN()
            subStates.append(new_S)
        if 'up' in self.direction:
            s = self.state.copy()
            temp = s[row -1,col]
            s[row - 1,col] = s[row, col]
            s[row, col] = temp
            new_S = State(s,'down',self,None,None,self.gN+1)
            if (sMethd == 0):
                new_S.calfN()
            elif (sMethd == 1):
                new_S.calfN_Mis()
            #new_S.calfN()
            subStates.append(new_S)
        if 'down' in self.direction:
            s = self.state.copy()
            temp = s[row + 1, col]
            s[row + 1, col] = s[row, col]
            s[row, col] = temp
            new_S = State(s,'up',self,None,None,self.gN+1)
            if (sMethd == 0):
                new_S.calfN()
            elif (sMethd == 1):
                new_S.calfN_Mis()
            #new_S.calfN()
            subStates.append(new_S)
        return subStates
    def solve(self, sMethd = 0):
        openTable = []
        closeTable = []

        openTable.append(self)

        #gN = 0
        resminH = 3000
        minH = resminH
        if(sMethd == 0):
            self.calfN()
        elif (sMethd == 1):
            self.calfN_Mis()
        #self.calfN()
        steps = 0

        while len(openTable) > 0:
            path = []
            for s in openTable:
                if(sMethd == 0):
                    if (s.fN <= minH):
                        minH = s.fN
                        tempS = s
                elif (sMethd == 1):
                    if (s.fN_Mis <= minH):
                        minH = s.fN_Mis
                        tempS = s
            sMin = tempS
            if (sMin.state == sMin.answer).all():
                while sMin.parent and sMin.parent != originState:
                    path.append(sMin.parent)
                    sMin = sMin.parent
                    steps += 1
                path.reverse()
                return path, steps
            openTable.pop(openTable.index(sMin))
            closeTable.append(sMin)
            subStates = sMin.gSubStates(sMethd)
            minH = resminH
            openTable.extend(subStates)
        return



if __name__ == '__main__':
    syEmpty = ' '
    originState = State(np.array([[syEmpty,2,4],[1,6,3],[5,9,7]]))
    print("From original state 1st,")
    s1 = State(state=originState.state)
    path1, steps1 = s1.solve(0)
    if path1:                        # if find the solution
        for node1 in path1:
                # print the path from the origin to final state
                node1.showInfo()
        print(s1.answer)
        print("Total steps when using Manhatan Distance as h is %d\n" % steps1)

    s1 = State(state=originState.state)
    path4, steps4 = s1.solve(1)
    if path4:                        # if find the solution
        for node4 in path4:
                # print the path from the origin to final state
                node4.showInfo()
        print(s1.answer)
        print("Total steps when using Misplaced tiles as h is %d\n" % steps4)

    originState = State(np.array([[syEmpty,2,3],[9,6,4],[5,1,7]]))
    print("From original state 2,")
    s2 = State(state=originState.state)
    path2, steps2 = s2.solve(0)
    if path2:                        # if find the solution
        for node2 in path2:
                # print the path from the origin to final state
                node2.showInfo()
        print(s2.answer)
        print("Total steps when using Manhatan Distance is %d\n" % steps2)

    s5 = State(state=originState.state)
    path5, steps5 = s5.solve(1)
    if path5:  # if find the solution
        for node5 in path5:
            # print the path from the origin to final state
            node5.showInfo()
        print(s5.answer)
        print("Total steps when using Misplaced tiles is %d\n" % steps5)

    originState = State(np.array([[7,5,1],[2,3,syEmpty],[4,6,9]]))
    print("From original state 3,")
    s3 = State(state=originState.state)
    path3, steps3 = s3.solve(0)
    if path3:  # if find the solution
        for node3 in path3:
            # print the path from the origin to final state
            node3.showInfo()
        print(s3.answer)
        print("Total steps when using Manhatan Distance is %d\n" % steps3)

    s6 = State(state=originState.state)
    path6, steps6 = s6.solve(1)
    if path6:  # if find the solution
        for node6 in path6:
            # print the path from the origin to final state
            node6.showInfo()
        print(s6.answer)
        print("Total steps when using Misplaced tiles is %d\n" % steps6)
