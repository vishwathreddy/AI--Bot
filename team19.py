import random
#import signal
import time
from copy import deepcopy


class Team19:

    def __init__(self):
        self.patterns = []
        self.boardheuristics = {}
        self.blockheuristics = {}
        self.count = 0
        self.randTable = [[[[long(0) for k in range(2)] for j in range(9)]
                           for i in range(9)] for ply in range(2)]
        self.randBlock = [[[long(0) for j in range(3)] for i in range(3)] for k in range(2)]
        self.mov = 'o'
        self.limit = 3
        self.hashtable = long(0)
        self.smallboard_win_points = 300
        self.position_weight = ((3,2,3),(2,4,2),(3,2,3))
        for j in range(3):
            temp_row = []
            temp_col = []
            for i in range(3):
                temp_row.append((j, i))
                temp_col.append((i, j))
            self.patterns.append(tuple(temp_row))
            self.patterns.append(tuple(temp_col))
        self.start = 0
        self.patterns.append(((0, 0), (1, 1), (2, 2)))
        self.patterns.append(((2, 0), (1, 1), (0, 2)))
        self.patterns = tuple(self.patterns)
        self.inithash()
        # s1 = board.small_boards_status
                    # playerCountold = 0
                    # playerCountnew = 0
                    # for k in range(2):
                    #     for i in range(3):
                    #         for j in range(3):
                    #             if s[k][i][j] == self.
    def inithash(self):
        for k in range(2):
            for j in range(9):
                for i in range(9):
                    for ply in range(2):
                        self.randTable[k][j][i][ply] = random.randint(0, 2**64)

    def Block_heuristic(self, block, flag):
        block_heu =0
        for pattern in self.patterns:
            temp = 0
            for p in pattern:
                if block[p[0]][p[1]] == flag:
                    temp+=1
                elif block[p[0]][p[1]] == self.opp(flag):
                    temp-=10
            if temp == 1:
                block_heu += 5
            elif temp == 2:
                block_heu +=30
            elif temp < 0:
                block_heu +=0

        for j in range(3):
            for i in range(3):
                block_heu += 0.2 * self.position_weight[i][j]
        return block_heu

    def opp(self,flag):
        if flag=='x': 
            return 'o'
        else:
            return 'x'

    def board_pattern_checker(self, k, pos, block):
        
        playercount = 0
        patterntemp = 0
        for p in pos:
            val = block[k][p[0]][p[1]]
            patterntemp += val
            if val < 0:
                return 0
            elif val == self.smallboard_win_points:
                playercount += 1
        multiplier = 1  
        if playercount == 1:
            multiplier = 2
        elif playercount == 2:
            multiplier = 5
        elif playercount == 3:
            multiplier = 500
        return multiplier * patterntemp

    def Board_heuristic(self, blockHeurs):
        temp = 0           
        for k in range(2):
            for j in range(3):
                for i in range(3):
                    if blockHeurs[k][j][i] > 0:
                        temp += 0.05*self.position_weight[j][i]*blockHeurs[k][j][i]

        return temp
 

    def add_move(self, cell, ply):
        k = cell[0]
        x = cell[1]
        y = cell[2]
        self.hashtable ^= self.randTable[k][x][y][ply]
        self.randBlock[k][x/3][y/3] ^= self.randTable[k][x][y][ply]

    def heuristic(self, flag, board):
        if (self.hashtable, flag) in self.boardheuristics:
            return self.boardheuristics[(self.hashtable, flag)]

        BlockValue = [[[long(0) for i in range(3)] for j in range(3)] for k in range(2) ]
        total = 0
        b = board.big_boards_status
        s = board.small_boards_status
        for k in range(2):
            for i in range(3):
                for j in range(3):
                    if s[k][i][j] == flag:
                        BlockValue[k][i][j] = self.smallboard_win_points
                    elif s[k][i][j] != flag and s[k][i][j] != '-':
                        BlockValue[k][i][j] = -1
                    else:
                        if (self.randBlock[k][i][j], flag) in self.blockheuristics:
                            BlockValue[k][i][j] = self.blockheuristics[(
                                self.randBlock[k][i][j], flag)]
                        else:
                            Block = tuple([tuple(b[k][3*i + x][3*j:3*(j+1)]) for x in xrange(3)])
                            # print Block
                            self.blockheuristics[(self.randBlock[k][i][j], flag)] = self.Block_heuristic(Block, flag)
                            BlockValue[k][i][j] = self.blockheuristics[(self.randBlock[k][i][j], flag)]

        
        # print BlockValue

        for k in range(2):
            for pos in self.patterns:
                total += self.board_pattern_checker(k,pos,BlockValue)
        total += self.Board_heuristic(BlockValue)
        self.boardheuristics[(self.hashtable, flag)]  = total
        # print total,"total"
        return total

    def algorithm(self, board, old_move, flag, depth, inc, alpha, beta, repeat):
        # print inc
        GoalState = board.find_terminal_state()
        if GoalState[1] == 'WON':
            if GoalState[0] == self.mov:
                return 100000, "placeholder"
            else:
                return -100000, "placeholder"
        elif GoalState[1] == 'DRAW':
            return -10000, "placeholder"
        if inc == depth or time.time() - self.start > 23:
            # return random.randrange(1000), "placeholder"
            return (self.heuristic(self.mov,board) - self.heuristic(self.opp(self.mov),board)), "placeholder"
            # return (self.heuristic(flag,board) - self.heuristic(self.opp(flag),board)), "placeholder"

        cells = board.find_valid_move_cells(old_move)

        if flag == self.mov:
            cell1 = cells[0]
            maxVal = float("-inf")
            for cell in cells:
                playercountold = 0
                playercountnew = 0
                s = board.small_boards_status
                board.update(old_move, cell, flag)
                s1 = board.small_boards_status
                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            if s[k][i][j] == flag:
                                playercountold += 1
                            if s1[k][i][j] == flag:
                                playercountnew += 1

                self.add_move(cell, 1)
                if playercountnew > playercountold and repeat == 0:
                    repeat = 1
                    val = self.algorithm(board, cell, flag, depth, inc + 1, alpha, beta, repeat)[0]
                else:
                    repeat = 0
                    val = self.algorithm(board, cell, self.opp(flag), depth, inc + 1, alpha, beta, repeat)[0]
                if val > maxVal:
                    maxVal = val
                    cell1 = cell
                if maxVal > alpha:
                    alpha = maxVal
                board.big_boards_status = list(board.big_boards_status)
                board.big_boards_status[cell[0]][cell[1]][cell[2]] = '-'
                board.big_boards_status = tuple(board.big_boards_status)
                board.small_boards_status = list(board.small_boards_status)
                board.small_boards_status[cell[0]][cell[1]/3][cell[2]/3] = '-'
                board.small_boards_status = tuple(board.small_boards_status)
                self.add_move(cell, 0)
                if beta <= alpha:
                    break
            return maxVal, cell1
            # else:
            #     cell1 = cells[0]
            #     maxVal = float("-inf")
            #     for cell in cells:
            #         board.update(old_move, cell, flag)
            #         self.add_move(cell, 0)

            #         val = self.algorithm(
            #             board, cell, 'x', depth, inc + 1, alpha, beta)[0]

            #         if val > maxVal:
            #             maxVal = val
            #             cell1 = cell
            #         if maxVal > alpha:
            #             alpha = maxVal
            #         board.big_boards_status = list(board.big_boards_status)
            #         board.big_boards_status[cell[0]][cell[1]][cell[2]] = '-'
            #         board.big_boards_status = tuple(board.big_boards_status)
            #         board.small_boards_status = list(board.small_boards_status)
            #         board.small_boards_status[cell[0]
            #                                   ][cell[1]/3][cell[2]/3] = '-'
            #         board.small_boards_status = tuple(
            #             board.small_boards_status)
            #         self.add_move(cell, 0)

            #         if beta <= alpha:
            #             break
            #     return maxVal, cell1

        else:
            minVal = float("inf")
            cell1 = cells[0]
            for cell in cells:
                playercountold = 0
                playercountnew = 0
                s = board.small_boards_status
                board.update(old_move, cell, flag)
                s1 = board.small_boards_status
                for k in range(2):
                    for i in range(3):
                        for j in range(3):
                            if s[k][i][j] == flag:
                                playercountold += 1
                            if s1[k][i][j] == flag:
                                playercountnew += 1

                self.add_move(cell, 1)
                if playercountnew > playercountold and repeat == 0:
                    repeat = 1
                    val = self.algorithm(board, cell, flag, depth, inc + 1, alpha, beta, repeat)[0]
                else:
                    repeat = 0
                    val = self.algorithm(board, cell, self.opp(flag), depth, inc + 1, alpha, beta, repeat)[0]

                if val < minVal:
                    minVal = val
                    cell1 = cell
                if minVal < beta:
                    beta = minVal
                board.big_boards_status = list(board.big_boards_status)
                board.big_boards_status[cell[0]][cell[1]][cell[2]] = '-'
                board.big_boards_status = tuple(board.big_boards_status)
                board.small_boards_status = list(board.small_boards_status)
                board.small_boards_status[cell[0]][cell[1]/3][cell[2]/3] = '-'
                board.small_boards_status = tuple(board.small_boards_status)
                self.add_move(cell, 1)
                if beta <= alpha:
                    break
            return minVal, "placeholder"

    #def sig_handler(self, signum, frame):
        #raise Exception("timeout")

    def move(self, board, old_move, flag):
        #signal.signal(signal.SIGALRM, self.sig_handler)
        #signal.alarm(5)
        self.count += 1
        self.start = time.time()
        self.mov = flag
        limit = 5

        if self.count > 30:
            limit = 7
        if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == self.opp(flag):
            self.add_move(old_move, 1)
        validcells = board.find_valid_move_cells(old_move)
        # try:
            # while limit<5:
                # self.boardHashSafeCopy = self.randTable
                # self.blockHashSafeCopy = deepcopy(self.randBlock)
                # b = deepcopy(board)
        best_move = self.algorithm(board, old_move, flag, limit, 1, -100000, 1000000,0)
                # limit += 1
                # best_move = val
                # del b
        # except Exception as e:
            # self.randTable = self.boardHashSafeCopy
            # self.randBlock = self.blockHashSafeCopy
            # pass
        #signal.alarm(0)
        #print best_move
        return best_move[1]
