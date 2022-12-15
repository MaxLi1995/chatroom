# CAPSTONE final project: 'Chatroom' Written description

## Distinctiveness and Complexity: 
This project is distinct by its functionality compare to all other projects, where the user can enter/host multiple rooms to chat in with many other users. The application fetches and updates from the backend constantly so the users will see their and other messages as fast as possible. The most similar project in concept to this one is project 4 'social network'. However, project 4 has the limitation where the information are only updated from user actions, thus limits the speed of which users can exchange information. In addition, project 4 has no privacy freedom as your posts are seen by everybody, where as chatroom allows the creation of private rooms as well as the ability for the room host to control who can be in the room. 

## Project description:
As stated above, Chatroom is a Discord like application that allows registered users to create open/private rooms to chat with others. The application fetches data automatically in a set interval to update the front end for all logged in users to see, allowing a fast pase exchange of information. 

## files:
the file structures are exactly the same as all previous projects. The files below are the ones with most amount of changes
url.py handles the routing of apis and the visible pages through URLs
views.py works together with url.py to handle api requests and update database. It also renders the correct html pages based on url
models.py defines the structure and parameters of our database
script.js takes care of all frontend functionalities, communicates with views.py (via url.py) to format and display html code by fetching necessary data in json and updates the database.
style.css has all styling on the application
layout.html contains the header for the other pages
index.html is the home page of the application
room_page.html is the chatroom page 

## How to run the application:
The same as all the project before
first cd chatroom to get to the file directory
then python manage.py makemigrations project
then python manage.py migrate
lastly python manage.py runserver
If you want to manually make change or modify the existing data run python manage.py createsuperuser to make admin account, don't forget to modify admin.py accordingly

## Additional info/author note:
When you login and joins a room, make sure to click leave room to to completely remove it. otherwise the room will keep you in the list forever. If you are the room owner, and you leave a room, the owner then is assigned automatically to the next person. 

Due to time constraints, this project is made very simple and quite a few features I had in mind were not implemented such as a profile page for users, better main page and a bunch of user utilities. I will improve on this project later on my own time as my personal project.