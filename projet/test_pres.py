import numpy as np
import utils
import cheminType4 as T4
import cheminType4bis as T4bis
import programmeLineaire as T4PL
import cheminType4BiDirection as BFSBD
import matplotlib.pyplot as plt
import time

pas = 5
nbSommet = 50

sommets = [i for i in range(10,nbSommet,pas)]



nbInstance = 10
probabilities = [0.4,0.5,0.6,0.7,0.8]

timeT4 = np.zeros((len(probabilities),len(sommets)))
timeT4b = np.zeros((len(probabilities),len(sommets)))
timeT4PL = np.zeros((len(probabilities),len(sommets)))
timeT4BFSbi = np.zeros((len(probabilities),len(sommets)))

timeT4.astype(float)
timeT4b.astype(float)
timeT4PL.astype(float)
timeT4BFSbi.astype(float)


t_alpha = 0
t_omega = 1e10

"""
5 graphiques avec dans chacun une probabilité différente, et avec les 4 algos de chemins de type 4.
"""
for p in range(len(probabilities)):
    for i in range(len(sommets)):
        currentTime = [0,0,0,0]
        timeGenerationGraphe = 0
        for k in range(nbInstance):
            # Generation du graphe
            V,E,s = utils.createArbreEnracine(sommets[i],probabilities[p])
            depart = str(s)
            arrivee = str((sommets[i]-1))
            # Transformation du graphe
            startGraphe = time.time()
            Gt = utils.transformG_avecDico((V,E))       
            endGraphe = time.time()
            timeGenerationGraphe = (endGraphe - startGraphe)

            start = time.time()
            # depart algo type 4
            T4.bfs_type4(Gt,depart,arrivee,t_alpha,t_omega)
            end = time.time()
            currentTime[0] += (end - start) + timeGenerationGraphe

            start = time.time()
            # depart algo type 4
            T4bis.dijkstra(Gt,depart,arrivee,t_alpha,t_omega)
            end = time.time()
            currentTime[1] += (end - start) + timeGenerationGraphe

            start = time.time()
            # depart algo type 4
            T4PL.resolve(Gt,depart,arrivee,t_alpha,t_omega)
            end = time.time()
            currentTime[2] += (end - start) + timeGenerationGraphe

            start = time.time()
            # depart algo type 4
            BFSBD.BFSBiDirection((V,E),depart,arrivee)
            end = time.time()
            currentTime[3] += (end - start) + timeGenerationGraphe
        for x in range(len(currentTime)):
            currentTime[x] /= nbInstance

        timeT4[p][i] = currentTime[0]
        timeT4b[p][i] = currentTime[1]
        timeT4PL[p][i] = currentTime[2]
        timeT4BFSbi[p][i] = currentTime[3]



print(timeT4)
print(timeT4b)
print(timeT4PL)
print(timeT4BFSbi)


# version normal

for p in range(len(probabilities)):
    plt.plot(sommets,timeT4[p], label= 'BFS')
    plt.plot(sommets,timeT4b[p], label= 'Dijkstra')
    plt.plot(sommets,timeT4PL[p], label= 'PL')
    plt.plot(sommets,timeT4BFSbi[p], label= 'Bi-direction')
    plt.xlabel("nombre de sommets")
    plt.ylabel("temps d'execution en s")
    plt.title("Temps d'execution en fonction du nombre de sommet avec une probabilité de "+str(probabilities[p]))
    plt.legend()
    plt.show()


# version log temps

for p in range(len(probabilities)):
    plt.yscale('log')
    plt.plot(sommets,timeT4[p], label= 'BFS')
    plt.plot(sommets,timeT4b[p], label= 'Dijkstra')
    plt.plot(sommets,timeT4PL[p], label= 'PL')
    plt.plot(sommets,timeT4BFSbi[p], label= 'Bi-direction')
    plt.xlabel("nombre de sommets")
    plt.ylabel("log temps d'execution en s")
    plt.title("Log du temps d'execution en fonction du nombre de sommet avec une probabilité de "+str(probabilities[p]))
    plt.legend()
    plt.show()