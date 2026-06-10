import zipfile
import xml.etree.ElementTree as ET

path = 'ref/论文 (2) (1).docx'
with zipfile.ZipFile(path) as z:
    data = z.read('word/document.xml')
root = ET.fromstring(data)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
texts = []
for para in root.findall('.//w:p', ns):
    runs = para.findall('.//w:t', ns)
    if runs:
        texts.append(''.join(t.text or '' for t in runs))
    else:
        texts.append('')
for i, t in enumerate(texts[:200], 1):
    print(f'{i:03}: {t}')
