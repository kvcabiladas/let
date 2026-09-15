import pypdf
import re
import json

reader = pypdf.PdfReader('/Users/kvcabiladas/.gemini/antigravity-ide/brain/3aa1c9e2-45b2-4ae3-bb31-b24814b6c7eb/.user_uploaded/media_1789426515998.pdf')

parsed_q = []

for p_idx in range(1, len(reader.pages) - 1):
    text = reader.pages[p_idx].extract_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    filtered = []
    for l in lines:
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
        filtered.append(l)

    # Separate lines into Prompts (lines ending with *) vs Non-prompts (options/scores)
    # Prompts appear at the bottom of the page in PDF text stream!
    prompts = []
    non_prompts = []
    
    in_prompts_section = False
    
    # Identify prompts: find all lines that form question prompts ending with *
    # Work backwards or forwards
    # Let's find index where question titles start
    title_start_idx = None
    for i, l in enumerate(filtered):
        if l.endswith('*') or re.match(r'^\d+\.\s+', l):
            # Check if this line is part of a prompt
            # Prompts usually contain question words like What, Which, How, Why, A teacher, In a, Several, etc.
            title_start_idx = i
            break
            
    # Wait, let's find all prompts on the page
    # A prompt is a paragraph ending with *
    p_lines = []
    o_lines = []
    
    # We can split filtered into option section and prompt section
    # Find the first line that is part of the first question title
    # Options come first, question titles come after
    
    # Let's look for lines ending with *
    q_prompts = []
    accum = []
    
    # Let's separate option lines and prompt lines
    for i, l in enumerate(filtered):
        if l.endswith('*'):
            # This line ends a prompt!
            accum.append(l)
            prompt = " ".join(accum).rstrip('*').strip()
            prompt = re.sub(r'\s+', ' ', prompt)
            q_prompts.append(prompt)
            accum = []
        elif len(q_prompts) > 0 or (i > 0 and ('?' in l or l.startswith('A ') or l.startswith('Which ') or l.startswith('What ') or l.startswith('How ') or l.startswith('Why ') or l.startswith('In ') or l.startswith('A Physical') or l.startswith('A teacher') or l.startswith('Coach') or l.startswith('Several') or l.startswith('Four') or l.startswith('When') or l.startswith('The') or l.startswith('Your') or l.startswith('To') or l.startswith('As')) and not l.startswith('A.') and not l.startswith('B.') and not l.startswith('C.') and not l.startswith('D.')):
            accum.append(l)
        else:
            o_lines.append(l)
            
    # Now parse o_lines into option sets
    # Remove score indicators like 1/1, 0/1, *1/1
    clean_o_lines = [l for l in o_lines if not re.match(r'^\*?\s*[01\xb7\.]+/(?:1|\.\.\.)$', l)]
    
    # Group clean_o_lines into sets of 4 options
    # An option starts with A., B., C., D. or is one of 4 lines
    option_sets = []
    curr_set = []
    curr_opt = ""
    
    in_override = False
    override_val = None
    overrides = []
    
    for l in clean_o_lines:
        if l == 'Correct answer':
            in_override = True
            continue
        if in_override:
            overrides.append(l)
            in_override = False
            continue
            
        if re.match(r'^[A-D]\.\s+', l):
            if curr_opt:
                curr_set.append(curr_opt)
            curr_opt = l
        elif len(curr_set) < 4 and not curr_opt and not re.match(r'^[A-D]\.\s+', l):
            # Unlettered option line
            curr_set.append(l)
        elif curr_opt:
            curr_opt += " " + l
            
        if len(curr_set) == 4 or (curr_opt and len(curr_set) == 3 and re.match(r'^[A-D]\.\s+', curr_opt) and curr_opt.startswith('D.')):
            if curr_opt and len(curr_set) == 3:
                curr_set.append(curr_opt)
                curr_opt = ""
            option_sets.append(curr_set)
            curr_set = []
            
    if curr_opt and len(curr_set) < 4:
        curr_set.append(curr_opt)
    if curr_set and len(curr_set) == 4:
        option_sets.append(curr_set)

    if len(option_sets) != len(q_prompts):
        print(f"Page {p_idx+1}: {len(option_sets)} option sets vs {len(q_prompts)} prompts")
        print("  Option sets:", option_sets)
        print("  Prompts:", q_prompts)
    else:
        for opts, pr in zip(option_sets, q_prompts):
            parsed_q.append({'page': p_idx+1, 'prompt': pr, 'opts': opts})

print(f"Total extracted: {len(parsed_q)}")
