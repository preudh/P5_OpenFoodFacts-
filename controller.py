#!/usr/bin/env python
#-*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
import requests
import os
from view import View
from model import Category
from model import Product
from model import Substitut
from database import DataBase
import json
import random



class Controller:

    def __init__(self):
        """ init controller"""
        
        self.view = View()              # instance View class
        self.database = DataBase()      # instance DataBase class  
        self.category = Category()      # instance Category class (model)
        self.product = Product()        # instance Product class (model)
        self.substitut = Substitut()    # instance Sustitut class (model)

    
    def process(self):
        ''' main loop'''
        
        continuer = True
        while continuer:
            try:
                val = self.view.choose_scenario()
                if val == 0: # create the database and tables for the first time
                    try :
                        self.create_db() 
                        self.choose_number_random_category()
                        self.get_category_data_off()
                        self.fill_tab_categories()
                        self.get_product_data_off()
                        self.fill_data_product()
                    except :
                        print('retour au menu principal')
                        return self.process()
                
                elif val == 1: # connect to existing database
                    self.connect_to_existing_database()

                elif val == 2: # search a substitut 
                    try :
                        self.select_category()
                        self.choose_product()
                        self.select_product()
                        self.propose_substitut()
                        self.record_substitut() 
                    except :
                        print('retour au menu principal!')
                        return self.process()

                elif val == 3: # display substitut already recorded
                    try :
                        self.display_records() 
                    except : 
                        print("Choisir 1 ou 0 car aucune base de données sélectionnée ou créée!")
                        return self.process()

                elif val == 4:  # exit program
                    os._exit(1)    
                else:
                    print("\nChoix invalide, entrez le chiffre correspondant à votre choix!") # 2nd error message if not good value 

            except ValueError:
                print("\nChoix invalide, entrez le chiffre correspondant à votre choix") # 1st error message if not integer

    def create_db(self):
        """create the database """
        #choose the database name
        self.view.choose_dbname() 
        
        #connection
        self.my_database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database=''
        )
        self.mycursor = self.my_database.cursor(prepared=True)
        
        #create database with name defined
        self.mycursor.execute("CREATE DATABASE {};".format(self.view.db_name))
        self.mycursor.execute("SHOW DATABASES")
        for x in self.mycursor:
            print(x)
        
        #connection to the database
        self.my_database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database= self.view.db_name
        )
        self.mycursor = self.my_database.cursor(prepared=True)
        
        #create database tables
        self.database.create_table(self.mycursor) 

        #add foreign keys to tables
        self.database.add_foreign_keys(self.mycursor)


    def connect_to_existing_database(self):
        """connection to database already created with its name"""
        self.my_database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database=''
        )
        self.mycursor = self.my_database.cursor(prepared=True)
        
        #create database with name defined
        self.mycursor.execute("SHOW DATABASES")
        for x in self.mycursor : # mycursor is a list
            print(x)
        
        db_name = input("Entrez le nom de la base de données?")
        forbidden_word = ['mysql', 'performance_schema', 'sys']
        if db_name in forbidden_word:
            print ("Choix interdit!")
            return self.connect_to_existing_database()

        try :
            self.my_database = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database= db_name
            )
            self.mycursor = self.my_database.cursor(prepared=True)
            print ("Base de données correctement selectionnée")

        except:
            print("Le nom de la base de données est-il correctement saisi? réessayez!")
            return self.connect_to_existing_database()        


    def choose_number_random_category(self):
        """Choose number of randomized categories from OFF"""
        self.view.choose_number_random_category()    


    def get_category_data_off(self):
            """get N randomized categories from fr.OFF database"""
            list_categories_name=[]
            cat = requests.get('https://fr.openfoodfacts.org/categories?json=true')
            cat_data = cat.json()
            tags_list = cat_data['tags']
            print (len(tags_list))
            list_of_random_tags_list = random.sample(tags_list, k=self.view.num_to_select)

            for category in list_of_random_tags_list:
                try :
                    category_name = category['name']
                    print(category_name)
                    list_categories_name.append(category_name)
                    print (list_categories_name)
                    self.list_categories = list_categories_name # list_categories_name is passed in the instance property
                except KeyError:
                    pass
                except UnicodeEncodeError:
                    pass    


    def fill_tab_categories(self):
        """fill the data in tab_categories"""
        self.category.fill_tab_categories(self.list_categories, self.mycursor, self.my_database) 


    def get_product_data_off(self):
        """method to get products from OFF database"""
        list_products_name = []
        for x in self.list_categories:    
            """get products' data from openfoodfacts api with string as paramaters"""
            parameters = {
            'action': 'process',
            'json': 1,
            'countries': 'France',
            'page_size': 100,
            'page': 1,
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': x
            }
            r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl',
                            params=parameters) # passing parameters in URL
            print(r.url)
            data = r.json() # r. from requests module decodes json file
            products = data['products'] #access dictionnary items by referring to its key name, products ordered by id
            list_products_name.append(products)  
            self.list_products = list_products_name # list_categories_name is passed in the instance property


    def fill_data_product(self):
        """fill products in tab_product"""
        self.product.fill_data_product(self.list_products, self.mycursor, self.my_database)


    def select_category(self) :
        '''choose one category into X availabled'''
        self.category.select_category(self.mycursor)
        self.view.select_category(self.category.myresult)
       

    def choose_product(self) :
        '''display the products from the category'''
        self.product.choose_product(self.view.user_choice_category, self.mycursor)
        if len(self.product.myresult1) == 0 :
            print("Il n'y a aucun produit dans cette catégorie, choisir une autre catégorie")
            return self.process()          
        elif len(self.product.myresult1) > 0 :
            self.view.choose_product(self.product.myresult1) 
        
           
    def select_product(self) :
        '''select the product you want to substitute with details and manage boundaries'''
        self.view.select_product_input()
        self.product.select_product(self.mycursor, self.view.user_choice_product) # query select the product you want to substitute with details
        self.product.exception_choose_product(self.view.user_choice_category, self.mycursor ) # query used for exception if user choice product is out of range
        max_number_choice = max(self.product.myresult11) # get maximum product_id in the category
        min_number_choice = min(self.product.myresult11) # get minimun product_id in the category
        user_choice = self.view.user_choice_product 
        
        if int(user_choice) < min_number_choice or int(user_choice) > max_number_choice:
            print("Entrez un nombre dans l'intervalle de selection")
            return self.select_product()
        
        self.view.select_product_view(self.product.myresult2) 

    def propose_substitut(self) :
        '''program proposes one substitute with details'''
        
        if len(self.product.myresult1) == 1:
            print("Désolé, il n'y a qu'un produit dans cette catégorie, aucun substitut de disponible")
            return self.process()

        elif len(self.product.myresult1) > 1 :
            self.product.propose_substitut(self.view.user_choice_product, self.mycursor)
            self.view.propose_substitut(self.product.myresult3) 


    def record_substitut(self) :    
        '''record substitut and manage exception if substitut already recorded in tab susbtitut or answer is non '''
        self.substitut.tab_substitut_exception(self.mycursor) 
        self.view.record_substitut() # is a string
        num_substitut = self.view.user_record_substitut
        int_num_substitut = int(num_substitut) # conversion integer to compare with myresult10
        
        exist = 0
        for element in self.substitut.myresult10: # myresult10 is list of integer (product_id) in tab_substitut
            if element == int_num_substitut:
                exist = 1
        if exist == 1:
            print("Désolé, le substitut est déjà enregistré, choisir une autre catégorie")
        else :
            self.substitut.record_substitut(num_substitut, self.mycursor, self.my_database)
            print("Substitut enregistré.")


    def display_records(self) :
        '''show detail of substitute previously recorded'''
        self.substitut.display_records(self.mycursor)
        self.view.display_records(self.substitut.myresult4)        
       

        
if __name__ == '__main__': # name variable equal to main, check controller file is directly runed or imported
       
    # create instance class controller
    Control1 = Controller()
    
    # instance methods 
    Control1.process()
    

   


    
   



