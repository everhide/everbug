# Everbug - Debugger for Django projects

![](https://img.shields.io/badge/build-passing-brightgreen.svg) ![](https://img.shields.io/badge/coverage-98%25-green.svg)

The Everbug is a lightweight Django middleware for Chrome/Firefox extension with easy install.
One of the advantages: the response body of target page remains clean and unchanged.  

Special summary:    
* Database queries with explains (Multiple database support)  
* Context variables  
* Profiles functions (cProfile through decorator)  
* Support ajax requests  

### Screenshots
![Context](/screenshots/context.png)
![Queries](/screenshots/queries.png)
![Profile](/screenshots/profile.png)

## Installing

For Django:
```
Run "pip install everbug".
Add "everbug" to your INSTALLED_APPS in settings.py.
Append "everbug.middleware.Tracer" to MIDDLEWARE or MIDDLEWARE_CLASSES in settings.py.
```

For browser:  
* [Chrome extension](https://chrome.google.com/webstore/search/everbug)   
* [Firefox extension](https://addons.mozilla.org/ru/firefox/addon/everbug/)

## Usage  

"Context" works for any view which has a "context_data". "Queries" works as-is for all databases in "DATABASES" section. "Profile" works through decorator (based on builtin cProfile). By default, profile output is truncated to 20 lines.    

Example usage:
```
from everbug.shortcuts import profile

@profile
def sample_method():
    // some code here ...  
```
Call @profile with argument for full view, for example:  
```
@profile(short=False)
def sample_method():
    // some code here ...  
```

## Running the tests
```
docker-compose  up -d 
docker exec -it everbug tox
```

## Requirements
Python >= 3.5  
Django >= 1.11

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
