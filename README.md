# Macuco Web App

Web application developed for **Bioparque Macuco**, focused on course management and sales offered by the park.

## Prerequisites

Before getting started, make sure you have the following tools installed:

- **Git** — [How to install Git](https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)
- **Docker** — [Docker installation](https://docs.docker.com/get-started/get-docker/)
- **Conda (Miniconda)** — [Miniconda installation](https://docs.anaconda.com/miniconda/install/)

## Quick Start

### 1. Clone the repository

If you've never cloned a repository before, check out this guide:
[How to clone a Git repository](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository)

You can clone using **SSH** or **HTTPS**:

#### Option A: SSH (recommended)

You need to generate an SSH key and add it to your GitHub account.
Follow this guide: [Generating a new SSH key and adding it to GitHub](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

Then clone:

```bash
git clone git@github.com:Bioparque-Macuco/macuco-web-app.git
cd macuco-web-app
```

#### Option B: HTTPS

You need to generate a Personal Access Token (PAT) to use as your password.
Follow this guide: [Creating a personal access token](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#criar-um-personal-access-token-classic)

Then clone (you'll be prompted for your username and token):

```bash
git clone https://github.com/Bioparque-Macuco/macuco-web-app.git
cd macuco-web-app
```

### 2. Set up Conda environment

After installing Miniconda in your home directory, activate it:

**Linux / macOS:**

```bash
source miniconda3/bin/activate
conda init
```

**Windows (PowerShell):**

```powershell
.\miniconda3\Scripts\activate
conda init
```

> On Windows you can also use the **Anaconda Prompt** that comes with the Miniconda installation.

Then create and activate the project environment:

```bash
conda create -n macuco_env python=3.13
conda activate macuco_env
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and set your own password:

**Linux / macOS:**

```bash
cp .env.example .env
```

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

Then edit the `.env` file and change `POSTGRES_PASSWORD` to a password of your choice.

### 5. Start the database

With Docker installed, run:

```bash
docker compose up -d
```

This will start a PostgreSQL container using the credentials defined in your `.env` file.
