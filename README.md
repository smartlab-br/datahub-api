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

# Third-party components used in our platform

**[Flask](https://github.com/pallets/flask)**\
Copyright © 2010 by the Pallets team - [BSD 3-Clause License](http://flask.pocoo.org/docs/1.0/license)

**[Flask-RESTful](https://flask-restful.readthedocs.io)**\
Copyright © 2018, Kevin Burke, Kyle Conroy, Ryan Horn, Frank Stratton, Guillaume Binet - [BSD License](https://github.com/flask-restful/flask-restful/blob/master/LICENSE)

**[Flask-CORS](https://flask-cors.readthedocs.io)**\
Copyright © 2013, Cory Dolphin - [MIT License](https://github.com/corydolphin/flask-cors/blob/master/LICENSE)

**[Flask-RESTful-Swagger](https://flask-restful-swagger.readthedocs.io/)**\
Copyright © 2016, Sobolev Nikita - [MIT License](https://github.com/andyzt/flask-restful-swagger/blob/master/LICENSE)

**[Pandas](https://pandas.pydata.org)**\
Copyright © 2008-2012, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team - [BSD 3-Clause License](http://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html#license)

**[Pylint](https://www.pylint.org)**\
Copyright © 1989, 1991 Free Software Foundation, Inc. - [GNU General Public License v2.0](https://github.com/PyCQA/pylint/blob/master/COPYING)

**[Nose2](https://nose2.readthedocs.io)**\
Copyright © 2012, Jason Pellerin - [BSD 3-Clause License](https://github.com/nose-devs/nose2/blob/master/license.txt)

**[NumPy](https://www.numpy.org)**\
Copyright © 2019 NumPy developers - [BSD 3-Clause License](https://www.numpy.org/license.html)

**[Impyla](https://github.com/cloudera/impyla)**\
Copyright © Impyla developers - [Apache 2.0 License](https://github.com/cloudera/impyla/blob/master/LICENSE.txt)

**[Kazoo](https://kazoo.readthedocs.io)**\
Copyright ©  2011-2014, Kazoo team - [Apache 2.0 License](https://github.com/python-zk/kazoo/blob/master/LICENSE)

**[Babel](http://babel.pocoo.org)**\
Copyright © 2018, The Babel Team - [BSD 3-Clause License](http://babel.pocoo.org/en/latest/license.html)

**[Ansi Colors](https://github.com/jonathaneunice/colors)**\
Copyright © 2012 Giorgos Verigakis - [ISC License](https://github.com/jonathaneunice/colors/blob/master/LICENSE)

**[Requests](http://python-requests.org)**\
Copyright © 2018 Kenneth Reitz - [Apache 2.0 License](https://2.python-requests.org/en/master/user/intro/#requests-license)

**[PyYAML](https://pyyaml.org)**\
Copyright © 2017-2019 Ingy döt Net, Copyright © 2006-2016 Kirill Simonov - [MIT License](https://pyyaml.org/wiki/PyYAML)
