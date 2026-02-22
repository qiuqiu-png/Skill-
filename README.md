# Claude Code Skills Collection

My personal collection of Claude Code skills, organized by category.

## Categories

### Data & Excel Tools

| Skill | Description |
|---|---|
| [excel-insert-images](excel-insert-images/) | Batch insert images into Excel cells, matching by filename |
| [excel-comment-images](excel-comment-images/) | Insert images as Excel cell comments (hover to preview) |
| [excel-row-copier](excel-row-copier/) | Batch copy rows in Excel/WPS spreadsheets |
| [image-batch-processor](image-batch-processor/) | Batch compress and convert images to JPG |
| [document-skills](document-skills/) | PDF processing (form filling, conversion, extraction) |

### Video Tools

| Skill | Description |
|---|---|
| [video-to-portrait](video-to-portrait/) | Convert landscape video to 9:16 portrait with blur background |
| [video-crop-borders](video-crop-borders/) | Auto-detect and crop black borders from video |
| [video-random-concatenate](video-random-concatenate/) | Split video into segments and randomly reassemble |
| [youtube-clipper](youtube-clipper/) | YouTube video clipper with bilingual subtitle support |

### Design & Creative

| Skill | Description |
|---|---|
| [frontend-design](frontend-design/) | Production-grade frontend UI design |
| [canvas-design](canvas-design/) | Create visual art in PNG/PDF with Canvas |
| [algorithmic-art](algorithmic-art/) | Generative art with p5.js |
| [theme-factory](theme-factory/) | Apply pre-set or custom themes to any artifact |

### Dev Tools

| Skill | Description |
|---|---|
| [mcp-builder](mcp-builder/) | Guide for building MCP servers (Python/TypeScript) |
| [webapp-testing](webapp-testing/) | Playwright-based web app testing toolkit |
| [remotion-best-practices](remotion-best-practices/) | Best practices for Remotion (React video framework) |
| [doc-coauthoring](doc-coauthoring/) | Structured workflow for co-authoring documentation |

### Meta Skills (for creating new skills)

| Skill | Description |
|---|---|
| [skill-from-github](skill-from-github/) | Create skills by learning from GitHub projects |
| [skill-from-masters](skill-from-masters/) | Create skills from real-world golden examples |
| [skill-from-notebook](skill-from-notebook/) | Extract methodologies from documents into skills |

## Setup

```bash
# Clone to Claude Code skills directory
git clone git@github.com:qiuqiu-png/Skill-.git ~/.claude/skills

# Dependencies
pip install openpyxl pandas Pillow  # Excel & image skills
brew install ffmpeg                  # Video skills
```

## License

- Official skills (from [anthropics/skills](https://github.com/anthropics/skills)): subject to original license
- Custom skills: personal use
