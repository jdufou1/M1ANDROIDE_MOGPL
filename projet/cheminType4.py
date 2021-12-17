"""
Algo : 
1 - Transformation de G en G/
2 - Ajout d'arete a G/ tel que pour tous sommet (s_i,t_i) de G/, si il existe une arete tel que ((s1,t1),time,(s2,t2)) ou s1 = s_i alors
on créer une arete de s_i vers s2. Cela permet de contourner la contrainte des aretes nulle qui bloquent le fonctionnement de BFS
3 - On lance l'algo BFS a partir du coefficient minimal du sommet de départ en cherchant le coefficient maximal du sommet d'arrivée afin de
pouvoir couvrir toutes les possibilités de trajet.


Rq : la transformation à l'étape 3 est assez couteuse (double boucle)
"""
def transformGtoGb(G):
    V,E = G
    Vb = V
    Eb = set()
    for (s,t) in V:
        for ((s1,t1),time,(s2,t2)) in E :
            if s1 == s and t1 > t :
                Eb.add(((s,t),0,(s2,t2)))
            Eb.add(((s1,t1),0,(s2,t2)))
    return (Vb,Eb)

class Node:
    def __init__(self,element = None,pere = None):
        self.element = element
        self.pere = pere

    def setPere(self,pere):
        self.pere = pere

    def getElement(self):
        return self.element

    def getPere(self):
        return self.pere

    def getSolution(self):
        if self.element == None:
            return []
        if self.pere == None:
            return [self.element]
        else :
            return self.getPere().getSolution() + [self.element]
    
    def isTerminal(self,dest):
        return self.element == dest

## PARCOURS BFS
## Prend en parametre un graphe transformé
def bfs_type4(G,init,dest, t_alpha, t_omega):
    init = getVertexWithIdMin(G,init, t_alpha)
    dest = getVertexWithIdMax(G,dest, t_omega)
    G = transformGtoGb(G)

    dejaDev = []
    frontiere = []
    frontiere.append(Node(init))
    while len(frontiere) != 0 :
        n = frontiere[0]  # n : node
        if n.isTerminal(dest) :
            return n.getSolution()
        else :
            frontiere.remove(n)
            dejaDev.append(n)
            successeurs = getSuccesseurT4(G,n.getElement())
            for s in successeurs:
                _,_,s2, = s
                newNode = Node(s2,n)
                if newNode.isTerminal(dest):
                    return newNode.getSolution()
                frontiere.append(Node(s2,n))
    return []

def getSuccesseurT4(G,node):
    _,A = G
    succ = set()
    for (s1,time,s2) in A:
        if s1 == node :
            succ.add((s1,time,s2))
    return succ

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


