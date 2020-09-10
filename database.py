#!/usr/bin/env python
#-*- coding: utf-8 -*-
import mysql.connector
import requests
from mysql.connector import Error


class DataBase:


    def create_table(self, mycursor):        
        """connection to the database name"""
        self.mycursor = mycursor

        """ create table categories, product, substitut, assoc_product_substitut"""
        self.mycursor.execute("CREATE TABLE tab_categories (categories_id INT(11) NOT NULL AUTO_INCREMENT,\
        categories_name VARCHAR(150) NOT NULL,\
        PRIMARY KEY (categories_id))\
        ENGINE=InnoDB")
        
        self.mycursor.execute("CREATE TABLE tab_product (product_id INT(11) NOT NULL AUTO_INCREMENT,\
        product_name VARCHAR(150) NOT NULL,\
        brands VARCHAR(150) NOT NULL,\
        stores VARCHAR(150) NOT NULL,\
        nutriscore_grade VARCHAR(1) NOT NULL,\
        url VARCHAR(150) NOT NULL,\
        image_front_url VARCHAR(150) NOT NULL,\
        categories_id INT(11) NOT NULL,\
        PRIMARY KEY (product_id))\
        ENGINE=InnoDB")
        
        self.mycursor.execute("CREATE TABLE tab_substitut (substitut_id INT(11) NOT NULL AUTO_INCREMENT,\
        product_id int,\
        PRIMARY KEY (substitut_id))\
        ENGINE=InnoDB")
        
        self.mycursor.execute("CREATE TABLE tab_assoc_product_substitut (assoc_product_substitut_id INT(11) NOT NULL AUTO_INCREMENT,\
        product_id int,\
        substitut_id int,\
        PRIMARY KEY (assoc_product_substitut_id))\
        ENGINE=InnoDB")

    def add_foreign_keys(self, mycursor):
        """add foreign keys to tables"""

        self.mycursor.execute("ALTER TABLE tab_product ADD CONSTRAINT FK_categories_id FOREIGN KEY (categories_id) REFERENCES tab_categories(categories_id)")
        self.mycursor.execute("ALTER TABLE tab_substitut ADD CONSTRAINT FK_product_id FOREIGN KEY (product_id) REFERENCES tab_product(product_id)")
        self.mycursor.execute("ALTER TABLE tab_assoc_product_substitut ADD FOREIGN KEY (product_id) REFERENCES tab_product(product_id)") #  just remove the optional keyword CONSTRAINT since InnoDB will automatically generate unique symbols for each. (+1)
        self.mycursor.execute("ALTER TABLE tab_assoc_product_substitut ADD FOREIGN KEY (substitut_id) REFERENCES tab_substitut(substitut_id)") #  just remove the optional keyword CONSTRAINT since InnoDB will automatically generate unique symbols for each. (+1)