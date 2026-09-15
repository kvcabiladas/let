import re
import json

ans_key_raw = """
51. A
52. D
53. C
54. B
55. A
56. A
57. C
58. B
59. C
60. A
61. B
62. B
63. C
64. A
65. D
66. C
67. B
68. A
69. A
70. D
71. D
72. D
73. A
74. D
75. A
76. A
77. D
78. D
79. A
80. D
81. B
82. C
83. D
84. C
85. A
86. C
87. B
88. A
89. A
90. A
91. C
92. D
93. A
94. A
95. B
96. B
97. D
98. A
99. B
100. A
"""

ans_dict = {}
for line in ans_key_raw.strip().split('\n'):
    m = re.match(r'^(\d+)\.\s+([A-D])$', line.strip())
    if m:
        num = int(m.group(1))
        let = m.group(2)
        idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}[let]
        ans_dict[num] = idx

print("Answer key count:", len(ans_dict))

with open('scratch/mapeh6_raw.txt') as f:
    text = f.read()

# Skip answer key page (Page 5)
text_q = text.split('--- PAGE 5 ---')[0]

# Clean trash header lines
lines = []
for l in text_q.split('\n'):
    l_str = l.strip()
    if ('www.teachpinas.com' in l_str or 
        'MAPEH PART 6' in l_str or 
        re.match(r'^--- PAGE \d+ ---$', l_str)):
        continue
    if l_str:
        lines.append(l_str)

# Group text into question blocks: each question starts with "51.", "52.", etc.
q_blocks = []
curr_q = []

for l in lines:
    if re.match(r'^\d+\.\s+', l):
        if curr_q:
            q_blocks.append("\n".join(curr_q))
        curr_q = [l]
    elif curr_q:
        curr_q.append(l)

if curr_q:
    q_blocks.append("\n".join(curr_q))

print("Extracted question blocks count:", len(q_blocks))

parsed_questions = []

for q_text_block in q_blocks:
    # Match q_num and q_text
    lines = q_text_block.split('\n')
    header = lines[0]
    m_num = re.match(r'^(\d+)\.\s+(.*)$', header)
    if not m_num:
        continue
    q_num = int(m_num.group(1))
    first_line_prompt = m_num.group(2)
    
    # Separate options from prompt
    prompt_lines = [first_line_prompt]
    opts_lines = []
    
    in_opts = False
    
    for l in lines[1:]:
        if re.match(r'^[A-Da-d]\.\s+', l) or re.match(r'^[1-4]\.\s+', l) or (in_opts and re.match(r'^[a-d]\.\s+', l)):
            in_opts = True
            opts_lines.append(l)
        elif in_opts:
            opts_lines.append(l)
        else:
            prompt_lines.append(l)
            
    q_prompt = " ".join(prompt_lines).strip()
    q_prompt = re.sub(r'\s+', ' ', q_prompt)
    
    # Parse options A, B, C, D
    opts = []
    curr_o = ""
    for l in opts_lines:
        if re.match(r'^[A-Da-d]\.\s+', l):
            if curr_o:
                opts.append(curr_o)
            curr_o = re.sub(r'^[A-Da-d]\.\s+', '', l).strip()
        elif re.match(r'^[1-4]\.\s+', l):
            if curr_o:
                opts.append(curr_o)
            curr_o = l
        elif curr_o:
            curr_o += " " + l
        else:
            curr_o = l
    if curr_o:
        opts.append(curr_o)
        
    corr_idx = ans_dict.get(q_num, 0)
    
    parsed_questions.append({
        'id': q_num,
        'questionText': q_prompt,
        'options': opts,
        'correctAnswerIndex': corr_idx
    })

print("Parsed items count:", len(parsed_questions))
for pq in parsed_questions[:5]:
    print(pq)

