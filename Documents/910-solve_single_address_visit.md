The issue arises because the rewrite rule in your Apache configuration is redirecting requests to `/server-status` to `index.html`. To resolve this, we need to explicitly exclude `/server-status` from the rewrite rules.

### Updated Configuration File

Modify your `000-default.conf` as follows:

```apache
<VirtualHost *:80>
    ServerName www.xxxxx.com
    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        RewriteEngine On
        # Exclude /server-status from being rewritten
        RewriteCond %{REQUEST_URI} !=/server-status
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule ^ /index.html [L]
    </Directory>

    <Location "/server-status">
        SetHandler server-status
        Require local
    </Location>
</VirtualHost>
```

### Explanation of Changes

- **`RewriteCond %{REQUEST_URI} !=/server-status`**: Ensures requests to `/server-status` are not redirected to `index.html`.
- The rest of the configuration remains the same.

### Apply the Changes

1. Save the updated configuration file.
2. Restart Apache to apply the changes:
   ```bash
   sudo systemctl restart apache2
   ```

### Test the Changes

1. Visit `http://www.xxxxx.com/about` to confirm React routing still works.
2. Visit `http://localhost/server-status` or `http://localhost/server-status?auto` to confirm the server status page is accessible locally.

This should resolve the issue. Let me know if you encounter further problems!
