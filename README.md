# Magic The Gathering game

This project is built using react.js and redux and the django framework


## Start application on localhost
1) git clone ...
2) cd `magic/react_app`
3) `npm install`
4) `npm run`
5) `mkvirtualenv -p /usr/bin/python3 magic`
6) `pip install -r setup/requirements-dev.txt`
7) cd `../web_app`
8) `cp magic/settings/local_settings_example.py magic/settings/local_settings.py` and modify to your local needs.
9) `./manage migrate`
10) `./manage run server`
11) check your application at [http://localhost:8000]()



## Documentation
To get familiar with the used frameworks check out the following tutorials

**react.js**
 - https://reactjs.org/tutorial/tutorial.html

React also created it's own [README-react.md](README-react.md) for this project

**redux**
 - https://redux.js.org/introduction/learning-resources
 - https://egghead.io/lessons/react-redux-the-single-immutable-state-tree

**django framework**
 - https://docs.djangoproject.com/en/2.0/
