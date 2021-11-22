# Final project
   This code is a combination of the third and fourth assignments.
It provides a web page with a login form that checks the correctness of the information entered against the database, and if everything matches, then proceeds to a page with a text input field that asks for the name of the coin. After entering the name of the coin, the web page displays a list of news, which consists of a title and a description of the news itself, associated with the coin entered. Also, after the description, you can see the summation of the text, which was done through Hugging face. In addition, all data is stored in a database.

### Team members 
#### Shamshidin Sabina (SE-2008), Shaliyeva Nurzhamal (SE-2012)



## Installation 
_Note: Before you work create a project folder and a venv folder, activate the corresponding environment_

**flask**
```
$ pip install Flask
```

**flask_sqlalchemy**
```
$ pip install SQLAlchemy
```

**requests**
```
$ pip install requests
```

**beautifulSoup**
```
$ pip install beautifulsoup4
```

**Huggingface** 
```
$ pip install transformers
```



## Usage
You can run code by downloading ZIP file. 

Before you start check how to work [with form data](https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask). 

Project has following methods:
   * Login
   * Searchbar: user inputs a cryptocurrency to find infromation about it
   * Table as an output for user request

### Login 
```
@app.route('/')
def login_form():
    return render_template('login.html')
```
![Снимок экрана 2021-11-22 в 22 40 03](https://user-images.githubusercontent.com/74738634/142909210-6195b3e2-f914-4f61-97c0-b3c451617169.jpeg)





## Examples 
