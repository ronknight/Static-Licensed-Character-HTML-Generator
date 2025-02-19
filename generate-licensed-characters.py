import csv
import re
from collections import defaultdict

def slugify(text):
    # Convert to lowercase and replace special chars with hyphens
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def get_first_letter(licensedcharacter):
    # Get first letter, handle numbers/special cases
    first = licensedcharacter[0].upper()
    return '#' if first.isdigit() or not first.isalpha() else first

def build_url(url, licensed_character_slug):
    if "utm_source=" in url:
        return url
    else:
        return f"{url}&utm_source=webjaguar&utm_medium=website&utm_campaign=licensed-character-page&utm_content={licensed_character_slug}-link"

def generate_popular_html():
    # Read and sort licensedcharacters by Popular-License-Rating
    popular_licensedcharacters = []
    with open('licensedcharacterList.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include licensedcharacters with rating AND Active = TRUE
            if row['Popular-License-Rating'] and row['Active'].upper() == 'TRUE':
                row['Popular-License-Rating'] = int(row['Popular-License-Rating'])
                popular_licensedcharacters.append(row)
    
    # Sort by Popular-License-Rating
    popular_licensedcharacters.sort(key=lambda x: x['Popular-License-Rating'])
    
    # Generate popular.html
    html = ['<div class="popular-licensed-characters">']
    
    for licensedcharacter in popular_licensedcharacters:
        licensed_character_slug = slugify(licensedcharacter['LicensedCharacterName'])
        final_url = build_url(licensedcharacter['URL'], licensed_character_slug)
        html.append(f'''    <a href="{final_url}">
        <span class="tag {licensed_character_slug}">{licensedcharacter['LicensedCharacterName']}</span>
    </a>''')
    
    html.append('</div>')
    
    with open('popular-licensed-characters.html', 'w') as f:
        f.write('\n'.join(html))

def generate_licensedcharacters_html():
    # Group licensed characters by first letter
    letter_groups = defaultdict(list)
    
    with open('licensedcharacterList.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Active'].upper() == 'TRUE':
                first_letter = get_first_letter(row['LicensedCharacterName'])
                letter_groups[first_letter].append(row)
    
    html = ['''<div class="container">
    <!-- Masonry Grid -->
    <div class="row" id="masonry-grid">''']
    
    letters = sorted(letter_groups.keys())
    if '#' in letters:
        letters.remove('#')
        letters.insert(0, '#')
        
    for letter in letters:
        # Match exact format from base copy.html
        html.append(f'''        <!-- Example Card -->
        <div class="col-xs-12 col-sm-6 col-md-3 masonry-item" id="{letter}">
            <h4>{letter}</h4>
            <div class="items-container">''')
        
        licensedcharacters_in_group = sorted(letter_groups[letter], key=lambda x: x['LicensedCharacterName'])
        for licensedcharacter in licensedcharacters_in_group:
            licensed_character_slug = slugify(licensedcharacter['LicensedCharacterName'])
            final_url = build_url(licensedcharacter['URL'], licensed_character_slug)
            class_attr = f'item {licensed_character_slug}' if licensedcharacter.get('Popular-License-Rating') else 'item'
            
            html.append(f'''                <a href="{final_url}"
                    class="{class_attr}">{licensedcharacter['LicensedCharacterName']}</a>''')
        
        html.append('''            </div>
        </div>''')
    
    html.append('''    </div>
</div>''')
    
    with open('licensed-characters.html', 'w') as f:
        f.write('\n'.join(html))

generate_licensedcharacters_html()