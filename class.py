#Unionfindtree
class Unionfindtree:
    def __init__(self, number):
        self.par = [i for i in range(number)]
        self.rank = [0] * (number)

    def find(self, x):  # 親を探す
        if self.par[x] == x:
            return x
        else:
            self.par[x] = self.find(self.par[x])
            return self.par[x]

    def union(self, x, y):  # x,yを繋げる
        px = self.find(x)
        py = self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            self.par[px] = py
        else:
            self.par[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

    def connect(self, x, y):  # 親が同じかみる
        return self.find(x) == self.find(y)

#重み付きUnionfindtree
#(参考 https://qiita.com/drken/items/cce6fc5c579051e64fab)

class WeightUnionfindtree:
    def __init__(self, number):
        self.par = [i for i in range(number)]
        self.rank = [0] * (number)
        self.weight = [0] * (number)

    def find(self, x):  # 親を探す xの親を示す
        if self.par[x] == x:
            return x
        else:
            r = self.find(self.par[x])
            self.weight[x] += self.weight[self.par[x]]
            self.par[x] = r
            return self.par[x]

    def weighted(self, x):  # 重みの更新をして真の重みを出す
        self.find(x)
        return self.weight[x]

    def union(self, x, y, w):  # weight(y) = weight(x) + w となるように x と y をマージする
        w += self.weighted(x)
        w -= self.weighted(y)
        px = self.find(x)
        py = self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            self.par[px] = py
            self.weight[px] = -w
        else:
            self.par[py] = px
            self.weight[py] = w
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

    def connect(self, x, y):  # 親が同じかみる
        return self.find(x) == self.find(y)

    def diff(self, x, y):  # yとxの重みの差を見る、重みの更新も自動でしてくれる
        return self.weighted(y) - self.weighted(x)

#素因数分解を行うクラス、素数かどうかも判定
from collections import defaultdict
class Prime:
    def __init__(self, number):  # N以下の素数
        self.jud = [True] * (number + 5)
        self.pri = []
        self.jud[0] = False
        self.jud[1] = False
        for i in range(number):
            if self.jud[i]:
                self.pri.append(i)
                for j in range(2, (number) // i + 1):
                    self.jud[i * j] = False

    def judge(self, x):
        return self.jud[x]

    def decom(self, x):
        s = x
        a = defaultdict(int)
        if s == 1:
            return a
        while s > 1:
            for p in self.pri:
                if s % p == 0:
                    a[p] += 1
                    s = s // p
                    break
        return a

#Dijkstra法、ダイクストラ法
from heapq import heappush, heappop


class Dijk:
    def __init__(self, n):
        self.table = [[] for i in range(n)]
        self.n = n

    def add(self, x, y, f):
        self.table[x].append((y, f))

    def di(self, s):
        inf = 10 ** 20
        self.val = [inf] * self.n
        self.val[s] = 0
        h = []
        heappush(h, (0, s))
        while h:
            q, i = heappop(h)
            if self.val[i] < q:
                continue
            for x, c in self.table[i]:
                if self.val[x] > self.val[i] + c:
                    self.val[x] = self.val[i] + c
                    heappush(h, (self.val[x], x))

    def dist(self, s, t):
        return self.val[t]

#Segment tree min
#再帰使ってるから遅い
class Segmenttree_min():
    def __init__(self, number):
        n = 1
        inf = (1 << 31) - 1
        while n < number:
            n *= 2
        self.n = n
        self.list = [inf] * (2 * n - 1)

    def add(self, i, x):  # 0indexed ith add x
        i += self.n - 1
        self.list[i] = x
        while i > 0:
            i = (i - 1) // 2
            self.list[i] = min(self.list[2 * i + 1], self.list[2 * i + 2])

    def search(self, a, b, k, l, r):  # call as search(a,b,0,0,self.n) minimun in [a,b)
        if r <= a or b <= l:
            return (1 << 31) - 1
        elif a <= l and r <= b:
            return self.list[k]
        else:
            vl = self.search(a, b, 2 * k + 1, l, (l + r) // 2)
            vr = self.search(a, b, 2 * k + 2, (l + r) // 2, r)
            return min(vl, vr)

#Segment tree max
#再帰使ってるから遅い
class Segmenttree_max():
    def __init__(self, number):
        n = 1
        while n < number:
            n *= 2
        self.n = n
        self.list = [0] * (2 * n - 1)

    def add(self, i, x):  # 0indexed ith add x
        i += self.n - 1
        self.list[i] = x
        while i > 0:
            i = (i - 1) // 2
            self.list[i] = max(self.list[2 * i + 1], self.list[2 * i + 2])

    def search(self, a, b, k, l, r):  # call as search(a,b,0,0,self.n) maximum in [a,b)
        if r <= a or b <= l:
            return 0
        elif a <= l and r <= b:
            return self.list[k]
        else:
            vl = self.search(a, b, 2 * k + 1, l, (l + r) // 2)
            vr = self.search(a, b, 2 * k + 2, (l + r) // 2, r)
            return max(vl, vr)

#Segment tree sum
#再帰使ってるから遅い
class Segmenttree_sum():
    def __init__(self, number):
        n = 1
        while n < number:
            n *= 2
        self.n = n
        self.list = [0] * (2 * n - 1)

    def add(self, i, x):  # 0indexed ith add x
        i += self.n - 1
        self.list[i] = +x
        while i > 0:
            i = (i - 1) // 2
            self.list[i] = self.list[2 * i + 1] + self.list[2 * i + 2]

    def search(self, a, b, k, l, r):  # call as search(a,b,0,0,self.n) sum in [a,b)
        if r <= a or b <= l:
            return 0
        elif a <= l and r <= b:
            return self.list[k]
        else:
            vl = self.search(a, b, 2 * k + 1, l, (l + r) // 2)
            vr = self.search(a, b, 2 * k + 2, (l + r) // 2, r)
            return vl + vr

#binary index tree
class BIT():
    def __init__(self, number):
        self.n = number
        self.list = [0] * (number + 1)

    def add(self, i, x):  # ith added x  1indexed
        while i <= self.n:
            self.list[i] += x
            i += i & -i

    def search(self, i):  # 1-i sum
        s = 0
        while i > 0:
            s += self.list[i]
            i -= i & -i
        return s

    def suma(self, i, j):  # i,i+1,..j sum
        return self.search(j) - self.search(i - 1)

#フォードファルカーソン法、フロー１
#Ford-Fulkerson
import sys
sys.setrecursionlimit(10 ** 8)
class FK:
    def __init__(self, n):
        self.table = [[0] * n for i in range(n)]
        self.n = n

    def add(self, x, y, f):
        self.table[x][y] = f

    def ford(self, s, t, f):
        self.visit[s] = True
        if s == t:
            return f
        for i in range(self.n):
            if (not self.visit[i]) and self.table[s][i] > 0:
                df = self.ford(i, t, min(f, self.table[s][i]))
                if df > 0:
                    self.table[s][i] -= df
                    self.table[i][s] += df
                    return df
        return 0

    def flow(self, s, t):
        ans = 0
        inf = 10 ** 20
        while True:
            self.visit = [False] * (self.n)
            df = self.ford(s, t, inf)
            if df == 0:
                break
            ans += df
        return ans

#Dinic法、フロー2
from collections import deque
import sys
sys.setrecursionlimit(10 ** 8)
class Dinic:
    def __init__(self, number):
        self.table = [[0] * (number) for i in range(number)]
        self.n = number

    def add(self, x, y, f):
        self.table[x][y] = f

    def bfs(self, x):
        self.visit[x] = 0
        h = deque()
        h.append(x)
        while h:
            y = h.popleft()
            for i in range(self.n):
                if self.visit[i] == -1 and self.table[y][i] > 0:
                    self.visit[i] = self.visit[y] + 1
                    h.append(i)
        return 0

    def dinic(self, s, t, f):
        if s == t:
            return f
        for i in range(self.n):
            if self.visit[i] > self.visit[s] and self.table[s][i] > 0:
                df = self.dinic(i, t, min(f, self.table[s][i]))
                if df > 0:
                    self.table[s][i] -= df
                    self.table[i][s] += df
                    return df
        return 0

    def flow(self, s, t):
        ans = 0
        inf = 10 ** 20
        while True:
            self.visit = [-1] * (self.n)
            self.bfs(s)
            if self.visit[t] == -1:
                break
            while True:
                df = self.dinic(s, t, inf)
                if df == 0:
                    break
                ans += df
        return ans
