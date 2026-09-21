#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 questions.json 合成一份按「学科 → 题型」分类组织的 docx 题库文档。
输出: 两学题库_含答案.docx"""
import json
import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

SRC = os.path.join(os.path.dirname(__file__), "questions.json")
OUT = os.path.join(os.path.dirname(__file__), "两学题库_含答案.docx")

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

# 学科与题型的展示顺序
SUBJECT_ORDER = ["高等教育学", "高等教育心理学"]
TYPE_LABEL = {"单选": "单选题", "多选": "多选题", "判断": "判断题"}
TYPE_ORDER = ["单选", "多选", "判断"]

doc = Document()

# 全局中文字体
style = doc.styles["Normal"]
style.font.name = "宋体"
style.font.size = Pt(11)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

# 封面标题
title = doc.add_heading("两学题库（含答案）", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = sub.add_run("高等教育学 · 高等教育心理学 · 共 %d 题" % len(data))
run.bold = True

# 文档级统计
total = {"单选": 0, "多选": 0, "判断": 0}
for q in data:
    total[q["type"]] += 1

doc.add_heading("题库总览", level=1)
tbl = doc.add_table(rows=2, cols=4)
tbl.style = "Light Shading Accent 1"
hdr = tbl.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = "题型", "数量", "备注", ""
row = tbl.rows[1].cells
row[0].text, row[1].text, row[2].text, row[3].text = ("总计", str(len(data)), "含答案与解析", "")
# 简化：上面表格占位，下面再按学科细列
doc.add_paragraph()
p = doc.add_paragraph()
p.add_run("各学科明细：").bold = True
for subj in SUBJECT_ORDER:
    cnt = {t: sum(1 for q in data if q["subject"] == subj and q["type"] == t) for t in TYPE_ORDER}
    doc.add_paragraph("%s：单选 %d · 多选 %d · 判断 %d" % (subj, cnt["单选"], cnt["多选"], cnt["判断"]))

# 按学科 → 题型 分类导出
idx = 0  # 全局题号(合并到题干前)
for subj in SUBJECT_ORDER:
    doc.add_heading(subj, level=1)
    for qtype in TYPE_ORDER:
        items = [q for q in data if q["subject"] == subj and q["type"] == qtype]
        if not items:
            continue
        doc.add_heading(TYPE_LABEL[qtype] + "（%d 题）" % len(items), level=2)
        for k, q in enumerate(items, 1):
            idx += 1
            # 题干
            qp = doc.add_paragraph()
            qp.paragraph_format.space_before = Pt(6)
            qp.paragraph_format.space_after = Pt(2)
            qp.add_run("%d. %s" % (k, q["question"])).bold = True
            # 选项
            if q.get("options"):
                for letter, text in q["options"].items():
                    op = doc.add_paragraph("%s. %s" % (letter, text))
                    op.paragraph_format.left_indent = Pt(18)
                    op.paragraph_format.space_after = Pt(0)
            # 答案
            ans = doc.add_paragraph("【答案】%s" % q["answer"])
            ans.paragraph_format.left_indent = Pt(0)
            ans.paragraph_format.space_after = Pt(0)
            # 解析（若有）
            if q.get("explanation"):
                ex = doc.add_paragraph("【解析】%s" % q["explanation"])
                ex.paragraph_format.left_indent = Pt(0)
                ex.paragraph_format.space_after = Pt(0)
            # knowledge（若有）
            if q.get("knowledge"):
                kv = doc.add_paragraph("【考点】%s" % q["knowledge"])
                kv.paragraph_format.left_indent = Pt(0)
                kv.paragraph_format.space_after = Pt(0)

doc.save(OUT)
sz = os.path.getsize(OUT)
print("已生成: %s  (%.1f KB)" % (OUT, sz / 1024))
print("总题数: %d" % len(data))
print("各学科:" )
for subj in SUBJECT_ORDER:
    cnt = {t: sum(1 for q in data if q["subject"] == subj and q["type"] == t) for t in TYPE_ORDER}
    print("  %s: 单选%d 多选%d 判断%d" % (subj, cnt["单选"], cnt["多选"], cnt["判断"]))