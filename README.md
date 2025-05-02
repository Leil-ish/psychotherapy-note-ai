# Clinical AI Prompt Engineer Take-Home Exercise - Upheal

## Project Overview

This repository contains the submission for the practical exercise component of the interview process for the Clinical AI Prompt Engineer role at Upheal. The goal of this project was to demonstrate the ability to acquire clinical data (a therapy session transcript), design and implement prompts for a Large Language Model (LLM) to generate structured clinical notes (SOAP, MSE, Risk Assessment), evaluate the output, and iteratively refine the prompt for improved quality.

## Methodology & Project Steps

The project followed these key steps:

1.  **Data Acquisition & Preparation:**
    * Selected and downloaded a therapeutic session video from YouTube using `yt-dlp`.
    * Extracted the audio track from the video.
    * Transcribed the audio using OpenAI's `Whisper` model to generate a text transcript using the medium model size.
    * Performed light cleaning/formatting on the transcript as needed.

2.  **Initial Prompt Design & Implementation (v1):**
    * Designed a structured prompt for the Google Gemini API Gemini 2.0 Flash instructing it to generate a clinical note including:
        * SOAP Note (Subjective, Objective, Assessment, Plan) for individual psychotherapy.
        * Mental Status Examination (MSE).
        * Risk Assessment.
    * Defined the expected information for each section within the prompt.
    * Used Python and the `google-generativeai` library to send the prompt and transcript to the Gemini API.
    * Generated the first version of the clinical note (`output_v1.txt`).

3.  **Output Analysis (Descriptive Statistics):**
    * Performed basic descriptive statistical analysis on the generated note (v1 and later v2), including:
        * Word counts per major section (SOAP, MSE, Risk).
        * Total word count.
        * Readability score.
        * Average sentence length.

4.  **Definition of Evaluation Criteria:**
    * Defined the following criteria for clinical evaluation of the generated note's quality:
        * **Criterion 1:** Clinical Accuracy: Does the note accurately reflect likely details from a standard therapy session without hallucinating facts or making unsupported interpretations? 
        * **Criterion 2:** Professional Tone & Objectivity: Does the tone match what would be expected from an experienced clinician AEB being nonjudgmental, objective, and appropriately detailed?
        * **Criterion 3:** Completeness: Are all requested sections (SOAP, MSE, Risk) present and appropriately addressed based on typical session content?
        * **Criterion 4:** Clinical Relevance/Salience: Does the note capture clinically significant information vs. conversational filler? 
        * **Criterion 5:** Responsible Risk Assessment: Are safety related details highlighted in a way that makes them easily accessible to a reviewer?

5.  **Iterative Prompt Refinement:**
    * Evaluated the first generated note (`output_v1.txt`) against the defined criteria.
    * Based on the evaluation, identified areas for improvement.
    * Adjusted the initial prompt to create a refined version (v2).
    * **Rationale for Adjustments:** *[User: Briefly explain *why* you made specific changes to the prompt - e.g., "Added stronger constraints against inference," "Clarified instructions for the MSE section," "Modified the role prompt for better tone," etc.]*

6.  **Generation of Improved SOAP Note (v2):**
    * Used the refined prompt (v2) with the same transcript to generate a second version of the clinical note (`output_v2.txt`) via the Gemini API.
    * Performed the same descriptive statistical analysis on this second version.

7.  **Final Evaluation & Comparative Analysis:**
    * Evaluated the second note (`output_v2.txt`) using the original criteria.
    * Compared the first and second versions, documenting improvements:
        * *[User: Summarize the key improvements observed between v1 and v2 based on your evaluation criteria and statistical analysis. Be specific - e.g., "Version 2 showed fewer unsubstantiated claims," "The MSE section was more comprehensive in v2," "Word count distribution across sections became more balanced," etc.]*

## Technology Stack

* **Programming Language:** Python 3.11
* **LLM API:** Google Gemini API (Model: `Gemini 2.0 Flash`) via `google-generativeai` library
* **Audio Transcription:** OpenAI Whisper (`medium`)
* **Audio Acquisition:** `yt-dlp`
* **Audio Processing:** `ffmpeg`
* **Data Analysis (Optional):** `[e.g., pandas, nltk, textstat - if used]`

## Repository Structure

├── data/
│   ├── transcript_cleaned.txt       # Cleaned transcript used for prompting
│   └── session_audio_new.mp3        # Downloaded audio file (or similar name)
│
├── prompts/
│   ├── prompt_v1.txt                # Initial prompt text
│   └── prompt_v2.txt                # Refined prompt text
│
├── scripts/
│   ├── 01_generate_note.py          # Python script to call Gemini API
│   └── 02_analyze_output.py         # Script for statistical analysis
│
├── outputs/
│   ├── output_v1.txt                # Clinical note generated by prompt v1
│   ├── output_v2.txt                # Clinical note generated by prompt v2
│   └── analysis_results.csv         # Results of statistical analysis
│
├── evaluation/
│   └──evaluation_output_v1.md       # Notes on the v1 evaluation process and findings
│   └──evaluation_output_v2.md       # Notes on the v2 evaluation process and findings
│
└── README.md                        # This file


## Setup and Usage

1.  **Clone Repository:** `git clone [Your Repo URL]`
2.  **Install Requirements:** `pip install -r requirements.txt` *(User: You may need to create a `requirements.txt` file)*
3.  **API Key:** Set your Google AI Studio API key as an environment variable: `export GOOGLE_API_KEY='YOUR_API_KEY'` (Linux/macOS) or `$env:GOOGLE_API_KEY='YOUR_API_KEY'` (Windows PowerShell).
4.  **Run Scripts:** Execute the Python scripts in order (if provided) or follow manual steps outlined in the code comments/notebooks.

## Results & Discussion

*[User: Add a summary paragraph discussing the overall success of the prompt refinement. Did the refined prompt (v2) produce a significantly better clinical note according to your criteria? Briefly mention any interesting findings or challenges encountered during the process.]*
