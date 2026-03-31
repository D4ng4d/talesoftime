# Tales of Time: RPG Management System

Welcome to the **Tales of Time** project. This is a Flask-based web application designed to manage characters, items, and quests for a tabletop RPG. This repository serves as your primary workspace for implementing a secure, relational Data Access Layer.

## 🛠 Technology Stack

* **Language:** Python 3.x
* **Web Framework:** Flask
* **Database:** SQLite 3
* **Data Access:** Raw SQL using the Repository Pattern

---

## 🚀 Getting Started

Follow these steps in sequence to set up your local development environment.

### 1. Clone the Repository
Open your terminal and run:
```bash
git clone [https://github.com/](https://github.com/)[YOUR-USERNAME]/talesoftime.git
cd talesoftime
```


2. Initialise the Database
This command creates the database skeleton and all 13 tables defined in your schema.

```bash
python -c "from models.models import init_db; init_db(); print('Database Skeleton Created Successfully!')"
```

3. Seed the Game Data
Populate your lookup tables and core entities with starting data to make the app functional.

```bash
python database/seed.py
```
4. Launch the Application
Start the Flask development server to view your project in the browser.

```bash
python app.py
```
Access the app at: http://127.0.0.1:5000

# 📝 Core Development Tasks

During this module, you are responsible for designing and implementing the core architectural components of the application. Development is structured into **three distinct phases**, each aligned with industry-standard software engineering principles, including separation of concerns, security, and maintainability.

---

## Phase 1: Database Schema

**File:** `database/schema.sql`

You will design and implement the relational database structure using **DDL SQL**, ensuring data integrity, normalisation, and long-term scalability.

### Responsibilities

#### Lookup Tables

Static reference tables used to enforce controlled vocabularies and reduce redundancy:

- `Classes`
- `Species`
- `Alignments`
- `Regions`

These tables should contain immutable or rarely changing data and be referenced via foreign keys.

#### Core Entities

Primary domain tables representing the main game data:

- `Characters`
- `Items`
- `Quests`

Each table must define:

- A clear primary key  
- Appropriate data types  
- Foreign key relationships where applicable  

#### Join Tables

Support **many-to-many relationships** required by the domain model, including:

- Character inventories  
- Quest history and progression tracking  

Join tables must enforce referential integrity using foreign key constraints.

---

## Phase 2: Connection Logic

**File:** `models/models.py`

You will implement the database access layer that bridges **Python** and **SQLite**, ensuring reliability and consistency across the application lifecycle.

### Responsibilities

#### Database Connection Factory: `get_db()`

The connection factory must:

- Enable relational enforcement using:

```sql
PRAGMA foreign_keys = ON;
``


# ✅ Common Git Commands (Quick Reference)

| Command | Purpose |
|-------|---------|
| `git status` | Shows which files have been modified, staged, or are untracked in your local workspace. |
| `git add .` | Stages **all changes** so they are ready to be committed. |
| `git commit -m "message"` | Saves a snapshot of your work locally with a clear description of what changed. |
| `git push origin main` | Sends your committed changes to the `main` branch on GitHub. |
| `Ctrl + C` | Safely stops a running Flask web server in the terminal. |

---

## ⚠️ Troubleshooting Guide

| Issue | What It Means | How to Fix It |
|-----|--------------|---------------|
| **Database is locked** | Another program is using the SQLite database. | Close any external tools such as **DB Browser for SQLite**, then restart the app. |
| **Foreign key constraint error** | You tried to delete data that is still linked elsewhere. | Check your schema and ensure `ON DELETE CASCADE` is set where appropriate. |
| **Missing or empty data** | The database has not been populated. | Make sure you have run `python database/seed.py` before starting the app. |

---

## ✅ If Something Breaks

1. Stop the server (`Ctrl + C`)
2. Run `git status`
3. Read the error message carefully
4. Fix **one issue at a time**
5. Commit once it works again
