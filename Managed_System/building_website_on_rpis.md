# Buinding website on RPIs

- [Buinding website on RPIs](#buinding-website-on-rpis)
  - [1. Install React](#1-install-react)
  - [2. Install Apache and run the web app from step1](#2-install-apache-and-run-the-web-app-from-step1)
  - [3. Put your website to public through cloudflare](#3-put-your-website-to-public-through-cloudflare)
    - [That's about it, good luck!](#thats-about-it-good-luck)

## 1. Install React

1. **Update your system.** It's needed, otherwise I found I couldn't install node.js with <br>
   `sudo apt update`

   This will get the update list (not actually install the packages)
   `Sudo apt upgrade`

2. **Install Node.js and npm**. React requires Node.js and npm (Node Package Manager) to run. <br>
   `sudo apt install curl`

   `curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - sudo` <br>

   `apt install nodejs`

   > Note: if you clone a repo from github, use `npm install` command to install all the dependencies in the first time.

3. **Verify Node.js and npm version** <br>
   use

   `node -v` and

   `npm -v`

4. **Create a new React project** <br>
   `npx create-react-app my-app` <br>
   `cd my-app` <br>
   `npm start`
5. **Create the app to release npm run build** <br>
   `npm run build`

   This will generates a 'build' directory that contains all the static files(html, css, javascript) necessary to run the React app.

## 2. Install Apache and run the web app from step1

1. **Update your system**, as in last step [Install React](#1-install-react)
2. **Install Apache**

   `sudo apt install apache2 -y`

   Once it's installed, Apache should start automatically. You can check if it's running by entering your Rpi's IP address (or just 'localhost' )in a browser, which shows a default apache page from `/var/www/html`.

3. **Copy 'build' folder to Rpi** Use whatever method. Simply you can just use a usb key. (or you can use ssh if you want).

   Then use this command to put the content of 'build' to folder /var/www/html (which is created by Apache by default):

   `sudo mv ~/build/* /var/www/html/`

   You may want to use this command to delete content if you mistake anything:

   `sudo rm -rf /var/www/html/*`

   Check the directory is empty by listing its contents:

   `ls /var/www/html`

4. **Check the website**. You can check if it's running by entering your Rpi's IP address (or just 'localhost' )in a browser

## 3. Put your website to public through cloudflare

**Knowledge**.
If you're using a education network which block port 22, the we will have to use Cloudflare Tunnel [https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/ ]

Cloudflare Tunnel can connect HTTP web servers, ssh servers to Cloudflare.

1. **Install cloudflared**

   download and install with command line tool according to the guideline.

2. **Authenticate cloudflared**

   `cloudflared tunnel login`

   If you Rpi is too slow to login, you can alternatively paste the info to your laptop to authenticate it.

3. **Create a tunnel and name it**

   `cloudflared tunnel create tunnel1`

   Here, I name it as 'tunnel1'. This command will

   1. generate a tunnel credentials file in the cloudflared directory on you Rpi,
   2. Create a subdomain of .cfargotunnel.com
   3. This command will return the tunnel's UUID which will be used in following steps

   > Use this command: `cloudflared tunnel list` to confirm that the tunnel has been successfully created.

4. **Create a configuration file**

   In your .cloudflared directory, created a config.yml file:

   ```
   url: http://localhost:8000
   tunnel: <Tunnel-UUID>
   credentials-file: /root/.cloudflared/<Tunnel-UUID>.json
   ```

   This will configure the tunnel to route traffic from a given origin to the hostname of your choice

5. **Start routing traffic**
   Assign a CNAME record that points traffic to your tunnel subdomain.

   usage: `cloudflared tunnel route dns <UUID or NAME> <hostname>`

   e.g.: `cloudflared tunnel route dns tunnel1 arthurqiangli.com`

   use the following command to see if the route has been successfully established, you can also check it on your cloudflared account.

   `cloudflared tunnel route ip show`

6. **Run the tunnel**

   Run the tunnel to proxy incoming traffic from the tunnel to services(unlimited) running on you RPI :

   usage: `cloudflared tunnel run <UUID or NAME>`

   e.g.: `sudo cloudflared tunnel run tunnel1`

### That's about it, good luck!
