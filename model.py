#!/usr/bin/env python
#-*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
import requests
from database import DataBase

        
class Category:
    """class to create categories"""
      

    def fill_tab_categories(self, list_categories, mycursor, my_database):
        """fill the data in tab_categories"""
        for tup in list_categories: 
            sql_insert_query1 = "INSERT INTO tab_categories (categories_name) VALUES (%s)" 
            insert_tuple_1 = (tup,)
            mycursor.execute(sql_insert_query1, insert_tuple_1) 
            my_database.commit() 
            print("Data inserted successfully into user table_categories using the prepared statement")


    def select_category(self, mycursor):
        '''choose one category into 5 availabled'''
        sql_select_query4 = "SELECT * FROM tab_categories"
        mycursor.execute(sql_select_query4)
        self.myresult = mycursor.fetchall()


class Product:


    def fill_data_product(self, list_products, mycursor, my_database):
        """fill products in tab_product"""
        for cat in list_products: #list_products = x list of categories in which x dictionnaries = products items
            y = list_products.index(cat)
            z = y + 1   
            for product in cat:    
                try:
                    product_name = product['product_name']
                    brands = product['brands']
                    stores = product['stores']
                    nutriscore_grade = product['nutrition_grades']
                    url = product['url']
                    image_front_url = product['image_front_url']
                    list_item_product = []
                    list_item_product.extend((product_name, brands, stores, nutriscore_grade, url, image_front_url,z))
                    sql_insert_query2 = "INSERT INTO tab_product (product_name, brands,\
                    stores, nutriscore_grade, url, image_front_url, categories_id)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    insert_tuple_2 = (list_item_product)
                    mycursor.execute(sql_insert_query2, insert_tuple_2)
                    my_database.commit()
                    print("Data inserted successfully into user table_product using the prepared statement")
                except KeyError:
                    pass
                except UnicodeEncodeError:
                    pass


    def choose_product(self, user_choice_category, mycursor) : 
        '''display the products from the category'''
        self.m = user_choice_category 
        sql_select_query5 = "SELECT product_id, product_name, nutriscore_grade FROM tab_product WHERE categories_id = '{}'".format(self.m)
        mycursor.execute(sql_select_query5) 
        self.myresult1 = mycursor.fetchall() 


    def exception_choose_product(self, user_choice_category, mycursor) :
        '''use for exception if user choice product is out of range'''
        m = user_choice_category
        sql_select_query11 = ("SELECT * FROM tab_product WHERE categories_id = '{}'".format(m))
        mycursor.execute(sql_select_query11)
        self.myresult11 = [rec[0] for rec in mycursor.fetchall()] # list comprehension to pick out the fields product_id and get list of integer


    def select_product(self, mycursor, user_choice_product) :
        '''select the product you want to substitute with details'''
        n = user_choice_product  
        sql_select_query6 = "SELECT product_id, product_name, nutriscore_grade, brands, stores, url, image_front_url FROM tab_product WHERE product_id = '{}'".format(n)
        mycursor.execute(sql_select_query6) 
        self.myresult2 = mycursor.fetchone() # is a tuple


    def propose_substitut (self, user_choice_product, mycursor) :
        '''program proposes one substitute with details'''
        n = user_choice_product 
        sql_select_query7 = "SELECT product_id, product_name, nutriscore_grade, brands, stores, url, image_front_url\
        FROM tab_product\
        WHERE categories_id = '{}' AND NOT product_id = '{}'\
        ORDER BY nutriscore_grade ASC\
        LIMIT 1 ".format(self.m, n) 
        mycursor.execute(sql_select_query7)
        self.myresult3 = mycursor.fetchone() 

class Substitut:
    """class to create substitut"""


    def record_substitut(self, n, mycursor, my_database) :
        '''record in the database the product you want to substitute'''
        prod_id = n # product_id
        sql_insert_query8 = "INSERT INTO tab_substitut (product_id) VALUES (%s)" 
        insert_tuple_8 = (prod_id,)
        mycursor.execute(sql_insert_query8, insert_tuple_8)
        my_database.commit()
        print("product_id inserted successfully into user tab_substitut using the prepared statement")
        mycursor.execute("SELECT substitut_id FROM tab_substitut WHERE product_id = '{}'".format(prod_id))
        sub_id = mycursor.fetchone() # is a tuple
        sub_id = sub_id[0] # select the id column from the row
        mycursor.execute ("INSERT IGNORE INTO tab_assoc_product_substitut (product_id, substitut_id)\
        VALUES ({}, {})".format(prod_id, sub_id))
        my_database.commit()
        
    def tab_substitut_exception(self, mycursor) : 
        '''manage exception if substitut already recorded in tab susbtitut'''
        sql_select_query10 = ("SELECT * FROM tab_substitut")
        mycursor.execute(sql_select_query10) 
        self.myresult10 = [rec[1] for rec in mycursor.fetchall()] # list comprehension to pick out the fields product_id and get list of integer 
        

    def display_records(self, mycursor) :
        '''show detail of substitute previously recorded'''
        sql_select_query_9 = "SELECT \
                                tab_product.product_id,\
                                tab_product.product_name,\
                                tab_product.brands,\
                                tab_product.stores,\
                                tab_product.nutriscore_grade,\
                                tab_product.url,\
                                tab_product.image_front_url,\
                                tab_categories.categories_name \
                            FROM tab_substitut \
                            INNER JOIN tab_assoc_product_substitut ON tab_assoc_product_substitut.substitut_id = tab_substitut.substitut_id \
                            INNER JOIN tab_product ON tab_product.product_id = tab_substitut.product_id \
                            INNER JOIN tab_categories ON tab_categories.categories_id = tab_product.categories_id"      
        mycursor.execute(sql_select_query_9)  
        self.myresult4 = mycursor.fetchall()
        