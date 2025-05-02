import google.generativeai as genai
import os
import pathlib
import argparse
import sys

def generate_note(prompt_path, transcript_path, output_path, model_name):
    """
    Loads prompt and transcript, calls Gemini API, saves the generated note.
    """
    try:
        # --- 1. Configure Gemini API ---
        print("Configuring Gemini API...")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        print(f"Using Gemini model: {model_name}")

        # --- 2. Load Prompt and Transcript Files ---
        print(f"Loading prompt from: {prompt_path}")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        print(f"Loading transcript from: {transcript_path}")
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()

        # --- 3. Format the Full Prompt ---
        # Assumes the prompt template expects the transcript appended after it
        full_prompt = f"{prompt_template}\n\n--- TRANSCRIPT START ---\n{transcript_content}\n--- TRANSCRIPT END ---"
        print("Prompt formatted.")
        # print(f"DEBUG: Prompt starts with:\n{full_prompt[:500]}...") # Uncomment to debug prompt

        # --- 4. Call Gemini API ---
        print("Sending request to Gemini API... (This may take a moment)")
        # Optional: Configure safety settings to be less restrictive if needed
        # Adjust thresholds as necessary: BLOCK_NONE, BLOCK_LOW_AND_ABOVE, BLOCK_MEDIUM_AND_ABOVE, BLOCK_HIGH_AND_ABOVE
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        # Optional: Configure generation config (e.g., temperature)
        # generation_config = genai.types.GenerationConfig(temperature=0.7)

        response = model.generate_content(
            full_prompt,
            safety_settings=safety_settings
            # generation_config=generation_config # Uncomment to use
            )

        # --- 5. Process Response ---
        generated_text = ""
        try:
            # Attempt to access the text directly
            generated_text = response.text
            print("Response received successfully.")
        except ValueError as e:
            # If direct text access fails, likely blocked content or other issue
            print(f"Warning: Could not directly access response text. Checking feedback. Error: {e}")
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                 block_reason = response.prompt_feedback.block_reason
                 print(f"Request blocked due to: {block_reason}")
                 generated_text = f"Error: Content generation blocked - {block_reason}"
            else:
                 print("Error: Response received but contained no valid text and no block reason found.")
                 print("Full Response Parts:", response.parts) # Log parts for debugging
                 generated_text = "Error: Failed to generate content or extract text from response. See logs."

        # --- 6. Save Output ---
        print(f"Saving output to: {output_path}")
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated_text)
        print(f"Output saved to {output_path}")

    except FileNotFoundError as e:
        print(f"Error: Input file not found - {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Error: Configuration or value error - {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        # Optional: print full traceback for debugging
        # import traceback
        # traceback.print_exc()

# --- Main execution block ---
if __name__ == "__main__":
    # --- Argument Parsing ---
    # Sets up command-line arguments for flexibility
    parser = argparse.ArgumentParser(description="Generate clinical notes using Gemini API.")
    parser.add_argument("--prompt", required=True, help="Path to the prompt template file (e.g., prompts/prompt_v1.txt).")
    parser.add_argument("--transcript", default="data/transcript_cleaned.txt", help="Path to the transcript file (default: data/transcript_cleaned.txt).")
    parser.add_argument("--output", required=True, help="Path to save the generated output note (e.g., outputs/output_v1.txt).")
    parser.add_argument("--model", default="gemini-1.5-flash-latest", help="Gemini model name (default: gemini-1.5-flash-latest).")
    args = parser.parse_args()

    # Convert file path strings to Path objects
    prompt_file = pathlib.Path(args.prompt)
    transcript_file = pathlib.Path(args.transcript)
    output_file = pathlib.Path(args.output)

    # --- Call the main function ---
    generate_note(prompt_file, transcript_file, output_file, args.model)