# Generic ETL Data Processing Engine

A modular Python-based ETL (Extract, Transform, Load) engine designed to automate data extraction, cleaning, validation, quality reporting, rejection handling, and loading of valid records into PostgreSQL.

The project was built as a practical data engineering project and is designed to be extended for larger and more complex datasets.

---

## Project Overview

Real-world datasets are rarely clean.

Data can contain:

* Missing values
* Incorrect data types
* Negative values where they are not expected
* Inconsistent text formatting
* Empty rows
* Duplicate records
* Invalid records
* Unexpected values

This ETL engine provides a structured pipeline to process such data.

### Pipeline


                RAW DATA
                   │
                   ▼
             ┌───────────┐
             │  EXTRACT  │
             │   Excel   │
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │ TRANSFORM │
             │   Clean   │
             │   Data    │
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │  VALIDATE │
             │  Quality  │
             │   Checks  │
             └─────┬─────┘
                   │
            ┌──────┴──────┐
            │             │
            ▼             ▼
      VALID RECORDS   INVALID RECORDS
            │             │
            │             ▼
            │       ┌─────────────┐
            │       │  QUARANTINE │
            │       └─────────────┘
            │
            ▼
       ┌───────────┐
       │   LOAD    │
       │ PostgreSQL│
       └───────────┘
```

---

#  Features

## 1. Data Extraction

The engine extracts data from Excel files using Pandas.

Example:

```python
df = pd.read_excel(file_path)
```

The input file location is configurable rather than being permanently embedded into the transformation logic.

---

## 2. Data Transformation

The transformation layer cleans and standardizes raw data.

Current transformations include:

### Empty row removal

Completely empty records are removed before further processing.

### Amount cleaning

The engine converts values such as:

```text
500
5000
"4500"
-500
```

into a consistent numeric format.

For example:

```text
"4500" → 4500.0
```

### City standardization

Text values are cleaned and standardized.

For example:

```text
mysore
MYSORE
 Mysore
```

can be standardized to:

```text
Mysore
```

---

#  3. Data Validation

After transformation, the dataset is checked for quality issues.

The current validation layer checks:

* Total number of records
* Missing customer values
* Missing amount values
* Negative amounts
* Missing city values
* Duplicate records

Example data-quality report:

```text
DATA QUALITY REPORT

total_records: 5
missing_customer: 0
missing_amount: 1
negative_amount: 1
missing_city: 0
duplicate_records: 0
```

This provides a quick overview of the quality of the incoming dataset.

---

#  4. Invalid Record Detection

Records that fail validation are separated from valid records.

Example:

```text
VALID RECORDS:

customer  Amount       City
Rahul     500.0        Bangalore
Rahul     5000.0       Bangalore
Ravi      4500.0       Bangalore
```

Invalid records:

```text
INVALID RECORDS:

customer  Amount    City
Anil      NaN       Mysore
Suresh    -500.0    Mysore
```

This prevents invalid data from being loaded into the main database table.

---

#  5. Rejection Report

The engine creates a rejection report explaining why each invalid record was rejected.

Example:

```text
REJECTION REPORT:

customer  Amount    City    rejection_reason
Anil      NaN       Mysore  Missing Amount
Suresh    -500.0    Mysore  Negative Amount
```

This provides traceability for rejected records and makes it easier to investigate data-quality problems.

---

#  6. Quarantine System

Invalid records are not simply deleted.

Instead, they are separated and stored through the quarantine component.

This creates a basic data-quality workflow:

```text
Raw Data
   │
   ├── Valid ────────► PostgreSQL
   │
   └── Invalid ──────► Quarantine
```

The quarantine approach makes it possible to inspect rejected records later instead of losing them.

---

#  7. PostgreSQL Loading

Valid records are loaded into PostgreSQL.

The project uses:

* PostgreSQL
* SQLAlchemy
* Psycopg

The valid dataset is loaded into a database table such as:

```text
sales
```

Example:

```sql
SELECT * FROM sales;
```

Output:

```text
 customer | Amount |   City
----------+--------+-----------
 Rahul    |    500 | Bangalore
 Rahul    |   5000 | Bangalore
 Ravi     |   4500 | Bangalore
```

---

#  8. Environment Variable Security

Database credentials are not hard-coded into the production version of the code.

The project uses a `.env` file for sensitive credentials.

Example:

```text
DB_PASSWORD=your_postgresql_password
```

The `.env` file is excluded from Git using `.gitignore`.

A `.env.example` file is provided as a safe configuration template.

This prevents accidentally exposing database credentials in a public repository.

---

#  9. Configuration Management

Database and input configuration are separated from the main ETL logic.

Example configuration:

```yaml
input_file: "data/input.xlsx"

database:
  host: "localhost"
  port: 5432
  database: "etl_project"
  username: "postgres"
```

This makes the project easier to configure without modifying the core Python code.

---

#  10. Logging

The project includes an ETL logging system.

Important stages are logged, including:

```text
ETL process started
Data extraction completed
Transformation completed
Validation completed
Data loaded successfully
```

Errors are also recorded.

For example:

```text
Data extraction failed
Transformation failed
Data validation failed
Data loading failed
```

Logging makes the ETL pipeline easier to monitor and debug.

---

#  Project Structure

```text
ETL Project/
│
├── main.py
│
├── config/
│   └── config.yaml
│
├── config_loader.py
│
├── logger.py
│
├── Load/
│   └── database_loader.py
│
├── Transform/
│   └── transform.py
│
├── validation/
│   └── validate.py
│
├── quarantine/
│   └── quarantine.py
│
├── data/
│   └── input.xlsx
│
├── logs/
│   └── etl.log
│
├── requirements.txt
│
├── .env.example
│
└── .gitignore
```

Generated files such as the local `.env`, logs, input Excel files, rejected CSV files, and Python cache files are excluded from the public repository where appropriate.

---

#  End-to-End Workflow

The complete pipeline works as follows:

### Step 1 — Extract

The engine reads the input dataset.

```text
Excel → Pandas DataFrame
```

### Step 2 — Transform

The raw data is cleaned.

```text
Raw Data
   ↓
Remove empty rows
   ↓
Clean numeric fields
   ↓
Standardize text fields
```

### Step 3 — Validate

The cleaned data is checked for quality issues.

```text
Missing values
Negative values
Duplicates
Invalid records
```

### Step 4 — Separate

The dataset is divided into:

```text
VALID RECORDS
        +
INVALID RECORDS
```

### Step 5 — Generate Rejection Report

Invalid records receive a reason for rejection.

```text
Missing Amount
Negative Amount
...
```

### Step 6 — Quarantine

Invalid records are stored separately.

### Step 7 — Load

Only valid records are loaded into PostgreSQL.

```text
Valid Data → PostgreSQL
```

### Step 8 — Logging

Important ETL events and errors are recorded in the logging system.

---

#  Example Dataset

The current demonstration dataset contains intentionally problematic records to demonstrate the validation pipeline.

Example:

```text
customer  Amount       City
Rahul     500           Bangalore
Anil      NaN           Mysore
Rahul     5000          Bangalore
Ravi      "4500"        Bangalore
Suresh    -500          mysore
```

The engine identifies:

```text
Anil
→ Missing Amount

Suresh
→ Negative Amount
```

And transforms:

```text
"4500" → 4500.0

mysore → Mysore
```

The resulting valid records are loaded into PostgreSQL.

---

#  Technologies Used

| Technology    | Purpose                            |
| ------------- | ---------------------------------- |
| Python        | ETL application                    |
| Pandas        | Data extraction and transformation |
| NumPy         | Data processing                    |
| PostgreSQL    | Database                           |
| SQLAlchemy    | Database connectivity and loading  |
| Psycopg       | PostgreSQL driver                  |
| PyYAML        | Configuration management           |
| python-dotenv | Environment variable management    |
| Logging       | Pipeline monitoring                |
| Git           | Version control                    |
| GitHub        | Source-code hosting                |

---

#  Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd ETL-Project
```

---

## 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

#  Configuration

Create a `.env` file in the project root:

```text
DB_PASSWORD=your_postgresql_password
```

Do not commit this file.

The repository contains:

```text
.env.example
```

as a template.

Update the database configuration in:

```text
config/config.yaml
```

Example:

```yaml
input_file: "data/input.xlsx"

database:
  host: "localhost"
  port: 5432
  database: "etl_project"
  username: "postgres"
```

---

#  Running the ETL Pipeline

From the project root:

```powershell
python main.py
```

The pipeline will:

1. Extract the input data
2. Transform the data
3. Validate the data
4. Generate a quality report
5. Separate valid and invalid records
6. Generate a rejection report
7. Quarantine rejected records
8. Load valid records into PostgreSQL
9. Record important events in the log

---

#  Checking the Database

After the pipeline runs, connect to PostgreSQL:

```bash
psql -U postgres -d etl_project
```

Then check the loaded table:

```sql
SELECT * FROM sales;
```

To inspect the table structure:

```sql
\d sales
```

---

#  Current Output

For the demonstration dataset, the pipeline identifies:

```text
Total Records: 5

Missing Customer: 0
Missing Amount: 1
Negative Amount: 1
Missing City: 0
Duplicate Records: 0
```

Three valid records are loaded into PostgreSQL.

Two records are rejected:

```text
Anil  → Missing Amount
Suresh → Negative Amount
```

---

#  Design Goals

The project is designed around several principles:

### Modularity

Different ETL responsibilities are separated into different modules.

```text
Transform
Validation
Quarantine
Load
Configuration
Logging
```

### Reusability

The engine is designed so that transformation and validation functions can be expanded for additional datasets.

### Traceability

Invalid records are not silently discarded.

The system records why records were rejected.

### Security

Database credentials are separated from source code using environment variables.

### Maintainability

Configuration, transformation, validation, loading, and logging are kept separate.

---

#  Current Limitations

The current version is a **working prototype/portfolio project**, not a production-scale enterprise ETL platform.

Current limitations include:

* The demonstration input dataset is small.
* The current transformation rules are tailored to the fields used in the example dataset.
* Validation rules are currently implemented for specific data-quality checks.
* The pipeline currently uses Excel as the demonstration input source.
* PostgreSQL is currently used as the target database.
* There is no orchestration/scheduling system yet.
* There is no automated test suite yet.
* Large-scale distributed processing is not implemented.

These limitations provide opportunities for future development.

---

#  Future Improvements

Planned improvements include:

## 1. Generic Schema Detection

Automatically identify:

* Numeric columns
* Date columns
* Text columns
* Missing-value patterns
* Potential identifier columns

---

## 2. More Data Sources

Support additional sources such as:

```text
CSV
Excel
JSON
APIs
SQL databases
```

---

## 3. More Validation Rules

Add configurable checks for:

```text
Missing values
Duplicates
Outliers
Invalid dates
Invalid categorical values
Range violations
Data-type mismatches
Referential integrity
```

---

## 4. Configurable Validation Rules

Instead of hard-coding validation logic, allow validation rules to be defined through configuration.

For example:

```yaml
validation:
  Amount:
    allow_negative: false
    required: true

  City:
    required: true
```

---

## 5. Automated Testing

Add unit tests for:

```text
Transformation
Validation
Quarantine
Database loading
Configuration
```

using Python testing frameworks.

---

## 6. ETL Pipeline Orchestration

The project can eventually be integrated with orchestration tools such as:

```text
Apache Airflow
AWS Glue
```

for scheduled and automated workflows.

---

## 7. Cloud Integration

Future versions could support cloud storage and databases such as:

```text
AWS S3
AWS RDS
Azure Blob Storage
Google Cloud Storage
```

---

## 8. Data Quality Dashboard

A future dashboard could display:

```text
Total Records
Valid Records
Rejected Records
Missing Values
Duplicate Records
Validation Errors
ETL Execution Time
```

using tools such as Power BI or a web dashboard.

---

#  Learning Objectives

This project was created to develop practical understanding of:

* ETL architecture
* Python data processing
* Pandas
* Data cleaning
* Data validation
* Data-quality management
* Error handling
* Logging
* PostgreSQL
* SQLAlchemy
* Database loading
* Configuration management
* Environment variables
* Git and GitHub
* Modular Python project design

---

#  Project Status

**Status: Working Prototype / Portfolio Project**

The current pipeline successfully demonstrates:

```text
Excel
  ↓
Extraction
  ↓
Transformation
  ↓
Validation
  ↓
Rejection Handling
  ↓
PostgreSQL
```

The project is actively designed for further expansion into a more generic and competition-ready ETL engine.

---

#  License

This project is intended for educational and portfolio purposes.

A license can be added when the repository is published publicly.

---

##  If you find this project useful

Feel free to explore the code, suggest improvements, or use the architecture as a learning reference for building Python ETL pipelines.
