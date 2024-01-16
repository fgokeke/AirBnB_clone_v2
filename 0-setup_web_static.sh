#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static

# Install Nginx if it's not already installed
if ! command -v nginx >/dev/null 2>&1; then
	sudo  apt-get update
	sudo apt-get install -y nginx
fi

# Create the necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Create a symbolic link, deleting the old link if it exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the 'ubuntu' user and group
sudo chown -hR ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content

sudo sed -i '/^\}$/i \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo service nginx start

exit 0
