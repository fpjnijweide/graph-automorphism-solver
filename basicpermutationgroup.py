# permutation group algorithms for calculating orbits, transversals, Schreier generators for finding stablizers, etc.
# original authors: P. Bonsma (2015)

from permutation import permutation


def Orbit(generators, el, returntransversal=False):
    O = [el]
    if len(generators) == 0:
        return O, None
    n = generators[0].n
    memberVec = [0] * n
    memberVec[el] = 1
    if returntransversal:
        U = [permutation(n)]
    ind = 0
    while ind < len(O):
        el = O[ind]
        for P in generators:
            mapel = P[el]
            if not memberVec[mapel]:
                memberVec[mapel] = 1
                O.append(mapel)
                if returntransversal:
                    U.append(P * U[ind])
        ind += 1
    for el in O:
        memberVec[el] = 0
    if returntransversal:
        return O, U
    else:
        return O


def SchreierGenerators(generators, el):
    O, U = Orbit(generators, el, True)
    SchrGen = []
    for ind in range(len(O)):
        el = O[ind]
        for P in generators:
            mapel = O.index(P[el])
            newgen = -U[mapel] * P * U[ind]
            if not newgen.istrivial():
                SchrGen.append(newgen)
    return SchrGen


def FindNonTrivialOrbit(generators):
    if generators == []:
        return None
    n = generators[0].n
    for P in generators:
        for el in range(n):
            if P[el] != el:
                return el


def Reduce(generators, wordy=0):
    if wordy >= 1:
        print("  Reducing. Input length:", len(generators))
    if generators == []:
        return generators
    n = generators[0].n
    outputgenerators = []
    todo = generators
    while todo != []:
        el = FindNonTrivialOrbit(todo)
        if el == None:  # can happen if the input (erroneously) contains trivial permutations
            break
        if wordy >= 2:
            print("    Next iteration: still to reduce:\n     ", todo)
            print("    Reducing for element", el)
        images = [None] * n
        todonext = []
        for P in todo:
            if P[el] == el:
                todonext.append(P)
            elif images[P[el]] == None:
                if wordy >= 2:
                    print("      Keeping", P, "which maps", el, "to", P[el])
                outputgenerators.append(P)
                images[P[el]] = P
            else:
                Q = -images[P[el]] * P
                if wordy >= 2:
                    print("      Changing", P, "to", Q)
                if not Q.istrivial():
                    todonext.append(Q)
        todo = todonext
    if wordy >= 1:
        print("  Output length:", len(outputgenerators))
    return outputgenerators


def Stabilizer(generators, el):
    return Reduce(SchreierGenerators(generators, el), 0)
