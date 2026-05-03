# Running JB2 as a Web App

## Prpare the Node Environmnet

```bash
# Switch to Node 20
nvm install 20
nvm use 20

# Install the MyST engine and PM2 (the process manager)
npm install -g mystmd pm2

# Install system libraries for image optimization (essential for your image-heavy pages)
sudo apt update
sudo apt install -y imagemagick inkscape webp
```

## Launch the Apps with PM2


```bash
cd /path/to/project1
pm2 start "myst start --headless --host 0.0.0.0 --port 3000" --name "nla"
```

```bash
cd /path/to/project2
pm2 start "myst start --headless --host 0.0.0.0 --port 3001" --name "genealogy"
```


## Make Sure they Stay Alive After Server Reboot

```bash
pm2 save
pm2 startup
```

## Configure Ngxin as the Gateway

For each subdomain running a JB2 app, create this: 

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name nla.krueckeberg.org;

    # Keep your existing redirect
    location / {
       return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;

    server_name nla.krueckeberg.org;

    # Your existing SSL certificates
    ssl_certificate /etc/letsencrypt/live/krueckeberg.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/krueckeberg.org/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # NEW: Proxy to the Jupyter Book 2 App
    location / {
        proxy_pass http://localhost:3000; # Use the port you assigned in PM2
        proxy_http_version 1.1;
        
        # Required for "App" features and instant updates
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Standard headers to pass the user's IP to the app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_cache_bypass $http_upgrade;
    }

    # Optional: Keep phpmyadmin if you still need it on this subdomain
    include snippets/phpmyadmin.conf;
}
```

### Enable and Restart nginx

```bash
sudo ln -s /etc/nginx/sites-available/jupyter_books /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 4: Secure with SSL (Highly Recommended)

```bash
sudo apt install python3-certbot-nginx
sudo certbot --nginx -d genealogy.yourdomain.com -d linux-docs.yourdomain.com
```

