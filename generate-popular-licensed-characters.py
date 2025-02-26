import csv
import re

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def build_url(url, licensed_character_slug):
    if "utm_source=" in url:
        return url
    else:
        return f"{url}&utm_source=webjaguar&utm_medium=website&utm_campaign=licensedcharacters-page&utm_content={licensed_character_slug}-link"

def generate_popular_html():
    licensedcharacters = []
    with open('LicensedCharacterList.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include licensedcharacters that have a Popular-License-Rating > 0 and are Active
            if row['Popular-License-Rating'] and row['Active'].upper() == 'TRUE' and int(row['Popular-License-Rating']) > 0:
                licensedcharacters.append(row)
    
    licensedcharacters.sort(key=lambda x: int(x['Popular-License-Rating']))
    html = ['<div class="popular-licensed-characters">']
    
    for licensedcharacter in licensedcharacters:
        licensed_character_slug = slugify(licensedcharacter['LicensedCharacterName'])
        final_url = build_url(licensedcharacter['URL'], licensed_character_slug)
        logo = licensedcharacter.get('LogoName', '').strip()
        # Debug output:
        print(f"DEBUG: {licensedcharacter['LicensedCharacterName']} logo: '{logo}'")
        if logo:
            if logo.startswith("http"):
                logo_url = logo
            else:
                image_url = licensedcharacter.get('Image_URL', '').strip()
                logo_url = f"{image_url}{logo}"
            html.append(f'''    <a href="{final_url}">
    <img src="{logo_url}" alt="Wholesale {licensedcharacter['LicensedCharacterName']}" class="licensed-characters-logo">
    <p class="licensed-character-name">{licensedcharacter['LicensedCharacterName']}</p>
</a>''')
        else:
            html.append(f'''    <a href="{final_url}">
    <span class="tag {licensed_character_slug}">{licensedcharacter['LicensedCharacterName']}</span>
</a>''')
    html.append('</div>')
    
    with open('popular-licensed-characters.html', 'w') as f:
        f.write('\n'.join(html))

generate_popular_html()