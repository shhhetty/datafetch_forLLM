# Data & Prompt Engineering Pipeline for AI Quality Scoring

> This repository is the data engineering foundation for our AI-assisted assortment quality scoring system. It is an automated ETL pipeline that curates product data and programmatically assembles the complex, retailer-specific prompts needed to guide a powerful LLM like Gemini 2.5 Pro.

## 1. The Business Problem
To use a state-of-the-art LLM for a nuanced task like "scoring assortment quality," we must provide it with two things: 1) the specific product data for the assortment, and 2) a detailed set of instructions (a "prompt rubric") on how to score it. Because each of our retailers has different data formats and business rules, manually creating this combined payload for every keyword was the primary bottleneck in our QA workflow.

## 2. My Solution: A Prompt-Aware ETL Pipeline
I designed and built a configuration-driven Python pipeline that automates this entire preparation process. It treats the prompt itself as a key piece of data, managed and assembled by the system.

**Architectural Breakdown:**
1.  **Configuration-Driven:** The system is controlled by retailer-specific configurations. Each configuration defines what data fields to extract and points to the correct prompt template.
2.  **Data Extraction (The "E"):** The pipeline fetches the raw product attributes for a given assortment.
3.  **Prompt & Data Transformation (The "T"):** This is the core logic. The pipeline retrieves the appropriate prompt rubric (the detailed scoring instructions) for the given retailer. It then meticulously injects the cleaned product data into this prompt template.
4.  **Structured Output (The "L"):** The final output is a perfectly structured "gem" file (in JSON format). This file contains the complete, ready-to-use payload: the full prompt with all instructions, rules, and the embedded product data. This gem is the direct input for the user-facing `sensical_modelbased` tool.

## 3. Technologies & Skills
-   **Language:** Python
-   **Libraries:** Pandas, JSON
-   **Core Skills:**
    -   **Data Engineering** & **ETL Pipeline Development**
    -   **Advanced Prompt Engineering** (Systemic management of prompt templates)
    -   **System Architecture** (Configuration-Driven Design)
    -   **MLOps** (Data preparation for AI systems)

## 4. The Impact
-   **Foundation of the AI Workflow:** This pipeline is the critical backend that makes the entire AI scoring system possible.
-   **Ensured Consistency:** Guarantees that every evaluation uses the exact same data format and scoring rubric, eliminating process errors.
-   **Massive Time Savings:** Automates the most tedious and error-prone part of the workflow, allowing the QA team to focus on evaluation, not preparation.

## How to Run Locally
1. Clone the repository:
    git clone https://github.com/shhhetty/datafetch_forLLM.git

2. Navigate to the project directory:
    cd datafetch

3. Install dependencies:
    pip install -r requirements.txt

4. Run the app:
    streamlit run streamlit_app.py
