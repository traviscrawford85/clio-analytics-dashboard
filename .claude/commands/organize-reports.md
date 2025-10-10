# Project Directory Structure Setup

This document outlines the standardized folder structure for organizing business reports, automation scripts, and documentation within the project repository.

---

## 📁 Reports

All `.csv`, `.xlsx`, and other structured data files should be organized by business domain:

```bash
mkdir -p reports/{task_reports,matter_reports,custom_field_reports,contact_reports}


reports/task_reports/: Stores task-related reports and exports.

reports/matter_reports/: Legal matter-specific data and analysis.

reports/custom_field_reports/: Reports and exports of custom field configurations.

reports/contact_reports/: Contact and client export data.

🧠 Scripts

Place all Python and other automation scripts in a centralized scripts/ directory. This encourages reuse, visibility, and version control.

mkdir -p scripts


Scripts should be:

Modular and reusable

Named using snake_case (e.g., export_contacts.py)

Logged to stdout and/or logs/ if applicable

Optional: categorize by domain if many scripts exist:

mkdir -p scripts/{tasks,matters,contacts,custom_fields}


📁 Documentation

All written documents should be placed in the docs/ folder:

mkdir -p docs

Include:

README.md: overview of the project or submodules

CHANGELOG.md: update history

architecture_overview.md: diagrams or system design

.docx, .pdf, .md formats

📂 Final Command

Run the following to scaffold the project structure:

mkdir -p reports/{task_reports,matter_reports,custom_field_reports,contact_reports} \
         scripts \
         docs

Optionally, extend it for script subfolders:

mkdir -p reports/{task_reports,matter_reports,custom_field_reports,contact_reports} \
         scripts/{tasks,matters,contacts,custom_fields} \
         docs
