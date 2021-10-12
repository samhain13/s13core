# S13Core
S13Core is a Django application that aims to help website developers to easily set-up and customise Django-based, content-driven websites.

## Setting up for development
It is recommended that you run a Python3 virtual environment.

1. Install dependencies:

        $ pip install -r requirements.txt

2. Take the sample website for a spin:

        $ ./manage.py runserver localhost:5000
    Navigate your browser to http://localhost:5000/

3. Make an S13Core clone and set it up for development:

        $ ./manage.py s13clone [project name]
        $ mv [project name] /other/location/on/disk/
        $ cd /other/location/on/disk/[project name]
        $ rm [project name]/sample-content.sqlite3
        $ ./manage.py s13setup
    The fifth command will make the necessary migrations and ask you for your app's superuser credentials. It will also ask you for some basic information like your website's title, a description, and some initial keywords. These are all required now but you can always change the values later on.

4. Run your development site:

        $ manage.py runserver localhost:5000
    Navigate your browser to http://localhost:5000/s13admin/ and login.

## Customisations
All of your website templates must be placed inside **/other/location/on/disk/[project name]/[project name]/templates** in order for s13core.content_management.views to find them. You can always change this location, among other things, in your settings file(s).

## Deployment
Install Apache2, Mod WSGI in your target system, and start with the following configuration:

        <VirtualHost *:80>
            ServerName www.server-name.com  # Your domain name.
            ServerAlias server-name.com     # Your domain name alias.
            ServerAdmin webmaster@server-name.com
            
            # Django/Python essentials:
            WSGIDaemonProcess server-name python-home=/path/to/venv python-path=/path/to/website
            WSGIProcessGroup server-name
            
            WSGIScriptAlias / /path/to/website/website/wsgi.py
            <Directory /path/to/website/website>
                <Files wsgi.py>
                    Require all granted
                </Files>
            </Directory>
            
            # Static files:
            Alias /static/ /path/to/website/website/static/
            <Directory /path/to/website/website/static>
                Require all granted
                
                RewriteEngine on
                RewriteBase /
                RewriteCond %{REQUEST_FILENAME} !-f
                RewriteRule (.*) x/x/x [P,L]
            </Directory>
            
            # All supposed DocumentRoot files like robots.txt are in the
            # falseroot directory.
            Alias "/placeholder.txt" /path/to/website/website/falseroot/placeholder.txt
            <Directory /path/to/website/website/falseroot>
                Require all granted
            </Directory>
        </VirtualHost>

Change all **/path/to/...** instances accordingly. By default, your website will be served using **website.settings.development**. You may change that by editing your website's wsgi.py file.

## Common Context Data Keys

The following keys are included in the context data passed by the public Content Management views to the Jinja templates:

* **s:** the active website settings *object*
* **article:** the requested article *object*, if any
* **articles:** a *list* of articles associated with the requested article, if any
* **sections:** a *list* of site section objects, if any

Additionally, the following keys are passed through the Jijna environment:

* **h:** the s13core helpers sub-module, which as some helper functions
* **reverse:** the reverse function from django.urls for creating internal links
* **get_messages:** messages.get_messages method for displaying system messages
* **dir:** python's built-in dir function to be used for debugging
