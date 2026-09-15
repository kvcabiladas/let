import re
import json

with open('scratch/drill8_combined.txt') as f:
    text = f.read()

# Remove page header/footer lines
lines = []
for l in text.split('\n'):
    l_str = l.strip()
    if ('https://docs.google.com' in l_str or 
        'DRILL 8' in l_str or 
        'cabiladasnicole' in l_str or 
        'SCHOOL' in l_str or
        'QUESTIONS 146' in l_str or
        l_str.startswith('SIS') or
        'BASIC INFORMATION' in l_str or
        'Hello Future' in l_str or
        'Please complete' in l_str or
        'The respondent' in l_str or
        'EMAIL ADDRESS' in l_str or
        'FULL NAME' in l_str or
        'SESSION' in l_str or
        'BRANCH' in l_str or
        'This content is neither created nor endorsed' in l_str or
        'Does this form look suspicious' in l_str or
        l_str == 'Forms' or
        re.match(r'^--- PAGE \d+ ---$', l_str) or
        re.match(r'^\d+/\d+/\d+', l_str)):
        continue
    if l_str:
        lines.append(l_str)

print("Total cleaned lines:", len(lines))

# Let's find all question prompts (lines ending with *)
# Each question prompt ends with '*'
prompt_indices = [i for i, l in enumerate(lines) if l.endswith('*')]

print(f"Found {len(prompt_indices)} question prompt endings.")

