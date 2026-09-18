# -*- coding: utf-8 -*-
"""批量生成「音频背题」mp3（基于 Edge-TTS，微软神经网络语音，免费音质好）。

用法（在 commands 里选择音色）：
    python generate_audio.py --sub 高等教育学 --type 单选
    python generate_audio.py --sub 高等教育学 --type 单选 --voice zh-CN-YunxiNeural
    python generate_audio.py --sub 高等教育心理学 --type 判断 --limit 10   # 试听用

参数：
    --sub    科目：高等教育学 / 高等教育心理学
    --type   题型：单选 / 多选 / 判断
    --voice  edge-tts 音色名（默认 zh-CN-XiaoxiaoNeural 晓晓，女声温柔）
    --limit  只生成前 N 题（用于先试听）
    --force  已存在也重新生成

输出到 audio/<sub>/<type>/<id>.mp3，并生成 audio/index.json 供页面播放器引用。
"""
import argparse, asyncio, json, re, sys
from pathlib import Path

import edge_tts

BASE = Path(__file__).resolve().parent.parent      # 项目根目录
SRC = BASE / "questions.js"
OUT = BASE / "audio"

# edge-tts 中文音色参考（都是神经网络音色，音质区别见注释）
VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",   # 晓晓：温柔女声（默认，资讯类）
    "xiaoyi":   "zh-CN-XiaoyiNeural",     # 晓伊：活泼女声
    "yunxi":    "zh-CN-YunxiNeural",      # 云希：阳光男声
    "yunyang":  "zh-CN-YunYangNeural",    # 云扬：播音男声（更适合答题/播报）
    "xiaochen": "zh-CN-XiaochenNeural",   # 晓辰：成熟男声
}


def load_questions():
    src = SRC.read_text(encoding="utf-8")
    m = re.search(r"QUESTION\w*\s*=\s*(\[.*?\])\s*;", src, re.S)
    if not m:
        sys.exit("未在 questions.js 中找到 QUESTIONS 数组")
    return json.loads(m.group(1))


def build_text(q):
    """把一道题拼成适合朗读的一段话。"""
    subject, type_, question = q["subject"], q["type"], q["question"]
    answer = q["answer"]

    parts = [f"{subject}，{type_}题。", f"题目：{question}"]
    # 选项
    opts = q.get("options") or {}
    if opts:
        # 判断题选项可能为 {对/错}，也照读
        for k in ("A", "B", "C", "D", "对", "错"):
            if k in opts:
                parts.append(f"{k}，{opts[k]}。")
    # 答案 + 解析
    parts.append(f"正确答案：{answer}。")
    expl = (q.get("explanation") or "").strip()
    if expl:
        parts.append(f"解析：{expl}")
    # 知识点
    know = (q.get("knowledge") or "").strip()
    if know:
        parts.append(f"知识点：{know}")
    return "，".join(parts)


async def synth(voice, text, out_path):
    c = edge_tts.Communicate(text, voice, rate="+0%")
    await c.save(str(out_path))


async def main():
    ap = argparse.ArgumentParser(description="生成音频背题 mp3")
    ap.add_argument("--sub", required=True, choices=["高等教育学", "高等教育心理学"])
    ap.add_argument("--type", required=True, choices=["单选", "多选", "判断"])
    ap.add_argument("--voice", default="xiaoxiao",
                    help="音色键名: xiaoxiao/xiaoyi/yunxi/yunyang/xiaochen")
    ap.add_argument("--limit", type=int, default=0,
                    help="只生成前 N 题（默认全部）")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if args.voice not in VOICES:
        sys.exit(f"音色 {args.voice} 不在 {list(VOICES)} 中")
    voice = VOICES[args.voice]

    questions = load_questions()
    picked = [q for q in questions if q["subject"] == args.sub and q["type"] == args.type]
    picked.sort(key=lambda q: q["id"])
    if args.limit:
        picked = picked[: args.limit]

    sub_dir = OUT / args.sub / args.type
    sub_dir.mkdir(parents=True, exist_ok=True)

    print(f"科目={args.sub} 题型={args.type} 音色={voice} 共{len(picked)}题 "
          f"{'(限 '+str(args.limit)+' 题)' if args.limit else ''}")

    key = f"{args.sub}/{args.type}"
    index_path = OUT / "index.json"
    index = {}
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            index = {}
    current = index.setdefault(key, {"voice": voice, "subject": args.sub, "type": args.type, "files": []})
    current["files"] = []   # 重建本分类列表，避免残留旧项/重复

    ok = fail = 0
    for i, q in enumerate(picked, 1):
        mp3 = sub_dir / f"{q['id']}.mp3"
        if not (mp3.exists() and not args.force):
            try:
                await synth(voice, build_text(q), mp3)
                ok += 1
                print(f"  [{i}/{len(picked)}] id={q['id']} ✓")
            except Exception as e:
                fail += 1
                print(f"  [{i}/{len(picked)}] id={q['id']} ✗ {e}")
                continue
        else:
            ok += 1
        entry = {"id": q["id"], "file": f"audio/{args.sub}/{args.type}/{q['id']}.mp3"}
        current["files"].append(entry)

    current["count"] = len(current["files"])
    current["total"] = len(picked)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    total_files = sum(v["count"] for v in index.values())
    print(f"完成：成功{ok} 失败{fail}，{key} 现有{current['count']}个可用音频，全部分类共{total_files}个")


if __name__ == "__main__":
    asyncio.run(main())