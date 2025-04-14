# Capstone 2024-2025

## Server Setup

1. Clone the Repository

```bash
git clone https://github.com/rkbhamra/NG03_CAPSTONE2024-25.git
```

2. Setup the python environment and install the required packages

```bash
pip install -r requirements.txt
```

3. Before running the server, update the Hosting IP Address

- Find your current IP address by running the command:

  ```bash
  ipconfig
  ```

  Look for the `IPv4 Address` under your active network connection.

- Open `server.py` and replace `<your-current-ip>` with your IP address:

  ```python
  app.run(host='<your-current-ip>', port=5000, debug=True)
  ```

4. Run the Python Server

```bash
python server.py
```

## App Setup

- Visit the [Releases](https://github.com/rkbhamra/NG03_CAPSTONE2024-25/releases) page of the repository.
- Download the latest `.apk` file available.

