# -*- coding: utf-8 -*-
"""
解析《两学题库-合成版.docx》为结构化 JSON 题库
结构（经人工勘察确认）：
  第一部分 单选：q1-230 高等教育学，q231-304 高等教育心理学
  第二部分 多选：高等教育学
  第三部分 判断：高等教育学
  第四部分 单选：高等教育心理学
  第五部分 多选：高等教育心理学
  第六部分 判断：高等教育心理学
解析规则：
  - 题干行：以数字开头
  - 选项行：A./A、/A． 开头（仅出现在答案行之前）
  - 判断题选项：整行为「对」或「错」
  - 答案行：正确答案: X / XX / 对 / 错 / 错误
  - 答案行之后、下一题之前的内容视为解析（若有）
"""
import json
import re
import sys
from docx import Document

DOCX = r"d:\MyProjects\MindGym\两学题库-合成版.docx"
OUT = r"d:\MyProjects\MindGym\questions.json"

doc = Document(DOCX)
paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# --- 分段边界：按"题号回到 1"的六段 ---
def section_of(idx):
    # idx 为段落索引；边界由前期勘察得到
    if idx <= 2142:   return 1  # 教育学单选(1-230)+心理学单选(231-304)
    if idx <= 2724:   return 2  # 教育学多选
    if idx <= 3150:   return 3  # 教育学判断
    if idx <= 4096:   return 4  # 心理学单选
    if idx <= 4860:   return 5  # 心理学多选
    return 6                 # 心理学判断

RE_Q     = re.compile(r'^(\d+)[\.、．]?\s*(.+)$')
RE_OPT   = re.compile(r'^([A-D])[\.、．]\s*(.+)$')
RE_ANS   = re.compile(r'^正确答案\s*[:：]\s*(.+)$')

questions = []
cur = None
errors = []

def finish(cur):
    """校验并收尾一道题"""
    if cur is None:
        return
    qtype, subject, qtext, opts, ans, expl = \
        cur['type'], cur['subject'], cur['text'], cur['options'], cur['answer'], cur['explanation']
    if not ans:
        errors.append(f"无答案: {cur['no']} {qtext[:30]}")
    if not qtext:
        errors.append(f"空题干: 题号{cur['no']}")
    if qtype in ('single', 'multi') and not opts:
        errors.append(f"选择题无选项: {cur['no']} {qtext[:30]}")
    questions.append(cur)

for text in paras:
    # 答案行
    m = RE_ANS.match(text)
    if m and cur is not None and cur['answer'] is None:
        raw = m.group(1).strip()
        if raw in ('对', '正确'): ans = '对'
        elif raw in ('错', '错误', '不正确'): ans = '错'
        else:
            letters = ''.join(sorted(set(re.findall(r'[A-D]', raw.upper()))))
            ans = letters
        cur['answer'] = ans
        # 根据答案推断/校正题型
        if cur['type'] == 'judge' and ans not in ('对', '错'):
            errors.append(f"判断题答案异常: {cur['no']} -> {raw}")
        continue
    # 选项行（仅在尚未出答案时有效）
    m = RE_OPT.match(text)
    if m and cur is not None and cur['answer'] is None:
        cur['options'][m.group(1)] = m.group(2).strip()
        continue
    # 判断题选项（占位行，无需记录；仅出现在答案行之前）
    if text in ('对', '错') and cur is not None and cur['answer'] is None:
        continue
    # 新题干
    m = RE_Q.match(text)
    if m:
        no = int(m.group(1)); qtext = m.group(2).strip()
        if cur is not None:
            finish(cur)
        sec = None
        cur = {
            'no': no, 'section': None, 'type': None, 'subject': None,
            'text': qtext, 'options': {}, 'answer': None, 'explanation': ''
        }
        continue
    # 其它内容：作为解析文本挂在当前题上
    if cur is not None and cur['answer'] is not None:
        cur['explanation'] = (cur['explanation'] + '\n' + text).strip()
    elif cur is not None:
        # 题干与选项之间的意外行，附加到题干
        cur['text'] += ' ' + text
finish(cur)

# --- 补充 section/subject/type ---
for q in questions:
    pass  # 需要段落索引，改在主循环里做不了，用题号规则处理

# 重新按段落索引走一遍以精确分段（上面主循环没记录索引，改为重算）
# 简单方案：用题库内部顺序重建
# 六段的题号序列是 1..304 / 1..N2 / 1..N3 / 1..N4 / 1..N5 / 1..N6
# 依相邻题是否回到 1 来切段
secs = [[]]
for q in questions:
    if secs[-1] and q['no'] == 1 and secs[-1][-1]['no'] != 0:
        secs.append([])
    secs[-1].append(q)

print(f"共解析 {len(questions)} 题，切分为 {len(secs)} 段")
for i, s in enumerate(secs, 1):
    print(f"  段{i}: {len(s)} 题, 题号 {s[0]['no']}-{s[-1]['no']}")

meta = {
    1: {'subject': '混合', 'type': '单选'},   # 教育学+心理学，后面按题号拆
    2: {'subject': '高等教育学', 'type': '多选'},
    3: {'subject': '高等教育学', 'type': '判断'},
    4: {'subject': '高等教育心理学', 'type': '单选'},
    5: {'subject': '高等教育心理学', 'type': '多选'},
    6: {'subject': '高等教育心理学', 'type': '判断'},
}

out = []
qid = 0
for si, s in enumerate(secs, 1):
    info = meta.get(si, {'subject': '未分类', 'type': '单选'})
    for q in s:
        qid += 1
        subject = info['subject']
        qtype = info['type']
        if si == 1:
            # q1-230 教育学，q231-304 心理学
            subject = '高等教育学' if q['no'] <= 230 else '高等教育心理学'
        # 多选/单选按答案长度自动校正
        if qtype == '单选' and q['answer'] and len(q['answer']) >= 2:
            qtype = '多选'
        if qtype == '多选' and q['answer'] and len(q['answer']) == 1:
            qtype = '单选'
        out.append({
            'id': qid,
            'subject': subject,
            'type': qtype,
            'question': q['text'],
            'options': q['options'] if q['options'] else None,
            'answer': q['answer'],
            'explanation': q['explanation'] or None,
        })

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

# --- 校验报告 ---
print(f"\n输出 {len(out)} 题到 {OUT}")
from collections import Counter
print('学科分布:', dict(Counter(q['subject'] for q in out)))
print('题型分布:', dict(Counter(q['type'] for q in out)))
bad_ans = [q for q in out if not q['answer'] or
           (q['type'] in ('单选', '多选') and not re.fullmatch(r'[A-D]+', q['answer'])) or
           (q['type'] == '判断' and q['answer'] not in ('对', '错'))]
print('答案异常题数:', len(bad_ans))
for q in bad_ans[:10]:
    print('  -', q['id'], q['type'], q['answer'], q['question'][:40])
no_opt = [q for q in out if q['type'] in ('单选', '多选') and
          (not q['options'] or set(q['options']) != {'A', 'B', 'C', 'D'})]
print('选项不全题数:', len(no_opt))
for q in no_opt[:10]:
    print('  -', q['id'], q['type'], list((q['options'] or {}).keys()), q['question'][:40])
if errors:
    print('\n解析告警:', len(errors))
    for e in errors[:15]:
        print('  !', e)
