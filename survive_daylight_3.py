import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,Toplevel
from PIL import Image, ImageTk, ImageDraw
import random
import time

class Plateau(tk.Tk):
    def __init__(self,game):
        super().__init__() # on hérite des attributs de la classe jeu 
        self.game=game #instanciation de la classe jeu pour les échanges entres classes
        self.geometry("1600x900") 
        self.bouton_choisi=None 
        self.save_image_tk=None  
        self.carte_tire_afficher_image=None
        self.image_objet_tk_dict={} #dictionnaire pour sauvegarder les image tk de tous les objet de pioche_objet avec les clés "nom" de l'objet
        self.image_perso_tk_dict={}
        self.image_errant_tk_dict={}
        self.image_pillard_tk_dict={}
        self.image_brute_tk_dict={}
        self.image_monstre_tk_dict={}
        self.image_survivant_tk_dict={}
        self.image_tk_save=[]
        self.lance_crafte=0
        self.barricade_crafte=0
        self.grenade_crafte=0
        self.piege_crafte=0
        #appels aux methodes préparatoire au jeux :     
        self.preparer_personnage()        
        self.preparer_image_objet()
        self.preparer_image_ennemi()
        self.preparer_fenetre()                          
        
    def preparer_personnage(self):
        """charge les images de la carte perso, de son arme unique, de ses pouvoirs et de l'arme de base choisie par le joueur """
        dic_arme_perso={'clepto':"fourche_clepto",'gachette':"pistolet_gachette",'pilier':"batte_pilier",'psycho':"couteau_psycho",
                        'hipster':"arc_hipster",'hogler':"revolver_hogler"}
        dic_pouvoir_perso={'clepto':("piocher une carte de la défausse à la fin du tour","défausser un objet pour prendre une carte mod supplémentaire"),
                           'gachette':("répartissez les dégâts d'une attaque au pistolet entre la cible et ses voisins","recevez une munition de la défausse à la fin de la phase de combat"),
                           'pilier':("1 fois par combat echanger la position de deux ennemis",""),
                           'psycho':("chaque attaque inflige aussi un dégat aux cibles adjacentes","vous pouvez a chaque attaque prendre un dégat pour doubler vos dégat"),
                           'hipster':("+ 1 carte mod par combat","1 fois par combat si vous tuez avec votre arc, gagner une attaque supplémentaire"),
                           'hogler':("fabriquer pour 1 ingrédient et un déchet (1x par tour)","fabriquer un objet ne consomme pas votre action du tour")}
        chaine_perso=f"daylight/{self.game.perso}.png" 
        chaine_arme_perso = f"daylight/{dic_arme_perso[self.game.perso]}.png"
        chaine_arme_base = f"daylight/{self.game.arme['nom']}.png" 
        self.image_perso = Image.open(chaine_perso).resize((228,350))
        self.image_arme = Image.open(chaine_arme_perso).resize((105,180))
        self.image_perso_tk = ImageTk.PhotoImage(self.image_perso)
        self.image_arme_tk= ImageTk.PhotoImage(self.image_arme)
        self.image_gun= Image.open(chaine_arme_base).resize((105,180))
        self.image_gun_tk = ImageTk.PhotoImage(self.image_gun)           
        self.text_pouvoir1=dic_pouvoir_perso[self.game.perso][0]
        self.text_pouvoir2=dic_pouvoir_perso[self.game.perso][1]

    def preparer_image_objet(self): 
        """charge toutes les images des objets de pioche_objet" et les auvergardes dans le dictionnaire : self.image_objet_tk_dic"""      
        for item in self.game.pioche_objet :            
            chemin=f"daylight/{item['nom']}.png"
            try :
                image_objet = Image.open(chemin).resize((105,180))                
                image_objet_tk = ImageTk.PhotoImage(image_objet)
                self.image_objet_tk_dict[item["nom"]] = image_objet_tk
                #item["photo"]=image_objet_tk                   
            except FileNotFoundError :
                print(f"⚠️ Image non trouvée : {chemin}") 
        #ajout de l'image vague
        image_vague = Image.open(r"daylight/vague.png").resize((105,180))                
        image_vague_tk = ImageTk.PhotoImage(image_vague)
        self.image_objet_tk_dict["vague"]=image_vague_tk         

    def preparer_image_ennemi(self):
        for k in range (1,4):
            str_survivant=f"daylight/survivant-{k}.png"
            str_errant=f"daylight/errant-{k}.png"
            str_pillard=f"daylight/pillard-{k}.png"
            str_brute=f"daylight/brute-{k}.png"
            str_monstre=f"daylight/monstre-{k}.png"
            try :
                image_survivant=Image.open(str_survivant).resize((180,340))
                image_errant=Image.open(str_errant).resize((180,340))
                image_pillard=Image.open(str_pillard).resize((180,340))
                image_brute=Image.open(str_brute).resize((180,340))
                image_monstre=Image.open(str_monstre).resize((180,340))
                image_survivant_tk=ImageTk.PhotoImage(image_survivant)
                image_errant_tk=ImageTk.PhotoImage(image_errant)
                image_pillard_tk=ImageTk.PhotoImage(image_pillard)
                image_brute_tk=ImageTk.PhotoImage(image_brute)
                image_monstre_tk=ImageTk.PhotoImage(image_monstre)
                str_k=str(k)
                self.image_survivant_tk_dict[str_k]=image_survivant_tk
                self.image_errant_tk_dict[str_k]=image_errant_tk
                self.image_pillard_tk_dict[str_k]=image_pillard_tk
                self.image_brute_tk_dict[str_k]=image_brute_tk
                self.image_monstre_tk_dict[str_k]=image_monstre_tk
            except FileNotFoundError :
                print("image non trouvée")
        image_brute_4=Image.open(r"daylight/brute-4.png").resize((180,340))
        image_brute_4_tk=ImageTk.PhotoImage(image_brute_4)
        self.image_brute_tk_dict['4']=image_brute_4_tk           

    def preparer_fenetre(self):
        #canvas pour l'affichage de la fiche perso, des pouvoirs du perso, des points de vie, de l'arme unique du perso et de l'arme de base choisie par le joueur
        self.canvas = tk.Canvas(self, width=360, height=450,bd=2,relief="ridge")
        self.canvas.place(x=10, y=10,anchor='nw')          
        self.canvas.create_image(10,10, image=self.image_perso_tk, anchor='nw') 
        self.canvas.create_image(250,10, image=self.image_arme_tk, anchor='nw')
        self.canvas.create_image(250,210, image=self.image_gun_tk, anchor='nw')        
        self.message_pdv= self.canvas.create_text(60,370,text=f"points de vie : {self.game.pdv}",font=('Arial', 12, 'bold'), fill='red', anchor='w')
        self.canvas.create_text(15,415,text=f"1 : {self.text_pouvoir1}",font=('Arial', 8, 'bold'), fill='black', anchor='w')
        self.canvas.create_text(15,440,text=f"2 : {self.text_pouvoir2}",font=('Arial', 8, 'bold'), fill='black', anchor='w')
        #canvas pour l'affichage de l'inventaire
        self.canvas_inventaire=tk.Canvas(self, width=600, height=450,bd=2,relief="ridge")
        self.canvas_inventaire.place(x=380, y=10,anchor='nw') 
        #canvas pour la création des cartes tirés : objets du paquets, défausse et craft
        self.image_paquet= Image.open(r"daylight/image_paquet.png").resize((550,450))
        self.image_paquet_tk = ImageTk.PhotoImage(self.image_paquet) 
        self.canvas_paquet=tk.Canvas(self, width=550, height=450,bd=2,relief="ridge")
        self.canvas_paquet.place(x=1000,y=10,anchor='nw')
        self.image_paquet=self.canvas_paquet.create_image(0,0,anchor='nw',image=self.image_paquet_tk)
        self.image_tk_save.append(self.image_paquet_tk)
        #canvas pour afficher les cartes vagues :
        self.canvas_vagues=tk.Canvas(self,width=300,height=420,bd=2,relief="ridge")
        self.canvas_vagues.place(x=10,y=480,anchor='nw')
        self.canvas_vagues.create_text(10,15,text="Vagues d'ennemis",font=('Arial',16, 'bold'), fill='red', anchor='w')
        self.canvas_vagues.create_text(10,35,text="Eliminez les 6 vagues pour remporter la victoire",font=('Arial',8, 'bold'), fill='black', anchor='w')        
        #canvas pour les ennemis : 1 canvas pour le pool d'ennemis, 1 autre pour leur pdv
        self.canvas_ennemi=tk.Canvas(self,width=1200,height=420,bd=2,relief='ridge')
        self.canvas_ennemi.place(x=320,y=480,anchor='nw')
        self.canvas_pool_ennemi=tk.Canvas(self.canvas_ennemi,width=1200,height=355)
        self.canvas_pool_ennemi.place(x=0,y=0,anchor='nw')
        self.canvas_pdv_ennemi=tk.Canvas(self.canvas_ennemi,width=1200,height=25)
        self.canvas_pdv_ennemi.place(x=0,y=356,anchor='nw')

    def affichage_inventaire(self):  
        """affichage des cartes de l'inventaire """
        self.canvas_inventaire.delete('all')         
        for item in self.game.inventaire :
            print(item)            
            if item["objet"]!=None :                           
                self.canvas_inventaire.create_image(item["coord"][0],item["coord"][1],anchor='nw',image=self.image_objet_tk_dict[item["objet"]["nom"]])
                if item['stack']==2 :
                    self.canvas_inventaire.create_image(item["coord"][0]+3,item["coord"][1]+8,anchor='nw',image=self.image_objet_tk_dict[item["objet"]["nom"]])
                if item['stack']==3 :
                    self.canvas_inventaire.create_image(item["coord"][0]+3,item["coord"][1]+8,anchor='nw',image=self.image_objet_tk_dict[item["objet"]["nom"]])
                    self.canvas_inventaire.create_image(item["coord"][0]+6,item["coord"][1]+16,anchor='nw',image=self.image_objet_tk_dict[item["objet"]["nom"]])       

    def affichage_carte_paquet(self) : 
        """affichage de la carte tiré du paquet"""
        if self.carte_tire_afficher_image!=None :
            self.canvas_paquet.delete(self.carte_tire_afficher_image)
        print("methode affichage carte tire : ",self.game.carte_tire)        
        self.carte_tire_afficher_image=self.canvas_paquet.create_image(120,30, image=self.image_objet_tk_dict[self.game.carte_tire["nom"]], anchor='nw')
    
    def mettre_carte_defausse(self,carte):        
        if self.game.defausse!=[] :
            self.canvas_paquet.delete(self.carte_dessus_defausse)
        self.carte_dessus_defausse=self.canvas_paquet.create_image(419,30,anchor="nw",image=self.image_objet_tk_dict[carte["nom"]])

    def garder_carte(self) :
        """méthode qui génére les boutons prendre et défausser lorsqu'une carte du paquet est piochée """
        self.bouton_choisi_var = tk.StringVar()
        self.bouton_prendre_carte  = tk.Button(self.canvas_paquet, text="PRENDRE",font=('Arial', 10, 'bold'), fg='red',bg='yellow',command=lambda: self.bouton_appuye('prendre')) 
        self.bouton_prendre_carte.place(x=10, y=70,anchor='nw')
        self.bouton_defausser_carte  = tk.Button(self.canvas_paquet, text="DEFAUSSER",font=('Arial', 10, 'bold'), fg='red',bg='yellow',command=lambda: self.bouton_appuye("defausser")) 
        self.bouton_defausser_carte.place(x=10, y=130,anchor='nw')        
    
    def bouton_appuye(self,valeur): 
        """méthode qui recupere le bouton prendre ou défausser choisi par le joueur lorsqu'une carte 
        du paquet est tiré"""      
        self.bouton_choisi=valeur 
        self.bouton_choisi_var.set(valeur)
        self.bouton_prendre_carte.place_forget()
        self.bouton_defausser_carte.place_forget()
        self.canvas_paquet.delete(self.carte_tire_afficher_image) 
    
    def demander_choix(self,titre,message):
        return messagebox.askyesno(titre,message)                    
    
    def afficher_info(self,titre,message):
        messagebox.showinfo(titre, message)
    
    def defausser_objet(self) :
        def on_select(nom_objet):
            nonlocal objet_selectionne
            objet_selectionne = nom_objet
            fenetre_inv_defausser.destroy()
        fenetre_inv_defausser = Toplevel(self)
        fenetre_inv_defausser.title("Choisissez un objet à défausser")
        cadre = tk.Frame(fenetre_inv_defausser)
        cadre.pack(padx=10, pady=10)
        objet_selectionne = None
        for item in self.game.inventaire:
            if item["objet"]!=None :         
                bouton_defausser = tk.Button(cadre, image=self.image_objet_tk_dict[item["objet"]["nom"]], command=lambda o=item['objet']: on_select(o))
                bouton_defausser.image = self.image_objet_tk_dict[item["objet"]["nom"]]  # Conserver une référence à l'image pour éviter la suppression par le garbage collector
                bouton_defausser.pack(side="left", padx=5)
        fenetre_inv_defausser.wait_window()  # Attendre la fermeture de la boîte de dialogue
        return objet_selectionne
    
    def utiliser_objet(self):
        def toggle_selection(nom_objet, bouton):
            """Ajoute/enlève un objet de la sélection et met à jour l'apparence du bouton."""
            if nom_objet in objets_selectionnes:
                objets_selectionnes.remove(nom_objet)
                bouton.config(relief="raised")  # Visuellement désélectionné
            else:
                objets_selectionnes.add(nom_objet)
                bouton.config(relief="sunken")  # Visuellement sélectionné
        def valider_selection():
            fenetre_inv.destroy()
        fenetre_inv = Toplevel(self)
        fenetre_inv.title("Choisissez les objets à utiliser")
        cadre = tk.Frame(fenetre_inv)
        cadre.pack(padx=10, pady=10)
        objets_selectionnes = set()
        boutons = {}
        for item in self.game.inventaire:  
            if item["objet"]!=None and item["objet"]["effet"]!=None and item['objet']['type']!='munition':                 
                bouton = tk.Button(cadre, image=self.image_objet_tk_dict[item["objet"]["nom"]], relief="raised")
                bouton.image = self.image_objet_tk_dict[item["objet"]["nom"]]  # Éviter le garbage collector                
                def creer_callback(o,b):
                    return lambda : toggle_selection(o,b)
                bouton.config(command=creer_callback(item["objet"]['nom'],bouton))
                bouton.pack(side="left",padx=5,pady=5)
                boutons[item["objet"]["nom"]]=bouton
        # Bouton de validation
        btn_valider = tk.Button(fenetre_inv, text="Valider", command=valider_selection)
        btn_valider.pack(pady=10)
        fenetre_inv.wait_window()  # Attendre la fermeture de la boîte de dialogue
        liste_objet_selectionne=[]
        for item in self.game.inventaire :
            if item["objet"]!=None and item['objet']['nom'] in objets_selectionnes : liste_objet_selectionne.append(item['objet'])
        return liste_objet_selectionne 
    
    def designer_cible(self) :
        def on_select(ennemi):
            nonlocal ennemi_cible
            ennemi_cible = ennemi
            fenetre_cible.destroy()
        fenetre_cible = Toplevel(self)
        fenetre_cible.title("Sélection de la cible")
        cadre = tk.Frame(fenetre_cible)
        cadre.pack(padx=10, pady=10)
        ennemi_cible = None
        boutons_ennemi={}
        for item in self.game.pool_ennemi :
            print (item)
        for ennemi in self.game.pool_ennemi : 
            if ennemi['type']!='survivant' :          
                if ennemi["type"]=='errant' : image_pool=self.image_errant_tk_dict[str(ennemi["id"])]
                if ennemi["type"]=='pillard' : image_pool=self.image_pillard_tk_dict[str(ennemi["id"])]
                if ennemi["type"]=='brute' : image_pool=self.image_brute_tk_dict[str(ennemi["id"])]
                if ennemi["type"]=='monstre' : image_pool=self.image_monstre_tk_dict[str(ennemi["id"])] 
                if image_pool is None:  # Vérifier si l'image existe
                    print(f"⚠ Erreur : Image non trouvée pour {ennemi['type']} ID {ennemi['id']}")
                    continue  # Évite de planter le programme           
                bouton = tk.Button(cadre, image=image_pool, relief="raised")
                bouton.image = image_pool  # Éviter le garbage collector                
                def creer_callback(o):
                    return lambda : on_select(o)
                bouton.config(command=creer_callback(ennemi))
                bouton.pack(side="left",padx=5,pady=5)
                boutons_ennemi[ennemi['nom']]=bouton           
        fenetre_cible.wait_window()  # Attendre la fermeture de la boîte de dialogue
        return ennemi_cible
        

    def maj_pdv(self) :
        """methooe pour mettre à jour les pdv"""
        self.canvas.delete(self.message_pdv)
        self.message_pdv=self.canvas.create_text(60,370,text=f"points de vie : {self.game.pdv}",font=('Arial', 12, 'bold'), fill='red', anchor='w')  

    def maj_vague(self) :        
        x0=10
        y0=self.game.compteur_vague*60
        self.canvas_vagues.create_text(x0,y0,text=f"Vague : {self.game.compteur_vague}     {self.game.vague_tire["id"]}",font=('Arial', 10, 'bold'), fill='red', anchor='w')
        liste_vague=['survivant','errant','pillard','brute','monstre']
        compteur_ligne=1
        print(self.game.vague_tire)
        for k in range(0,5):
            if self.game.vague_tire["contenu"][k]!=0 :
                self.canvas_vagues.create_text(x0+20,y0+compteur_ligne*15,text=f"- {self.game.vague_tire["contenu"][k]} --> {liste_vague[k]}",font=('Arial', 9, 'bold'), fill='black', anchor='w')
                compteur_ligne+=1
    
    def afficher_bouton_craft(self): 
        """parcour la liste des objets craftable et creer des boutons les boutons renvois à la methode bouton_craft_appuye"""             
        for item in self.game.liste_craftable :
            if item=='lance':
                self.bouton_craft_lance  = tk.Button(self.canvas_paquet, text="CRAFTER",font=('Arial', 10, 'bold'), fg='red',bg='yellow',command=lambda: self.bouton_craft_appuye('lance')) 
                self.bouton_craft_lance.place(x=10, y=267,anchor='nw') 
                self.game.bouton_craft_cree.append('lance')               
            if item=='barricade':
                self.bouton_craft_barricade  = tk.Button(self.canvas_paquet, text="CRAFTER",font=('Arial', 10, 'bold'), fg='red',bg='yellow',command=lambda: self.bouton_craft_appuye('barricade')) 
                self.bouton_craft_barricade.place(x=10, y=315,anchor='nw')
                self.game.bouton_craft_cree.append('barricade')
            if item=='grenade':
                self.bouton_craft_grenade  = tk.Button(self.canvas_paquet, text="CRAFTER",font=('Arial', 10, 'bold'), fg='red',bg='yellow',command=lambda: self.bouton_craft_appuye('grenade')) 
                self.bouton_craft_grenade.place(x=10, y=362,anchor='nw')
                self.game.bouton_craft_cree.append('grenade')
            if item=='piege':
                self.bouton_craft_piege  = tk.Button(self.canvas_paquet, text="CRAFTER",font=('Arial', 10, 'bold'), fg='red',bg='yellow',command=lambda: self.bouton_craft_appuye('piege')) 
                self.bouton_craft_piege.place(x=10, y=267,anchor='nw')
                self.game.bouton_craft_cree.append('piege')
    
    def bouton_craft_appuye(self,valeur):  
        """lorsqu un bouton de craft est activé, on appelle la methode de la classe jeu : crafter_objet """      
        if valeur=='lance' : self.canvas_paquet.destroy(self.bouton_craft_lance)
        if valeur=='barricade' : self.canvas_paquet.destroy(self.bouton_craft_barricade)
        if valeur=='grenade' : self.canvas_paquet.destroy(self.bouton_craft_grenade)
        if valeur=='piege' : self.canvas_paquet.destroy(self.bouton_craft_piege)
        self.game.crafter(valeur)
    
    def supprimer_bouton_craft(self,valeur) :
        """méthode activée pour supprimer un bouton de craft déjà crée. si par exemple on a plus assez d'objet pour le fabriquer  """
        if valeur=='lance' : self.canvas_paquet.destroy(self.bouton_craft_lance)
        if valeur=='barricade' : self.canvas_paquet.destroy(self.bouton_craft_barricade)
        if valeur=='grenade' : self.canvas_paquet.destroy(self.bouton_craft_grenade)
        if valeur=='piege' : self.canvas_paquet.destroy(self.bouton_craft_piege)
    
    def selection_craft(self):        
        def on_select(objet):
            nonlocal objet_craft
            objet_craft = objet
            fenetre_craft.destroy()
        fenetre_craft = Toplevel(self)
        fenetre_craft.title("Sélection de l'objet à crafter")
        cadre = tk.Frame(fenetre_craft)
        cadre.pack(padx=10, pady=10)
        objet_craft = None
        boutons_craft={}
        for item in self.game.liste_craftable :                       
            bouton = tk.Button(cadre, text=item,font=('Arial', 10, 'bold'), fg='red',bg='yellow', relief="raised")                          
            def creer_callback(o):
                 return lambda : on_select(o)
            bouton.config(command=creer_callback(item))
            bouton.pack(side="left",padx=5,pady=5)
            boutons_craft[item]=bouton           
        fenetre_craft.wait_window()  # Attendre la fermeture de la boîte de dialogue
        return objet_craft

    def bouton_utiliser_craft(self,valeur):
        if valeur=='lance' : 
            self.canvas_paquet.destroy(self.bouton_utiliser_lance)
            self.lance_crafte-=1
        if valeur=='barricade' : 
            self.canvas_paquet.destroy(self.bouton_utiliser_barricade)
            self.barricade_crafte-=1
        if valeur=='grenade' : 
            self.canvas_paquet.destroy(self.bouton_utiliser_grenade)
            self.grenade_crafte-=1
        if valeur=='piege' : 
            self.canvas_paquet.destroy(self.bouton_utiliser_piege)
            self.piege_crafte-=1
        self.game.utiliser_craft(valeur)

    def affichage_pool_ennemi(self) :
        self.canvas_pool_ennemi.delete('all')
        x0,y0=10,10    
        for k in range(len(self.game.pool_ennemi)) :
            if self.game.pool_ennemi[k]["type"]=="survivant":
                self.canvas_pool_ennemi.create_image(x0+k*200,y0,anchor='nw',image=self.image_survivant_tk_dict[str(self.game.pool_ennemi[k]["id"])])
            if self.game.pool_ennemi[k]["type"]=="errant":
                self.canvas_pool_ennemi.create_image(x0+k*200,y0,anchor='nw',image=self.image_errant_tk_dict[str(self.game.pool_ennemi[k]["id"])])
            if self.game.pool_ennemi[k]["type"]=="pillard":
                self.canvas_pool_ennemi.create_image(x0+k*200,y0,anchor='nw',image=self.image_pillard_tk_dict[str(self.game.pool_ennemi[k]["id"])])
            if self.game.pool_ennemi[k]["type"]=="brute":
                self.canvas_pool_ennemi.create_image(x0+k*200,y0,anchor='nw',image=self.image_brute_tk_dict[str(self.game.pool_ennemi[k]["id"])])
            if self.game.pool_ennemi[k]["type"]=="monstre":
                self.canvas_pool_ennemi.create_image(x0+k*200,y0,anchor='nw',image=self.image_monstre_tk_dict[str(self.game.pool_ennemi[k]["id"])])        
    
    def affichage_pdv_ennemi(self) : 
        self.canvas_pdv_ennemi.delete('all')
        x0=10    
        for k in range(len(self.game.pool_ennemi)) : 
            self.canvas_pdv_ennemi.create_text(x0+k*200+40,0,text=f"pdv restants : {self.game.pool_ennemi[k]["carac"][0]}",font=('Arial', 12, 'bold'), fill='red', anchor='nw')
        for item in self.game.pool_ennemi :
            print(item)

class Jeu :
    def __init__(self,perso,arme,pioche_mod,pioche_objet): #les paramètres son ceux défini dans le main
        self.plateau=None
        self.perso=perso
        self.arme=arme
        self.pioche_mod=pioche_mod
        self.pioche_objet=pioche_objet                    
        self.pouvoir_1=False
        self.pouvoir_2=False
        self.defausse=[]
        self.nb_objet=0       
        self.isstackable=False 
        self.compteur_vague=0 
        self.objet_crafte=[]
        self.liste_craftable=[]
        self.bouton_craft_cree=[] 
        self.pioche_errant=[] 
        self.pioche_pillard=[] 
        self.pioche_brute=[] 
        self.pioche_monstre=[] 
        self.pioche_survivant=[] 
        self.pool_ennemi=[] 
        
        self.caracteristique_perso()  
        #l'inventaire ets une liste de 8 dictionnaires d'emplacement  donc la clé "objet" est un dictionnaire des objets stockées depuis la pioche_objet      
        self.inventaire=[{"emplacement":1,"coord":(0,0,105,180),"objet":None,"stack":1},
                         {"emplacement":2,"coord":(125,0,230,180),"objet":None,"stack":1},
                         {"emplacement":3,"coord":(250,0,355,180),"objet":None,"stack":1},
                         {"emplacement":4,"coord":(375,0,480,180),"objet":None,"stack":1},
                         {"emplacement":5,"coord":(0,200,105,380),"objet":None,"stack":1},
                         {"emplacement":6,"coord":(125,200,230,380),"objet":None,"stack":1},
                         {"emplacement":7,"coord":(250,200,355,380),"objet":None,"stack":1},
                         {"emplacement":8,"coord":(375,200,480,380),"objet":None,"stack":1}]         

    def set_plateau(self, plateau):
        """Lier le plateau au jeu. on le lie après le constructeur car on a un liage croisé"""
        self.plateau = plateau
        self.start()              

    def caracteristique_perso(self):
        """méthode qui défini les pdv et l'arme unique du perso"""
        if self.perso=='clepto' :            
            self.pdv=8
            self.arme_perso={"nom":"fourche","pa":2,"mod":1,"condition":None}
        if self.perso=='gachette' :            
            self.pdv=7
            self.arme_perso={"nom":"pistolet","pa":3,"mod":1,"condition":"munitions"}
        if self.perso=='pilier' : 
            self.pdv=10
            self.arme_perso={"nom":"batte","pa":2,"mod":1,"condition":None}
        if self.perso=='psycho' :
            self.pdv=10
            self.arme_perso={"nom":"couteau","pa":2,"mod":1,"condition":None}
        if self.perso=='hipster' :
            self.pdv=7
            self.arme_perso={"nom":"arc","pa":3,"mod":1,"condition":"flèches"}
        if self.perso=='hogler' :
            self.pdv=8
            self.arme_perso={"nom":"revolver","pa":2,"mod":1,"condition":"munitions"} 

    def start(self) : 
        """méthode démarrage du jeu"""
        self.preparer_vague()
        self.preparer_paquet()
        self.preparer_ennemi()
        for i in self.paquet:
            print(i)
        self.phase_loot()

    def preparer_vague(self) :
        """méthode qui prépare et mélange les 6 cartes de vague """
        #contenu de la vague sous la forme de tuples : (survivant,errants,pillards,brute,montres)
        self.pioche_vague=[{"id":"rapaces","contenu":(1,0,2,0,0)},
               {"id":"nuée","contenu":(1,2,0,0,0)},
               {"id":"avant-garde","contenu":(1,1,1,0,0)},
               {"id":"brutal","contenu":(1,1,0,1,0)},
               {"id":"abusif","contenu":(1,0,1,1,0)},
               {"id":"carnage","contenu":(1,0,0,0,1)}]
        random.shuffle(self.pioche_vague)    
    
    def preparer_paquet(self):
        """méthode qui pépare le paquet de loot de 7 cartes dont la carte vague"""
        self.paquet=[]        
        for i in range (6) :
            self.paquet.append(self.pioche_objet.pop(0))
        self.paquet.append({"nom":"vague","type":"monstre","effet":None,"stackable":0})
        random.shuffle(self.paquet)   

    def preparer_ennemi(self):
        """méthode qui prépare les paquets ennemis"""
        #caractéristique des ennemis sous la forme d'un tuple (pdv,dégat,mod,vol,defonce_barricade,renforcement)
        survivant=[{'nom':'s1','type':"survivant",'id':1,'carac':(1,0,0,0,0,0)},
                   {'nom':'s2','type':"survivant",'id':2,'carac':(1,0,0,0,0,0)},
                   {'nom':'s3','type':"survivant",'id':3,'carac':(1,0,0,0,0,0)}]
        errant=[{'nom':'e1','type':'errant','id':1,'carac':(2,2,0,0,0,0)},
                {'nom':'e2','type':'errant','id':2,'carac':(2,1,1,0,0,0)},
                {'nom':'e3','type':'errant','id':3,'carac':(2,0,2,0,0,0)}]
        pillard=[{'nom':'p1','type':'pillard','id':1,'carac':(3,0,2,1,0,0)},
                {'nom':'p2','type':'pillard','id':2,'carac':(3,2,0,1,0,0)},
                {'nom':'p3','type':'pillard','id':3,'carac':(3,1,1,1,0,0)}]
        brute=[{'nom':'b1','type':'brute','id':1,'carac':(4,0,3,0,1,0)},
                {'nom':'b2','type':'brute','id':2,'carac':(4,1,2,0,1,0)},
                {'nom':'b3','type':'brute','id':3,'carac':(4,2,1,0,1,0)},
                {'nom':'b4','type':'brute','id':4,'carac':(4,3,0,0,1,0)}]
        monstre=[{'nom':'m1','type':'monstre','id':1,'carac':(7,2,3,0,0,1)},
                {'nom':'m2','type':'monstre','id':2,'carac':(7,3,2,0,0,1)},
                {'nom':'m3','type':'monstre','id':3,'carac':(7,4,1,0,0,1)}]
        #pour chaque type d'ennemis on ajoute 4 cartes à la pioche de ces ennemis
        for k in range (0,3):
            for _ in range (0,4):
                self.pioche_survivant.append(survivant[k])
                self.pioche_errant.append(errant[k])
                self.pioche_pillard.append(pillard[k])
                self.pioche_brute.append(brute[k])
                self.pioche_monstre.append(monstre[k])                
        for _ in range(0,4):
            self.pioche_brute.append(brute[3])
        random.shuffle(self.pioche_survivant)
        random.shuffle(self.pioche_errant)
        random.shuffle(self.pioche_pillard)
        random.shuffle(self.pioche_brute)
        random.shuffle(self.pioche_monstre)
    
    def vol_objet(self):
        """méthode qui choisit un objet et le retire de l'inventaire pour simuler un vol. L'inventaire ets reclassé pour qu'il n'y ai pas de trous.
          Si l'objet volé ets dans un stack, on décrémente simplement le stack"""                    
        emplacement_vole=random.randint(0,self.nb_objet-1)  
        self.plateau.mettre_carte_defausse(self.inventaire[emplacement_vole]["objet"]) 
        self.defausse.append(self.inventaire[emplacement_vole]["objet"])       
        if self.inventaire[emplacement_vole]["stack"]>1 : self.inventaire[emplacement_vole]["stack"]-=1                     
        else :               
            if emplacement_vole==self.nb_objet-1 :                
                self.inventaire[emplacement_vole]["objet"]=None
            else : 
                for k in range(emplacement_vole,self.nb_objet-1) :
                    self.inventaire[k]["objet"]=self.inventaire[k+1]["objet"]
                self.inventaire[self.nb_objet-1]["objet"]=None
            self.nb_objet-=1
        self.plateau.affichage_inventaire()            

    def defausser_objet_inventaire(self):
        objet_defausse=self.plateau.defausser_objet()        
        self.plateau.mettre_carte_defausse(objet_defausse)
        self.defausse.append(objet_defausse)
        for k in range (len(self.inventaire)) :
            if self.inventaire[k]["objet"]!=None and self.inventaire[k]["objet"]['nom']==objet_defausse['nom']: emplacement=k
        if self.inventaire[emplacement]["stack"]>1 : self.inventaire[emplacement]["stack"]-=1
        else :               
            if emplacement==self.nb_objet-1 :                
                self.inventaire[emplacement]["objet"]=None
            else : 
                for k in range(emplacement,self.nb_objet-1) :
                    self.inventaire[k]["objet"]=self.inventaire[k+1]["objet"]
                self.inventaire[self.nb_objet-1]["objet"]=None
            self.nb_objet-=1
        self.plateau.affichage_inventaire()
    
    def verifier_craft(self):
        """verifie si l'inventaire permet de crafter des objets"""        
        self.liste_craftable=[]
        liste_craft=[]
        #on récupère dans liste_craft tous les objets craftables de l'inventaire       
        for item in self.inventaire :
            if item["objet"]['type']=="craft":
                liste_craft.append(item["objet"]['nom'])              
        #on regarde les objet craftables à partir de liste_craft et on les stockent dans self.liste_craftable
        if 'planches' in liste_craft and 'clous' in liste_craft : self.liste_craftable.append("barricade")              
        if 'planches' in liste_craft and 'fragments' in liste_craft : self.liste_craftable.append("lance")               
        if 'explosifs' in liste_craft and 'clous' in liste_craft : self.liste_craftable.append("grenade")          
        if 'explosifs' in liste_craft and 'câbles' in liste_craft : self.liste_craftable.append("piege")
        if self.liste_craftable==[] :
            self.plateau.afficher.info("Fabrications d'objets","Désolé, vous ne pouvez rien fabriquer...")
        else : self.crafter_objet()   
            
    def crafter_objet(self) : 
        dict_craft={'lance':("planches","fragments"),'barricade':("planches","clous"),'grenade':("explosifs","clous"),
                    'piege':("explosifs","câbles")}         
        objet_crafte=self.plateau.selection_craft()
        self.nb_craft-=1
        for item in self.inventaire : 
            if item["objet"]!=None :
                if item["objet"]["nom"]==dict_craft[objet_crafte][0] or item["objet"]["nom"]==dict_craft[objet_crafte][1]:
                    if item["stack"]>1 :
                        item["stack"]-=1  
                        self.plateau.mettre_carte_defausse(item["objet"])
                        self.defausse.append[item]
                    else : 
                        self.plateau.mettre_carte_defausse(item["objet"])
                        self.defausse.append[item]
                        self.nb_objet-=1                
                        temp_inv=[]            
                        for item in self.inventaire :
                            if item['objet']!=None : temp_inv.append(item["objet"])                         
                        for k in range(len(self.inventaire)):
                            if k<=len(temp_inv)-1 : self.inventaire[k]["objet"]=temp_inv[k]
                            else : self.inventaire[k]["objet"]=None                   
                    self.plateau.affichage_inventaire()
        
                
    def utiliser_craft(self):
        pass

    
    
    def phase_loot(self):
        """première phase du jeu : le loot """
        self.isloot=True        
        while self.isloot :
            self.isstackable=False
            self.carte_tire=self.paquet.pop(0)
            self.plateau.affichage_carte_paquet()        
            #verif des cartes spéciales : vague, rat, corbeau, fracture
            if self.carte_tire["nom"] =="vague":
                reponse =self.plateau.demander_choix("La vague arrive...","Voulez-vous sacrifier un Pdv pour continuer la phase de loot ?")                
                if reponse :
                    self.pdv-=1
                    self.plateau.maj_pdv()
                    self.paquet.append({"nom":"vague","type":"monstre","effet":None,"stackable":0})
                    random.shuffle(self.paquet)                    
                else :                     
                    print("phase préparation combat")
                    break
            elif self.carte_tire["nom"] =="attaque de rat":
                self.plateau.afficher_info("Attaque de rat !!!","Ca grouille, ça couine... et ça mort ! Vous perdez un point de vie")
                self.pdv-=1
                self.plateau.maj_pdv()
                
            elif self.carte_tire["nom"] =="fracture":
                self.plateau.afficher_info("Fracture !!!","Ouh que ça fait mal ! Vous perdez deux points de vie")
                self.pdv-=2
                self.plateau.maj_pdv()                
            
            elif self.carte_tire["nom"] =="attaque de corbeau":
                self.plateau.afficher_info("Attaque de corbeau !!!","Ceux-la ne se contentent pas de picorer... vous perdez un objet !")
                if self.nb_objet!=0 :
                    self.vol_objet()          
            #tous les autres cas
            else :
                self.plateau.garder_carte()
                self.plateau.wait_variable(self.plateau.bouton_choisi_var) #suspend le promgramme en attendant que le joueur appuye sur un bouton 
                print(self.plateau.bouton_choisi)
                #si le bouton choisi est "prendre"
                if self.plateau.bouton_choisi=="prendre" :
                    #si la carte la carte est stackable
                    if self.carte_tire["stackable"]==1 and self.nb_objet>0:
                        print("carte stackable")
                        #on vérifie que la carte tiré stackable est présente ou non dans l'inventaire
                        self.objet_a_stacker=None
                        for item in self.inventaire :
                            #si c'est le cas :
                            if item["objet"]!=None and item["objet"]["nom"]==self.carte_tire["nom"]: 
                                self.isstackable=True
                                item["stack"]+=1 
                                self.objet_a_stacker=item["objet"]['nom']
                        #si ce n'est pas le cas  
                        if self.objet_a_stacker==None : 
                            #si il y a de la place dans l'inventaire (procédure normale)
                            if self.nb_objet<8 :
                                print("assez de place dans l'inventaire")               
                                self.nb_objet+=1                    
                                self.inventaire[self.nb_objet-1]["objet"]=self.carte_tire
                            if self.nb_objet==8 :
                                print("pas assez de place dans l'inventaire") 
                                self.defausser_objet_inventaire()
                    #si il y a assez d'emplacement dans l'inventaire"       
                    elif self.nb_objet<8 : 
                        print("assez de place dans l'inventaire")               
                        self.nb_objet+=1                    
                        self.inventaire[self.nb_objet-1]["objet"]=self.carte_tire
                    #si il n'y a pas assez d'emplacement dans l'inventaire" 
                    elif self.nb_objet==8 :
                        print("pas assez de place dans l'inventaire")
                        """self.plateau.canvas_inventaire.bind("<Button-1>",self.plateau.clic_carte_inventaire)
                        self.defausse.append(self.inventaire[self.zone_clic-1])
                        self.inventaire[self.zone_clic-1]["objet"]=self.carte_tire"""
                        self.defausser_objet_inventaire()                        
                #si le bouton choisi est "défausser"  
                else :                  
                    self.plateau.mettre_carte_defausse(self.carte_tire)  
                    self.defausse.append(self.carte_tire)             
                self.plateau.affichage_inventaire() 
        self.phase_preparatoire_combat()

    def phase_preparatoire_combat(self):
        self.degat=0
        self.mod_combat=0
        self.nb_attaque=0
        self.nb_craft=0 
        self.degat_collateraux=False
        self.degat_libre=False
        #tirage de la carte vague
        if self.compteur_vague<6 :
            self.compteur_vague+=1
            self.vague_tire=self.pioche_vague.pop(0)        
            self.plateau.maj_vague()
        #tirage des ennemis
        temp_ennemi=[]                
        for k in range (0,5):
            if k==0 and self.vague_tire['contenu'][k]!=0 :
                for _ in range(0,self.vague_tire['contenu'][0]) :              
                    temp_ennemi.append(self.pioche_survivant.pop(0))
            if k==1 and self.vague_tire['contenu'][k]!=0:
                for _ in range(0,self.vague_tire['contenu'][1]) :               
                    temp_ennemi.append(self.pioche_errant.pop(0))
            if k==2 and self.vague_tire['contenu'][k]!=0:
                for _ in range(0,self.vague_tire['contenu'][2]) :               
                    temp_ennemi.append(self.pioche_pillard.pop(0))
            if k==3 and self.vague_tire['contenu'][k]!=0:
                for _ in range(0,self.vague_tire['contenu'][3]) :               
                    temp_ennemi.append(self.pioche_brute.pop(0))
            if k==4 and self.vague_tire['contenu'][k]!=0:
                for _ in range(0,self.vague_tire['contenu'][4]) :               
                    temp_ennemi.append(self.pioche_monstre.pop(0)) 
        random.shuffle(temp_ennemi) #on mélange les ennemis tirés         
        #ajout des ennemis au pool d'ennemis et affichage des ennemis       
        for item in temp_ennemi :
            self.pool_ennemi.append(item)           
        self.plateau.affichage_pool_ennemi()
        self.plateau.affichage_pdv_ennemi()      
        #utiliser les objets de l'inventaire
        self.plateau.afficher_info("préparer vous au combat !", "choissiez les objets que vous voulez utilisez...")
        liste_objet_utilise=self.plateau.utiliser_objet() 
        print(liste_objet_utilise) 
        if liste_objet_utilise!=[]:
            for item in liste_objet_utilise :            
                if item['effet'][0]!=0 : 
                    self.pdv+=item['effet'][0]
                    self.plateau.maj_pdv()
                if item['effet'][1]!=0 : self.nb_attaque+=item['effet'][1]
                if item['effet'][2]!=0 : self.nb_craft+=item['effet'][2]
                if item['effet'][3]!=0 : self.mod_combat+=item['effet'][3]
                if item['effet'][4]!=0 : self.degat_collateraux=True
                if item['effet'][5]!=0 : self.degat_libre=True                
                self.plateau.mettre_carte_defausse(item)
                self.defausse.append(item)
                for objet in self.inventaire :
                    if objet['objet']!=None :
                        if objet['objet']['nom']==item['nom'] and objet['stack']>1:
                            objet['stack']-=1                        
                        elif objet['objet']['nom']==item['nom'] :
                            objet['objet']=None
                            self.nb_objet-=1
            #réorganisation de l'inventaire
            temp_inv=[]            
            for item in self.inventaire :
                if item['objet']!=None : temp_inv.append(item["objet"])   
                      
            for k in range(len(self.inventaire)):
                if k<=len(temp_inv)-1 : self.inventaire[k]["objet"]=temp_inv[k]
                else : self.inventaire[k]["objet"]=None                   
            self.plateau.affichage_inventaire()
        #choix combat ou craft
        if self.perso == 'hogler' :
            reponse=self.plateau.demander_choix("Choissiez de crafter ou de combattre","Voulez vous fabriquez un objet? \n\n" \
            "Votre pouvoir 1 vous permet de fabriquer un objet sans dépenser d'action donc vous pourrez aussi attaquer")
        else :
            reponse=self.plateau.demander_choix("Choissiez de crafter ou de combattre","Voulez vous fabriquez un objet? \n\n ATTENTION :" \
            "Vous n'avez qu'une action possible : attaquer un ennemi ou fabriquer un objet")
            if reponse :                 
                self.nb_craft+=1
                self.verifier_craft
            else : 
                self.nb_attaque+=1
                self.phase_combat()                

    def phase_combat(self):
        #bonus des persos
        self.mod_combat+=self.arme_perso['mod']                
        if self.perso=='clepto' : 
            message_clepto=f"vous avez {self.mod_combat} modificateur de dégâts.\n\n Voulez vous défausser un objet pour utiliser votre pouvoir 2 et gagner un modificateur supplémentaire?"
            reponse=self.plateau.demander_choix("Modificateurs de combats",message_clepto)
            if reponse and self.pouvoir_2 == False:
                self.defausser_objet_inventaire()
                self.mod_combat+=1
        if self.perso=='psycho' :
            self.degat_collateraux=True
            message_psycho=f"Vous avez {self.mod_combat} modificateurs de dégâts. \n\nVotre pouvoir 1 vous octroie 1 dégats sur les ennemis adjacents à votre cible. \n\nVoulez vous sacrifier un pdv pour doubler vos dégats?"
            reponse=self.plateau.demander_choix("Modificateurs de combats",message_psycho)
            if reponse : 
                self.pdv-=1
                self.plateau.maj_pdv()
        if self.perso=="hipster" and self.pouvoir_1==False:
            self.mod_combat+=1
            self.pouvoir_1=True
            self.plateau.afficher_info("Modificateur de dégats",f"Vous avez {self.mod_combat} modificateur de dégats. \n\n Votre pouvoir 1 vous en a accordé un supplémentaire")
        # choix de l'arme :
        is_munition_arme_perso=False
        is_munition_arme=False
        is_attaque_arme_perso=False
        is_attaque_arme=False
        #vrifie si les armes ont besoi de munition et si il y en a dans l'inventaire       
        if self.arme_perso["condition"]!=None :
            for item in self.inventaire : 
                if item["objet"]!=None and item["objet"]["nom"]==self.arme_perso["condition"] : 
                    is_munition_arme_perso=True 
                    is_attaque_arme_perso=True 
        else : is_attaque_arme_perso=True   
        if self.arme["condition"]!=None :
            for item in self.inventaire : 
                if item["objet"]!=None and item["objet"]["nom"]==self.arme["condition"] : 
                    is_munition_arme=True
                    is_attaque_arme=True
        else : is_attaque_arme=True    
        #attribution de l'arme.
        if is_attaque_arme_perso==False and is_attaque_arme==False: 
            message_arme=f"Désolé, vous n'avez aucune munition/flèches pour attaquer avec vos deux armes. Vous ne pouvez pas attaquer."
            self.plateau.afficher_info("Sélections de l'arme",message_arme)
            self.tour_combat_ennemi()
        elif is_attaque_arme_perso==False and is_attaque_arme==True:
            message_arme=f"Vous n'avez pas de munitions/flèches pour utiliser votre arme personnelle.\n\nVous attaquerez donc avec votre arme secondaire"
            self.plateau.afficher_info("Sélections de l'arme",message_arme)
            self.arme_selectionnee=self.arme   
            
        elif is_attaque_arme==False and is_attaque_arme_perso==True:
            message_arme=f"Vous n'avez pas de munitions/flèches pour utiliser votre arme secondaire.\n\nVous attaquerez donc avec votre arme principale"
            self.plateau.afficher_info("Sélections de l'arme",message_arme)
            self.arme_selectionnee=self.arme_perso           
        else :
            reponse=self.plateau.demander_choix("Sélection de l'arme","Voulez vous attaquer avec votre arme personnelle?")
            if reponse : 
                self.arme_selectionnee=self.arme_perso
            else : 
                self.arme_selectionnee=self.arme
        print(self.arme_selectionnee)                     
        self.selectionner_cible()
            
    def selectionner_cible(self) : 
        self.cible=None        
        self.cible=self.plateau.designer_cible()
        print("cible choisi",self.cible)
        self.resolution()

    def resolution(self) :
        "tirage des modificateur"




    def tour_combat_ennemi() :
        pass


if __name__ == "__main__":
    
    def preparer_modificateur():
        """fonction qui prépare la pioche des modificateurs de combat"""
        #l'id ets un tuple (mod,dommage_collatéraux,pdv,vol)
        mod=[{"id":(3,0,-1,0),"nb":1},{"id":(3,0,0,1),"nb":1},{"id":(-2,0,0,0),"nb":5},{"id":(-1,0,0,0),"nb":7},{"id":(0,0,0,0),"nb":6},
            {"id":(0,1,0,0),"nb":2},{"id":(1,0,0,0),"nb":4},{"id":(1,1,0,0),"nb":2},{"id":(2,0,0,0),"nb":4},{"id":(2,1,0,0),"nb":2}]
        pioche_mod=[]
        for item in mod :
            for nombre in range(item["nb"]) :
                pioche_mod.append(item["id"])
        random.shuffle(pioche_mod)
        return pioche_mod    
 
    def preparer_objet():
        """fonction qui prépare la pioche des objets"""
        #les effets bonus ou malus sont représneter par une liste d'effet : [pdv,action_attaque,action_craft,mod,degats_collatéraux,degat_libre,vol] vol c'est juste pour lescorbeau
        objets=[{"nom":"pêches au sirop","type":"heal","effet":[3,0,0,0,0,0,0],"nb":1,"stackable":0},
                {"nom":"raviolis","type":"heal","effet":[3,0,0,0,0,0,0],"nb":1,"stackable":0},
                {"nom":"soupe","type":"heal","effet":[3,0,0,0,0,0,0],"nb":1,"stackable":0},
                {"nom":"barre céréales","type":"heal","effet":[2,0,0,0,0,0,0],"nb":2,"stackable":0},
                {"nom":"bouteille d'eau","type":"heal","effet":[1,0,0,0,0,0,0],"nb":2,"stackable":0},
                {"nom":"munitions","type":"munition","effet":[0,0,0,1,0,0,0],"nb":5,"stackable":1},
                {"nom":"flèches","type":"munition","effet":[0,0,0,1,0,0,0],"nb":5,"stackable":1},
                {"nom":"déchets","type":"déchets","effet":None,"nb":5,"stackable":0},
                {"nom":"explosif","type":"craft","effet":None,"nb":2,"stackable":1},
                {"nom":"clous","type":"craft","effet":None,"nb":2,"stackable":1},
                {"nom":"planches","type":"craft","effet":None,"nb":3,"stackable":1},
                {"nom":"câbles","type":"craft","effet":None,"nb":2,"stackable":1},
                {"nom":"fragments","type":"craft","effet":None,"nb":2,"stackable":1},
                {"nom":"boisson énergisante","type":"boost","effet":[-1,1,0,0,0,0,0],"nb":2,"stackable":0},
                {"nom":"boisson concentration","type":"boost","effet":[-1,0,1,0,0,0,0],"nb":2,"stackable":0},
                {"nom":"rage sanguinaire","type":"boost","effet":[-1,0,0,0,1,0,0],"nb":1,"stackable":0},
                {"nom":"concentration","type":"boost","effet":[0,0,0,0,0,1,0],"nb":1,"stackable":0},
                {"nom":"chance","type":"boost","effet":[0,0,0,1,0,0,0],"nb":1,"stackable":0},
                {"nom":"vitamines","type":"boost","effet":[0,0,0,2,0,0,0],"nb":1,"stackable":0},
                {"nom":"attaque de rat","type":"malus","effet":[-1,0,0,0,0,0,0],"nb":1,"stackable":0},
                {"nom":"fracture","type":"malus","effet":[-2,0,0,0,0,0,0],"nb":1,"stackable":0},
                {"nom":"attaque de corbeau","type":"malus","effet":[0,0,0,0,0,0,1],"nb":1,"stackable":0}]        
        pioche_objet=[]
        for item in objets :
            for nombre in range(item["nb"]):
                pioche_objet.append({"nom":item["nom"],"type":item["type"],"effet":item["effet"],"stackable":item["stackable"]})
        random.shuffle(pioche_objet)  
        return pioche_objet           
    
    arme_base=[{"nom":"arc","pa":3,"mod":0,"condition":"flèches"},
                {"nom":"pistolet","pa":3,"mod":0,"condition":"munitions"},                
                {"nom":"marteau","pa":2,"mod":0,"condition":None},
                {"nom":"pied de biche","pa":2,"mod":0,"condition":None}]
    persos=["clepto","gachette","pilier","psycho","hipster","hogler"]
    armes=["arc","pistolet","marteau","pied de biche"]

    def valider_selection():
        """fonciton qui sert à valider les choix de la combobox de la fenetre d'accueil"""
        if combo_personnage.get() and combo_arme.get():
            global personnage_choisi, arme_choisi
            personnage_choisi = combo_personnage.get()
            arme_choisi = combo_arme.get()
            for arme in arme_base :
                if arme["nom"]==arme_choisi : arme_choisi=arme  
            accueil.quit()
            accueil.destroy()

    ################################### Fenetre d'accueil ###################################
    accueil=tk.Tk()    
    accueil.geometry("400x250")
    # Label et liste déroulante pour le personnage
    tk.Label(accueil, text="Choisissez votre personnage :").pack(pady=5)
    combo_personnage = ttk.Combobox(accueil, values=persos, state="readonly")
    combo_personnage.pack(pady=5)
    combo_personnage.bind("<<ComboboxSelected>>", lambda e: valider_selection())
    # Label et liste déroulante pour l'objet de départ
    tk.Label(accueil, text="Choisissez votre objet de départ :").pack(pady=5)
    combo_arme = ttk.Combobox(accueil, values=armes, state="readonly")
    combo_arme.pack(pady=5)
    combo_arme.bind("<<ComboboxSelected>>", lambda e: valider_selection())   
    accueil.mainloop()

    ################################ Initialisation du jeu ##################################
    print(personnage_choisi,arme_choisi)
    pioche_objet=preparer_objet()
    pioche_mod=preparer_modificateur()
    game=Jeu(personnage_choisi,arme_choisi,pioche_mod,pioche_objet)
    plateau=Plateau(game)
    game.set_plateau(plateau)
    plateau.mainloop()

