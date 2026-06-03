#!/usr/bin/env python3
"""生成 GitHub README 格式的技能推荐文件，每个 skill 名字可点击跳转。"""
import json

OUTPUT_FILE = "outputs/GITHUB_SKILL_RECOMMENDATIONS.md"

def load_data():
    with open("data/visualization_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_github_url(skill):
    """从skill数据中提取GitHub链接"""
    link = skill.get("link", "")
    if link:
        return link
    repo = skill.get("repo", "")
    if repo and not repo.startswith("http"):
        return f"https://github.com/{repo}"
    return repo

def write_official_section(f, data):
    """表4：官方技能来源"""
    official = data.get("official_companies", [])

    f.write("## 📚 官方技能来源\n\n")
    f.write("本技能商店收录了来自以下顶级团队的官方技能：\n\n")

    # official_companies 已经是按 count 降序排列的
    for comp_data in official:
        company = comp_data["company"]
        count = comp_data["count"]
        examples = comp_data.get("examples", [])

        # 选取前5个代表 skill，构建可点击链接
        representative = []
        for ex in examples[:5]:
            skill_name = ex["name"]
            skill_link = ex.get("link", "")
            # 简化显示名（取最后的路径部分）
            if "/" in skill_name:
                short = skill_name.split("/")[-1]
            else:
                short = skill_name

            if skill_link:
                representative.append(f"[`{short}`]({skill_link})")
            else:
                representative.append(f"`{short}`")

        display_list = "、".join(representative) if representative else "—"
        if count > 5:
            display_list += " 等"

        f.write(f"- **{company}** ({count}个) - {display_list}\n")

    f.write("\n")

def write_community_section(f, data):
    """表5：社区技能分领域推荐"""
    categories = data.get("community_categories", [])

    f.write("## 💾 社区技能库\n\n")

    for cat in categories:
        cat_name = cat.get("category", "未知")
        count = cat.get("count", 0)
        recommended = cat.get("recommended", [])

        if not recommended:
            continue

        f.write(f"### {cat_name}（{count}个）\n\n")

        for skill in recommended:
            name = skill.get("name", "")
            desc = skill.get("effect", skill.get("description", ""))
            stars = skill.get("rating_stars", "")
            rating_name = skill.get("rating_name", "")

            github_url = get_github_url(skill)

            # 构建星级显示
            if stars and rating_name:
                star_display = f"{stars} {rating_name}"
            elif stars:
                star_display = stars
            else:
                star_display = ""

            # 构建可点击的链接
            if github_url:
                link = f"[{name}]({github_url})"
            else:
                link = f"`{name}`"

            desc_text = f" - {desc}" if desc else ""

            f.write(f"- {link} {star_display}{desc_text}\n")

        f.write("\n")


def main():
    data = load_data()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# 🤖 Claude Skill Recommendations\n\n")
        write_official_section(f, data)
        write_community_section(f, data)

    print(f"✅ GitHub README 技能推荐文件已生成：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()