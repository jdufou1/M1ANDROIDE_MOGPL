from time import process_time
import utils

"""
Chemin type1

On suppose que G=(V,E) est un graphe transforme pour toutes les fct ici
On suppose que V est une matrice de set(sommet) et E = set( ((s1,t1), 0-1, (s2,t2)) )

Algo : 
entrée : Graphe G, depart char, arrivee char

- Transformation de G en G/
- Transformation des aretes de G/ tel que toutes les aretes sont valués par t2-t1 hormis les aretes entre l'arrivee
- Application de Dijkstra avec pour depart le noeud a coefficient minimal de depart
- on renvoit le chemin selon Dijkstra sur la destination a coefficient maximal de l'arrivee
Retourne un chemin de G/
"""
def getVertexWithIdMin(G,id,time):
    """
       suppose time = t_alpha et V = dico((lettre, time): indice_int) 
       en effet, la fonction dijkstra utilise cette fonction pour trouver le sommet depart
    """
    V,_ = G
    minVal = 1e3
    minSommet = id
    for (idSommet,valSommet) in V:
        if idSommet == id :
            if valSommet < minVal and valSommet >= time: #il faut que temps_sommet >= t_alpha
                minVal = valSommet
                minSommet = idSommet
    if minVal == 1e3 :
        return None
    else :
        return (minSommet,minVal)

def getVertexWithIdMax(G,id,time):
    """
       suppose time = t_omega
       en effet, la fonction dijkstra utilise cette fonction pour trouver le sommet arrivee
    """
    V,_ = G
    maxVal = -1
    maxSommet = id
    for (idSommet,valSommet) in V:
        if idSommet == id :
            if valSommet > maxVal and valSommet <= time: #il faut que temps_sommet <= t_omega
                maxVal = valSommet
                maxSommet = idSommet
    if maxVal == -1 :
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

def trouveMin(V,d):
    mini = 1e10
    sommet = None
    for v in V:
        if d[V[v]] < mini :
            mini = d[V[v]]
            sommet = v
    return sommet

def transformGtype1(G, arrivee):
    V,E = G
    resE = set()
    for ((s,t),time,(s2,t2)) in E :
        if s == s2 and s == arrivee:
            resE.add(((s,t),time,(s2,t2)))
        else :
            resE.add( ((s,t),(t2-t),(s2,t2)) )
    return V,resE

def dijkstra(G, depart, arrivee, t_alpha, t_omega):
    """
        Suppose que G=(V,E) et V = dict[ (lettre,time): indice_int ]
        Suppose depart et arrive sont une lettre ou un entier
    """
    G = transformGtype1(G,arrivee)
    # arrivee : (sommet,time)
    arrivee = getVertexWithIdMax(G,arrivee, t_omega) 
    # depart : (sommet,time)
    depart = getVertexWithIdMin(G,depart, t_alpha)

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
    s = arrivee
    Sol = [s]
    while s != depart and s!=None :
        s = tabPred[V[s]]
        Sol = [s] + Sol
    if s == None:
        return []
    return Sol