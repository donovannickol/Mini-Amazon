Team members: Akash Mullick, Mazen Selim, Jamael Smith, Donovan Nickol, Joshua Kang
Project option: Standard project
Team name: Rainforest
Gitlab repository: https://gitlab.oit.duke.edu/cs-316-team-rainforest/mini-amazon
Demo video: http://youtu.be/stfeceOZUkk


All the code for generating and populating the databases can be found within db/data. The data was generated in steps. The first level is the source level, within db/data/gen/sources. In here there is code to take scraped data and plain texts and reformat them into a more usable format.
At the second level, in the db/data/gen/ai_supplemented directory, the python file gen.py calls on products.py, reviews.py, and conversations.py to generate realistic data
using GPT-3. Then, at the third and final level, the raw data that has been transformed is finally used to atomically generate all the daatasets such that they all satisfy foreign key and uniqueness constraints, and this is through data/gen.

Donovan's updates: Created detailed order page that displays info of an order. Added submit order functionality. Added a saved for later section on the cart page. Changed schema to incorporate saved for later.
Joshua's weekly update: Check if the current user is signed in. If not, they cannot see seller reviews. Check if the current user is signed in and has purchased a product. If they haven’t purchased, we prompt them to purchase the product to leave a review. If they have purchased, we give them the option to leave a product rating. No matter what, we show the available sellers and all product ratings from the product page. From the user’s personal page, we show the user who they have left reviews for, and which products they left reviews for. If they haven’t left reviews for a seller or product, but they have purchased them/from them, we let them know that they can leave a review for them.
Akash's updates: Minor UI updates.
Mazen's Weekly Update: Refind seller inventory page to conform to card view, added seller analytics and seller history, as well as a mechanism to mark orders as fulfilled.
Jamael's update: Created public view page for account as well as button to access account, added buttons to that page for user to access their purchase history and update information/balance. Also added address, city, and state fields for registration window. 
