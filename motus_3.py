import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import pygame
import time
import copy

pygame.mixer.init()
son_bip=pygame.mixer.Sound("motus/motus_bip.wav")
son_bip_grave=pygame.mixer.Sound('motus/motus_bip_grave.wav')
son_bip.set_volume(0.5)
son_bip_grave.set_volume(0.5)
#pygame.mixer.music.load("motus/motus-boule-noire.mp3")
#pygame.mixer.music.load("motus/motus-remuer-boule.mp3")
#pygame.mixer.music.play()

def preparer_grille_numero(compteur_grille):
    if compteur_grille == 1 :
        numero_grille = [7,17,35,49,57,11,25,29,51,59,3,19,41,43,69,5,21,33,53,63,9,23,37,45,61]
        numero_valide = [7,49,29,59,19,33,63,9]
    if compteur_grille == 2 :
        numero_grille = [1,17,39,51,59,5,21,41,53,67,11,27,29,47,69,7,15,37,43,63,13,25,33,55,61]
        numero_valide = [59,5,41,47,7,15,25,61]
    if compteur_grille == 3 :
        numero_grille = [7,27,35,51,61,1,25,37,45,69,5,17,29,55,57,11,19,41,43,63,3,15,39,49,59]
        numero_valide = [27,37,45,5,41,63,15,59]
    if compteur_grille == 4 :
        numero_grille=[1,19,41,53,67,5,25,37,55,61,13,27,29,45,63,9,15,35,51,59,11,21,31,49,69]
        numero_valide = [53,67,25,13,45,9,31,69]
    if compteur_grille == 5 :
        numero_grille=[5,27,37,55,67,1,15,41,49,69,9,21,33,43,59,13,23,29,47,65,7,19,35,51,63]
        numero_valide = [5,37,49,21,59,29,7,51]
    if compteur_grille == 6 :
        numero_grille=[1,27,41,47,69,5,21,33,51,59,11,17,29,55,57,9,15,35,45,65,13,23,31,43,63]
        numero_valide = [41,5,51,11,57,15,35,43]

    def preparer_jarre(numero_grille,numero_valide):
        jarre=[]
        for elem in numero_grille :
            if elem not in numero_valide : jarre.append(elem)
        for _ in range(0,3):
            jarre.append(100)
        return jarre

    def preparer_matrice_grille(numero_grille, numero_valide):
        matrice = [numero_grille[i:i+5] for i in range(0, len(numero_grille), 5)]
        for i in range(0,5):
            for j in range(0,5) :
                if matrice[i][j] in numero_valide : matrice[i][j]=100
        return matrice

    jarre = preparer_jarre(numero_grille,numero_valide)
    matrice_grille = preparer_matrice_grille(numero_grille,numero_valide)
    return numero_grille,numero_valide,jarre,matrice_grille

def charger_mots(n):
    with open("motus/ods6.txt", "r", encoding="utf-8") as f:
        return [mot.strip().upper() for mot in f if len(mot.strip()) == n]
    
def jouer_mp3(son):
    pygame.mixer.music.load(son)  
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()   
    # Boucle d'attente jusqu'à la fin de la lecture
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)  # Évite de bloquer inutilement le CPU
    
def nouvelle_partie() :
    global mot_secret,essai_actuel,liste_rouge,tirage   
    mot_secret=random.choice(mots_possibles)
    tirage=0
    liste_rouge=[mot_secret[0],"","","","",""]
    essai_actuel[0]=0
    canvas.delete("all")
    canvas.create_image(0,0,anchor='nw',image=image_fond_tk)
    canvas_fonction.itemconfig(message, text="")
    entree.delete(0,tk.END)    
    dessiner_case_rectangle(canvas,0,0,mot_secret[0],couleur="")

def verifier_tentative(event=None):
    global liste_rouge,temp_mot
    mot = entree.get().strip().upper()
    if len(mot) != TAILLE or mot not in mots_possibles:
        canvas_fonction.itemconfig(message, text="Mot invalide.")
        return
    canvas_fonction.itemconfig(message, text="")
    entree.delete(0, tk.END)
    print(mot_secret)
    temp_mot_secret=list(mot_secret)
    temp_mot=list(mot)
    print(mot)
    for k in range(0,len(mot_secret)) :
        if mot_secret[k]==mot[k] :             
            temp_mot.remove(mot[k])
            temp_mot_secret.remove(mot_secret[k])
    print(temp_mot_secret) 
    print(temp_mot)   

    def afficher_lettre(i) :
        temp_mot_secret                
        lettre = mot[i]        
        if lettre == mot_secret[i]:            
            liste_rouge[i]=lettre
            son_bip.play()
            dessiner_case_rectangle(canvas,i, essai_actuel[0], lettre,"red")
        elif lettre in temp_mot_secret:  
            son_bip.play()          
            dessiner_case_cercle(canvas,i, essai_actuel[0], lettre,'yellow')
        else: 
            if lettre == liste_rouge[i] :
                canvas.delete(liste_bonne_lettre[i])
            son_bip_grave.play()            
            dessiner_case_rectangle(canvas,i, essai_actuel[0], lettre,couleur="")
    
    def afficher_sequence(i=0):
        global liste_bonne_lettre
        if i < TAILLE:
            afficher_lettre(i)            
            racine.after(250, lambda: afficher_sequence(i + 1))  # délai entre chaque bip/lettre
        else :    
            if essai_actuel[0]<TAILLE-1 and mot != mot_secret:                                
                for k in range(TAILLE):
                    if liste_rouge[k]!="": 
                        bonne_lettre=dessiner_case_rectangle(canvas,k,essai_actuel[0]+1,mot_secret[k],couleur="")  
     
            if mot == mot_secret:
                pygame.mixer.music.load("motus/motus-mot-trouve.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play()
                global mots_trouves,score
                mots_trouves+=1
                score+=SCORE_PAR_MOT
                canvas_fonction.itemconfig(compteur_mots, text=f"Mots trouvés : {mots_trouves}")
                canvas_fonction.itemconfig(compteur_score, text=f"Score : {score}")  
                canvas_fonction.itemconfig(message, text="*** Bravo !!! ***")
                racine.after(3500,tirage_numero)
            elif essai_actuel[0] >= MAX_ESSAIS - 1:
                canvas_fonction.itemconfig(message, text=f"Perdu ! le mot était : {mot_secret}")
                racine.after(2000,nouvelle_partie)
            essai_actuel[0] += 1
    afficher_sequence()

def tirage_numero() :
    global ismotus,I,J
    tirer_numero()       
    racine.after(3500,verifier_motus)
def second_tirage() :
    global ismotus,I,J
    tirer_numero()       
    racine.after(3500,verifier_motus)
    
def tirer_numero():    
    global jarre,score,numero_grille    
    jouer_mp3("motus/motus-remuer-boule.mp3")
    random.shuffle(jarre)        
    boule_tire=jarre.pop(0)          
    if boule_tire==100 :
        affichage_boule_tire=canvas_grille_numero.create_oval(70, 220, 150, 300, fill= "black")
        score+=PENALITE_NOIRE
        canvas_fonction.itemconfig(compteur_score, text=f"Score : {score}") 
        pygame.mixer.music.load("motus/motus-boule-noire.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()
        canvas_grille_numero.after(3200, lambda: canvas_grille_numero.delete(affichage_boule_tire))
    else :
        affichage_tirage(canvas_grille_numero,numero_grille,boule_tire)            
                
def affichage_tirage(canvas_cible,numero_grille,boule_tire)  :          
    affichage_boule_tire=canvas_cible.create_oval(70, 220,150, 300, fill= "#cc9900")
    affichage_boule_tire_text=canvas_cible.create_text(110, 260, text=boule_tire, font=("Arial", 20), fill="white",anchor='center')
    ajouter_grille_numero(canvas_cible,numero_grille,boule_tire)    
    canvas_cible.after(2800,lambda :(canvas_cible.delete(affichage_boule_tire),canvas_cible.delete(affichage_boule_tire_text)))

def ajouter_grille_numero(canvas_cible,numero_grille,boule_tire) :
    global matrice_grille,I,J
    x0,y0,taille = 10, 10, 40
    index_numero= numero_grille.index(boule_tire)
    i = index_numero // 5
    j = index_numero % 5
    matrice_grille[i][j]=100
    I=i
    J=j
    print(matrice_grille)
    ovale=canvas_cible.create_oval(x0 + j * taille + 3, y0 + i * taille + 3, x0 + (j + 1) * taille - 3, y0 + (i + 1) * taille - 3, fill= "red", outline="")
    #ovale_text=canvas_cible.create_text(x0 + j * taille + taille // 2, y0 + i * taille + taille // 2, text=str(boule_tire), font=("Arial", 12),fill='black') 
    pygame.mixer.music.load("motus/affichage_numero.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    canvas_cible.after(2000,lambda :(canvas_cible.delete(ovale),
                                     canvas_cible.create_oval(x0 + j * taille + 3, y0 + i * taille + 3, x0 + (j + 1) * taille - 3, y0 + (i + 1) * taille - 3, fill= "#cc9900", outline=""),
                                     canvas_cible.create_text(x0 + j * taille + taille // 2, y0 + i * taille + taille // 2, text=str(boule_tire), font=("Arial", 12),fill='black')))

def nouvelle_grille() :
    global matrice_grille,compteur_grille_numero,numero_grille,numero_valide,jarre
    canvas_grille_numero.delete(all)
    compteur_grille_numero+=1
    numero_grille,numero_valide,jarre,matrice_grille = preparer_grille_numero(compteur_grille_numero)    
    dessiner_grille_numero(canvas_grille_numero,numero_grille,numero_valide)
    nouvelle_partie()

def verifier_motus():
    global matrice_grille, score, compteur_grille_numero, ismotus, I, J,tirage,message_motus
    compteur_ligne,compteur_diagonale_1,compteur_diagonale_2,compteur_colonne = 0, 0, 0, 0
    tirage+=1
    i=I
    j=J
    dj1,dj2 = 0, 4
    liste_motus=[]
    nb_motus = 0
    for k in range(0,5):
        if matrice_grille[i][k] == 100 : compteur_ligne+=1            
        if matrice_grille[k][j] == 100 : compteur_colonne+=1
        if matrice_grille[k][dj1] == 100 : compteur_diagonale_1+=1
        if matrice_grille[k][dj2] == 100 : compteur_diagonale_2+=1
        dj1+=1
        dj2-=1  
    if compteur_ligne == 5 or compteur_colonne == 5 or compteur_diagonale_1 == 5 or compteur_diagonale_2 == 5  :               
        if compteur_ligne == 5 : 
            liste_motus.extend([(i,0),(i,1),(i,2),(i,3),(i,4)])
            nb_motus+=1
        if compteur_colonne == 5 : 
            liste_motus.extend([(0,j),(1,j),(2,j),(3,j),(4,j)])
            nb_motus+=1
        if compteur_diagonale_1 == 5 :
            liste_motus.extend([(0,0),(1,1),(2,2),(3,3),(4,4)])
            nb_motus+=1
        if compteur_diagonale_2 == 5 :
            liste_motus.extend([(0,4),(1,3),(2,2),(3,1),(4,0)])
            nb_motus+=1
        x0, y0, taille = 10, 10, 40
        for case in liste_motus :
            canvas_grille_numero.create_rectangle(x0 + case[1] * taille, y0 + case[0] * taille, x0 + (case[1]+1) * taille, y0 + (case[0]+1) * taille, fill="red")
        message_motus = canvas_grille_numero.create_text(110, 260, text="*** MOTUS ***", font=("Arial", 20), fill="red",anchor='center') 
        score+=nb_motus*100
        canvas_fonction.itemconfig(compteur_score, text=f"Score : {score}")
        ismotus=True
        racine.after(2800,nouvelle_grille)
    else : 
        if tirage == 1 : second_tirage()
        else : nouvelle_partie()

def dessiner_case_rectangle(canvas_cible,col, ligne, lettre, couleur):
    dx=2
    dy=2
    x, y = cases_positions[ligne * TAILLE + col]  # Récupérer la position exacte
    canvas_cible.create_rectangle(x+dx, y+dy, x - dx + 155//2, y - dy + 153//2, fill=couleur, outline="")
    canvas_cible.create_text(x + 77//2, y + 76//2, text=lettre, font=("Arial", 24), fill="white")

def dessiner_case_cercle(canvas_cible,col,ligne,lettre,couleur):
    dx=4
    dy=4
    x, y = cases_positions[ligne * TAILLE + col]
    canvas_cible.create_oval(x+dx, y+dy, x-dx + 155//2, y-dy + 153//2, fill= "#cc9900", outline="")
    canvas_cible.create_text(x + 77//2, y + 76//2, text=lettre, font=("Arial", 24), fill= "white" )

def dessiner_grille_numero(canvas_cible,numero_grille,numero_valide):
    x0 = 10
    y0 = 10
    taille = 80//2
    for i in range(5):
        for j in range(5):
            index = i * 5 + j
            numero = numero_grille[index]
            #rempli = matrix_grille[i][j] != 0 or numero in numero_valide
            canvas_cible.create_rectangle(x0 + j * taille, y0 + i * taille, x0 + (j + 1) * taille, y0 + (i + 1) * taille, fill="#92D8FB", outline="white")
            if numero in numero_valide:
                canvas_cible.create_oval(x0 + j * taille + 3, y0 + i * taille + 3, x0 + (j + 1) * taille - 3, y0 + (i + 1) * taille - 3, fill= "#cc9900", outline="")
                canvas_cible.create_text(x0 + j * taille + taille // 2, y0 + i * taille + taille // 2, text=str(numero), font=("Arial", 12),fill='black')
            else : canvas_cible.create_text(x0 + j * taille + taille // 2, y0 + i * taille + taille // 2, text=str(numero), font=("Arial", 12),fill='black')

########################################    Initialisation   ################################################
# Paramètres du jeu
TAILLE = 6  # Nombre de lettres par mot
MAX_ESSAIS = 6  # Nombre d'essais maximum
SCORE_PAR_MOT =50
PENALITE_NOIRE= -20
MOTUS=100
I=0
J=0
# Charger les coordonnées des cases détectées
cases_positions_1024 = [
    (17, 12), (182, 13), (348, 13), (514, 13), (679, 12), (844, 13),
    (17, 179), (182, 180), (348, 180), (514, 180), (679, 179), (844, 180),
    (17, 345), (182, 346), (348, 346), (514, 346), (679, 345), (844, 346),
    (17, 512), (182, 513), (348, 513), (514, 513), (679, 512), (844, 513),
    (17, 678), (182, 679), (348, 679), (514, 679), (679, 678), (844, 679),
    (17, 839), (182, 840), (348, 840), (514, 840), (679, 839), (844, 840)]
cases_positions=[]
for item in cases_positions_1024 :
    cases_positions.append((item[0]//2,item[1]//2))

compteur_grille_numero = 1
numero_grille,numero_valide,jarre,matrice_grille = preparer_grille_numero(compteur_grille_numero)
print(matrice_grille)
mots_possibles = charger_mots(TAILLE)
mot_secret = random.choice(mots_possibles)
mots_trouves = 0
score= 0
ismotus=True
tirage=0
print(f"[DEBUG] Mot secret : {mot_secret}")
#####################################   Interface graphique  ##################################################
racine = tk.Tk()
racine.geometry("800x550")
racine.title("Motus")
image_fond = Image.open("motus/motus_grille_4.png")
image_fond = image_fond.resize((512, 512), Image.Resampling.LANCZOS)
image_fond_tk = ImageTk.PhotoImage(image_fond)
canvas = tk.Canvas(racine, width=512, height=512,bd=2,relief="raised")
canvas.create_image(0, 0, anchor='nw', image=image_fond_tk)
canvas.place(x=10,y=10)
canvas_grille_numero= tk.Canvas(racine,width=220,height=320,bd=2,relief="raised")
canvas_grille_numero.place(x=540,y=10)
canvas_fonction= tk.Canvas(racine, width=220, height=180,bd=2,relief="raised")
canvas_fonction.place(x=540,y=340)
entree = tk.Entry(canvas_fonction, width=18, font=("Arial", 14))
entree.place(x=10,y=40,anchor='nw')
entree.bind("<Return>",verifier_tentative)
message_invitation=canvas_fonction.create_text(15,24,text="Entrez votre mot ici :", fill="black", font=("Arial", 11),anchor='w')
message = canvas_fonction.create_text(110, 170, text="", fill="blue", font=("Arial", 14), anchor='center')
compteur_mots = canvas_fonction.create_text(30, 90, anchor='nw', text="Mots trouvés : 0", fill="green", font=("Arial", 14))
compteur_score = canvas_fonction.create_text(30, 120, anchor='nw', text="Score : 0", fill="red", font=("Arial", 14))
essai_actuel = [0]
dessiner_case_rectangle(canvas,0,0,mot_secret[0],couleur="")
dessiner_grille_numero(canvas_grille_numero,numero_grille,numero_valide)
liste_rouge=[mot_secret[0],"","","","",""]
liste_bonne_lettre=[]
racine.mainloop()
