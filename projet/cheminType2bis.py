"""

Entrée : a  : sommet depart et b sommet arrivé
Idée : transformer G en un graphe G_2 tel que les aretes (b,b,0) et les autres valent(u,v,vt-ut)
Appliquer dijstra sur G_2 

"""
def transformGtype2toG2(G,depart):
    V,E = G
    Vn,En = V,set()
    for ((u,tu),_,(v,vt)) in E:
        if u == v and u == depart :
            En.add(((u,tu),0,(v,vt)))
        else:
            En.add(((u,tu),(vt-tu),(v,vt)))
    return Vn,En

def dijkstra(G, depart, arrivee):
    G = transformGtype2toG2(G,depart)
    """
        Suppose que G=(V,E) et V est un DICO (car init peut etre int, char, str, etc....)   
    """
    arrivee = getVertexWithIdMax(G,arrivee)
    depart = getVertexWithIdMin(G,depart)
    V,E = G
    tabDegres, tabPred = initDijkstra(G, depart)
    DejaVu = set()
    NonVisite = V.copy()
    while len(NonVisite)!=0 and (trouveMin(NonVisite,tabDegres) != arrivee):
        s1,t1 = trouveMin(NonVisite,tabDegres)
        DejaVu.add(s1)
        NonVisite.pop((s1,t1))
        for ((s,t),time,(s2,t2)) in E :
            if (s,t) == (s1,t1) :
                if tabDegres[V[(s2,t2)]] > tabDegres[V[(s1,t1)]] + time :
                    tabDegres[V[(s2,t2)]] = tabDegres[V[(s1,t1)]] + time
                    tabPred[V[(s2,t2)]] = (s1,t1)
    ## on a des None dans pred, donc je retourne la solution ici
    s = arrivee
    Sol = [s]
    while s != depart and s!=None :
        s = tabPred[V[s]]
        Sol = [s] + Sol
    if s == None:  # j'ai trouver un sommet None, on n'a pas de pere possible, donc on n'a pas de chemin possible
        return []
    return Sol

def getVertexWithIdMin(G,id):
    V,_ = G
    minVal = 1e3
    minSommet = id
    for (idSommet,valSommet) in V:
        if idSommet == id :
            if valSommet < minVal :
                minVal = valSommet
                minSommet = idSommet
    if minVal == 1e3 :
        return None
    else :
        return (minSommet,minVal)

def getVertexWithIdMax(G,id):
    V,_ = G
    maxVal = 0
    maxSommet = id
    for (idSommet,valSommet) in V:
        if idSommet == id :
            if valSommet > maxVal :
                maxVal = valSommet
                maxSommet = idSommet
    if maxVal == 0 :
        return None
    else :
        return (maxSommet,maxVal)

def initDijkstra(G, init):
    """
        Suppose que G=(V,E) et V est un DICO (car init peut etre int, char, str, etc....)
    """
    V,_ = G
    pred = [None for i in range(len(V))]
    degres = [1e10 for i in range(len(V))]
    for sommet in V :
        degres[V[sommet]] = 1e2
        pred[V[sommet]] = None
    degres[V[init]] = 0
    return degres, pred


def constructSol(G,depart,arrivee,pred):
    V,_ = G
    s = arrivee
    Sol = [s]
    while s != depart :
        s = pred[V[s]]
        Sol = [s] + Sol
    return Sol
"""
Input :
V : (Any,int)
d : List[float]
Retourne le sommet avec la valeur minumum
return (Any,int)
"""
def trouveMin(V,d):
    mini = 1e10
    sommet = None
    for v in V:
        if d[V[v]] < mini :
            mini = d[V[v]]
            sommet = v
    return sommet