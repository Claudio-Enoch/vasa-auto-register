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
    - `vasa_registration.json` is the config file used to register for classes
- build docker image `docker build -t <image_name> .`
- run container `docker run -d --restart unless-stopped <image_name>`

### Notes

The vasa-cron job will run every hour at the 28 and 58 minute marks.  
This will result in continuous polling of available classes for the next few minutes.  
Check logging from std::out in the Docker container's `/var/log/cron.log`  