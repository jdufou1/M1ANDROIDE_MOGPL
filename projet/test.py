import numpy as np
import cheminType1 as T1
import cheminType2 as T2
import cheminType2bis as T2b
import cheminType3 as T3
import cheminType3bis as T3b
import cheminType4 as T4
import cheminType4bis as T4b
import cheminType4BiDirection as BFSBD
import testPL as pl
import programmeLineaire as pl2
import algo
import matplotlib.pyplot as plt
import time
import math

def calcule_qualiter_temps_execution(listeListeGraphe,liste_fonction):
    temps_execution = []
    qualiter = []
    for i in np.arange(len(liste_fonction)):
        resultat = []
        resultat2 = [] 
        for list_graphe in listeListeGraphe:
            temps = []
            temps2 = []
            # Parcours chaque graphe de parametre n,p de la liste_graphe
            for graphe in list_graphe :
                # Calcule le temps d’exécution pour un graphe pour une fonction
                debut = time.time()
                couverture = liste_fonction[i](graphe,str(0),str(len(graphe)-1),-math.inf,math.inf)
                fin = time.time()
                temps.append((fin - debut))
                if couverture == None: 
                    temps2.append(0)
                else:
                    temps2.append(len(couverture))
               
            resultat.append(np.mean(temps))
            resultat2.append(np.mean(temps2))
            
        temps_execution.append(resultat)
        qualiter.append(resultat2)
       
    return np.array(temps_execution),np.array(qualiter)
    
def graphique_comparaison(n_p,resultat_temps,P,nom_axeX,nom_axeY,nom_titre):
    
    val = int(len(n_p) / len(P))
    for i in range(1,len(P)+1):
       
        x = n_p[(i-1)*val:i*val,0]
        y = resultat_temps[(i-1)*val:i*val]
        plt.plot(x,y, label= ' p = ' + str(P[i-1]))

    plt.xlabel(nom_axeX)
    plt.ylabel(nom_axeY)
    plt.title(nom_titre)
    plt.legend()
    plt.show()

    coeff_directeur = []
   
    x = np.array(n_p)
    y = np.array(resultat_temps)
    for i in range(0,len(P)):
       
        deltaX = x[(i+1)*val-1] - x[i*val]
        deltaY = y[(i+1)*val-1] - y[i*val]
        coeff_directeur.append(deltaY/deltaX[0])
    return coeff_directeur

def graphique_passage_log(n_p,resultat_temps,P,nom_axeX,nom_axeY,nom_titre):
    x = np.array(n_p)
    y = np.log(np.array(resultat_temps))
    val = int(len(n_p) / len(P))
    graphique_comparaison(x,y,P,nom_axeX,nom_axeY,nom_titre)
    coeff_directeur = []
    
    for i in range(0,len(P)):
        deltaX = x[(i+1)*val-1] - x[i*val]
        deltaY = y[(i+1)*val-1] - y[i*val]
        coeff_directeur.append(deltaY/deltaX[0])
    return coeff_directeur

def graphique_passage_log_log(n_p,resultat_temps,P,nom_axeX,nom_axeY,nom_titre):
    x = np.log(np.array(n_p))
    y = np.log(np.array(resultat_temps))
    val = int(len(n_p) / len(P))
    graphique_comparaison(x,y,P,nom_axeX,nom_axeY,nom_titre)
    coeff_directeur = []
    for i in range(0,len(P)):
        deltaX = x[(i+1)*val-1] - x[i*val]
        deltaY = y[(i+1)*val-1] - y[i*val]
        coeff_directeur.append(deltaY/deltaX[0])
    return coeff_directeur

def parametre_grille_search(nmin,nmax,pas_n,pmin,pmax,pas_p):
    N = [i for i in np.arange(nmin,nmax,pas_n) ]
    P = [i for i in np.arange(pmin,pmax,pas_p)]
    return np.array([(n,p) for p in P for n in N ]),N,P

def graphe_grille_search(n_p,iters=10):
    listeListeGraphe = []
    for n,p in n_p :
        temps = []
        for _ in np.arange(iters):
            #changer que ici 
            V,E,_ = algo.createArbreEnracine(int(n),p)
            temps.append(algo.transformG_avecDico( (V,E) ))
        listeListeGraphe.append(temps)
    return np.array(listeListeGraphe)


def test_experimentale(n_p,P,iters,liste_fonction,nom_liste_fonction,dico_bool):
    listeListeGraphe = graphe_grille_search(n_p,iters)
    execution,_ = calcule_qualiter_temps_execution(listeListeGraphe,liste_fonction)
    coeff_directeur = []
    coeff_directeur_log = []
    coeff_directeur_log_log = []

    if dico_bool['execution'] :
        #Temps execution
        for i in np.arange(len(execution)):
            coeff_directeur.append((nom_liste_fonction[i],graphique_comparaison(n_p,execution[i],P,'Nombre de sommets','Temps en secondes','Algo ' + nom_liste_fonction[i] ))) 
            coeff_directeur_log.append((nom_liste_fonction[i],graphique_passage_log(n_p,execution[i],P,'Nombre de sommets','Temps en Log secondes','Algo ' + nom_liste_fonction[i] + ' Log')))
            coeff_directeur_log_log.append((nom_liste_fonction[i],graphique_passage_log_log(n_p,execution[i],P,'Nombre de Log sommets','Temps en Log secondes','Algo '+ nom_liste_fonction[i] +' Log-Log')))
        
    dico_resultat = dict()
    dico_resultat['coeff_directeur'] = coeff_directeur
    dico_resultat['coeff_directeur_log'] = coeff_directeur_log
    dico_resultat['coeff_directeur_log_log'] = coeff_directeur_log_log
    dico_resultat['execution'] = execution
    return dico_resultat

n_p,_,P = parametre_grille_search(10,70,2,0.3,0.61,0.1) #nmin,nmax,pas_n,pmin,pmax,pas_p
liste_fonction = [BFSBD.BFSBiDirection]
nom_liste_fonction = ['Recherche Bi-directionnelle']
dico_bool = {'execution':True, 'nb_couverture': False, 'rapport': False}
dico_resultat = test_experimentale(n_p,P,10,liste_fonction,nom_liste_fonction,dico_bool)
print(dico_resultat)