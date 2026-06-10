import re

lines = open('d:/paper_acm/docx_text.txt', 'r', encoding='utf-8').read().splitlines()

# Extract title, abstract, keywords
title = lines[0].strip()
keywords = ''
abstract = []
body = []
state = 'start'
for line in lines[1:]:
    s = line.strip()
    if s == '摘要':
        state = 'abstract'
        continue
    if s.startswith('关键词：'):
        keywords = s[len('关键词：'):].strip()
        state = 'body'
        continue
    if state == 'abstract':
        abstract.append(s)
        continue
    if s == '':
        body.append('')
        continue
    if re.match(r'^\d+\.\d+\.\d+\s+', s):
        body.append('\\subsubsection{' + re.sub(r'^\d+\.\d+\.\d+\s+', '', s) + '}')
        continue
    if re.match(r'^\d+\.\d+\s+', s):
        body.append('\\subsection{' + re.sub(r'^\d+\.\d+\s+', '', s) + '}')
        continue
    if re.match(r'^\d+\.\s+', s):
        body.append('\\section{' + re.sub(r'^\d+\.\s+', '', s) + '}')
        continue
    if s in ['致谢', '参考文献']:
        body.append('\\section*{' + s + '}')
        continue
    if s.startswith('附录'):
        body.append('\\appendix')
        body.append('\\section{' + s + '}')
        continue
    # Escape LaTeX specials
    s = s.replace('\\', '\\textbackslash{}')
    s = s.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
    s = s.replace('#', '\\#').replace('_', '\\_').replace('{', '\\{').replace('}', '\\}')
    body.append(s)

tex = [
    '\\documentclass[acmtog,screen]{acmart}',
    '\\usepackage[UTF8]{ctex}',
    '\\setcopyright{none}',
    '\\acmYear{2026}',
    '\\acmDOI{}',
    '\\acmJournal{PACM}',
    '\\acmVolume{0}',
    '\\acmNumber{0}',
    '\\acmArticle{0}',
    '\\acmMonth{0}',
    '\\begin{document}',
    '\\title{' + title + '}',
    '\\author{蒋军}',
    '\\email{junji.jiang@edu.cn}',
    '\\affiliation{%',
    '  \\institution{计算机科学与技术学院}',
    '  \\country{China}',
    '}',
    '\\author{吕卓亮}',
    '\\email{zhuoliang.lv@edu.cn}',
    '\\affiliation{%',
    '  \\institution{计算机科学与技术学院}',
    '  \\country{China}',
    '}',
    '\\author{杨沛文}',
    '\\email{peiwen.yang@edu.cn}',
    '\\affiliation{%',
    '  \\institution{计算机科学与技术学院}',
    '  \\country{China}',
    '}',
    '\\renewcommand{\\shortauthors}{蒋军等}',
    '\\begin{abstract}',
]
for line in abstract:
    tex.append(line)
tex.extend([
    '\\end{abstract}',
    '\\keywords{' + keywords + '}',
    '\\maketitle',
])
tex.extend(body)
tex.append('\\section*{参考文献}')
tex.append('本论文引用的参考文献条目待补充。')
tex.append('\\end{document}')

open('d:/paper_acm/paper.tex', 'w', encoding='utf-8').write('\n'.join(tex))
print('paper.tex created with', len(tex), 'lines')
