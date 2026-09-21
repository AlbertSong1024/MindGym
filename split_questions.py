#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 questions.json 按 40KB 上限切成若干份,每份为完整数组,不拆散单题。
输出: questions_part_1.json / questions_part_2.json / ... (保留原 questions.json 不变)"""
import json
import os

SRC = os.path.join(os.path.dirname(__file__), "questions.json")
MAX_BYTES = 38 * 1024  # 38KB 目标,确保最终文件稳定 ≤ 40KB

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

# 按顺序切分：累积字节数,超上限则开新份
parts = []
cur = []
cur_bytes = 0

for q in data:
    # 单题序列化字节数
    item_bytes = len(json.dumps([q], ensure_ascii=False).encode("utf-8")) - 2  # 去掉两端括号
    if cur and cur_bytes + item_bytes > MAX_BYTES:
        parts.append(cur)
        cur = []
        cur_bytes = 0
    cur.append(q)
    cur_bytes += item_bytes

if cur:
    parts.append(cur)

# 写入输出文件
base = os.path.dirname(SRC)
out_files = []
for i, part in enumerate(parts, 1):
    out = os.path.join(base, f"questions_part_{i}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(part, f, ensure_ascii=False)
    out_files.append(out)

# 汇总信息
print(f"原文件: {SRC}")
print(f"总题数: {len(data)} 题")
print(f"切分成 {len(parts)} 份:")
total_pieces = 0
for i, part in enumerate(parts, 1):
    sz = os.path.getsize(out_files[i - 1])
    total_pieces += len(part)
    print(f"  questions_part_{i}.json  {len(part):3d} 题  {round(sz/1024,1)} KB")
print(f"合计: {total_pieces} 题")