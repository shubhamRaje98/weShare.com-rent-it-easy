# weShare.com-rent-it-easy
The application tries to solve the problem of renting, making it feasible to rent any thing to anybody using one central platform.
It is a Online renting platform to rent any thing. The web app aims to provide one platform to rent and make renting more feasible. Users can make accounts, interact with other users, can post product to rent or can purchase product on rent.

Technology Stack Used : 
  1. Front-end:
      HTML/CSS/Bootstrap
  2. Back-end:
      Python/Django (class based user specific views)
  3. Database:
      SQLite
  4. User Authentication: 
      django-allauth
  5. Payment Gateway:
      Rayzorpay
      
 To use the app user needs to create account first, any new/non-authenticated use will land on landing page. After loging in user will be redirected to the feed page where user can see the posted products catagory wise(i.e fasion, education, electronics etc.) He can make his profile by filling in his details. User can make post by clicking on user icon in navbar, providing all the neccessary deatils asked. 
 
 User can also purchase the product by clicking on procced button in product details page. User will be redirected to rayzorpay api to make purchase. 
 
 
