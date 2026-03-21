# Songhay IT Glossary — RAG Demo

A retrieval-augmented generation (RAG) app that lets you query a trilingual
IT glossary (English / French / Songhay) using natural language.

---

## Local Development

### Prerequisites
- GitHub account with repository access.
- Git CLI.
- PostgreSQL with pgvector extension.
- Python 3.10 or higher.

### Setup on macOS/Linux
1. **Clone the Repository**
   ```bash
   cd /path/to/put/project/in
   git clone https://github.com/Afudu/Songhay_RAG_Demo.git

2. **Move to the folder**
   ```bash
   cd Songhay_RAG_Demo

3. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   
4. **Activate Environment**
   ```bash
   source venv/bin/activate 

5. **Securely upgrade pip**
   ```bash
   python -m pip install --upgrade pip 

6. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
7. **To deactivate Environment**
   ```bash
   deactivate

### Setup on Windows

1. Follow the steps above.

2. To activate the environment:
   ```bash
   .\venv\Scripts\Activate

### Set up PostgreSQL + pgvector
```bash
psql -U postgres -f setup_db.sql
```

### Add Excel file
Place `it_maanatiira.xlsx` in the project folder.
Expected columns: English, Francais (or Français), Sonay (or Soŋay / Songhay)

### Configure environment (python-decouple)
Create .env file in the project folder with the required variables.

### Running the application
```bash
streamlit run app.py
```
First run indexes the Excel file into pgvector.
Subsequent runs use the cached index. 
To force re-index, set `pre_delete_collection=True` in app.py temporarily.

### Linting and Testing

- **Run Linting**
  ```bash
  flake8

- **Run Unit Tests**
  ```bash
  pytest

## Deploy to OCI


### Deployment Prerequisites

- OCI instance with Python and PostgreSQL installed.
- PostgreSQL configured with pgvector extension.
- GitHub repository with the project code and GitHub Actions workflow set up for deployment.
- Add all .env variables as GitHub Secrets.

### Steps to Deploy
1. Push changes to the main branch.
2. The pipeline will:
   - Build and test the code.
   - Deploy to the OCI instance if tests pass.

[//]: # (### Live Application)

[//]: # ()
[//]: # (- The app is live at: http://92.5.67.11/glossary/)