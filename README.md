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
Place .env in the project folder with the following variables:

| Variable                   | Description                     | Default                |
|----------------------------|---------------------------------|------------------------|
| AZURE_OPENAI_API_KEY       | Your Azure OpenAI key           | required               |
| AZURE_OPENAI_ENDPOINT      | Your resource endpoint URL      | required               |
| AZURE_OPENAI_API_VERSION   | API version                     | 2024-02-01-preview     |
| AZURE_DEPLOYMENT_NAME      | Chat model deployment name      | gpt-4o                 |
| AZURE_EMBEDDING_DEPLOYMENT | Embedding model deployment name | text-embedding-ada-002 |
| PG_CONNECTION_STRING       | PostgreSQL connection string    | required               |
| GLOSSARY_DATA_PATH         | Path to glossary Excel file     | it_maanatiira.xlsx     |

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
Add all .env variables as GitHub Secrets.

### Deployment Prerequisites

- OCI instance with Python and PostgreSQL installed.
- PostgreSQL configured with pgvector extension.
- GitHub repository with the project code and GitHub Actions workflow set up for deployment.

### Steps to Deploy
1. Push changes to the main branch.
2. The pipeline will:
   - Build and test the code.
   - Deploy to the OCI instance if tests pass.

   **Note:** Changes to non-main branch only trigger the build-and-test step.

### Live Application

- The app is live at: http://92.5.67.11/glossary/