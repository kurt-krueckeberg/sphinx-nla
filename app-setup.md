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
    server_name genealogy.yourdomain.com; # Project 1

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

server {
    listen 80;
    server_name linux-docs.yourdomain.com; # Project 2

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
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

