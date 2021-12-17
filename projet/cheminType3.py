"""
Algo : 
- On recupere tous les états de depart possible de la forme (d_s,d_t)
- On recupere tous les états d'arrivee possible de la forme (a_s,a_t)
- On trie toutes les combinaisons possible de trajet entre les d_s / a_s par ordre croissant en fonction de (a_t - d_t) et valeurs positive
tel que (a_t - d_t) > 0
- On lance BFS sur toutes ces combinaisons trier jusqua obtenir un trajet possible


Rq : resultat optimal mais approche naive coute cher, peut etre imaginer une autre construction du graphe...

"""
def quicksort(tab):
    less = []
    equal = []
    greater = []
    if len(tab) > 1:
        _,_,t = tab[0]
        for x,y,t2 in tab:
            if t2 < t:
                less.append((x,y,t2))
            elif t2 == t:
                equal.append((x,y,t2))
            elif t2 > t:
                greater.append((x,y,t2))
        return quicksort(less)+equal+quicksort(greater)
    else:  
        return tab

def type3(G,depart,dest, t_alpha, t_omega):
    V,E = G
    departPossible = []
    arriveePossible = []
    for (s,t) in V :
        if s == depart and t >= t_alpha: #il faut que temps_sommet >= t_alpha
            departPossible.append((s,t))
        elif s == dest and t <= t_omega: #il faut que temps_sommet <= t_omega
            arriveePossible.append((s,t))
    combinaisonsPossible = []
    for (d_s,d_t) in departPossible :
        for (a_s,a_t) in arriveePossible :
            if (a_t - d_t) > 0 :
                combinaisonsPossible.append(((d_s,d_t) , (a_s,a_t) , (a_t - d_t)))
    combinaisonsPossible = quicksort(combinaisonsPossible) # trie ordre croissant
    for d,a,_ in combinaisonsPossible :
        resultBFS = bfs(G,d,a)
        if resultBFS != None :
            return resultBFS
    return []

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
        if self.pere == None:
            return [self.element]
        else :
            return self.getPere().getSolution() + [self.element]
    
    def isTerminal(self,dest):
        return self.element == dest

def bfs(G,init,dest):
    """ 
        suppose G transformé
        Retourne un chemin realisable mais pas optimum
    """
    dejaDev = []
    frontiere = []
    frontiere.append(Node(init))
    while len(frontiere) != 0 :
        n = frontiere[0]
        if n.isTerminal(dest) :
            return n.getSolution()
        else :
            frontiere.remove(n)
            dejaDev.append(n)
            successeurs = getSuccesseur(G,n.getElement())
            for s in successeurs:
                ((_,_),_,(s2,t2)) = s
                frontiere.append(Node((s2,t2),n))

def getSuccesseur(G,element):
    _,A = G
    succ = set()
    for ((s1,t1),time,(s2,t2)) in A:
        if (s1,t1) == element :
            succ.add(((s1,t1),time,(s2,t2)))
    return succ
