Team members: Akash Mullick, Mazen Selim, Jamael Smith, Donovan Nickol, Joshua Kang
Project option: Standard project
Team name: Rainforest
Gitlab repository: https://gitlab.oit.duke.edu/cs-316-team-rainforest/mini-amazon

The code for creating and populating a sample database is in the create_ms2.sql and load_ms2.sql files.

All the code for generating and populating code can be found within db/generated. This is done in several steps. The first layer 
data_cleaner which interacts with data scraped from amazon and reformats it in a meaningful way. Then, there are gen_extras and gen_decsriptions
which interact with Faker and OpenAI to produce realistic data. Finally, there is gen.py which reformats all the previously produced data to fit the SQL schemas

Donovan's updates: Created add to cart button on product page, created cart page, created remove from cart button, created change quantity feature.
Joshua's weekly update: Created wireframe for feedback, view of product reviews, view of seller reviews, view of reviews by user, and messaging. Added code for creating sample product and seller feedback, as well as messaging.
Akash's updates: Created home page with all products (sorting, searching, filtering, pagination), individual product pages, form to add/edit products, and added triggers to db.
Mazen's Weekly Update: added a seller inventory page and created a realistic database for products, sales, reviews, etc.