"""
    PROJET MOGPL : Implémentation du programme linéaire du plus court chemin avec gurobi
    Jérémy DUFOURMANTELLE
    Juliette LING
    2021-2022
"""

import numpy as np
from gurobipy import *

def getVertexWithIdMin(G,id, time):
    """
       suppose time = t_alpha
       en effet, la fonction bfs_type4 utilise cette fonction pour trouver le sommet depart
    """
    V,_ = G
    minVal = 1e3
    minSommet = id
    for (idSommet,valSommet) in V:
        if idSommet == id :
            if valSommet < minVal and valSommet >= time:
                minVal = valSommet
                minSommet = idSommet
    if minVal == 1e3 :
        return None
    else :
        return (minSommet,minVal)

def getVertexWithIdMax(G,id,time):
    """
       suppose time = t_omega
       en effet, la fonction bfs_type4 utilise cette fonction pour trouver le sommet arrivee
    """
    V,_ = G
    maxVal = 0
    maxSommet = id
    for (idSommet,valSommet) in V:
        if idSommet == id :
            if valSommet > maxVal and valSommet <= time :
                maxVal = valSommet
                maxSommet = idSommet
    if maxVal == 0 :
        return None
    else :
        return (maxSommet,maxVal)

"""
Prend en entrée le graphe transformé
Retourne les sommets du chemin optimal.
"""
def resolve(G, depart, arrivee,t_alpha,t_omega):
    Vt,Et = G
    # Récupération des valeurs minimales et maximales des sommets du graphe transformé 
    # afin de couvrir tout le graphe.
    source = getVertexWithIdMin(G,depart,t_alpha)
    target = getVertexWithIdMax(G,arrivee,t_omega)
    # Définitions des caractéristiques du modele.
    contraintes = len(Vt) # autant de contraintes que de sommets
    variables = len(Et) # autant de variables que d'arcs
    lines = range(contraintes)
    columns = range(variables)
    V = list(Vt)
    E = [((s1,t1),(s2,t2)) for ((s1,t1),_,(s2,t2))in Et]
    # Matrice des contraintes
    a = np.zeros((contraintes, variables))
    for (s1,t1),_,(s2,t2) in Et: # on boucle sur toute les aretes pour definir la matrice des contraintes (incidence)
        i, j = V.index( (s1,t1)), V.index((s2,t2)) # index entrant , index sortant
        k = E.index(((s1,t1), (s2,t2))) 
        a[i, k] = 1
        a[j, k] = -1
    # Second membre
    b = np.zeros(contraintes) # Toutes les contraintes sont = 0 sauf pour celle du depart et de l'arivee
    b[V.index(source)] = 1
    b[V.index(target)] = -1
    # coefficients présents dans la fonction objectif
    c = [time for (_,_),time,(_,_) in Et] # time : cout de larc
    m = Model("pl")
    # Déclaration des variables de décision.
    x = [m.addVar(vtype=GRB.BINARY, lb=0, name=f"x{i+1}") for i in columns]
    # Model update
    m.update()
    obj = LinExpr()
    obj = 0
    for j in columns:
        obj += c[j] * x[j]
    # Nous définissons ici la fonction objectif
    m.setObjective(obj, GRB.MINIMIZE)
    # Définition des contraintes
    for i in lines:
        m.addConstr(quicksum(a[i][j] * x[j] for j in columns) == b[i], f"Contrainte{i}")
    m.optimize()
    path = [source]
    
    print("\nSolution optimale:")
    for j in columns:
        print(f"x{j+1}\t= {int(x[j].x)}")
        if x[j].x == 1:
            path.append(E[j][1])
    print("\nValeur de la fonction objectif :", m.objVal)
    
    return path
    



