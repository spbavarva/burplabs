Generated from GPT for now!

# PortSwiggerLab

**PortSwiggerLab** is a modular, Python-based CLI tool that automates solving labs from [PortSwigger Web Security Academy](https://portswigger.net/web-security).  
Think of it like `netexec`, but made for web app hacking.

---

## 🔧 Features

- 🚀 CLI interface for quickly solving labs
- 🧱 Modular architecture – each lab is a standalone Python file
- 🧠 Auto-discovery of all labs via `--list-labs`
- 🌐 Proxy support (`--proxy`, `--no-proxy`)
- 🐳 Docker-compatible
- 🔄 Easily extensible – add your own labs!

---

## 📦 Installation

(More options will be added)

### 🔹 Option 1: Install from GitHub (recommended)

```bash
pip install git+https://github.com/spbavarva/portswigger-labs-scripts.git
````

### 🔹 Option 2: Clone and Install Locally

```bash
git clone https://github.com/spbavarva/portswigger-labs-scripts.git
cd portswiggerlab
pip install .
```

---

## 🧪 Usage

### 🔹 View Help

```bash
portswiggerlab -h
```

### 🔹 List All Available Labs

```bash
portswiggerlab --list-labs
```

### 🔹 Solve a Lab

```bash
portswiggerlab sql_lab1 --url https://example.net/filter?category= --payload "'+OR+1=1--"
```

### 🔹 Disable Proxy

```bash
portswiggerlab sql_lab1 --url https://... --payload "..." --no-proxy
```

### 🔹 Use Custom Proxy

```bash
portswiggerlab sql_lab1 --url https://... --payload "..." --proxy http://127.0.0.1:8081
```

---

## 🧩 Adding New Labs

To add a new lab:

1. Create a new file in `portswiggerlab/labs/`, e.g. `sql_lab3.py`
2. It must define a `run(url, payload, proxies=None)` function
3. That’s it! The lab will be auto-detected and usable like:

```bash
portswiggerlab sql_lab3 --url ... --payload ...
```

---

## 🐳 Docker Support

Build the image:

```bash
docker build -t portswiggerlab .
```

Run it:

```bash
docker run --rm portswiggerlab sql_lab1 --url ... --payload ... --no-proxy
```

---

## ✨ Example Output

```bash
portswiggerlab sql_lab2 --url https://target/login --payload "administrator'--" --no-proxy

[+] Lab solved successfully!
```

---

## 🧠 Author

Built with 🔥 by [Sneh](https://github.com/YOUR_USERNAME)
If you like it, give it a ⭐ on GitHub!

---

## 📜 License

MIT License

````

---

## 📌 What to Do Now

1. Copy the above into `README.md`
2. Update `YOUR_USERNAME` with your actual GitHub username
3. Commit & push it:

```bash
git add README.md
git commit -m "Add complete README documentation"
git push
````