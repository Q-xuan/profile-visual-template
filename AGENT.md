# AGENT.md · profile visual template

这份文件给后续改主页的人或 agent 看。先改 `template/config.json`，再跑出图脚本。不要手改生成后的 README 排版。

Skill：[GitHub profile visual](sand-workflow:github-profile-visual)

## 文件

| 路径 | 作用 |
|---|---|
| `template/config.json` | 文案和五个项目。改主页先改这个 |
| `template/banner-source.png` | 无字山水素图 |
| `scripts/compose_profile.py` | 生成头图、卡片、README |
| `assets/header.png` | 生成的头图 |
| `assets/works.png` | 生成的五张卡 |
| `README.md` | 在 `USERNAME/USERNAME` 里，这就是主页 |
| `examples/` | 预览和 Q-xuan 的一份实例 config |

## 怎么更新

```sh
python3 scripts/compose_profile.py
```

只改一句中文：编辑 `line1` / `line2`。
只换项目：编辑 `cards`，标题必须四个汉字。
只换背景：替换 `banner-source.png`，字仍然只画在左侧。

## 视觉

- 墨黑底、骨色字、朱砂竖线、暗金辅字
- 山干净。禁止词云
- 左侧可留 `Agent  ·  Harness  ·  Context  ·  rg`
- 标签四个字，能看懂。不要「只读」「名物」「寻迹」

## 文案

- 中文先写人话，再带 geek 名词
- 英文给工具和术语
- 未完成、汉化、fork、study 仓库放 Also，不当主卡

## GitHub 边界

不能写 CSS / JS，不能改左侧栏和贡献日历。置顶、简介、时区在 Settings 里改。
