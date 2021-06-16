# permutation class
# originally written by P. Bonsma in 2015

testvalidity = True

safeInit = True

UseReadableOutput = True



class permutation():
    def __init__(self, n, cycles=None, mapping=None):
        self.n = n
        if mapping != None:
            if testvalidity:
                assert len(mapping) == n
                # if len(mapping)!=n:
                #	raise permError
                test = [0] * n
                for val in mapping:
                    test[val] += 1
                    assert test[val] <= 1
            # if test[val]>1:
            #	raise permError
            if safeInit:
                self.P = mapping[:]  # safe
            else:
                self.P = mapping  # fast
        elif cycles != None:
            self.P = [i for i in range(n)]
            for cycle in cycles:
                for i in range(len(cycle)):
                    assert self.P[cycle[i]] == cycle[i]
                    # if self.P[cycle[i]]!=cycle[i]:
                    #	raise permError
                    self.P[cycle[i]] = cycle[(i + 1) % len(cycle)]
        else:
            self.P = [i for i in range(n)]

    def cycles(self):
        C = []
        incyc = [0] * self.n
        for i in range(self.n):
            if not incyc[i]:
                if self.P[i] != i:
                    newcycle = [i]
                    C.append(newcycle)
                    incyc[i] = 1
                    next = self.P[i]
                    while next != i:
                        newcycle.append(next)
                        incyc[next] = 1
                        next = self.P[next]
        return C

    def __repr__(self):
        if UseReadableOutput:
            return str(self)
        else:
            return 'permutation(' + str(self.n) + ',cycles=' + str(self.cycles()) + ')'

    def __str__(self):
        C = self.cycles()
        s = ''
        for cycle in C:
            cyclestr = '('
            for el in cycle:
                cyclestr += str(el) + ','
            s += cyclestr[:len(cyclestr) - 1] + ')'
        if s == '':
            s = '()'
        return s

    def __getitem__(self, key):
        return self.P[key]

    def __neg__(self):
        Q = [0] * self.n
        for i in range(self.n):
            Q[self.P[i]] = i
        return permutation(self.n, mapping=Q)

    def __mul__(self, other):
        if self.n != other.n:
            raise permError
        Q = [0] * self.n
        for i in range(self.n):
            Q[i] = self.P[other.P[i]]
        return permutation(self.n, mapping=Q)

    def __pow__(self, i):
        if i == 0:
            return permutation(self.n)
        if i < 0:
            i = -i
            P = -self
        else:
            P = self
        Q = permutation(self.n)
        while i != 0:
            if i % 2 == 1:
                Q *= P
            i = i // 2
            P = P * P
        return Q

    def istrivial(self):
        for i in range(self.n):
            if self.P[i] != i:
                return False
        return True

    def __eq__(self, other):
        if not hasattr(other, 'P'):
            return False
        for i in range(self.n):
            if self.P[i] != other.P[i]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.P))
