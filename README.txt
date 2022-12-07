Team members: Akash Mullick, Mazen Selim, Jamael Smith, Donovan Nickol, Joshua Kang
Project option: Standard project
Team name: Rainforest
Gitlab repository: https://gitlab.oit.duke.edu/cs-316-team-rainforest/mini-amazon
Demo video: http://youtu.be/stfeceOZUkk


All the code for generating and populating the databases can be found within db/data. The data was generated in steps. The first level is the source level, within db/data/gen/sources. In here there is code to take scraped data and plain texts and reformat them into a more usable format.
At the second level, in the db/data/gen/ai_supplemented directory, the python file gen.py calls on products.py, reviews.py, and conversations.py to generate realistic data
using GPT-3. Then, at the third and final level, the raw data that has been transformed is finally used to atomically generate all the daatasets such that they all satisfy foreign key and uniqueness constraints, and this is through data/gen.

Donovan's updates: Created add to cart button on product page, created cart page, created remove from cart button, created change quantity feature.
Joshua's weekly update: Created wireframe for feedback, view of product reviews, view of seller reviews, view of reviews by user, and messaging. Added code for creating sample product and seller feedback, as well as messaging.
Akash's updates: Minor UI updates.
Mazen's Weekly Update: added a seller inventory page and created a realistic database for products, sales, reviews, etc.
Jamael's update: Created public view page for account as well as button to access account, added buttons to that page for user to access their purchase history and update information/balance. Also added address, city, and state fields for registration window. 
