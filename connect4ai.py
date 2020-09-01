'''0 is no one
1 is player1
2 is player2
3 is a blocker'''

class Player:
    
    blockercount = 2
    
    def __init__(self, color):
        self.color = color
        
    def canMove(self, board, col):
        if board[0][col] == 0:
            #if board[row + 1][col] != 0: #or (blockerct[player - 1] > 0 and board[row + 2][col] != 0):
            return True
        return False
    
    def move(self, mvboard, player, col):
        for row in range(6):
            if mvboard[5 - row][col] == 0:
                mvboard[5 - row][col] = player
                break
            else:
                continue
            
class AI(Player):
    
    import copy
    from sys import maxsize
    fitness = 0
    win = maxsize
    blockercount = [2, 2]
    
    def __init__(self, color, chromosome):
        Player.__init__(self, color)
        self.chromosome = chromosome
        self.opponent = color % 2 + 1
    
    def inarow(self, board, player, n):
        blocked = 0
        opentotal = 0
        blockedtotal = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                #check board index
                skiprow = row + n > len(board)
                skipcol = col + n > len(board[row])
                compare = board[row][col]
                 
                if compare == player:
                    #check rows
                    if not skiprow:
                        blocked = 0
                        found = True
                        for value in range(n):
                            if board[row + value][col] != compare:
                                found = False
                                break
                        if found:
                            #return if n = 4
                            if n == 4:
                                return (1, 0)
                            #check if blocked
                            if row + n < len(board):
                                nextpos = board[row + n][col]
                                if nextpos == player:
                                    blocked += 10
                                elif nextpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                            if row - 1 >= 0:
                                prevpos = board[row - 1][col]
                                if prevpos == player:
                                    blocked += 10
                                elif prevpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                                
                            if blocked == 0:
                                opentotal += 1
                            elif blocked == 1:
                                blockedtotal += 1
    
                    if not skipcol:
                        #check cols
                        blocked = 0
                        found = True
                        for value in range(n):
                            if board[row][col + value] != compare:
                                found = False
                                break
                        if found:
                            #return if n = 4
                            if n == 4:
                                return (1, 0)
                            #check if blocked
                            if col + n < len(board[row]):
                                nextpos = board[row][col + n]
                                if nextpos == player:
                                    blocked += 10
                                elif nextpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                            if col - 1 >= 0:
                                prevpos = board[row][col - 1]
                                if prevpos == player:
                                    blocked += 10
                                elif prevpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                                
                            if blocked == 0:
                                opentotal += 1
                            elif blocked == 1:
                                blockedtotal += 1
                    
                    if not skiprow and not skipcol:
                        #check diagonal
                        blocked = 0
                        found = True
                        for value in range(n):
                            if board[row + value][col + value] != compare:
                                found = False
                                break
                        if found:
                            #return if n = 4
                            if n == 4:
                                return (1, 0)
                            #check if blocked
                            if col + n < len(board[row]) and row + n < len(board):
                                nextpos = board[row + n][col + n]
                                if nextpos == player:
                                    blocked += 10
                                elif nextpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                            if col - 1 >= 0 and row - 1 >= 0:
                                prevpos = board[row - 1][col - 1]
                                if prevpos == player:
                                    blocked += 10
                                elif prevpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                                
                            if blocked == 0:
                                opentotal += 1
                            elif blocked == 1:
                                blockedtotal += 1
                                 
                if not skiprow and not skipcol:
                    compare = board[row + n - 1][col]
                    if compare == player:
                        #check other weird diagonal
                        blocked = 0
                        found = True
                        for value in range(n):
                            if board[row + n - 1 - value][col + value] != compare:
                                found = False
                                break
                        if found:
                            #return if n = 4
                            if n == 4:
                                return (1, 0)
                            #check if blocked
                            if col + n < len(board[row]) and row + n < len(board):
                                nextpos = board[row + n][col + n]
                                if nextpos == player:
                                    blocked += 10
                                elif nextpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                            if col - 1 >= 0 and row - 1 >= 0:
                                prevpos = board[row - 1][col - 1]
                                if prevpos == player:
                                    blocked += 10
                                elif prevpos != 0:
                                    blocked += 1
                            else: 
                                blocked += 1
                                
                            if blocked == 0:
                                opentotal += 1
                            elif blocked == 1:
                                blockedtotal += 1
    
        return (opentotal, blockedtotal)
    
    def finish(self, board):
        connect4 = self.inarow(board, self.color, 4)[0]
        return connect4 > 0
    
    def tie(self, board):
        for i in range(len(board[0])):
            if board[0][i] == 0: 
                return False
        return True
        
    def evaluate(self, board, player, blockerct):
        score = 0
        opponent = 2
        if player == 2:
            opponent -= 1
        #evaluate player
        open2 = self.inarow(board, player, 2)[0]
        blocked2 = self.inarow(board, player, 2)[1]
        open3 = self.inarow(board, player, 3)[0]
        blocked3 = self.inarow(board, player, 3)[1]
        connect4 = self.inarow(board, player, 4)[0]
        if connect4 > 0:
            return self.win
        
        score += blocked2 * self.chromosome[0]
        score += open2 * self.chromosome[1]
        score += blocked3 * self.chromosome[2]
        score += open3 * self.chromosome[3]
        score += blockerct[player - 1] * self.chromosome[4]
        #subtract opponent
        open2 = self.inarow(board, opponent, 2)[0]
        blocked2 = self.inarow(board, opponent, 2)[1]
        open3 = self.inarow(board, opponent, 3)[0]
        blocked3 = self.inarow(board, opponent, 3)[1]
        connect4 = self.inarow(board, opponent, 4)[0]
        if connect4 > 0:
            return -self.win
        score -= blocked2 * self.chromosome[5]
        score -= open2 * self.chromosome[6]
        score -= blocked3 * self.chromosome[7]
        score -= open3 * self.chromosome[8]
        score -= blockerct[opponent - 1] * self.chromosome[9]
        return score
       
       
    def unmove(self, mvboard, col):
        for row in range(6):
            if mvboard[row][col] == 0:
                continue
            else:
                mvboard[row][col] = 0
                break
          
    def maximize(self, values):
        maxval = values[0]
        for i in range(len(values)):
            if values[i] > maxval:
                maxval = values[i]
        return maxval
    
    def minimize(self, values):
        minval = values[0]
        for i in range(len(values)):
            if values[i] < minval:
                minval = values[i]
        return minval
    
    def maxindex(self, values):
        maxindex = 0
        for i in range(len(values) - 1):
            if values[i + 1] > values[maxindex]:
                maxindex = i + 1
        return maxindex
    
    #return best col to move to
    def minimax(self, board, maximizing=True, depth=0, alpha=-maxsize, beta=maxsize, blockerct=blockercount):
        
        #check max depth or if a player has won
        mmboard = self.copy.deepcopy(board)
        blockerctcpy = self.copy.deepcopy(blockerct)
        a = alpha #copy.deepcopy(alpha)
        b = beta #copy.deepcopy(beta)
        boardvalue = self.evaluate(mmboard, self.color, blockerctcpy)
        if boardvalue == self.win:
            return boardvalue - depth
        elif boardvalue == -self.win:
            return boardvalue + depth
        elif depth == 2:   
            return boardvalue
        #maximizing decision
        if maximizing:
            values = []
            
            for col in range(7):
                if blockerctcpy[self.color - 1] > 0:
                    for blockercol in range(7):
                        #check if can move to certain column
                        if self.canMove(mmboard, blockercol):
                            self.move(mmboard, 3, blockercol)
                        else:
                            #SKIP MOVE AND FILL VALUE FOR IT TO KEEP RESULT ARRAY SAME
                            values.append(-self.win)
                            continue
                        #move after blocker
                        if self.canMove(mmboard, col):
                            self.move(mmboard, self.color, col)
                        else:
                            self.unmove(mmboard, blockercol)
                            values.append(-self.win)
                            continue
                            
                        blockerctcpy[self.color - 1] -= 1
                        value = self.minimax(mmboard, False, depth + 1, a, b, blockerctcpy)
                        blockerctcpy[self.color - 1] += 1
                        
                        if value > a:
                            a = value
                        if value > b:
                            #print('cut max', depth)
                            #self.unmove(mmboard, col)
                            #self.unmove(mmboard, blockercol)
                            return value
                        values.append(value)                        
                        
                        
                        self.unmove(mmboard, col)
                        self.unmove(mmboard, blockercol)
                else:
                    for blockercol in range(7):
                        values.append(-self.win)
                
                if self.canMove(mmboard, col):
                    self.move(mmboard, self.color, col)
                else: 
                    values.append(-self.win)
                    continue
                
                value = self.minimax(mmboard, False, depth + 1, a, b, blockerctcpy)
                if value > a:
                    a = value
                if value > b:
                    #print('cut max', depth)
                    #self.unmove(mmboard, col)
                    return value
                values.append(value)
                
                self.unmove(mmboard, col)
            
            if depth == 0:
                return self.maxindex(values)
            return self.maximize(values)
        #minimizing decision
        else:
            values = []
            for col in range(7):
                if blockerctcpy[self.opponent - 1] > 0:
                    for blockercol in range(7):
                        if self.canMove(mmboard, blockercol):
                            self.move(mmboard, 3, blockercol)
                        else:
                            values.append(self.win)
                            continue
                        
                        if self.canMove(mmboard, col):
                            self.move(mmboard, self.opponent, col)
                        else:
                            self.unmove(mmboard, blockercol)
                            values.append(self.win)
                            continue
                            
                        blockerctcpy[self.opponent - 1] -= 1
                        value = self.minimax(mmboard, True, depth + 1, a, b, blockerctcpy)
                        blockerctcpy[self.opponent - 1] += 1
                        
                        if value < b:
                            b = value
                        if value < a:
                            #print('cut min', depth)
                            #self.unmove(mmboard, col)
                            #self.unmove(mmboard, blockercol) 
                            return value
                        values.append(value)
                        
                        
                        self.unmove(mmboard, col)
                        self.unmove(mmboard, blockercol) 
                else:
                    for blockercol in range(7):
                        values.append(self.win)        
                
                if self.canMove(mmboard, col):
                    self.move(mmboard, self.opponent, col)
                else: 
                    values.append(self.win)
                    continue
                
                value = self.minimax(mmboard, True, depth + 1, a, b, blockerctcpy)
                if value < b:
                    b = value
                if value < a:
                    #print('cut min', depth)
                    #self.unmove(mmboard, col)
                    return value
                values.append(value)
                
                self.unmove(mmboard, col)   
            return self.minimize(values)
    
    def optimalMove(self, board):
        bestmove = self.minimax(board)
        blocker = -1
        if (bestmove + 1) % 8 == 0:
            bestmove += 1
            bestmove //= 8
            bestmove -= 1
            
            self.move(board, self.color, bestmove)
            return 0
        
        else:
            blocker += 1
            blocker += (bestmove + 1) % 8 - 1
            bestmove //= 8
            
            self.move(board, 3, blocker)
            self.blockercount[self.color - 1] -= 1
            self.move(board, self.color, bestmove)
            return 1
        