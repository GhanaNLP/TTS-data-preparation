import csv
import re
import os

input_csv = "/media/owusus/Godstestimo/NLP-Projects/asr-datasets/data/youversion/bible_chapters_output-nzema.csv"
output_folder = "/media/owusus/Godstestimo/NLP-Projects/asr-datasets/data/youversion/data/txt"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        title = row.get("Title", "")
        content = row.get("Content", "")
        url = row.get("URL", "")
        
        match = re.search(r'/bible/\d+/([A-Z0-9]+\.\d+)', url)
        if not match:
            print(f"❌ Skipping row with invalid URL: {url}")
            continue
        
        code = match.group(1)
        
        # --- Simplified Text Processing ---
        
        # 0. Remove text in parentheses (including the parentheses) - FIRST STEP
        content = re.sub(r'\([^)]*\)', '', content)
        title = re.sub(r'\([^)]*\)', '', title)
        
        # 1. Remove all numbers from content
        content = re.sub(r'\d+', '', content)
        
        # 2. Insert full stop at end of each line without punctuation
        lines = content.splitlines()
        processed_lines = []
        for line in lines:
            line = line.strip()
            if line:  # Only process non-empty lines
                # Add full stop if line doesn't end with punctuation
                if line[-1] not in ['.', '!', '?', ':', ';']:
                    line += '.'
                processed_lines.append(line)
        
        # 3. Replace all new lines with spaces
        content = ' '.join(processed_lines)
        
        # 4. Prepend title with full stop at the end
        title = title.strip()
        if title and not title.endswith('.'):
            title += '.'
        full_text = f"{title} {content}"
        
        # 5. Remove all quotation marks and brackets
        full_text = re.sub(r'[\"\'“”‘’\(\)\[\]\{\}]', '', full_text)
        
        # 6. Collapse multiple spaces
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        
        # 7. Replace double or mixed punctuation with a single period
        full_text = re.sub(r'[,.]{2,}', '.', full_text)  # handles .. ,, .,, etc.
        full_text = re.sub(r'([,.!?;:])\.', '.', full_text)  # handles ., !., etc.
        
        # 8. Ensure text ends with a full stop
        if full_text and not full_text.endswith('.'):
            full_text += '.'
        
        # Write to output file
        output_path = os.path.join(output_folder, f"{code}.txt")
        with open(output_path, mode='w', encoding='utf-8') as out_file:
            out_file.write(full_text)

print(f"✅ Done. Saved cleaned text files with titles prepended using book code names like PSA.1.txt.")
