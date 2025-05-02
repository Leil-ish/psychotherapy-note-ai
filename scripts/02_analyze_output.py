import pathlib
import re
import textstat
import sys

def parse_sections(text):
    """
    Parses the clinical note text into major sections using regex.
    Handles headings that might be at the very start of the file.
    Assumes headings like **1. SOAP Note:**, **2. ...**, **3. ...**
    """
    sections = {'SOAP': '', 'MSE': '', 'Risk': '', 'Header': '', 'Other': ''}
    # Regex to find the start of each main section heading
    # MODIFIED: Allows matching at start of string (\A) OR after a newline (\n)
    pattern = r'(?:\n|\A)\s*\*\*(\d\.\s*(?:SOAP Note|Mental Status Examination \(MSE\)|Risk Assessment))\*\*\s*\n?' # Made trailing \n optional too

    # Find all matches and their start positions
    matches = list(re.finditer(pattern, text))

    if not matches:
        print("Warning: Could not find standard section headings. Treating entire text as one section.", file=sys.stderr)
        sections['Other'] = text.strip() # Put all text in 'Other' if no headings found
        return sections

    # Extract text before the first match ONLY if the first match isn't at the very start
    first_match_start = matches[0].start()
    if first_match_start > 0:
        sections['Header'] = text[:first_match_start].strip()
    else:
         sections['Header'] = '' # No header if first match is at the start

    # Extract text for each identified section
    for i, match in enumerate(matches):
        # Start extracting content *after* the full matched heading pattern
        start_pos = match.end()
        # Determine end position: start of the next match's pattern, or end of the text
        end_pos = matches[i+1].start() if (i + 1) < len(matches) else len(text)
        section_text = text[start_pos:end_pos].strip()

        # Identify section based on heading text captured in group 1
        heading_text = match.group(1).lower() # Group 1 contains the heading like "1. SOAP Note"
        if 'soap note' in heading_text:
            sections['SOAP'] = section_text
        elif 'mental status examination' in heading_text:
            sections['MSE'] = section_text
        elif 'risk assessment' in heading_text:
            sections['Risk'] = section_text
        else:
            # Capture unexpected sections if any
            sections['Other'] += section_text + "\n"

    sections['Other'] = sections['Other'].strip() # Clean up 'Other' section

    return sections

def calculate_stats(file_path):
    """
    Loads text from file, parses sections, parses SOAP subsections using
    robust line-by-line checking that handles content on the heading line,
    and calculates statistics. FINAL VERSION 2.0.
    """
    try:
        # Optional: Keep if you want separation
        # print(f"\n--- Analyzing {file_path.name} ---")
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()

        if not full_text or full_text.startswith("Error:"):
             print(f"Skipping analysis for {file_path.name} due to error content or empty file.")
             return None

        # Parse major sections first using regex (assuming this part works)
        sections = parse_sections(full_text) # Assumes parse_sections function exists
        stats = {}

        # --- Basic counts on full text ---
        stats['Total Word Count'] = len(full_text.split())
        stats['Total Sentence Count'] = textstat.sentence_count(full_text)
        stats['Average Sentence Length'] = round(textstat.avg_sentence_length(full_text), 2)

        # --- Readability (on full text) ---
        stats['Flesch-Kincaid Grade'] = textstat.flesch_kincaid_grade(full_text)
        stats['Flesch Reading Ease'] = textstat.flesch_reading_ease(full_text)

        # --- Word counts per MAJOR section ---
        stats['Word Count SOAP'] = len(sections.get('SOAP', '').split()) if sections.get('SOAP') else 0
        stats['Word Count MSE'] = len(sections.get('MSE', '').split()) if sections.get('MSE') else 0
        stats['Word Count Risk'] = len(sections.get('Risk', '').split()) if sections.get('Risk') else 0

        # --- Parse SOAP Subsections using robust line checking ---
        soap_text = sections.get('SOAP', '')
        # Use lists to store lines for each subsection
        soap_subsection_lines = {'Subjective': [], 'Objective': [], 'Assessment': [], 'Plan': []}
        current_subsection = None

        # Define the core heading strings (up to and including the colon) that mark the START of a section
        heading_markers = {
            "* **Subjective:**": "Subjective",
            "* **Objective:**": "Objective",
            "* **Assessment:**": "Assessment",
            "* **Plan:**": "Plan"
        }

        if soap_text:
            for line in soap_text.splitlines():
                stripped_line = line.strip() # Strip whitespace for checking
                matched_heading_key = None

                # Check if this line marks the beginning of a known subsection
                for marker, section_name in heading_markers.items():
                    if stripped_line.startswith(marker):
                        current_subsection = section_name # Update which section we are currently in
                        matched_heading_key = marker # Remember which marker we matched
                        # print(f"DEBUG: Found heading marker '{marker}' for section '{current_subsection}'") # Optional Debug
                        break # Stop checking markers once one is found

                # --- LOGIC CHANGE HERE ---
                if matched_heading_key:
                    # Found a heading. Extract content AFTER the marker ON THE SAME LINE.
                    content_on_heading_line = stripped_line[len(matched_heading_key):].strip()
                    if content_on_heading_line: # If there's text after the marker on this line...
                        # print(f"DEBUG: Appending content from heading line to '{current_subsection}': '{content_on_heading_line[:50]}...'") # Optional Debug
                        soap_subsection_lines[current_subsection].append(content_on_heading_line)
                elif current_subsection:
                     # This line is NOT a heading, and we know which section we are in.
                     # Append the original line (or stripped) if it has content.
                    if line.strip(): # Check original line to preserve potential leading whitespace if needed
                        # print(f"DEBUG: Appending content line to '{current_subsection}': '{line[:50]}...'") # Optional Debug
                        soap_subsection_lines[current_subsection].append(line.strip()) # Append stripped line for consistency

        # Join the collected lines back together for each subsection and calculate sentence count
        for section_name, lines_list in soap_subsection_lines.items():
            # Join lines, ensuring consistent newline handling, then strip leading/trailing whitespace from the final block
            subsection_text = " ".join(lines_list).strip() # Join with spaces, not newlines, as we handled lines individually
            key_name = f'Sentence Count {section_name}'
            stats[key_name] = textstat.sentence_count(subsection_text) if subsection_text else 0

        return stats

    # (Keep the except blocks and __main__ block the same)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}", file=sys.stderr)
        # import traceback # Uncomment for detailed debug
        # traceback.print_exc() # Uncomment for detailed debug
        return None

if __name__ == "__main__":
    # Define paths to the output files
    output_v1_path = pathlib.Path("outputs/output_v1.txt")
    output_v2_path = pathlib.Path("outputs/output_v2.txt")

    # Calculate stats for both versions
    stats_v1 = calculate_stats(output_v1_path)
    stats_v2 = calculate_stats(output_v2_path)

    # --- Print Comparative Results ---
    print("\n\n--- Comparative Statistics ---")
    if stats_v1 and stats_v2:
        # Define the order of metrics to print
        metrics = [
            'Total Word Count', 'Total Sentence Count', 'Average Sentence Length',
            'Flesch-Kincaid Grade', 'Flesch Reading Ease',
            'Word Count SOAP', 'Word Count MSE', 'Word Count Risk',
            'Sentence Count Subjective', 'Sentence Count Objective',
            'Sentence Count Assessment', 'Sentence Count Plan'
        ]
        # Print header
        print(f"{'Metric':<28} | {'Version 1':<10} | {'Version 2':<10}")
        print("-" * 55) # Adjust separator length
        # Print each metric row
        for metric in metrics:
            val1 = stats_v1.get(metric, 'N/A')
            val2 = stats_v2.get(metric, 'N/A')
            print(f"{metric:<28} | {str(val1):<10} | {str(val2):<10}")
    else:
        print("Could not generate comparative statistics due to errors in processing one or both files.")

# --- Main execution block ---
if __name__ == "__main__":
    # Define paths to the output files
    output_v1_path = pathlib.Path("outputs/output_v1.txt")
    output_v2_path = pathlib.Path("outputs/output_v2.txt")

    # Calculate stats for both versions
    stats_v1 = calculate_stats(output_v1_path)
    stats_v2 = calculate_stats(output_v2_path)

    # --- Print Comparative Results ---
    print("\n\n--- Comparative Statistics ---")
    if stats_v1 and stats_v2:
        # Define the order of metrics to print
        metrics = [
            'Total Word Count', 'Total Sentence Count', 'Average Sentence Length',
            'Flesch-Kincaid Grade', 'Flesch Reading Ease',
            'Word Count SOAP', 'Word Count MSE', 'Word Count Risk',
            'Sentence Count Subjective', 'Sentence Count Objective',
            'Sentence Count Assessment', 'Sentence Count Plan'
            # Add Word Count subsections here if you uncommented them in calculate_stats
        ]
        # Print header
        print(f"{'Metric':<28} | {'Version 1':<10} | {'Version 2':<10}")
        print("-" * 55) # Adjust separator length
        # Print each metric row
        for metric in metrics:
            val1 = stats_v1.get(metric, 'N/A')
            val2 = stats_v2.get(metric, 'N/A')
            print(f"{metric:<28} | {str(val1):<10} | {str(val2):<10}")
    else:
        print("Could not generate comparative statistics due to errors in processing one or both files.")