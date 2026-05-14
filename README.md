# Record Assistant Reply Skill

这个 Skill 用于在 AI 聊天过程中记录当前或上一条机器人回复。

当用户说“帮我记录一下”时，AI 应该把最近一条机器人回复内容传给 `scripts/record_reply.py`，脚本会把内容追加到同一个 Markdown 文件中，并按日期分段。

## 文件结构

```bash
record-assistant-reply/
├── SKILL.md
├── README.md
└── scripts/
    └── record_reply.py
```

## 使用方式

```bash
python scripts/record_reply.py \
  --content "这里是需要记录的机器人回复" \
  --title "可选标题"
```

默认会生成或更新：

```bash
records/assistant_reply_records.md
```

## 记录效果

```markdown
# Assistant Reply Records

## 2026-05-14

### 16:30:21｜未命名记录

这里是机器人刚才回复的内容。

---
```
