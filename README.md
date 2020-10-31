![Image of Vasa app](app/vasa_no_tap.png)

# Vasa Auto Register
Automate the registration of Vasa classes.  

### Requirements
 - Docker  
 - Python3.8+  

### Getting Started
 - copy and update `.env.template` file, removing `.template` from file name  
   - `.env` contains personal login information and the gym location id  
 - copy and update `vasa_registration.json.template` file, removing `.template` from file name  
   `vasa_registration.json` contains the desired classed for auto registration  
 - run with docker `docker build -t vasa . && docker run -d vasa`  
 - run with python `python main.py`  
