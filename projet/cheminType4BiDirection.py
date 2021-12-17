"""
Bonus :
Calcul du plus court chemin par exploration bidirectionnelle du parcours en largeur dabord
Chemin Type 4
"""
def getSuccesseurGForward(G , node):
    """
        Suppose que G est grahe orientee normal
        Retourne les successeurs du sommet node.getElement()    
    """
    _,A = G
    elem = node.getElement()
    succ = set()
    for (s1,s2,time,lam) in A:
        # verification contrainte de temps
        if s1 == elem and int(time) > int(node.getEdge()):
            succ.add((s1,s2,time,lam))
    return succ

def getSuccesseurGBackWard(G , node):
    """
        Suppose que G est grahe orientee normal
        Retourne les successeurs du sommet node.getElement()    
    """
    _,A = G
    elem = node.getElement()
    succ = set()
    for (s1,s2,time,lam) in A:
        # verification contrainte de temps
        if s2 == elem :
            if node.getEdge() == 0:
                succ.add((s1,s2,time,lam)) 
            elif int(time) < int(node.getEdge()):
                succ.add((s1,s2,time,lam))
    return succ

class Node:
    def __init__(self,element = None,pere = None, edge = None):
        self.element = element
        self.pere = pere
        self.edge = edge

    def setPere(self,pere):
        self.pere = pere

    def getElement(self):
        return self.element

    def setEdge(self,edge) :
        self.edge = edge

    def getEdge(self):
        return int(self.edge)

    def getPere(self):
        return self.pere

    def getSolution(self):
        if self.element == None:
            return []
        if self.pere == None:
            return [self.element]
        else :
            return self.getPere().getSolution() + [(self.element)]
    
    def printSolution(self):
        if self.element == None:
            return ""
        if self.pere == None:
            return str(self.element)
        else :
            return self.getPere().printSolution() + " -> " + str(self.getEdge()) + "  ->  " + str(self.element) 
    
    def isTerminal(self,dest):
        return self.element == dest

class BFS:
    def __init__(self,G,initial,final,forward=True):
        self.G = G
        if forward:
            self.initial = initial
            self.final = final
        else:
            self.initial = final
            self.final = initial
        self.frontiere = [Node(self.initial,None,0)]
        self.dejaDev = set()
        self.forward = forward
    
    def setInitial(self,initial):
        self.initial = initial
    
    def setFinal(self,final):
        self.final = final

    def getInitial(self):
        return self.initial

    def getFinal(self):
        return self.final

    def getFrontiere(self):
        return self.frontiere
        # Met a jour la frontiere
    def evalNode(self):
        if len(self.frontiere) == 0 :
            return None
        else:
            n = self.frontiere[0]  # n : node
            self.dejaDev.add(n)
            if self.forward:
                successeurs = getSuccesseurGForward(self.G,n)
                for s in successeurs:
                    _,s2,time,_  = s
                    tmp = Node(n.getElement(),n.getPere(),n.getEdge())
                    if tmp.getEdge() == 0:
                        tmp.setEdge(time)
                    self.frontiere.append(Node(s2,tmp,time))
            else:
                successeurs = getSuccesseurGBackWard(self.G,n)
                for s in successeurs:
                    s1,_,time,_  = s
                    tmp = Node(n.getElement(),n.getPere(),n.getEdge())
                    if tmp.getEdge() == 0:
                        tmp.setEdge(time)
                    self.frontiere.append(Node(s1,tmp,time))

"""
Détecte si l'intersection de frontiere(bfs1) et frontiere(bfs2) 
(tel que les contraintes de temps soient respestées) non vide
"""
def connexion(bfs1,bfs2):
    for n1 in bfs1.getFrontiere():
        for n2 in bfs2.getFrontiere():
            if n1.getElement() == n2.getElement() and n1.getEdge() < n2.getEdge():
                return True
    return False

# Construit la solution
def buildSolution(bfs1,bfs2):
    for n1 in bfs1.getFrontiere():
        for n2 in bfs2.getFrontiere():
            if n1.getElement() == n2.getElement() and n1.getEdge() < n2.getEdge():
                return build(n1,n2)
    return None

def build(n1,n2):
    result = n1
    last = n2
    first = True
    while last.getPere() != None:
        if first:
            first = False
        else:
            result = Node(last.getElement(),result,last.getEdge())
        last = last.getPere()
    return Node(last.getElement(),result,last.getEdge())
    
# Point d'entrée de l'algo
def BFSBiDirection(G,init,dest):
    bfs1 = BFS(G,init,dest,True) # Exploration a partir du sommet de départ
    bfs2 = BFS(G,init,dest,False) # Exploration a partir du sommet d'arrivé
    try:
        while not connexion(bfs1,bfs2):
            bfs1.evalNode()
            if connexion(bfs1,bfs2):
                break
            else:
                bfs2.evalNode()
            if connexion(bfs1,bfs2):
                break
            
            # Suppression du premier element de la frontiere de BFS1
            f1 = bfs1.getFrontiere()
            n1 = f1[0]
            f1.remove(n1)
            # Suppression du premier element de la frontiere de BFS2
            f2 = bfs2.getFrontiere()
            n2 = f2[0]
            f2.remove(n2)

            if bfs1.getFrontiere() == [] or bfs2.getFrontiere() == []:
                raise Exception("Aucune chemin trouvé.")
        print(buildSolution(bfs1,bfs2).printSolution())
        return buildSolution(bfs1,bfs2).getSolution()
    except Exception as e:
        print(e)
