"""
Ce fichier contient des fonctions générales qui pourront servir dans les algos
de recherche dans les graphes.

"""

"""
Retourne un graphe un multigraphe sans circuit G a partir d'un fichier
"""
def graphfromFile(filename):
    E = set()
    V = dict()
    f = open(filename)
    nbVertex = 0
    nbEdge = 0
    elements = f.readlines()
    for i in range(len(elements)):
        elem = elements[i]
        if i != len(elements) -1 :
            elem = elem[:len(elements[i])-1]
        if i == 0:
            nbVertex = int(elem)
        if i == 1:
            nbEdge = int(elem) 
        if i>=2 and i<nbVertex+2:
            V[elem]=i-2
        if i >= nbVertex+2:
            elem = elem[1:len(elem)-1].split(",")
            s1=elem[0]
            s2=elem[1]
            time=elem[2]
            l=elem[3]
            E.add((s1,s2,time,l))
    return (V,E)
"""
Fonction de transformation de graphe
"""
def transformG_avecDico(G):
    """
        suppose G est le graphe normal
    """
    V,E = G
    # Vt : dict[(sommet, time): int]
    Vt = dict()
    Et = set()
    i = 0
    for (s1,s2,time,_) in E:
        # Ajout des sommets
        if (s1,int(time)) not in Vt: 
            Vt[(s1,int(time))] =  i
            i += 1
        if (s2,int(time)+1) not in Vt:
            Vt[(s2,int(time)+1)] = i
            i += 1
        # Ajout des aretes
        Et.add( ((s1,int(time)),1,(s2,int(time)+1)))
    toRemove = Vt.copy()
    while len(toRemove) != 0:
        s1, t1 = list(toRemove)[0] #on a la clé
        toRemove.pop((s1,t1))

        # stock = liste des sommets avec meme lettre
        stock = []
        stock.append((s1,t1))
        for s2,t2 in toRemove :
            if s1 == s2 :
                stock.append((s2,t2))
        stock = quicksort(stock) # trier stock
        for i in range(len(stock)):
            if stock[i] in toRemove:
                toRemove.pop(stock[i])
            if i < len(stock) - 1 :
                Et.add((stock[i],0,stock[i+1]))
    return (Vt,Et)

def quicksort(tab):
    less = []
    equal = []
    greater = []
    if len(tab) > 1:
        p,t = tab[0]
        for x,t2 in tab:
            if t2 < t:
                less.append((x,t2))
            elif t2 == t:
                equal.append((x,t2))
            elif t2 > t:
                greater.append((x,t2))
        return quicksort(less)+equal+quicksort(greater)
    else:  
        return tab

def construireSolution(G, depart, arrivee,pere):
    S, A = G
    if arrivee == pere[S[arrivee]] :
        return [arrivee]
    else :
        chemin = [arrivee]
        i = pere[S[arrivee]]
        while i != depart:
            chemin = [i] + chemin
            i = pere[S[i]]
        return [depart] + chemin

def getSuccesseur(G,node):
    S,A = G
    succ = set()
    for (s1,s2,time,lam) in A:
        if s1 == node :
            succ.add((s1,s2,time,lam))
    return succ
"""
Fonction d'affichage du graphe
"""
def affiche_graphe(G):
    V,E=G
    print("Nb sommets dans le graphe transforme : ",len(V))
    print(V)
    print("Nb aretes dans le graphe transforme : ",len(E))
    print(E)
"""
Fonction d'affichage de la solution d'un algorithme de recherche dans un graphe
"""
def displayPath(nodeList):
    if nodeList == [] or nodeList == None:
        return "Il n'y a aucun chemin de disponible."
    result = ""
    if len(nodeList) != 0 :
        lamb = 1
        state,_ = nodeList[0]
        for i in range(len(nodeList)-1) :
            s2,t2 = nodeList[i+1]
            if state != s2 :
                result += str(state)
                result += " -> "
                result += str((t2-lamb)) 
                result += " -> "
                result += str(s2)
                result += " | "
                state = s2
    return result

# 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

def construireSolutionPLGt(solutionPath):
    if solutionPath == []:
        return "Il n'y a pas de chemin disponible."
    res = " "
    for (s1,s2) in solutionPath:
        if s1[0] != s2[0]:
            res += (s1 + " vers " + s2 + " ")
    return res 

def construireSolutionPLG(solutionPath):
    if solutionPath == []:
        return "Il n'y a pas de chemin disponible."
    res = " "
    for (s1,s2) in solutionPath:
        if s1[0] != s2[0]:
            res += (s1[0] + " -> " + s1[1] +" -> "+ s2[0] + " ")
    return res 

import random
import numpy as np
def createArbreEnracine(n,p=0.5,lambd=1):
    V = []
    E = set()
    for i in range(n):
        V.append(str(i))
    for i in range(len(V)):
        sommetRestants = V[(i+1):]
        for j in sommetRestants:
            tirage = random.random()
            if tirage <= p:
                E.add((str(i),j,random.randint(1,np.ceil(n/2)),lambd))
    Vr = {}
    for i in range(len(V)):
        Vr[V[i]] = i
    return Vr,E,V[0]




## Fonction de saisie au clavier d'un graphe
def saisieClavier():
    V = set()
    E = set()
    try:
        nbSommet = int(input("Nombre de sommets : "))
        nbAretes = int(input("Nombre d'arête : "))
        for i in range(nbSommet):
            V.add(input("Nom du sommet {0} : ".format(i)))
        for i in range(nbAretes):
            s1 = str(input("Arête {0} depart : ".format(i)))
            if s1 not in V:
                raise Exception("le sommet {0} n'est pas présent dans la liste de sommet".format(s1))
            s2 = str(input("Arête {0} arrivée : ".format(i)))
            if s2 not in V:
                raise Exception("le sommet {0} n'est pas présent dans la liste de sommet".format(s2))
            time = int(input("Arête {0} : valeur de l'arete (entier):".format(i)))
            lambda_ = int(input("Arête {0} : lambda de l'arete (entier) : ".format(i)))
            E.add((s1,s2,time,lambda_))
    except ValueError:
        print("Valeur inscrite incorrect")
    except Exception as e:
        print(e)
    return V,E
    

#print(saisieClavier())
                