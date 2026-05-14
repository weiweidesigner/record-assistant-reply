# Record Assistant Reply Skill

## Description

This skill records the assistant's latest reply into a Markdown file.

When the user says something like:

- 帮我记录一下
- 记录一下
- 保存一下刚才的回答
- 把这个回答记下来
- 帮我存一下
- save this response
- record this

The assistant should call this skill and pass the latest assistant reply content to the script.

The skill stores all records in one Markdown file and groups them by date.

Each time the skill is used, it updates the existing file instead of creating a new one.

## Core Behavior

- Save the latest assistant reply into a persistent Markdown file.
- Use date-based sections.
- If today's date section already exists, append the new record under that section.
- If today's date section does not exist, create a new date section.
- Add a timestamp for each saved record.
- Keep the file updated to the latest version.
- Do not overwrite previous records.

## Input

The skill expects the assistant to provide the content that should be recorded.

Input fields:

```json
{
  "content": "The assistant reply that needs to be recorded.",
  "title": "Optional title for this record."
}
```

## Output

The skill should return:

```json
{
  "success": true,
  "file_path": "records/assistant_reply_records.md",
  "message": "Recorded successfully."
}
```

## When to Use

Use this skill when the user explicitly asks to record, save, store, or keep the assistant's current or previous reply.

Examples:

User:
帮我记录一下

Assistant should:
1. Identify the latest assistant reply.
2. Pass that reply content into this skill.
3. Tell the user it has been recorded.

## Important Notes

- The skill itself cannot automatically read the chat UI history.
- The assistant must pass the reply content into the script.
- If the user says "帮我记录一下", the assistant should record the most recent assistant answer, not the user's message.
- If there is no previous assistant reply available, ask the user which content should be recorded.
