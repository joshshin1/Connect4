'''0 is no one
1 is player1
2 is player2
3 is a blocker'''
import sys
sys.path.append('.')

from connect4ai import AI

def printboard(board):
    for i in range(len(board)):
        row = ''
        for j in range(len(board[i])):
            row = row + '    ' + str(board[i][j])
        print(row)
        print()
    print()

ai1 = AI(1, (50, 100, 500, 1000, 2000, 50, 100, 500, 1000, 2000))
ai2 = AI(2, (50, 100, 500, 1000, 2000, 50, 100, 500, 1000, 2000))

board = [[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0]]

printboard(board)

#AI PLAY AGAINST EACH OTHER
while True:
    print('BLOCKER COUNT: AI -', ai1.blockercount[0], ' AI2 -', ai2.blockercount[1])
    if not ai2.finish(board) and not ai1.tie(board):    
        blockai1 = ai1.optimalMove(board)
    else:
        print('ai2 wins')
        break
    
    if not ai1.finish(board) and not ai1.tie(board):
        blockai2 = ai2.optimalMove(board)
    else:
        print('ai1 wins')
        break
    
    printboard(board)

