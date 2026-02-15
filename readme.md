# AD Applicability Extractor

## Overview

This project implements an **LLM-based system** to extract structured information from **Airworthiness Directives (AD)** documents and determine aircraft applicability (e.g., *Affected* vs. *Not affected*).

The system focuses on:

* Extracting structured applicability rules from AD documents
* Mapping aircraft models, MSN (Manufacturer Serial Number), and modification status
* Determining whether a specific aircraft is affected by a given AD
* Validating extraction accuracy through evaluation tests

The project is built using:

* **LangChain** (LLM orchestration)
* **Pydantic** (structured data modeling & validation)
* **PyPDF2** (PDF document parsing)

## Installation

### 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd ad-applicability-extractor
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

* **Linux / macOS**

  ```bash
  source venv/bin/activate
  ```

* **Windows**

  ```bash
  venv\Scripts\activate
  ```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=your_selected_model
```

## Usage

### 🔍 Extract Applicability Rules from AD

Extract structured applicability data from an AD document:

```bash
python main.py extract --ad pdf\EASA_AD_2025-0254R1_1.pdf
```

This will output the parsed AD structure, including aircraft models, MSN constraints, and modification rules.


### ✈️ Check Aircraft Applicability

Check whether a specific aircraft is affected by an AD:

```bash
python main.py check \
  --ad pdf\EASA_AD_2025-0254R1_1.pdf \
  --model A320-214 \
  --msn 4500 \
  --mod None
```

Example output:

```
The aircraft IS affected by this AD.
```

or

```
The aircraft is NOT affected by this AD.
```



## Evaluation

To evaluate the system using predefined test cases for the two AD documents:

```bash
python evaluate.py
```

This will:

* Run multiple aircraft scenarios
* Compare predicted results with expected outputs
* Assert correctness
* Print evaluation results


## Current Limitations

* Prompt optimization is based on only two AD documents.
* Rules may not fully generalize to different AD formats.
* No fine-tuning has been applied yet.
* Applicability logic assumes no cross-model modification interaction.



## Future Improvements

* Expand dataset with more AD documents
* Improve rule generalization
* Explore fine-tuning or VLM-based extraction
