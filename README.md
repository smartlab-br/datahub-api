# SmartLab Flask

Flask for SmartLab developers 

==> Environment for development in Flask in MPT

     > Run app with pure Flask
       docker run -p 8080:5000 -d -v /path/app:/app smartlab/flask

     > Run app with uWSGI
       docker run -p 8080:5000 -d -v /path/app:/app smartlab/flask uwsgi

     > Run app in debug mode
       docker run -p 8080:5000 -d -v /path/app:/app smartlab/flask debug

     > Run tools to test code quality
       docker run -p 8080:5000 -d -v /path/app:/app smartlab/flask test

     > Run terminal to inspect container
       docker run -p 8080:5000 -it -v /path/app:/app smartlab/flask terminal

Note: the main file must be named as main.py
