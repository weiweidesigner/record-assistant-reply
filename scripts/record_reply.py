#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Record Assistant Reply HTML Note Skill

This script saves assistant replies into a single rich HTML note file,
grouped by date and appended with timestamps.
"""

import argparse
import html
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


DEFAULT_RECORD_DIR = "records"
DEFAULT_RECORD_FILE = "assistant_reply_diary.html"
APP_TITLE = "我的AI笔记"


STYLE = """    :root {
      color-scheme: light;
      --bg: #ffffff;
      --paper: #ffffff;
      --ink: #171717;
      --muted: #737373;
      --line: #e5e5e5;
      --line-strong: #d4d4d4;
      --accent: #2563eb;
      --accent-soft: #eff6ff;
      --danger: #dc2626;
      --code-bg: #f7f7f7;
      --shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    }

    body[data-theme="dark"] {
      color-scheme: dark;
      --bg: #0f1115;
      --paper: #171a21;
      --ink: #f4f4f5;
      --muted: #a1a1aa;
      --line: #2a2f3a;
      --line-strong: #3f4654;
      --accent: #93c5fd;
      --accent-soft: #172033;
      --danger: #f87171;
      --code-bg: #111827;
      --shadow: none;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.68;
    }

    main {
      width: min(1040px, calc(100% - 32px));
      margin: 0 auto;
      padding: 36px 0 64px;
    }

    header {
      padding-bottom: 8px;
      margin-bottom: 24px;
    }

    .topbar {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
    }

    h1, h2, h3 {
      margin: 0;
      line-height: 1.25;
    }

    h1 {
      font-size: 28px;
      font-weight: 720;
      letter-spacing: 0;
    }

    .date-section {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      margin: 20px 0;
      padding: 22px;
    }

    .date-heading {
      margin: 0 0 18px;
      text-align: center;
    }

    .date-section h2 {
      color: var(--ink);
      font-size: 18px;
      font-weight: 680;
      margin: 0;
      padding-bottom: 0;
    }

    .weekday {
      color: var(--muted);
      font-size: 12px;
      margin-top: 4px;
    }

    .entry {
      padding: 6px 0 18px;
    }

    .entry[hidden] {
      display: none;
    }

    .time-divider {
      align-items: center;
      color: var(--muted);
      display: flex;
      font-size: 12px;
      gap: 12px;
      letter-spacing: 0;
      margin: 8px 0 18px;
      white-space: nowrap;
    }

    .time-divider::before,
    .time-divider::after {
      border-top: 1px dashed var(--line-strong);
      content: "";
      flex: 1;
      height: 0;
    }

    .entry-toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }

    h3 {
      font-size: 17px;
      font-weight: 660;
    }

    .actions {
      display: flex;
      gap: 6px;
      align-items: center;
    }

    .icon-button {
      align-items: center;
      background: transparent;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--muted);
      cursor: pointer;
      display: inline-flex;
      height: 34px;
      justify-content: center;
      padding: 0;
      position: relative;
      width: 34px;
    }

    .icon-button:hover {
      background: var(--accent-soft);
      border-color: var(--line-strong);
      color: var(--accent);
    }

    .icon-button.danger:hover {
      background: color-mix(in srgb, var(--danger) 10%, transparent);
      color: var(--danger);
    }

    .icon-button svg {
      height: 17px;
      width: 17px;
      stroke: currentColor;
    }

    .icon-button::after {
      background: var(--ink);
      border-radius: 6px;
      color: var(--paper);
      content: attr(aria-label);
      font-size: 12px;
      left: 50%;
      line-height: 1;
      opacity: 0;
      padding: 7px 8px;
      pointer-events: none;
      position: absolute;
      top: calc(100% + 8px);
      transform: translateX(-50%) translateY(-2px);
      transition: opacity 120ms ease, transform 120ms ease;
      white-space: nowrap;
      z-index: 10;
    }

    .icon-button:hover::after,
    .icon-button:focus-visible::after {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }

    .header-actions {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .content {
      overflow-wrap: anywhere;
    }

    .content p {
      margin: 0 0 12px;
    }

    .content a {
      color: var(--accent);
    }

    .content h1,
    .content h2,
    .content h3,
    .content h4 {
      line-height: 1.3;
      margin: 20px 0 10px;
    }

    .content h1 {
      font-size: 26px;
    }

    .content h2 {
      border-bottom: 1px solid var(--line);
      font-size: 22px;
      padding-bottom: 6px;
    }

    .content h3 {
      font-size: 18px;
    }

    .content h4 {
      font-size: 16px;
    }

    .content ul,
    .content ol {
      margin: 0 0 14px 24px;
      padding: 0;
    }

    .content li {
      margin: 4px 0;
    }

    .content blockquote {
      border-left: 4px solid var(--line-strong);
      color: var(--muted);
      margin: 14px 0;
      padding: 2px 0 2px 14px;
    }

    .content table {
      border-collapse: collapse;
      display: block;
      margin: 14px 0;
      overflow-x: auto;
      width: 100%;
    }

    .content th,
    .content td {
      border: 1px solid var(--line);
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }

    .content th {
      background: var(--code-bg);
      font-weight: 660;
    }

    .content hr {
      border: 0;
      border-top: 1px solid var(--line);
      margin: 22px 0;
    }

    .content input[type="checkbox"] {
      margin-right: 6px;
    }

    .content img,
    .content video {
      display: block;
      max-width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      margin: 14px 0;
      background: var(--paper);
    }

    .content video {
      max-height: 520px;
    }

    .mermaid,
    .echart {
      width: 100%;
      min-height: 320px;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      margin: 14px 0;
      background: var(--paper);
    }

    textarea {
      display: none;
      width: 100%;
      min-height: 420px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--paper);
      color: var(--ink);
      font: 14px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      padding: 14px;
      resize: vertical;
    }

    .editing .content {
      display: none;
    }

    .editing textarea {
      display: block;
    }

    pre {
      overflow-x: auto;
      background: var(--code-bg);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }

    code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.95em;
    }

    .pdf-exporting {
      background: #ffffff !important;
      color: #111111 !important;
      left: -100000px;
      max-width: none;
      padding: 32px;
      position: fixed;
      top: 0;
      width: max-content;
    }

    .pdf-exporting .header-actions,
    .pdf-exporting .actions,
    .pdf-exporting textarea {
      display: none !important;
    }

    .pdf-exporting .date-section {
      box-shadow: none;
    }

    .pdf-exporting * {
      color-adjust: exact;
      print-color-adjust: exact;
      -webkit-print-color-adjust: exact;
    }"""


ICON_EDIT = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>'
ICON_SAVE = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2Z"/><path d="M17 21v-8H7v8"/><path d="M7 3v5h8"/></svg>'
ICON_PREVIEW = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>'
ICON_DELETE = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>'
ICON_MOON = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3 6.7 6.7 0 0 0 21 12.8Z"/></svg>'
ICON_EXPORT = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M12 18v-6"/><path d="M9 15l3 3 3-3"/></svg>'


SCRIPT = """    const storagePrefix = "assistant-reply-diary:";
    const deletedKey = storagePrefix + "deleted";
    const themeKey = storagePrefix + "theme";

    function escapeHtml(value) {
      return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function escapeAttr(value) {
      return escapeHtml(value).replaceAll("`", "&#96;");
    }

    function deletedIds() {
      try {
        return new Set(JSON.parse(localStorage.getItem(deletedKey) || "[]"));
      } catch {
        return new Set();
      }
    }

    function saveDeletedIds(ids) {
      localStorage.setItem(deletedKey, JSON.stringify([...ids]));
    }

    function applyTheme(theme) {
      document.body.dataset.theme = theme;
      localStorage.setItem(themeKey, theme);
      if (window.mermaid) {
        mermaid.initialize({ startOnLoad: false, securityLevel: "loose", theme: theme === "dark" ? "dark" : "default" });
      }
    }

    function rerenderEntries() {
      document.querySelectorAll(".entry:not([hidden])").forEach((entry) => {
        renderRichContent(entry);
      });
    }

    function initTheme() {
      const saved = localStorage.getItem(themeKey);
      const preferred = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      applyTheme(saved || preferred);
      document.getElementById("themeToggle").addEventListener("click", () => {
        applyTheme(document.body.dataset.theme === "dark" ? "light" : "dark");
        rerenderEntries();
      });
    }

    async function exportPdf() {
      await Promise.all([...document.querySelectorAll(".entry:not([hidden])")].map((entry) => renderRichContent(entry)));
      if (!window.html2canvas || !window.jspdf?.jsPDF) {
        alert("PDF 导出依赖还在加载，请稍后再试。");
        return;
      }

      const source = document.querySelector("main");
      const clone = source.cloneNode(true);
      clone.classList.add("pdf-exporting");
      document.body.appendChild(clone);

      try {
        clone.querySelectorAll(".entry:not([hidden])").forEach((entry) => {
          const content = entry.querySelector(".content");
          const original = document.querySelector(`.entry[data-record-id="${entry.dataset.recordId}"] .content`);
          if (content && original) content.innerHTML = original.innerHTML;
        });

        const canvas = await html2canvas(clone, {
          backgroundColor: "#ffffff",
          scale: Math.min(2, window.devicePixelRatio || 1),
          useCORS: true,
          windowWidth: clone.scrollWidth,
          windowHeight: clone.scrollHeight
        });
        const image = canvas.toDataURL("image/jpeg", 0.95);
        const orientation = canvas.width >= canvas.height ? "landscape" : "portrait";
        const pdf = new jspdf.jsPDF({
          orientation,
          unit: "px",
          format: [canvas.width, canvas.height],
          compress: true
        });
        pdf.addImage(image, "JPEG", 0, 0, canvas.width, canvas.height);
        pdf.save(`${document.title || "我的AI笔记"}.pdf`);
      } finally {
        clone.remove();
      }
    }

    function initExport() {
      document.getElementById("exportPdf").addEventListener("click", exportPdf);
    }

    function normalizeMediaLinks(raw) {
      let text = raw;
      text = text.replace(/(^|\\s)(https?:\\/\\/[^\\s<]+\\.(?:png|jpe?g|gif|webp|svg))(\\s|$)/gi, (_match, before, src, after) => `${before}![](${src})${after}`);
      text = text.replace(/(^|\\s)(https?:\\/\\/[^\\s<]+\\.(?:mp4|webm|ogg|mov))(\\s|$)/gi, (_match, before, src, after) => `${before}![](${src})${after}`);
      return text;
    }

    function renderMedia(src, alt = "") {
      const cleanSrc = escapeAttr(src);
      const label = escapeAttr(alt || "");
      const lower = src.toLowerCase();
      if (/\\.(mp4|webm|ogg|mov)(\\?.*)?$/.test(lower)) {
        return `<video controls src="${cleanSrc}">${label}</video>`;
      }
      return `<img src="${cleanSrc}" alt="${label}" loading="lazy">`;
    }

    function renderInline(value) {
      let html = escapeHtml(value);
      html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
      html = html.replace(/!\\[([^\\]]*)\\]\\(([^\\s)]+)(?:\\s+\"([^\"]*)\")?\\)/g, (_match, alt, src) => renderMedia(src, alt));
      html = html.replace(/\\[([^\\]]+)\\]\\(([^\\s)]+)(?:\\s+\"([^\"]*)\")?\\)/g, (_match, text, href) => {
        return `<a href="${escapeAttr(href)}" target="_blank" rel="noreferrer">${escapeHtml(text)}</a>`;
      });
      html = html.replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>");
      html = html.replace(/__([^_]+)__/g, "<strong>$1</strong>");
      html = html.replace(/(^|\\W)\\*([^*]+)\\*(?=\\W|$)/g, "$1<em>$2</em>");
      html = html.replace(/(^|\\W)_([^_]+)_(?=\\W|$)/g, "$1<em>$2</em>");
      return html;
    }

    function renderMarkdownWithMarked(raw, recordId) {
      if (!window.marked) return null;
      const renderer = new marked.Renderer();

      renderer.code = function(code, infostring = "") {
        if (typeof code === "object" && code !== null) {
          infostring = code.lang || "";
          code = code.text || "";
        }
        const normalized = String(infostring || "").trim().toLowerCase();
        const value = String(code || "").replace(/\\n$/, "");
        if (normalized === "mermaid") return `<div class="mermaid">${escapeHtml(value.trim())}</div>`;
        if (["echart", "echarts"].includes(normalized)) {
          return `<div class="echart" data-option="${encodeURIComponent(value.trim())}" id="echart-${recordId}-${Math.random().toString(36).slice(2)}"></div>`;
        }
        const langClass = normalized ? ` class="language-${escapeAttr(normalized)}"` : "";
        return `<pre><code${langClass}>${escapeHtml(value)}</code></pre>`;
      };

      renderer.image = function(href, title, text) {
        if (typeof href === "object" && href !== null) {
          text = href.text || "";
          href = href.href || "";
        }
        return renderMedia(String(href || ""), String(text || ""));
      };

      renderer.link = function(href, title, text) {
        if (typeof href === "object" && href !== null) {
          text = href.text || "";
          href = href.href || "";
        }
        return `<a href="${escapeAttr(String(href || ""))}" target="_blank" rel="noreferrer">${renderInline(String(text || ""))}</a>`;
      };

      renderer.html = function(value) {
        return escapeHtml(typeof value === "object" && value !== null ? value.text || "" : String(value || ""));
      };

      return marked.parse(normalizeMediaLinks(raw), {
        async: false,
        breaks: false,
        gfm: true,
        headerIds: false,
        mangle: false,
        renderer
      });
    }

    function renderMarkdownish(raw, recordId) {
      const markedHtml = renderMarkdownWithMarked(raw, recordId);
      if (markedHtml !== null) return markedHtml;

      const blocks = [];
      const token = (type, value) => {
        const index = blocks.push({ type, value }) - 1;
        return `\\n@@BLOCK_${index}@@\\n`;
      };

      let text = normalizeMediaLinks(raw).replace(/```(\\w+)?\\n([\\s\\S]*?)```/g, (_match, lang = "", code = "") => {
        const normalized = lang.trim().toLowerCase();
        if (normalized === "mermaid") return token("mermaid", code.trim());
        if (["echart", "echarts"].includes(normalized)) return token("echart", code.trim());
        return token("code", { lang: normalized, code: code.replace(/\\n$/, "") });
      });

      return text.split(/\\n{2,}/).map((part) => {
        const trimmed = part.trim();
        if (!trimmed) return "";
        const blockMatch = trimmed.match(/^@@BLOCK_(\\d+)@@$/);
        if (blockMatch) {
          const index = Number(blockMatch[1]);
          const block = blocks[index];
          if (block.type === "mermaid") return `<div class="mermaid">${escapeHtml(block.value)}</div>`;
          if (block.type === "echart") return `<div class="echart" data-option="${encodeURIComponent(block.value)}" id="echart-${recordId}-${index}"></div>`;
          const langClass = block.value.lang ? ` class="language-${escapeAttr(block.value.lang)}"` : "";
          return `<pre><code${langClass}>${escapeHtml(block.value.code)}</code></pre>`;
        }
        if (/^#{1,4}\\s+/.test(trimmed)) {
          const level = trimmed.match(/^#+/)[0].length;
          return `<h${level}>${renderInline(trimmed.replace(/^#{1,4}\\s+/, ""))}</h${level}>`;
        }
        if (/^>\\s?/.test(trimmed)) {
          return `<blockquote>${trimmed.split("\\n").map((line) => renderInline(line.replace(/^>\\s?/, ""))).join("<br>")}</blockquote>`;
        }
        if (/^[-*+]\\s+/m.test(trimmed)) {
          return `<ul>${trimmed.split("\\n").map((line) => `<li>${renderInline(line.replace(/^[-*+]\\s+/, ""))}</li>`).join("")}</ul>`;
        }
        if (/^\\d+\\.\\s+/m.test(trimmed)) {
          return `<ol>${trimmed.split("\\n").map((line) => `<li>${renderInline(line.replace(/^\\d+\\.\\s+/, ""))}</li>`).join("")}</ol>`;
        }
        return `<p>${renderInline(trimmed).replaceAll("\\n", "<br>")}</p>`;
      }).join("\\n");
    }

    async function renderRichContent(entry) {
      const id = entry.dataset.recordId;
      const content = entry.querySelector(".content");
      const editor = entry.querySelector("textarea");
      content.innerHTML = renderMarkdownish(editor.value, id);

      if (window.mermaid) {
        try {
          mermaid.initialize({ startOnLoad: false, securityLevel: "loose", theme: document.body.dataset.theme === "dark" ? "dark" : "default" });
          await mermaid.run({ nodes: content.querySelectorAll(".mermaid") });
        } catch (error) {
          console.warn("Mermaid render failed", error);
        }
      }

      if (window.echarts) {
        content.querySelectorAll(".echart").forEach((node) => {
          try {
            const existing = echarts.getInstanceByDom(node);
            if (existing) existing.dispose();
            const option = JSON.parse(decodeURIComponent(node.dataset.option || "{}"));
            const chart = echarts.init(node, document.body.dataset.theme === "dark" ? "dark" : null);
            chart.setOption(option);
            window.addEventListener("resize", () => chart.resize(), { once: false });
          } catch {
            node.innerHTML = `<pre><code>${escapeHtml(decodeURIComponent(node.dataset.option || ""))}</code></pre>`;
          }
        });
      }
    }

    function loadEntry(entry) {
      const id = entry.dataset.recordId;
      const content = entry.querySelector(".content");
      const editor = entry.querySelector("textarea");
      const saved = localStorage.getItem(storagePrefix + id);
      if (deletedIds().has(id)) {
        entry.hidden = true;
        return;
      }
      if (!editor.value.trim()) {
        editor.value = content.textContent;
      }
      if (saved !== null) {
        editor.value = saved;
      }
      renderRichContent(entry);
    }

    function initEntries() {
      document.querySelectorAll(".entry").forEach((entry) => {
        loadEntry(entry);
        entry.addEventListener("click", (event) => {
          const button = event.target.closest("button");
          if (!button) return;

          const editor = entry.querySelector("textarea");
          const id = entry.dataset.recordId;
          const action = button.dataset.action;

          if (action === "edit") {
            entry.classList.add("editing");
            editor.focus();
          }

          if (action === "save") {
            localStorage.setItem(storagePrefix + id, editor.value);
            renderRichContent(entry);
          }

          if (action === "preview") {
            renderRichContent(entry);
            entry.classList.remove("editing");
          }

          if (action === "delete") {
            if (!confirm("删除这条记录？")) return;
            const ids = deletedIds();
            ids.add(id);
            saveDeletedIds(ids);
            entry.hidden = true;
          }
        });
      });
    }

    initTheme();
    initExport();
    initEntries();"""


EXTERNAL_SCRIPTS = """  <script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>"""


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def button(action: str, label: str, icon: str, danger: bool = False) -> str:
    classes = "icon-button danger" if danger else "icon-button"
    return f'<button class="{classes}" type="button" data-action="{action}" aria-label="{label}" title="{label}">{icon}</button>'


def build_record_block(content: str, title: Optional[str] = None) -> str:
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    record_id = now.strftime("record-%Y%m%d-%H%M%S-%f")
    safe_title = title.strip() if title and title.strip() else "未命名记录"
    escaped_title = html.escape(safe_title)
    escaped_content = html.escape(content.strip())

    return f"""
      <article class="entry" data-record-id="{escape_attr(record_id)}">
        <div class="time-divider"><span>{time_str}</span></div>
        <div class="entry-toolbar">
          <h3>{escaped_title}</h3>
          <div class="actions">
            {button("edit", "编辑", ICON_EDIT)}
            {button("save", "保存", ICON_SAVE)}
            {button("preview", "预览", ICON_PREVIEW)}
            {button("delete", "删除", ICON_DELETE, True)}
          </div>
        </div>
        <div class="content">{escaped_content}</div>
        <textarea aria-label="编辑记录">{escaped_content}</textarea>
      </article>
"""


def build_header() -> str:
    return f"""    <header>
      <div class="topbar">
        <h1>{APP_TITLE}</h1>
        <div class="header-actions">
          <button class="icon-button" id="exportPdf" type="button" aria-label="导出 PDF" title="导出 PDF">{ICON_EXPORT}</button>
          <button class="icon-button" id="themeToggle" type="button" aria-label="切换深色模式" title="切换深色模式">{ICON_MOON}</button>
        </div>
      </div>
    </header>"""


def weekday_for(date_heading: str) -> str:
    names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    try:
        return names[datetime.strptime(date_heading, "%Y-%m-%d").weekday()]
    except ValueError:
        return ""


def date_heading_block(date_heading: str) -> str:
    weekday = weekday_for(date_heading)
    weekday_html = f'<div class="weekday">{html.escape(weekday)}</div>' if weekday else ""
    return f'<div class="date-heading"><h2>{html.escape(date_heading)}</h2>{weekday_html}</div>'


def build_document(date_heading: str, record_block: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{APP_TITLE}</title>
  <style>
{STYLE}
  </style>
{EXTERNAL_SCRIPTS}
</head>
<body>
  <main>
{build_header()}

    <section class="date-section" data-date="{escape_attr(date_heading)}">
      {date_heading_block(date_heading)}
{record_block}
    </section>
  </main>

  <script>
{SCRIPT}
  </script>
</body>
</html>
"""


def migrate_entry(article: str) -> str:
    content_match = re.search(r'<div class="content">([\s\S]*?)</div>', article)
    textarea_match = re.search(r'<textarea[^>]*>([\s\S]*?)</textarea>', article)
    title_match = re.search(r'<h3>([\s\S]*?)</h3>', article)
    time_match = re.search(r'<div class="time">([\s\S]*?)</div>', article) or re.search(r'<div class="time-divider">\s*<span>([\s\S]*?)</span>\s*</div>', article)
    id_match = re.search(r'data-record-id="([^"]+)"', article)

    record_id = id_match.group(1) if id_match else datetime.now().strftime("record-%Y%m%d-%H%M%S-%f")
    title = title_match.group(1).strip() if title_match else "未命名记录"
    source = textarea_match.group(1) if textarea_match else (content_match.group(1) if content_match else "")
    time_text = time_match.group(1).strip() if time_match else "--:--:--"
    if time_text == "--:--:--" and id_match:
        id_time = re.search(r"record-\d{8}-(\d{2})(\d{2})(\d{2})", id_match.group(1))
        if id_time:
            time_text = f"{id_time.group(1)}:{id_time.group(2)}:{id_time.group(3)}"

    return f"""
      <article class="entry" data-record-id="{escape_attr(html.unescape(record_id))}">
        <div class="time-divider"><span>{time_text}</span></div>
        <div class="entry-toolbar">
          <h3>{title}</h3>
          <div class="actions">
            {button("edit", "编辑", ICON_EDIT)}
            {button("save", "保存", ICON_SAVE)}
            {button("preview", "预览", ICON_PREVIEW)}
            {button("delete", "删除", ICON_DELETE, True)}
          </div>
        </div>
        <div class="content">{source}</div>
        <textarea aria-label="编辑记录">{source}</textarea>
      </article>
"""


def merge_date_sections(document: str) -> str:
    pattern = re.compile(
        r'\n\s*<section class="date-section"[^>]*data-date="([^"]+)"[^>]*>\s*<h2>[\s\S]*?</h2>([\s\S]*?)\n\s*</section>',
        re.DOTALL,
    )
    sections = []
    order = []
    for match in pattern.finditer(document):
        date = html.unescape(match.group(1))
        if date not in sections:
            sections.append(date)
            order.append([date, ""])
        for item in order:
            if item[0] == date:
                item[1] += match.group(2).strip() + "\n"
                break

    if not order:
        return document

    merged = "\n".join(
        f"""

    <section class="date-section" data-date="{escape_attr(date)}">
      {date_heading_block(date)}
{content.rstrip()}
    </section>"""
        for date, content in order
    )
    return pattern.sub("", document).replace("\n  </main>", merged + "\n  </main>")


def upgrade_existing_html(existing: str) -> str:
    updated = existing
    updated = re.sub(r"<title>.*?</title>", f"<title>{APP_TITLE}</title>", updated, flags=re.DOTALL)
    updated = re.sub(r"<style>.*?</style>", f"<style>\n{STYLE}\n  </style>", updated, count=1, flags=re.DOTALL)
    updated = re.sub(r'\n\s*<script src="https://cdn\.jsdelivr\.net/npm/mermaid[^"]*"></script>', "", updated)
    updated = re.sub(r'\n\s*<script src="https://cdn\.jsdelivr\.net/npm/echarts[^"]*"></script>', "", updated)
    updated = updated.replace("</head>", f"{EXTERNAL_SCRIPTS}\n</head>")

    updated = re.sub(r"<header>[\s\S]*?</header>", build_header(), updated, count=1)
    updated = re.sub(r'<section class="date-section"(?![^>]*data-date)([^>]*)>\s*<h2>(.*?)</h2>', r'<section class="date-section"\1 data-date="\2">\n      <h2>\2</h2>', updated, flags=re.DOTALL)
    updated = re.sub(r'<article class="entry"[\s\S]*?</article>', lambda match: migrate_entry(match.group(0)), updated)
    updated = merge_date_sections(updated)
    updated = re.sub(
        r"<script>\s*const storagePrefix = .*?</script>",
        lambda _match: f"<script>\n{SCRIPT}\n  </script>",
        updated,
        count=1,
        flags=re.DOTALL,
    )
    return updated


def ensure_record_file(file_path: Path, date_heading: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.write_text(build_document(date_heading, ""), encoding="utf-8")
        return

    existing = file_path.read_text(encoding="utf-8")
    if "<html" not in existing.lower():
        file_path.write_text(build_document(date_heading, ""), encoding="utf-8")
        return

    upgraded = upgrade_existing_html(existing)
    if upgraded != existing:
        file_path.write_text(upgraded, encoding="utf-8")


def append_record_by_date(file_path: Path, content: str, title: Optional[str] = None) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    record_block = build_record_block(content, title)
    ensure_record_file(file_path, today)

    existing = file_path.read_text(encoding="utf-8")
    section_pattern = re.compile(
        rf'(<section class="date-section"[^>]*data-date="{re.escape(today)}"[^>]*>.*?)(\n\s*</section>)',
        re.DOTALL,
    )
    if section_pattern.search(existing):
        updated = section_pattern.sub(lambda match: match.group(1).rstrip() + "\n" + record_block + match.group(2), existing, count=1)
    else:
        new_section = f"""

    <section class="date-section" data-date="{escape_attr(today)}">
      {date_heading_block(today)}
{record_block}
    </section>
"""
        updated = existing.replace("\n  </main>", new_section + "\n  </main>")

    file_path.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record assistant reply into a date-grouped rich HTML note file."
    )
    parser.add_argument("--content", required=True, help="The assistant reply content to record.")
    parser.add_argument("--title", required=False, default=None, help="Optional title for this record.")
    parser.add_argument(
        "--output",
        required=False,
        default=os.path.join(DEFAULT_RECORD_DIR, DEFAULT_RECORD_FILE),
        help="Output HTML note file path.",
    )
    args = parser.parse_args()
    content = args.content.strip()

    if not content:
        print(json.dumps({
            "success": False,
            "file_path": args.output,
            "message": "Content is empty. Nothing was recorded.",
        }, ensure_ascii=False, indent=2))
        return

    file_path = Path(args.output)
    try:
        append_record_by_date(file_path=file_path, content=content, title=args.title)
        result = {
            "success": True,
            "file_path": str(file_path),
            "message": "Recorded successfully. Open the HTML file to edit and preview rich content.",
        }
    except Exception as error:
        result = {
            "success": False,
            "file_path": str(file_path),
            "message": f"Failed to record content: {error}",
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
