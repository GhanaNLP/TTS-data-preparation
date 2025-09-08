import os
import re

# 📁 SET YOUR FILE PATH HERE
input_file = '/home/owusus/Dropbox/Mich/Projects/NLP-Projects/asr-datasets/data/youversion/data/AK1BSG.scores'
output_file = '/home/owusus/Dropbox/Mich/Projects/NLP-Projects/asr-datasets/data/youversion/data/AK1BSG.scores_output'  # Or set to None to overwrite input file

# Mapping of full book names to YouVersion short codes
book_codes = {
    'Genesis': 'GEN', 'Exodus': 'EXO', 'Leviticus': 'LEV', 'Numbers': 'NUM',
    'Deuteronomy': 'DEU', 'Joshua': 'JOS', 'Judges': 'JDG', 'Ruth': 'RUT',
    '1 Samuel': '1SA', '2 Samuel': '2SA', '1 Kings': '1KI', '2 Kings': '2KI',
    '1 Chronicles': '1CH', '2 Chronicles': '2CH', 'Ezra': 'EZR', 'Nehemiah': 'NEH',
    'Esther': 'EST', 'Job': 'JOB', 'Psalms': 'PSA', 'Proverbs': 'PRO',
    'Ecclesiastes': 'ECC', 'Song of Solomon': 'SNG', 'Isaiah': 'ISA',
    'Jeremiah': 'JER', 'Lamentations': 'LAM', 'Ezekiel': 'EZK', 'Daniel': 'DAN',
    'Hosea': 'HOS', 'Joel': 'JOL', 'Amos': 'AMO', 'Obadiah': 'OBA',
    'Jonah': 'JON', 'Micah': 'MIC', 'Nahum': 'NAM', 'Habakkuk': 'HAB',
    'Zephaniah': 'ZEP', 'Haggai': 'HAG', 'Zechariah': 'ZEC', 'Malachi': 'MAL',
    'Matthew': 'MAT', 'Mark': 'MRK', 'Luke': 'LUK', 'John': 'JHN',
    'Acts': 'ACT', 'Romans': 'ROM', '1 Corinthians': '1CO', '2 Corinthians': '2CO',
    'Galatians': 'GAL', 'Ephesians': 'EPH', 'Philippians': 'PHP', 'Colossians': 'COL',
    '1 Thessalonians': '1TH', '2 Thessalonians': '2TH', '1 Timothy': '1TI',
    '2 Timothy': '2TI', 'Titus': 'TIT', 'Philemon': 'PHM', 'Hebrews': 'HEB',
    'James': 'JAS', '1 Peter': '1PE', '2 Peter': '2PE', '1 John': '1JN',
    '2 John': '2JN', '3 John': '3JN', 'Jude': 'JUD', 'Revelation': 'REV'
}

# Normalize book keys for matching
normalized_books = {k.lower().replace(" ", ""): v for k, v in book_codes.items()}

# Add common alternative spellings and variations
alternative_spellings = {
    'songofsongs': 'SNG',           # Alternative name for Song of Solomon
    'songofsolomon': 'SNG',         # Standard name
    'canticles': 'SNG',             # Another alternative name
    'cant': 'SNG',                  # Abbreviation for Canticles
    'song': 'SNG',                  # Short form
    'sos': 'SNG'                    # Acronym
}

# Merge alternative spellings with normalized books
normalized_books.update(alternative_spellings)

def get_book_code(book_name):
    """Extract book code from book name using the same logic as the original script"""
    book_clean = book_name.lower().replace(" ", "").replace("%20", "")
    
    # Handle special cases and abbreviations
    special_cases = {
        "1corinthians": "1corinthians",
        "2corinthians": "2corinthians", 
        "1timothy": "1timothy",
        "2timothy": "2timothy",
        "1peter": "1peter",
        "2peter": "2peter",
        "1john": "1john",
        "2john": "2john",
        "3john": "3john",
        "1thess": "1thessalonians",
        "2thess": "2thessalonians",
        "1samuel": "1samuel",
        "2samuel": "2samuel",
        "1kings": "1kings",
        "2kings": "2kings",
        "1chronicles": "1chronicles",
        "2chronicles": "2chronicles",
        "songofsongs": "songofsongs",
        "songofsolomon": "songofsolomon"
    }
    
    if book_clean in special_cases:
        book_clean = special_cases[book_clean]
    
    return normalized_books.get(book_clean)

def process_identifier(identifier):
    """Process a single identifier and return the shortened version if possible"""
    # Pattern to match: [AB]##___##_BookName_____IDENTIFIER
    pattern = re.match(r'([AB]\d+)__+(\d+)_([^_]+?)_+([A-Z0-9]+)', identifier)
    
    if pattern:
        prefix = pattern.group(1)  # B01, A02, etc.
        chapter = pattern.group(2)  # 01, 02, etc.
        book_name = pattern.group(3)  # Matthew, Genesis, etc.
        suffix = pattern.group(4)  # AK1BSGN2DA, etc.
        
        book_code = get_book_code(book_name)
        
        if book_code:
            # Create shortened version: BOOK.CHAPTER
            return f"{book_code}.{int(chapter)}"
        else:
            print(f"Warning: Could not find book code for '{book_name}' in identifier '{identifier}'")
            return identifier
    else:
        # Try alternative pattern if the first one doesn't match
        alt_pattern = re.match(r'([AB]\d+)_([^_]+)_(\d+)', identifier)
        if alt_pattern:
            prefix = alt_pattern.group(1)
            book_name = alt_pattern.group(2)
            chapter = alt_pattern.group(3)
            
            book_code = get_book_code(book_name)
            if book_code:
                return f"{book_code}.{int(chapter)}"
        
        print(f"Warning: Could not parse identifier '{identifier}'")
        return identifier

def is_number(s):
    """Check if a string represents a number (int or float)"""
    try:
        float(s)
        return True
    except ValueError:
        return False

def process_line(line):
    """Process a single line and replace identifiers"""
    # Split the line into parts
    parts = line.strip().split()
    
    if len(parts) < 1:
        return line  # Return original line if it's empty
    
    # Check if we have the pattern: identifier + number (like duration)
    if len(parts) == 2 and is_number(parts[1]):
        # Pattern: B01___01_Matthew_____AK1BSGN2DA_00013 5.176000
        identifier = parts[0]
        number = parts[1]
        
        new_identifier = process_identifier(identifier)
        return f"{new_identifier} {number}\n"
    
    # Check if we have a single identifier (no additional data)
    elif len(parts) == 1:
        # Pattern: B01___04_Matthew_____AK1BSGN2DA_00006
        identifier = parts[0]
        new_identifier = process_identifier(identifier)
        return f"{new_identifier}\n"
    
    # Original pattern: two identifiers + optional additional data
    elif len(parts) >= 2:
        first_identifier = parts[0]
        second_identifier = parts[1]
        
        # Check if the second part is a number (duration case)
        if is_number(second_identifier):
            # This is actually the single identifier + number case
            new_first = process_identifier(first_identifier)
            return f"{new_first} {second_identifier}\n"
        else:
            # This is the original two identifiers case
            new_first = process_identifier(first_identifier)
            new_second = process_identifier(second_identifier)
            
            # Reconstruct the line with new identifiers and preserve the rest
            if len(parts) > 2:
                remaining_parts = ' '.join(parts[2:])
                return f"{new_first} {new_second} {remaining_parts}\n"
            else:
                return f"{new_first} {new_second}\n"
    
    # If we can't parse it, return the original line
    return line

# 🚀 Process the file
def main():
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    processed_lines = []
    changes_made = 0
    
    print(f"Processing file: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            original_line = line
            processed_line = process_line(line)
            
            if processed_line != original_line:
                changes_made += 1
                print(f"Line {line_num}: Changed")
                print(f"  From: {original_line.strip()}")
                print(f"  To:   {processed_line.strip()}")
            
            processed_lines.append(processed_line)
    
    # Write output
    output_path = output_file if output_file else input_file
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)
    
    print(f"\n✅ Processing complete!")
    print(f"📊 Total lines processed: {len(processed_lines)}")
    print(f"🔄 Lines changed: {changes_made}")
    print(f"📁 Output written to: {output_path}")

if __name__ == "__main__":
    main()
