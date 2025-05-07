# Clinical AI Prompt Engineer Take-Home Exercise - Upheal

## Project Overview

This repository contains the submission for the practical exercise component of the interview process for the Clinical AI Prompt Engineer role at Upheal. The goal of this project was to demonstrate the ability to acquire clinical data (a therapy session transcript), design and implement prompts for a Large Language Model (LLM) to generate structured clinical notes (SOAP, MSE, Risk Assessment), evaluate the output using defined clinical criteria, perform comparative analysis, and iteratively refine the prompt for improved quality based on that evaluation.

## Methodology & Project Steps

The project followed these key steps:

1.  **Data Acquisition & Preparation (Annabeth Session):**
    * Selected and downloaded a therapeutic session video ("Annabeth" session) from YouTube using `yt-dlp`.
    * Extracted the audio track from the video.
    * Transcribed the audio using OpenAI's `Whisper` model (`medium` model size) to generate a text transcript.
    * Saved the cleaned transcript as `data/transcript_cleaned.txt`.

2.  **Initial Prompt Design & Implementation (v1):**
    * Designed a structured zero-shot prompt (`prompts/prompt_v1.txt`) for the Google Gemini API (using `Gemini 2.0 Flash`) instructing it to generate a clinical note including:
        * SOAP Note (Subjective, Objective, Assessment, Plan)
        * Mental Status Examination (MSE)
        * Risk Assessment
    * Defined the expected information for each section and included initial constraints.
    * Used Python (`scripts/01_generate_note.py`) and the `google-generativeai` library to generate the first version of the clinical note (`outputs/output_v1.txt`).

3.  **Definition of Evaluation Criteria:**
    * Defined the following criteria (see `evaluation/evaluation_criteria.txt`) for clinical evaluation of the generated note's quality:
        * **Criterion 1:** Clinical Accuracy: Does the note accurately reflect likely details from the transcript without hallucinating facts or making unsupported interpretations?
        * **Criterion 2:** Professional Tone & Objectivity: Does the tone match what would be expected from an experienced clinician AEB being nonjudgmental, objective, and appropriately detailed?
        * **Criterion 3:** Completeness: Are all requested sections (SOAP, MSE, Risk) present and appropriately addressed based on transcript content?
        * **Criterion 4:** Clinical Relevance/Salience: Does the note capture clinically significant information vs. conversational filler?
        * **Criterion 5:** Responsible Risk Assessment: Are safety related details highlighted in a way that makes them easily accessible and clinically appropriate?

4.  **Output Analysis (Descriptive Statistics):**
    * Developed a Python script (`scripts/02_analyze_output.py`) using `textstat` to perform descriptive statistical analysis on generated notes, calculating:
        * Total Word Count & Sentence Count
        * Average Sentence Length
        * Flesch-Kincaid Grade Level & Flesch Reading Ease
        * Word Count per major section (SOAP, MSE, Risk)
        * Sentence Count per SOAP subsection (Subjective, Objective, Assessment, Plan)
    * The script prints results to the console, which were then copied to `outputs/analysis_results.csv` for this submission.

5.  **Iterative Prompt Refinement (v1 -> v2):**
    * Evaluated the first generated note (`output_v1.txt`) against the defined criteria (see `evaluation/evaluation_output_v1.md`). The primary issue identified was a failure in **Clinical Accuracy** due to the LLM hallucinating visual details (e.g., client's grooming, eye contact) not present in the audio transcript.
    * Adjusted the initial prompt (`prompt_v1.txt`) to create a refined version (`prompt_v2.txt`).
    * **Rationale for Adjustments:** To address the visual hallucinations, a **CRITICAL constraint** was added to `prompt_v2.txt` explicitly prohibiting the generation of visual appearance details, eye contact, facial expressions (unless described as sounds), or gestures unless EXPLICITLY stated in the transcript. Instructions for the Objective and MSE sections were also modified to focus only on information derivable from audio/text and to clearly state when visual information was unavailable.

6.  **Generation of Improved Note (v2):**
    * Used the refined prompt (`prompt_v2.txt`) with the original Annabeth transcript to generate a second version of the clinical note (`outputs/output_v2.txt`) using `scripts/01_generate_note.py`.

7.  **Final Evaluation & Comparative Analysis (v1 vs. v2):**
    * Evaluated the second note (`output_v2.txt`) using the original criteria (see `evaluation/evaluation_output_v2.md`).
    * Ran the analysis script (`scripts/02_analyze_output.py`) to generate comparative statistics for `output_v1.txt` and `output_v2.txt` (console output copied to `outputs/analysis_results.csv`).
    * **Comparison Summary:** Version 2 demonstrated a significant improvement in **Clinical Accuracy** by successfully eliminating the visual hallucinations present in v1 and correctly noting when visual information was unavailable. This directly resulted from the targeted prompt refinements. Both versions performed well on Completeness, Relevance, and Tone. The statistical analysis quantified changes, such as the now accurate sentence counts for v1 SOAP subsections after parsing fixes, and word count adjustments reflecting the removal of hallucinated content from v2. This iteration clearly showed the effectiveness of specific constraint-based prompt engineering.

8.  **Supplemental Test Case (Risk Assessment Vignette):**
    * This was conducted as a separate project (`psychotherapy-note-ai-2`) to further validate the refined prompt (`prompt_v2.txt`) on specialized content.

## Technology Stack

* **Programming Language:** Python 3.11
* **LLM API:** Google Gemini API (Model: `Gemini 2.0 Flash`) via `google-generativeai` library
* **Audio Transcription:** OpenAI Whisper (`medium` model)
* **Audio Acquisition:** `yt-dlp`
* **Audio Processing:** `ffmpeg`
* **Text Analysis:** `textstat` library

## Repository Structure

├── data/
│   └── transcript_cleaned.txt       # Cleaned transcript (Annabeth session)
│   └── session_audio.mp3            # (Optional) Downloaded audio file
│
├── prompts/
│   ├── prompt_v1.txt                # Initial prompt text
│   └── prompt_v2.txt                # Refined prompt text
│
├── scripts/
│   ├── 01_generate_note.py          # Python script to call Gemini API
│   └── 02_analyze_output.py         # Script for statistical analysis (outputs comparison)
│
├── outputs/
│   ├── output_v1.txt                # Clinical note from Annabeth transcript + prompt v1
│   ├── output_v2.txt                # Clinical note from Annabeth transcript + prompt v2
│   └── analysis_results.csv         # Console output of comparative stats (v1 vs v2) copied here
│
├── evaluation/
│   ├── evaluation_criteria.txt      # Definition of evaluation criteria
│   ├── evaluation_output_v1.md      # Evaluation notes for output_v1.txt
│   └── evaluation_output_v2.md      # Evaluation notes for output_v2.txt & comparison
│
├── .gitignore                       # Standard Python gitignore
├── requirements.txt                 # Python package requirements
└── README.md                        # This file


## Setup and Usage

1.  **Clone Repository:** `git clone https://github.com/Leil-ish/psychotherapy-note-ai`
2.  **Install Requirements:** Ensure Python 3.11 and FFmpeg are installed. Then run: `pip install -r requirements.txt`
3.  **API Key:** Set your Google AI Studio API key as an environment variable: `$env:GOOGLE_API_KEY='YOUR_API_KEY'` (Windows PowerShell) or `export GOOGLE_API_KEY='YOUR_API_KEY'` (Linux/macOS).
4.  **Run Generation:**
    * To generate note v1: `python scripts/01_generate_note.py --prompt prompts/prompt_v1.txt --transcript data/transcript_cleaned.txt --output outputs/output_v1.txt --model gemini-2.0-flash` (Adjust model if needed)
    * To generate note v2: `python scripts/01_generate_note.py --prompt prompts/prompt_v2.txt --transcript data/transcript_cleaned.txt --output outputs/output_v2.txt --model gemini-2.0-flash`
5.  **Run Analysis:**
    * The script `scripts/02_analyze_output.py` is configured to compare `outputs/output_v1.txt` and `outputs/output_v2.txt` by default.
    * Run: `python scripts/02_analyze_output.py`
    * Copy the printed "Comparative Statistics" table from the console into `outputs/analysis_results.csv` (or a `.txt` file).

## Results & Discussion

This project successfully demonstrated an iterative prompt engineering workflow for generating structured clinical notes from therapy transcripts. The initial prompt (v1) produced a structurally complete note but suffered from clinically significant visual hallucinations. Through systematic evaluation against defined criteria, this issue was identified and effectively addressed in `prompt_v2` by adding specific constraints.

The refined prompt (v2) successfully eliminated these hallucinations, leading to a more accurate and trustworthy note based solely on the transcript data. This was validated by both qualitative review and comparative statistical analysis (see `outputs/analysis_results.csv`). The process highlighted the critical importance of precise prompting and iterative refinement when working with LLMs for sensitive clinical applications.
