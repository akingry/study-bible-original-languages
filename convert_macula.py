from pathlib import Path
import csv, json, re

OUT = Path(r'D:\OC\studyBible\data\macula-original.json')
HEB = Path(r'D:\OC\studyBible\vendor\macula-hebrew\WLC\tsv\macula-hebrew.tsv')
GRK = Path(r'D:\OC\studyBible\vendor\macula-greek\macula-greek-Nestle1904.tsv')

BOOKS = ['Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1 Samuel','2 Samuel','1 Kings','2 Kings','1 Chronicles','2 Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs','Ecclesiastes','Song of Solomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi','Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians','Galatians','Ephesians','Philippians','Colossians','1 Thessalonians','2 Thessalonians','1 Timothy','2 Timothy','Titus','Philemon','Hebrews','James','1 Peter','2 Peter','1 John','2 John','3 John','Jude','Revelation']
OSIS = ['GEN','EXO','LEV','NUM','DEU','JOS','JDG','RUT','1SA','2SA','1KI','2KI','1CH','2CH','EZR','NEH','EST','JOB','PSA','PRO','ECC','SNG','ISA','JER','LAM','EZK','DAN','HOS','JOL','AMO','OBA','JON','MIC','NAM','HAB','ZEP','HAG','ZEC','MAL','MAT','MRK','LUK','JHN','ACT','ROM','1CO','2CO','GAL','EPH','PHP','COL','1TH','2TH','1TI','2TI','TIT','PHM','HEB','JAS','1PE','2PE','1JN','2JN','3JN','JUD','REV']
code_to_book={c:b for c,b in zip(OSIS,BOOKS)}
num_to_book={i+1:b for i,b in enumerate(BOOKS)}

def norm_strong(s):
    s=(s or '').strip()
    if not s: return ''
    m=re.search(r'(\d+)', s)
    return str(int(m.group(1))) if m else s

def ref_from_code(code, ch, vs):
    return f"{code_to_book.get(code, code)} {int(ch)}:{int(vs)}"

def heb_ref(ref):
    # GEN 1:1!1
    m=re.match(r'([A-Z0-9]+)\s+(\d+):(\d+)', ref)
    return ref_from_code(m.group(1), m.group(2), m.group(3)) if m else ref

def greek_ref(ref):
    # MAT 1:1!1 or n40001001001 id also available
    m=re.match(r'([A-Z0-9]+)\s+(\d+):(\d+)', ref)
    return ref_from_code(m.group(1), m.group(2), m.group(3)) if m else ref

verses={}
with HEB.open('r', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        ref=heb_ref(row['ref'])
        w={
            't': row.get('text',''),
            'a': row.get('after',''),
            'g': row.get('gloss') or row.get('english') or '',
            'l': row.get('lemma') or row.get('stronglemma') or '',
            's': norm_strong(row.get('strongnumberx')),
            'm': row.get('morph',''),
            'tr': row.get('transliteration','')
        }
        verses.setdefault(ref, {'lang':'hebrew','w':[]})['w'].append(w)

with GRK.open('r', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        ref=greek_ref(row['ref'])
        w={
            't': row.get('text',''),
            'a': row.get('after',''),
            'g': row.get('gloss') or row.get('english') or '',
            'l': row.get('lemma',''),
            's': norm_strong(row.get('strong')),
            'm': row.get('morph',''),
            'tr': row.get('normalized','')
        }
        verses.setdefault(ref, {'lang':'greek','w':[]})['w'].append(w)

out={'source':'MACULA Hebrew and Greek TSV, reduced for browser display','verses':verses}
OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(',',':')), encoding='utf-8')
print('verses', len(verses), 'bytes', OUT.stat().st_size)
for k in ['Genesis 1:1','John 1:1','Revelation 22:21']:
    print(k, verses.get(k,{}).get('lang'), len(verses.get(k,{}).get('w',[])), verses.get(k,{}).get('w',[])[:3])
