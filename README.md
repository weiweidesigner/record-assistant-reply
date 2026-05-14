# Record Assistant Reply HTML Note Skill

这个 Skill 用于记录当前或上一条机器人回复，并追加到同一个 HTML 笔记文件中。

页面标题为“我的AI笔记”。最新记录展示在当天最前面。页面是白底简洁风格，支持深色模式、PDF 单页导出、图标操作和悬停提示、删除记录、按日期卡片分组，以及 Mermaid、ECharts、图片和视频渲染。

## 使用方式

```bash
python scripts/record_reply.py \
  --content "这里是需要记录的机器人回复" \
  --title "可选标题"
```

默认会生成或更新：

```bash
records/assistant_reply_diary.html
```

## 富内容写法

Mermaid：

```markdown
```mermaid
flowchart TD
  A --> B
```
```

ECharts：

```markdown
```echarts
{"xAxis":{"type":"category","data":["A","B"]},"yAxis":{"type":"value"},"series":[{"type":"bar","data":[3,5]}]}
```
```

图片：

```markdown
![图片说明](https://example.com/image.png)
```

视频：

```markdown
![视频说明](https://example.com/video.mp4)
```
