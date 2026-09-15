import re
import json

with open('scratch/drill8_combined.txt') as f:
    text = f.read()

# Let's parse page by page
pages = text.split('--- PAGE ')

all_q = []

for page_str in pages:
    if not page_str.strip():
        continue
    lines = [l.strip() for l in page_str.split('\n') if l.strip()]
    header = lines[0]
    p_num = header.split(' ')[0]
    
    # Clean lines
    cleaned = []
    for l in lines[1:]:
        if ('https://docs.google.com' in l or 
            'DRILL 8' in l or 
            'cabiladasnicole' in l or 
            'SCHOOL' in l or
            'QUESTIONS 146' in l or
            l.startswith('SIS') or
            'BASIC INFORMATION' in l or
            'Hello Future' in l or
            'Please complete' in l or
            'The respondent' in l or
            'EMAIL ADDRESS' in l or
            'FULL NAME' in l or
            'SESSION' in l or
            'BRANCH' in l or
            'This content is neither created nor endorsed' in l or
            'Does this form look suspicious' in l or
            l == 'Forms' or
            re.match(r'^\d+/\d+/\d+', l)):
            continue
        cleaned.append(l)

    # Separate options lines from prompt lines
    # Option lines start with A., B., C., D. or score indicators 1/1, 0/1 or unlettered 4 options
    # Prompt lines are sentences ending with * or forming question titles
    
    # Find all prompts (multiline blocks ending with *)
    prompts = []
    curr_p = []
    
    # In pypdf text extraction for Google Forms, options are listed top, prompts listed bottom
    # Find index where prompt titles begin
    # Let's find all lines ending with *
    prompt_ends = [i for i, l in enumerate(cleaned) if l.endswith('*')]
    
    # For each prompt end, collect lines backwards until previous prompt end or options
    # Or collect from top to bottom:
    # Option lines: lettered A-D or 4 text options per question
    
    # Let's inspect page lines if prompt_ends is present
    if not prompt_ends:
        continue

print("Inspected pages successfully.")
