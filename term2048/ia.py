from term2048.board import Board
import random
import copy

class IA(object):
    def __str__(self, margins={}):
        return ""
        

    @staticmethod
    def randomNextMove(board):
        '''
        It's just a test for the validMove function
        '''
        if board.validMove(Board.UP):
            print "UP: ok"
        else:
            print "UP: no"
        if board.validMove(Board.DOWN):
            print "DOWN: ok"
        else:
            print "DOWN: no"
        if board.validMove(Board.LEFT):
            print "LEFT: ok"
        else:
            print "LEFT: no"
        if board.validMove(Board.RIGHT):
            print "RIGHT: ok"
        else:
            print "RIGHT: no"
        rm = random.randrange(1, 5)
        print rm 
        return rm
    
    @staticmethod
    def nextMove(board,recursion_depth=3):
        m,s = IA.nextMoveRecur(board,recursion_depth,recursion_depth)
        return m
        
    @staticmethod
    def nextMoveRecur(board,depth,maxDepth):
        bestScore = -1.
        bestMove = 0
        for m in range(1,5):
            if(board.validMove(m)):
                newBoard = copy.deepcopy(board)
                newBoard.move(m,add_tile=False)
                
                score = IA.evaluate(newBoard)
                if depth != 0:
                    my_m,my_s = IA.nextMoveRecur(newBoard,depth-1,maxDepth)
                    score += my_s/(maxDepth-depth+1)
                    
                if(score > bestScore):
                    bestMove = m
                    bestScore = score
                #print "Move " + str(m) +" - Score " + str(score)
                
        #print "BestMove " + str(bestMove) +" - BestScore " + str(bestScore)
        return (bestMove,bestScore);

    @staticmethod
    def evaluate(board,commonRatio=0.25):
        linearWeightedVal = 0
        invert = False
        weight = 4000000.
        minVal = board.getCell(0,0)
        malus = 0
        for y in range(0,board.size()):
            for x in range(0,board.size()):
                b_x = x
                if invert:
                    b_x = board.size() - 1 - x
                #linearW
                currVal=board.getCell(b_x,y)
                linearWeightedVal += currVal*weight
                weight *= commonRatio
                #low value malus
                if(currVal < minVal):
                    minVal = currVal
                else:
                    malus += currVal - minVal
                    
            invert = not invert
        
        return max(linearWeightedVal-malus,0)
        

    '''
    @staticmethod
    def evaluate(board):
        maxNegVal = -10000.
        val = 0
        for y in range(0,board.size()):
            line = board.getLine(y);
            for x in range(0,board.size()-1):
                if(line[x]<line[x+1]):
                    val += line[x]-line[x+1]
        for x in range(0,board.size()):
            col = board.getCol(x);
            for y in range(0,board.size()-1):
                if(col[y]<col[y+1]):
                    val += col[y]-col[y+1]
        #return 1.-val/maxNegVal  
        #return val
        monotonicScore = 1.-val/maxNegVal
        emptyCellsScore = 1.*len(board.getEmptyCells())/(board.size()*board.size());
        
        total = 0
        invert = False
        weight = 1.
        for y in range(0,board.size()):
            for x in range(0,board.size()):
                b_x = x
                if invert:
                    b_x = board.size() - 1 - x
                total += board.getCell(b_x,y)*weight
                weight /= 4
            invert = not invert
        
        return total
        #return total*monotonicScore*emptyCellsScore
        #return total*emptyCellsScore
    '''
    '''
    @staticmethod
    def evaluate(board):  
        maxNegVal = -10000.
        val = 0
        for y in range(0,board.size()):
            line = board.getLine(y);
            for x in range(0,board.size()-1):
                if(line[x]<line[x+1]):
                    val += line[x]-line[x+1]
        for x in range(0,board.size()):
            col = board.getCol(x);
            for y in range(0,board.size()-1):
                if(col[y]<col[y+1]):
                    val += col[y]-col[y+1]
        #return 1.-val/maxNegVal
        #return val
        testScore = 1.-val/maxNegVal
        
        total = 0
        for y in range(0,board.size()):
            for x in range(0,board.size()):
                total += board.getCell(x,y)*board.getCell(x,y)*board.getCell(x,y)
        
        cornerScore = 1.*board.getCell(0,0) + 0.5*board.getCell(0,1) +0.25*board.getCell(0,2) + 0.125*board.getCell(0,3)
        emptyCellsScore = 1.*len(board.getEmptyCells())/(board.size()*board.size());
        #return total*emptyCellsScore*cornerScore*testScore
        #return total
        #return total*cornerScore
        return cornerScore
    '''

