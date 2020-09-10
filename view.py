#!/usr/bin/env python
#-*- coding: utf-8 -*-


class View: 


    def choose_scenario(self) :
        """create database for the first time or search sustitute or display substitute or leave the program """
        print("\n---MENU PRINCIPAL---\n"
                "0 - Créer la base de donnéees?\n"
                "1 - Vous connecter à la base de donnée en entrant son nom si elle existe déjà?\n"
                "2 - Choisir une catégorie puis un aliment à substituer dans la catégorie?\n"
                "3 - Retrouver mes aliments substitués?\n"
                "4 - Quitter le programme?")
        #return input("\nEntrez votre choix : ")
        return int(input("\nEntrez votre choix : "))
       

    def choose_dbname(self) :
        """choose database name"""
        self.db_name = input("Entrez le nom base de données ?")
        print(self.db_name)

    
    def choose_number_random_category(self) :
        """Choose number of randomized categories from OFF"""
        self.num_to_select = int(input("Entrez le nombre de categories max 20:"))
        print (self.num_to_select)    


    def select_category(self, myresult) :
        '''choose one category'''
        print ("Cette application vous permet dans une catégorie d'aliments de substituer un produit "
        "avec un meilleur nutriscore à l'aliment selectionné")
        for x in myresult: 
            print(x)
        self.user_choice_category = input ("Selectionnez le numero de la catégorie:")
        print("votre choix est le numéro {}".format(self.user_choice_category))


    def choose_product(self, myresult1) :
        '''display the products from the category'''
        print ("selectionnez un aliment à substituer parmi la categorie préalablement selectionnée:")
        for x in myresult1: # is a list 
            print(x) 

    def select_product_input(self) :
        '''select the product you want to substitute with details'''    
        self.user_choice_product = input ("Selectionnez le numero du produit:")
        print("votre choix est le numéro {}".format(self.user_choice_product))
    

    def select_product_view(self, myresult2):     
        '''print details product'''
        print("\n \
        LES INFORMATIONS SUR LE PRODUIT SONT :")
        i = myresult2  # tuples 
        print("\n \
        Produit identifiant : {} \n \
        Nom du produit : {} \n \
        Nutri-score : {} \n \
        Marque : {} \n \
        Magasin : {} \n \
        Lien vers OpenFoodFacts : {} \n \
        Lien vers image : {}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


    def propose_substitut (self, myresult3) :
        '''program proposes one substitute with details'''
        print("\n \
        LE PROGRAMME VOUS PROPOSE LE SUBSTITUT SUIVANT :")
        i = myresult3 # tuples  
        print("\n \
        Produit identifiant : {} \n \
        Nom du produit : {} \n \
        Nutri-score : {} \n \
        Marque : {} \n \
        Magasins : {} \n \
        Lien vers OpenFoodFacts : {} \n \
        Lien vers image : {}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


    def record_substitut(self) :
        '''record in the database the product you want to substitute'''
        self.user_record_substitut = input ("\n \
        Vous avez la possibilité d'enregistrer son substitut en"
        " entrant son numéro ou tapez non:")
        print("votre choix est {}".format(self.user_record_substitut))
        if self.user_record_substitut == 'non':
           raise Exception () 


    def display_records(self, myresult4) :
        '''show detail of substitute previously recorded'''
        print ("Voici l'historique des aliments substitués:")
        for x in myresult4: # is a list 
            print(x) 

