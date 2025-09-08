import os
import re

# 📁 SET YOUR FOLDER PATH HERE
folder = '/media/owusus/Godstestimo/NLP-Projects/asr-datasets/data/youversion/data/mp3'

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

# 🚀 Process the folder
for filename in os.listdir(folder):
    if filename.endswith(".mp3"):
        book = None
        chapter = None
        book_code = None
        
        # Updated pattern to match both A## and B## prefixes
        # Pattern: [AB]##___##_BookName_IDENTIFIER.mp3 or [AB]##__###_BookName_IDENTIFIER.mp3
        new_pattern = re.match(r'[AB]\d+__+(\d+)_([^_]+?)_*([A-Z0-9]+)\.mp3', filename)
        if new_pattern:
            chapter = new_pattern.group(1)
            book_name = new_pattern.group(2)
            
            # Clean up book name
            book_clean = book_name.lower().replace(" ", "").replace("%20", "")
            
            # Handle special cases and abbreviations
            if book_clean == "1corinthians":
                book_clean = "1corinthians"
            elif book_clean == "2corinthians":
                book_clean = "2corinthians"
            elif book_clean == "1timothy":
                book_clean = "1timothy"
            elif book_clean == "2timothy":
                book_clean = "2timothy"
            elif book_clean == "1peter":
                book_clean = "1peter"
            elif book_clean == "2peter":
                book_clean = "2peter"
            elif book_clean == "1john":
                book_clean = "1john"
            elif book_clean == "2john":
                book_clean = "2john"
            elif book_clean == "3john":
                book_clean = "3john"
            elif book_clean == "1thess":
                book_clean = "1thessalonians"
            elif book_clean == "2thess":
                book_clean = "2thessalonians"
            elif book_clean == "1samuel":
                book_clean = "1samuel"
            elif book_clean == "2samuel":
                book_clean = "2samuel"
            elif book_clean == "1kings":
                book_clean = "1kings"
            elif book_clean == "2kings":
                book_clean = "2kings"
            elif book_clean == "1chronicles":
                book_clean = "1chronicles"
            elif book_clean == "2chronicles":
                book_clean = "2chronicles"
            # Add the Song of Songs variations
            elif book_clean == "songofsongs":
                book_clean = "songofsongs"
            elif book_clean == "songofsolomon":
                book_clean = "songofsolomon"
            
            book_code = normalized_books.get(book_clean)
            
        else:
            # Try original pattern: Book_Chapter_...
            parts = filename.split("_")
            if len(parts) >= 3:
                book_name = parts[1]
                chapter = parts[2].split(".")[0]
                book_clean = book_name.lower().replace(" ", "").replace("%20", "")
                book_code = normalized_books.get(book_clean)
        
        # If we found a match, rename the file
        if book_code and chapter:
            new_name = f"{book_code}.{int(chapter)}.mp3"
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            
            # Check if target file already exists
            if os.path.exists(new_path):
                print(f"Skipped (target exists): {filename} → {new_name}")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_name}")
        else:
            print(f"Skipped (no match): {filename}")
            # Debug: show what was extracted
            if new_pattern:
                print(f"  Debug: chapter={chapter}, book_name='{book_name}', cleaned='{book_clean if 'book_clean' in locals() else 'N/A'}'")
        
        # Clean up variables for next iteration
        if 'book_code' in locals():
            del book_code
