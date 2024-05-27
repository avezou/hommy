# Hommy
A minimalist dashboard for your homelab.

## Introduction
Yes, yet another dashboard. However, this one is built with simplicity and functionality in mind, tailored for personal use. I created Hommy to aggregate my services, providing a way to filter by tags, categories, and perform fuzzy searches. Existing solutions didn't meet these specific needs, so I developed Hommy and decided to share it with the community.

While there are many capable dashboards available, such as those listed on the [Awesome Self Hosted GitHub page](https://github.com/awesome-selfhosted/awesome-selfhosted), Hommy stands out with its minimalist design and limited configuration options.

This dashboard is designed to run on LXC containers or a local machine, as I prefer LXCs over Docker containers.

## Example
![](https://github.com/avezou/hommy/example.gif)

## Installation
To install Hommy, follow these steps:

1. Clone this repository or download the archive from GitHub:
   ```bash
   git clone https://github.com/avezou/hommy.git
   ```

2. Change to the cloned **_hommy_** directory.

3. Copy the **_.env.example_** file to **_.env_** and update the secret key value:
   ```bash
   SECRET_KEY=super_secret_hard_to_guess_or_crack_key_here
   UPLOAD_PATH='static/uploads'
   ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'svg', 'gif'])
   ```

4. Make the `start.sh` script executable:
   ```bash
   chmod +x start.sh
   ```

5. Start the application:
   ```bash
   ./start.sh
   ```

The application will be available at `http://localhost_or_ip:8000`.

## Running with Systemd
To run Hommy using **_systemd_**, create a `hommy.service` file or copy the provided one to the appropriate location:

- Copy `hommy.service` to:
  ```bash
  /etc/systemd/system/hommy.service
  ```
  or
  ```bash
  /lib/systemd/system/hommy.service
  ```

- Modify the paths in the service file to match your Hommy installation:
  ```ini
  [Unit]
  Description=Hommy homelab dashboard
  After=network.target

  [Service]
  WorkingDirectory=/path_to_hommy_root_dir
  Environment=FLASK_CONFIG=production
  ExecStart=/path_to_hommy_dir/env/bin/gunicorn -w $(nproc) --threads 2 --max-requests 2 app:app
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

To manage Hommy with systemd, use the following commands:
```bash
sudo systemctl start hommy   # to start it
sudo systemctl stop hommy    # to stop it
sudo systemctl enable hommy  # to enable hommy to start on boot
```

## TODO
- Move some of the hardcoded values to environment variables for easier customization.
- Add Docker and Docker Compose installation options.
- Add error pages templates

## Contributing
Feel free to fork this repository, build on top of it, or create pull requests.

## Credits
Background Photo by Abdullah Ghatasheh: [Pexels](https://www.pexels.com/photo/calm-body-of-water-during-golden-hour-1631677/)

SVG icons copied from: https://github.com/simple-icons/simple-icons

## License
Hommy is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.