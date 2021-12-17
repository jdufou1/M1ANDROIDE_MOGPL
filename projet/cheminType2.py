"""
Algo : 
entrée : Graphe G, depart char, arrivee char

- Transformation de G en G/
- On effetue BFS sur tous les sommets du depart dans G/ a partir du sommet de plus grande valeur
- Application de BFS

"""
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

"""
Algorithme de Breath First Search
Entree:
G : Graphe transformé
init,dest : sommet initial,final
"""
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

def cheminType2(G,init,dest, t_alpha, t_omega):
    # On recupere tous les noeuds qui ont le meme id que depart
    V,_ = G
    departsPossible = []
    for (s,t) in V:
        if s == init and t >= t_alpha : #il faut que temps_sommet >= t_alpha
            departsPossible.append((s,t))
    departsPossible = quicksort(departsPossible) # on trie de facon decroissant
    dest = getVertexWithIdMax(G,dest, t_omega) #il faut que temps_sommet <= t_omega
    for depart in departsPossible :
        resultBFS = bfs(G,depart,dest)
        if resultBFS != None :
            return resultBFS
    #print('Il n existe pas de chemin de type 2 possible de', depart, 'a', arrivee, 'entre les intervalles', t_alpha, 'et', t_omega)
    return []

"""
QuickSort version tri décroissant
"""
def quicksort(tab):
    less = []
    equal = []
    greater = []
    if len(tab) > 1:
        p,t = tab[0]
        for x,t2 in tab:
            if t2 > t:
                less.append((x,t2))
            elif t2 == t:
                equal.append((x,t2))
            elif t2 < t:
                greater.append((x,t2))
        return quicksort(less)+equal+quicksort(greater)
    else:  
        return tab

def getSuccesseur(G,element):
    _,A = G
    succ = set()
    for ((s1,t1),time,(s2,t2)) in A:
        if (s1,t1) == element :
            succ.add(((s1,t1),time,(s2,t2)))
    return succ

def getVertexWithIdMax(G,id,time):
    """
       suppose time = t_omega
       en effet, la fonction cheminType2 utilise cette fonction pour trouver le sommet arrivee
    """
    V,_ = G
    maxVal = 0
    maxSommet = id
    for (idSommet,valSommet) in V: # il prend les clés du dico
        if idSommet == id: 
            if valSommet > maxVal and valSommet <= time : #il faut que temps_sommet <= t_omega
                maxVal = valSommet
                maxSommet = idSommet
    if maxVal == 0 :
        return None
    else :
        return (maxSommet,maxVal)
