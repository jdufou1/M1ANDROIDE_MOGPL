import utils
import cheminType1 as T1
import cheminType2 as T2
import cheminType2bis as T2bis
import cheminType3 as T3
import cheminType3bis as T3bis
import cheminType4 as T4
import cheminType4bis as T4bis
import programmeLineaire as T4PL
import cheminType4BiDirection as BFSBD
import time

G = utils.graphfromFile('test.txt')
V,E = G
Gt = utils.transformG_avecDico(G)
Vt, Et = Gt

print("###########################  AFFICHAGE DU GRAPHE TRANSFORME ##################################################")
print("Nb sommets dans le graphe transforme : ",len(Vt))
print(Vt)
print("Nb aretes dans le graphe transforme : ",len(Et))
print(Et)
print("##############################################################################################################")

"""
n = 10
V,E,s = utils.createArbreEnracine(n,p=0.3)
#print(V,E)
Gt = utils.transformG_avecDico((V,E))
depart = str(s)
arrivee = str((n-1))
"""


"""
V,E = utils.saisieClavier() # A décommenter pour utilisation
Gt = utils.transformG_avecDico((V,E))
"""

depart = 'a'
arrivee = 'l'

t_alpha,t_omega = -1e10,1e10
### Chemin T1
start = time.time()
print("T1 : Le chemin d'arrivée au plus tot de ",depart," à ",arrivee,", dans le graphe G/ ",T1.dijkstra(Gt, depart, arrivee,t_alpha,t_omega))
end = time.time()
print("Dans le graphe G : ",utils.displayPath(T1.dijkstra(Gt, depart, arrivee,-1e10,1e10)))
print("Temps de calcul : ",(end - start)," ms", "\n")

### Chemin T2
start = time.time()
print("T2 : Le chemin de départ au plus tard de ",depart," à ",arrivee,", dans le graphe G/ " , T2.cheminType2(Gt,depart,arrivee,t_alpha,t_omega))
end = time.time()
print("Dans le graphe G : ",utils.displayPath(T2.cheminType2(Gt,depart,arrivee,t_alpha,t_omega)))
print("Temps de calcul : ",(end - start)," ms", "\n")

### Chemin T2 bis
start = time.time()
print("T2bis : Le chemin de départ au plus tard de ",depart," à ",arrivee,", dans le graphe G/ " , T2bis.dijkstra(Gt,depart,arrivee))
end = time.time()
print("Dans le graphe G : ",utils.displayPath( T2bis.dijkstra(Gt,depart,arrivee)))
print("Temps de calcul : ",(end - start)," ms", "\n")

### Chemin T3 :
start = time.time()
print("T3 : Le chemin le plus rapide de ",depart," à ",arrivee,", dans le graphe G/ ",T3.type3(Gt,depart,arrivee,t_alpha,t_omega))
end = time.time()
print("Dans le graphe G : ",utils.displayPath(T3.type3(Gt,depart,arrivee,t_alpha,t_omega)))
print("Temps de calcul : ",(end - start)," ms", "\n")

### Chemin T3 bis :
start = time.time()
print("T3bis : Le chemin le plus rapide de ",depart," à ",arrivee,", dans le graphe G/ ",T3bis.dijkstra(Gt,depart,arrivee))
end = time.time()
print("Dans le graphe G : ",utils.displayPath(T3bis.dijkstra(Gt,depart,arrivee)))
print("Temps de calcul : ",(end - start)," ms", "\n")

### chemin T4 :
start = time.time()
print("T4 : Le plus court chemin de ",depart," à ",arrivee,", dans le graphe G/ " , T4.bfs_type4(Gt,depart,arrivee,t_alpha,t_omega))
end = time.time()
print("Dans le graphe G : ",utils.displayPath(T4.bfs_type4(Gt,depart,arrivee,t_alpha,t_omega)))
print("Temps de calcul : ",(end - start)," ms", "\n")

### chemin T4 bis :
start = time.time()
print("T4 bis : Le plus court chemin de ",depart," à ",arrivee,", dans le graphe G/ " , T4bis.dijkstra(Gt,depart,arrivee,t_alpha,t_omega))
end = time.time()
print("Dans le graphe G : ",utils.displayPath(T4bis.dijkstra(Gt,depart,arrivee,t_alpha,t_omega)))
print("Temps de calcul : ",(end - start)," ms", "\n")

### Chemin T4 Recherche Bi directionnelle BFS Question Bonus
start = time.time()
print("T4 Recherche BFS Bi directionnelle  : Le plus court chemin de ",depart," à ",arrivee,", dans le graphe G " , BFSBD.BFSBiDirection((V,E),depart,arrivee))
end = time.time()
print("Temps de calcul : ",(end - start)," ms", "\n")

### Chemin T4 avec PL (Programme Linéaire)
start = time.time()
print(T4PL.resolve(Gt,depart,arrivee,t_alpha,t_omega))
end = time.time()
print("Temps de calcul : ",(end - start)," ms", "\n")