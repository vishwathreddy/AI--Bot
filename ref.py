import copy


def find(i, j, prev_state):
    temp = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    count = 0
    values = []
    for a in temp:
        if val(i+a[0], j+a[1]):
            values.append(prev_state[i+a[0]][j+a[1]])
        else:
            values.append(prev_state[i][j])
    max_val = -100000
    for k in range(0, 4):
        v1 = values[k % 4]
        v2 = values[(k+1) % 4]
        v3 = values[(k+2) % 4]
        va = v1*0.1+v2*0.8+v3*0.1
        max_val = max(va, max_val)
    return max_val


def val(i, j):
    if i < 0 or j < 0 or i > n-1 or j > m-1:
        return False
    if [i, j] in matW:
        return False
    return True

n, m = map(int, raw_input().split())
world = []
for i in range(0, n):
    vec = []
    vec = map(float, raw_input().split())
    world.append(vec)

e, w = map(int, raw_input().split())
matE = []
for i in range(e):
    vec = []
    vec = map(float, raw_input().split())
    matE.append(vec)

matW = []
for i in range(w):
    vec = []
    vec = map(float, raw_input().split())
    matW.append(vec)

start_x, start_y = map(float, raw_input().split())
#rew = raw_input()
reward = float(raw_input())

prev_state = copy.deepcopy(world)
present_state = copy.deepcopy(prev_state)
gamma = 0.99
th = 1e-20
error = 0.01
count = 0
while True:
    count += 1
    mi = 0
    for i in range(0, n):
        for j in range(0, m):
            if [i, j] in matW:
                continue
            elif [i, j] in matE:
                present_state[i][j] = prev_state[i][j]
            else:
                present_state[i][j] = reward + gamma * find(i, j, prev_state)
            de=0
            if prev_state[i][j] !=present_state[i][j]:
                de = (abs(present_state[i][j]-prev_state[i][j])+th)/(prev_state[i][j]+th)
            mi = max(de, mi)
    prev_state = copy.deepcopy(present_state)
    print present_state
    print mi 
    print "count",count
    if error * (1-gamma)/gamma > mi:
        break
   