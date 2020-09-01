'''0 is no one
1 is player1
2 is player2
3 is a blocker'''

import copy

win = 1000000
blockerct = [2, 2]

unmoves = 0
moves = 0

def printboard(board):
    for i in range(len(board)):
        row = ''
        for j in range(len(board[i])):
            row = row + '    ' + str(board[i][j])
        print(row)
        print()

def inarow(board, player, n):
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

                   
def finish(board):
    p1connect4 = inarow(board, 1, 4)
    p2connect4 = inarow(board, 2, 4)
    
    return p1connect4[0] + p2connect4[0] > 0


def canMove(board, col):
    if board[0][col] == 0:
        #if board[row + 1][col] != 0: #or (blockerct[player - 1] > 0 and board[row + 2][col] != 0):
        return True
    return False
    
 
def evaluate(board, player, blockerct):
    score = 0
    opponent = 2
    if player == 2:
        opponent -= 1
    #evaluate player
    open2 = inarow(board, player, 2)[0]
    blocked2 = inarow(board, player, 2)[1]
    open3 = inarow(board, player, 3)[0]
    blocked3 = inarow(board, player, 3)[1]
    connect4 = inarow(board, player, 4)[0]
    if connect4 > 0:
        return win
    
    score += open2 * 100
    score += blocked2 * 50
    score += open3 * 1000
    score += blocked3 * 500
    score += blockerct[player - 1] * 2000
    #subtract opponent
    open2 = inarow(board, opponent, 2)[0]
    blocked2 = inarow(board, opponent, 2)[1]
    open3 = inarow(board, opponent, 3)[0]
    blocked3 = inarow(board, opponent, 3)[1]
    connect4 = inarow(board, opponent, 4)[0]
    if connect4 > 0:
        return -win
    
    score -= open2 * 100
    score -= blocked2 * 50
    score -= open3 * 1000
    score -= blocked3 * 500
    score -= blockerct[opponent - 1] * 2000
    return score


def move(mvboard, player, col):
    for row in range(6):
        if mvboard[5 - row][col] == 0:
            mvboard[5 - row][col] = player
            global moves
            moves += 1
            break
        else:
            continue


def unmove(mvboard, col):
    for row in range(6):
        if mvboard[row][col] == 0:
            continue
        else:
            mvboard[row][col] = 0
            global unmoves
            unmoves += 1
            break

   
def maximize(values):
    maxval = values[0]
    for i in range(len(values)):
        if values[i] > maxval:
            maxval = values[i]
    return maxval


def minimize(values):
    minval = values[0]
    for i in range(len(values)):
        if values[i] < minval:
            minval = values[i]
    return minval


def maxindex(values):
    maxindex = 0
    for i in range(len(values) - 1):
        if values[i + 1] > values[maxindex]:
            maxindex = i + 1
    return maxindex

   
#return best col to move to
def minimax(board, player, opponent, maximizing=True, depth=0, alpha=-win, beta=win, blockerct=blockerct):
    #check max depth or if a player has won
    mmboard = copy.deepcopy(board)
    blockerctcpy = copy.deepcopy(blockerct)
    a = alpha #copy.deepcopy(alpha)
    b = beta #copy.deepcopy(beta)
    boardvalue = evaluate(mmboard, player, blockerctcpy)
    if boardvalue == win:
        return boardvalue - depth
    elif boardvalue == -win:
        return boardvalue + depth
    elif depth == 3:
        
        return boardvalue
    #maximizing decision
    if maximizing:
        values = []
        
        for col in range(7):
            if blockerctcpy[player - 1] > 0:
                for blockercol in range(7):
                    #check if can move to certain column
                    if canMove(mmboard, blockercol):
                        move(mmboard, 3, blockercol)
                    else:
                        #SKIP MOVE AND FILL VALUE FOR IT TO KEEP RESULT ARRAY SAME
                        values.append(-win)
                        continue
                    #move after blocker
                    if canMove(mmboard, col):
                        move(mmboard, player, col)
                    else:
                        unmove(mmboard, blockercol)
                        values.append(-win)
                        continue
                        
                    blockerctcpy[player - 1] -= 1
                    value = minimax(mmboard, player, opponent, False, depth + 1, a, b, blockerctcpy)
                    blockerctcpy[player - 1] += 1
                    
                    if value > a:
                        a = value
                    if value > b:
                        #print('cut max', depth)
                        unmove(mmboard, col)
                        unmove(mmboard, blockercol)
                        return value
                    values.append(value)                        
                    
                    
                    unmove(mmboard, col)
                    unmove(mmboard, blockercol)
            else:
                for blockercol in range(7):
                    values.append(-win)
            
            if canMove(mmboard, col):
                move(mmboard, player, col)
            else: 
                values.append(-win)
                continue
            
            value = minimax(mmboard, player, opponent, False, depth + 1, a, b, blockerctcpy)
            if value > a:
                a = value
            if value > b:
                #print('cut max', depth)
                unmove(mmboard, col)
                return value
            values.append(value)
            
            unmove(mmboard, col)
        
        if depth == 0:
            return maxindex(values)
        return maximize(values)
    #minimizing decision
    else:
        values = []
        for col in range(7):
            if blockerctcpy[opponent - 1] > 0:
                for blockercol in range(7):
                    if canMove(mmboard, blockercol):
                        move(mmboard, 3, blockercol)
                    else:
                        values.append(win)
                        continue
                    
                    if canMove(mmboard, col):
                        move(mmboard, opponent, col)
                    else:
                        unmove(mmboard, blockercol)
                        values.append(win)
                        continue
                        
                    blockerctcpy[opponent - 1] -= 1
                    value = minimax(mmboard, player, opponent, True, depth + 1, a, b, blockerctcpy)
                    blockerctcpy[opponent - 1] += 1
                    
                    if value < b:
                        b = value
                    if value < a:
                        #print('cut min', depth)
                        unmove(mmboard, col)
                        unmove(mmboard, blockercol) 
                        return value
                    values.append(value)
                    
                    
                    unmove(mmboard, col)
                    unmove(mmboard, blockercol) 
            else:
                for blockercol in range(7):
                    values.append(win)        
            
            if canMove(mmboard, col):
                move(mmboard, opponent, col)
            else: 
                values.append(win)
                continue
            
            value = minimax(mmboard, player, opponent, True, depth + 1, a, b, blockerctcpy)
            if value < b:
                b = value
            if value < a:
                #print('cut min', depth)
                unmove(mmboard, col)
                return value
            values.append(value)
            
            unmove(mmboard, col)
            
        return minimize(values)
    
#if minimax % 8 == 0 minimax / 8 = col to move player and no blocker
#if minimax % 8 != 0 minimax % 8 - 1 = col to move blocker minimax / 8 = col to move player
board = [[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0]]
printboard(board)
print()

#print(evaluate(board, 1, blockerct))
'''
for i in range(40):
    player = i % 2 + 1
    opponent = 2
    if player == 2:
        opponent = 1
    bestmove = minimax(board, player, opponent)
    blocker = -1
    print('TURN ', i + 1)
    if (bestmove + 1) % 8 == 0:
        bestmove += 1
        bestmove //= 8
        bestmove -= 1
    else:
        blocker += 1
        blocker += (bestmove + 1) % 8 - 1
        bestmove //= 8
        
    if blocker != -1:
        move(board, 3, blocker)
        blockerct[player - 1] -= 1;
        move(board, player, bestmove)
        printboard(board)
    else:
        move(board, player, bestmove)
        printboard(board)
        
    if finish(board):
        print(player, ' wins')
        break
'''
while not finish(board):
    player = 1
    ai = 2
    
    print('BLOCKER COUNT: AI -', blockerct[ai - 1], ' PLAYER -', blockerct[player - 1])
    
    #PLAYERS TURN
    playerblock = input('Where would you like to BLOCK? ')
    playermove = input('Where would you like to MOVE? ')
    playerblock = int(playerblock)
    playermove = int(playermove)
    
    if playerblock > -1 and blockerct[player - 1] > 0:
        move(board, 3, playerblock)
        blockerct[player - 1] -= 1
    move(board, player, playermove)
    
    print('PLAYER MOVE')
    printboard(board)
    print()
    
    #AI TURN
    bestmove = minimax(board, ai, player)
    blocker = -1
    if (bestmove + 1) % 8 == 0:
        bestmove += 1
        bestmove //= 8
        bestmove -= 1
        
        move(board, ai, bestmove)
        
        print('AI MOVE')
        printboard(board)
        print()
        
    else:
        blocker += 1
        blocker += (bestmove + 1) % 8 - 1
        bestmove //= 8
        
        move(board, 3, blocker)
        blockerct[ai - 1] -= 1;
        move(board, ai, bestmove)
        
        print('AI MOVE')
        printboard(board)
        print()
        
if inarow(board, player, 4)[0] == 1:
    print('PLAYER WINS!!!')
print('AI WINS!!!')
    
    