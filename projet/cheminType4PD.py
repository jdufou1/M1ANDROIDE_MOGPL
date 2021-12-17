"""
Chemin type 4 par programmation dynamique
"""

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




def prog_dyn_type_4(G,depart,arrivee):
    pass