# Application purpose:

* Project5 of Python developer training from OpenClassrooms (https://openclassrooms.com/fr) : use public data from
* OpenFoodFacts (https://fr.openfoodfacts.org)

* Create a program for the startup "Pur Beurre" which owns a restaurant. The team noticed that their users were keen 
* on changing their diet but were not sure where to start. The objective is to create a program that would interact
* with the Open Food Facts database to retrieve food products by categories, compare them and offer to the user a
* healthier substitute for the food product choosed in a specific category.  
  

# Requirements (see requirements.txt for details) :

* Python 3 : install (https://www.python.org/downloads/release/python-373/)
* MySQL :  install MySQL for python (https://dev.mysql.com/downloads/connector/python/) or install WampServer which is
* shipped with MySQL & phpMyAdmin (https://www.wampserver.com/). phpMyAdmin is recommanded but not required. It's a tool,
* intended to handle the administration of MySQL with a Web intuitive interface and support MySQL features. 


# Launch :

* start the program 'controller.py'
* Install packages (pip install -r testRequirements.txt)


# Design and Development:

* Develop with Windows 7
* User stories : see trello in the documentation folder or (https://trello.com/b/go5lXF7T/p5ocpreudh)
* The program interacts with the OpenFoodFacts API (see documentation (https://wiki.openfoodfacts.org/API), imports json
* files (not necessary to import all data, number of categories limited by the creator of the database) and a MySQL
* database is created on the local machine. Then, the database is used by the program to compare foods with healthier
* substitute (no direct search on OpenFoodFacts).
* The MVC (Model–view–controller) is used as design pattern.
* The MPD (Physical Data Model) is in the documentation folder.
* 3 mains classes (Category, Product, Substitut ) in model.py
* API Request from OpenFoodFacts in controller.py
* Views and interactions with the user in the terminal
* Authorize access to the database USER = 'root',  Password = ' ', server choice = 'MySQL'


# Process when using the program :

* Main menu

"0 - Créer la base de donnéees?
"1 - Vous connecter à la base de donnée en entrant son nom si elle existe déjà?
"2 - Choisir une catégorie puis un aliment à substituer dans la catégorie?
"3 - Retrouver mes aliments substitués?
"4 - Quitter le programme?"


* the user is on the ternminal
* You can create your own database, enter 0 then the database name and number of food categories (more or less 20 to limit
* data base volume) which will be loaded from openfoodfacts with a randomized method
* or you can choose a database that already exists : enter 1 and its name
* In the database you choose a specific food category amid all which are proposed : enter 2 and enter category number 
* In this category the program proposes several food products when exist : enter the product number,
* the program gives product details (name, nutriscore, brand, store, openfoodfacts.links)
* and proposes a substitut when exists with a better or similar nutriscore.
* Then you can record this substitut in the database with its number or enter 'non'
* You can find recorded substituts by typing 3
* You can quit the program by typing 4
* Exceptions, conditions are implemented to manage boundaries or user bad manual entries


# Author : Preudhomme Patrice - Python developer trainee


  