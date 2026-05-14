# Record Assistant Reply HTML Note Skill

## Description

This skill records the assistant's latest reply into a single rich HTML note file.

When the user asks to record, save, store, or keep the assistant's current or previous reply, call this skill and pass the latest assistant reply content to the script.

The skill stores all records in one HTML file and groups them by date. The page title is 我的AI笔记. The page uses a clean white design, supports dark mode, icon-only edit/save/preview/delete actions, date cards, time dividers, and rich rendering for Mermaid, ECharts, images, and videos.

## Core Behavior

- Save the latest assistant reply into a persistent HTML file.
- Use date-based card sections.
- Separate records in the same day with a centered timestamp divider.
- Add a timestamp for each saved record.
- Show newest records first within each date section.
- Keep the file updated to the latest version.
- Do not overwrite previous records.
- Title the page 我的AI笔记.
- Do not show a download button.
- Render Mermaid fenced code blocks.
- Render ECharts fenced code blocks containing JSON options.
- Render Markdown image syntax.
- Render Markdown video syntax for common video file extensions.
- Provide icon-only edit, save, preview, delete, export PDF, and theme controls.
- Support dark mode switching.
- Support directly exporting notes to a single long-page PDF from the browser script.
- Show hover tooltips for icon-only controls.

## Input

```json
{
  "content": "The assistant reply that needs to be recorded.",
  "title": "Optional title for this record."
}
```

## Output

```json
{
  "success": true,
  "file_path": "records/assistant_reply_diary.html",
  "message": "Recorded successfully. Open the HTML file to edit and preview rich content."
}
```

## Important Notes

- The skill itself cannot automatically read the chat UI history.
- The assistant must pass the reply content into the script.
- If the user says "帮我记录一下", record the most recent assistant answer, not the user's message.
- Browser-side edits, theme preference, and deleted records are saved in localStorage.
- Mermaid and ECharts rendering use external CDN resources when the HTML page is opened in the browser.
