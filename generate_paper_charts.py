# -*- coding: utf-8 -*-
"""
批量生成论文写作用静态图表与统计表。

输入：data/visualization_data.json
输出：
  - outputs/figures/*.png / *.svg：论文可直接插入的高清图
  - outputs/tables/*.csv / *.md：论文可引用的统计表
  - outputs/chart_index.md：图表清单与论文使用建议

运行：python generate_paper_charts.py
"""

import json
import math
import os
from datetime import datetime, timezone

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_PATH = "data/visualization_data.json"
FIGURE_DIR = "outputs/figures"
TABLE_DIR = "outputs/tables"
INDEX_PATH = "outputs/chart_index.md"

FIGURES = []
TABLES = []


def ensure_dirs():
    os.makedirs(FIGURE_DIR, exist_ok=True)
    os.makedirs(TABLE_DIR, exist_ok=True)


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def setup_style():
    """设置适合中文论文的绘图风格。"""
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS", "DejaVu Sans"
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 140
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["axes.titlesize"] = 15
    plt.rcParams["axes.labelsize"] = 11


def save_figure(fig, filename, title, usage):
    png_path = os.path.join(FIGURE_DIR, f"{filename}.png")
    svg_path = os.path.join(FIGURE_DIR, f"{filename}.svg")
    fig.tight_layout()
    fig.savefig(png_path, bbox_inches="tight")
    fig.savefig(svg_path, bbox_inches="tight")
    plt.close(fig)
    FIGURES.append({"title": title, "png": png_path, "svg": svg_path, "usage": usage})


def save_table(df, filename, title, usage):
    csv_path = os.path.join(TABLE_DIR, f"{filename}.csv")
    md_path = os.path.join(TABLE_DIR, f"{filename}.md")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    with open(md_path, "w", encoding="utf-8") as file:
        file.write(dataframe_to_markdown(df))
        file.write("\n")
    TABLES.append({"title": title, "csv": csv_path, "md": md_path, "usage": usage})


def dataframe_to_markdown(df):
    """不依赖 tabulate，直接把 DataFrame 转成 Markdown 表格。"""
    columns = [str(column) for column in df.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for column in df.columns:
            value = "" if pd.isna(row[column]) else str(row[column])
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def pct(value, total):
    return round(value / total * 100, 2) if total else 0


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def get_community_df(data):
    rows = []
    for item in data.get("enriched_community_skills", []):
        metrics = item.get("github_metrics") or {}
        detail = item.get("score_detail") or {}
        updated = parse_date(metrics.get("pushed_at") or metrics.get("updated_at"))
        days_since_update = None
        if updated:
            days_since_update = (datetime.now(timezone.utc) - updated.astimezone(timezone.utc)).days
        rows.append({
            "name": item.get("name"),
            "scenario_category": item.get("scenario_category"),
            "recommend_score": item.get("recommend_score") or 0,
            "rating_name": item.get("rating_name"),
            "rating_stars": item.get("rating_stars"),
            "effect": item.get("effect"),
            "language": metrics.get("language") or "未知",
            "stars": metrics.get("stars") or 0,
            "forks": metrics.get("forks") or 0,
            "readme_length": metrics.get("readme_length") or 0,
            "days_since_update": days_since_update,
            "场景匹配度": detail.get("scenario_match") or 0,
            "GitHub热度": detail.get("github_popularity") or 0,
            "维护活跃度": detail.get("maintenance") or 0,
            "文档质量": detail.get("documentation") or 0,
            "项目可信度": detail.get("trust") or 0,
            "功能明确度": detail.get("clarity") or 0,
        })
    return pd.DataFrame(rows)


def figure_source_pie(data):
    overview = data["overview"]
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    values = [overview["official_total"], overview["community_total"]]
    labels = ["官方 Skill", "社区 Skill"]
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#2563eb", "#7c3aed"],
        wedgeprops={"linewidth": 1, "edgecolor": "white", "width": 0.45},
        textprops={"fontsize": 11},
    )
    ax.text(0, 0, f"N={overview['total']}", ha="center", va="center", fontsize=14, weight="bold")
    ax.set_title("Skill 数据来源结构")
    save_figure(fig, "fig01_source_structure_pie", "图1 Skill 数据来源结构", "用于论文数据概况部分，说明官方与社区 Skill 的占比。")


def figure_official_company_top(data):
    df = pd.DataFrame(data.get("official_companies", [])).head(15)
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.barplot(data=df, y="company", x="count", ax=ax, color="#2563eb")
    ax.set_title("官方机构 Skill 供给数量 Top 15")
    ax.set_xlabel("Skill 数量")
    ax.set_ylabel("官方机构")
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=9)
    save_figure(fig, "fig02_official_company_top15_bar", "图2 官方机构 Skill 供给数量 Top 15", "用于分析官方 Skill 生态中的头部机构集中情况。")


def figure_scenario_top(data):
    rows = [
        {"场景类别": item["category"], "数量": item["count"]}
        for item in data.get("community_categories", [])
        if item.get("count", 0) > 0
    ]
    df = pd.DataFrame(rows).sort_values("数量", ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=df, y="场景类别", x="数量", ax=ax, hue="场景类别", palette="viridis", legend=False)
    ax.set_title("社区 Skill 应用场景数量分布 Top 15")
    ax.set_xlabel("Skill 数量")
    ax.set_ylabel("应用场景")
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=9)
    save_figure(fig, "fig03_community_scenario_top15_bar", "图3 社区 Skill 应用场景数量分布 Top 15", "用于论文结果分析部分，展示社区 Skill 的主要应用方向。")


def figure_rating_distribution(df):
    order = ["夯", "顶级", "人上人", "NPC", "拉完了"]
    counts = df["rating_name"].value_counts().reindex(order).fillna(0).astype(int)
    fig, ax = plt.subplots(figsize=(8, 5.2))
    bars = ax.bar(counts.index, counts.values, color=["#16a34a", "#2563eb", "#7c3aed", "#f97316", "#ef4444"])
    ax.set_title("社区 Skill 推荐评级分布")
    ax.set_xlabel("推荐评级")
    ax.set_ylabel("Skill 数量")
    ax.bar_label(bars, labels=[f"{v}\n({pct(v, len(df))}%)" for v in counts.values], padding=3, fontsize=9)
    save_figure(fig, "fig04_rating_distribution_bar", "图4 社区 Skill 推荐评级分布", "用于说明社区项目整体推荐质量的等级结构。")


def figure_score_histogram(df):
    fig, ax = plt.subplots(figsize=(8.5, 5.4))
    sns.histplot(df["recommend_score"], bins=18, kde=True, ax=ax, color="#2563eb")
    ax.axvline(df["recommend_score"].mean(), color="#ef4444", linestyle="--", label=f"均值={df['recommend_score'].mean():.1f}")
    ax.set_title("社区 Skill 综合推荐得分分布")
    ax.set_xlabel("综合推荐得分")
    ax.set_ylabel("频数")
    ax.legend()
    save_figure(fig, "fig05_recommend_score_histogram", "图5 社区 Skill 综合推荐得分分布", "用于观察推荐分数是否集中、高分项目占比与总体离散情况。")


def figure_score_box_by_scenario(df):
    top_categories = df["scenario_category"].value_counts().head(12).index
    plot_df = df[df["scenario_category"].isin(top_categories)].copy()
    order = plot_df.groupby("scenario_category")["recommend_score"].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(11, 7))
    sns.boxplot(data=plot_df, y="scenario_category", x="recommend_score", order=order, ax=ax, color="#bfdbfe")
    sns.stripplot(data=plot_df, y="scenario_category", x="recommend_score", order=order, ax=ax, size=3, color="#2563eb", alpha=0.45)
    ax.set_title("主要应用场景下推荐得分差异")
    ax.set_xlabel("综合推荐得分")
    ax.set_ylabel("应用场景")
    save_figure(fig, "fig06_score_boxplot_by_scenario", "图6 主要应用场景下推荐得分差异", "用于比较不同应用场景 Skill 的推荐质量差异。")


def figure_language_distribution(df):
    lang = df["language"].value_counts().head(12).reset_index()
    lang.columns = ["语言", "数量"]
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    sns.barplot(data=lang, x="数量", y="语言", ax=ax, hue="语言", palette="mako", legend=False)
    ax.set_title("社区 GitHub 项目主要开发语言分布 Top 12")
    ax.set_xlabel("项目数量")
    ax.set_ylabel("开发语言")
    for container in ax.containers:
        ax.bar_label(container, padding=3, fontsize=9)
    save_figure(fig, "fig07_github_language_top12_bar", "图7 社区 GitHub 项目主要开发语言分布 Top 12", "用于说明社区 Skill 的技术栈分布。")


def figure_stars_vs_score(df):
    plot_df = df.copy()
    plot_df["log_stars"] = plot_df["stars"].apply(lambda x: math.log10(x + 1))
    fig, ax = plt.subplots(figsize=(8.5, 5.8))
    sns.scatterplot(data=plot_df, x="log_stars", y="recommend_score", hue="rating_name", size="forks", sizes=(20, 220), alpha=0.72, ax=ax)
    ax.set_title("GitHub Star 热度与推荐得分关系")
    ax.set_xlabel("log10(stars + 1)")
    ax.set_ylabel("综合推荐得分")
    ax.legend(title="评级/分叉数", bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    save_figure(fig, "fig08_stars_vs_score_scatter", "图8 GitHub Star 热度与推荐得分关系", "用于分析项目热度是否与推荐质量存在相关趋势。")


def figure_score_dimension_heatmap(df):
    dimensions = ["场景匹配度", "GitHub热度", "维护活跃度", "文档质量", "项目可信度", "功能明确度"]
    top_categories = df["scenario_category"].value_counts().head(12).index
    heat = df[df["scenario_category"].isin(top_categories)].groupby("scenario_category")[dimensions].mean()
    heat = heat.loc[heat.mean(axis=1).sort_values(ascending=False).index]
    fig, ax = plt.subplots(figsize=(9.5, 7))
    sns.heatmap(heat, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("不同应用场景的评分维度均值热力图")
    ax.set_xlabel("评分维度")
    ax.set_ylabel("应用场景")
    save_figure(fig, "fig09_score_dimension_heatmap", "图9 不同应用场景的评分维度均值热力图", "用于解释不同场景在热度、维护、文档等维度上的差异。")


def figure_maintenance_distribution(df):
    bins = [-1, 30, 90, 180, 365, 10000]
    labels = ["30天内", "31-90天", "91-180天", "181-365天", "365天以上"]
    valid = df.dropna(subset=["days_since_update"]).copy()
    valid["维护间隔"] = pd.cut(valid["days_since_update"], bins=bins, labels=labels)
    counts = valid["维护间隔"].value_counts().reindex(labels).fillna(0).astype(int)
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    bars = ax.bar(counts.index.astype(str), counts.values, color="#0891b2")
    ax.set_title("社区 GitHub 项目最近维护时间分布")
    ax.set_xlabel("距最近更新/推送时间")
    ax.set_ylabel("项目数量")
    ax.bar_label(bars, padding=3, fontsize=9)
    save_figure(fig, "fig10_maintenance_recency_bar", "图10 社区 GitHub 项目最近维护时间分布", "用于衡量社区 Skill 项目的维护活跃程度。")


def figure_readme_vs_score(df):
    plot_df = df.copy()
    plot_df["log_readme_length"] = plot_df["readme_length"].apply(lambda x: math.log10(x + 1))
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    sns.regplot(data=plot_df, x="log_readme_length", y="recommend_score", ax=ax, scatter_kws={"alpha": 0.45, "s": 32}, line_kws={"color": "#ef4444"})
    ax.set_title("README 文档长度与推荐得分关系")
    ax.set_xlabel("log10(README 长度 + 1)")
    ax.set_ylabel("综合推荐得分")
    save_figure(fig, "fig11_readme_length_vs_score", "图11 README 文档长度与推荐得分关系", "用于讨论文档质量与项目推荐结果之间的关系。")


def build_tables(data, df):
    overview = data["overview"]
    overview_df = pd.DataFrame([
        ["总 Skill 数", overview["total"], "100%"],
        ["官方 Skill 数", overview["official_total"], f"{pct(overview['official_total'], overview['total'])}%"],
        ["社区 Skill 数", overview["community_total"], f"{pct(overview['community_total'], overview['total'])}%"],
        ["官方机构数", overview["official_company_count"], "—"],
        ["社区场景类别数", overview["community_category_count"], "—"],
    ], columns=["指标", "数值", "占比"])
    save_table(overview_df, "table01_overview_statistics", "表1 数据集总体统计", "用于论文数据来源和样本概况部分。")

    scenario_rows = []
    for item in data.get("community_categories", []):
        if item.get("count", 0) <= 0:
            continue
        scenario_rows.append({
            "场景类别": item["category"],
            "Skill数量": item["count"],
            "占社区比例(%)": pct(item["count"], overview["community_total"]),
            "推荐数量": item["recommended_count"],
            "代表Skill": item.get("recommended", [{}])[0].get("name", "—") if item.get("recommended") else "—",
        })
    scenario_df = pd.DataFrame(scenario_rows).sort_values("Skill数量", ascending=False)
    save_table(scenario_df, "table02_scenario_distribution", "表2 社区 Skill 应用场景分布", "用于论文结果分析中的类别统计表。")

    top_df = df.sort_values("recommend_score", ascending=False).head(30)[[
        "name", "scenario_category", "recommend_score", "rating_name", "effect", "stars", "forks", "language"
    ]].rename(columns={
        "name": "Skill名称",
        "scenario_category": "场景类别",
        "recommend_score": "推荐得分",
        "rating_name": "评级",
        "effect": "具体作用",
        "stars": "Stars",
        "forks": "Forks",
        "language": "语言",
    })
    save_table(top_df, "table03_top30_recommended_skills", "表3 社区 Skill 综合推荐 Top 30", "用于论文展示代表性高质量项目。")

    dimensions = ["场景匹配度", "GitHub热度", "维护活跃度", "文档质量", "项目可信度", "功能明确度", "recommend_score"]
    score_summary = df[dimensions].describe().T.reset_index()
    score_summary = score_summary[["index", "mean", "std", "min", "25%", "50%", "75%", "max"]]
    score_summary.columns = ["指标", "均值", "标准差", "最小值", "25%分位", "中位数", "75%分位", "最大值"]
    score_summary = score_summary.round(2)
    save_table(score_summary, "table04_score_dimension_descriptive_statistics", "表4 推荐评分维度描述性统计", "用于论文方法评价或实证结果的统计描述。")

    official_rows = []
    for company in data.get("official_companies", []):
        examples = company.get("examples", [])[:3]
        row = {
            "公司/机构": company.get("company", "—"),
            "Skill数量": company.get("count", 0),
        }
        for index in range(3):
            example = examples[index] if index < len(examples) else {}
            name = example.get("name", "—")
            effect = example.get("effect", "—")
            row[f"代表Skill{index + 1}"] = f"{name} - {effect}" if name != "—" else "—"
        official_rows.append(row)
    official_df = pd.DataFrame(official_rows).sort_values("Skill数量", ascending=False)
    save_table(
        official_df,
        "table05_official_skill_recommendation_collection",
        "表5 官方 Skill 推荐集合总表",
        "用于论文展示官方 Skill 集合：按公司/机构汇总 Skill 数量，并列出 3 个代表 Skill。",
    )

    community_rows = []
    community_summary_rows = []
    for category in data.get("community_categories", []):
        category_name = category.get("category", "—")
        all_recommended = category.get("recommended", [])
        high_score_items = [item for item in all_recommended if (item.get("recommend_score") or 0) >= 70]
        selected_items = high_score_items[:5]
        recommendation_type = "正式推荐"
        if not selected_items and all_recommended:
            selected_items = all_recommended[:1]
            recommendation_type = "候选推荐"
        if not selected_items:
            continue

        community_summary_rows.append({
            "场景类别": category_name,
            "原始Skill数量": category.get("count", 0),
            "推荐数量": len(selected_items),
            "最高得分": max(item.get("recommend_score") or 0 for item in selected_items),
            "推荐类型": recommendation_type,
            "代表Skill示例": "；".join(item.get("name", "—") for item in selected_items[:3]),
            "代表Skill链接": selected_items[0].get("link", ""),
        })

        for rank, item in enumerate(selected_items, start=1):
            metrics = item.get("github_metrics") or {}
            community_rows.append({
                "场景类别": item.get("scenario_category") or category_name,
                "类别内排名": rank,
                "Skill名称": item.get("name", "—"),
                "链接": item.get("link", ""),
                "推荐得分": item.get("recommend_score", 0),
                "评级": f"{item.get('rating_stars', '')} {item.get('rating_name', '')}".strip(),
                "具体作用": item.get("effect", "—"),
                "Stars": metrics.get("stars") or 0,
                "Forks": metrics.get("forks") or 0,
                "语言": metrics.get("language") or "未知",
            })
    community_df = pd.DataFrame(community_rows)
    save_table(
        community_df,
        "table06_community_skill_recommendation_collection",
        "表6 社区 Skill 分领域推荐集合总表",
        "用于论文展示社区 Skill 推荐集合：以场景类别为组织单位，每类最多 5 个正式推荐；若无 70 分以上 Skill，则保留最高分 1 个作为候选推荐。",
    )

    community_summary_df = pd.DataFrame(community_summary_rows).sort_values(["推荐类型", "最高得分"], ascending=[True, False])
    save_table(
        community_summary_df,
        "table07_community_recommendation_summary",
        "表7 社区 Skill 分领域推荐摘要表",
        "用于论文正文展示每个场景类别的推荐数量、最高得分和代表 Skill 示例，避免正文表格过长。",
    )


def write_index():
    lines = [
        "# 论文图表输出清单",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 图目录",
        "",
    ]
    for idx, item in enumerate(FIGURES, start=1):
        lines.extend([
            f"### {idx}. {item['title']}",
            f"- PNG：`{item['png']}`",
            f"- SVG：`{item['svg']}`",
            f"- 论文用途：{item['usage']}",
            "",
        ])
    lines.extend(["## 表目录", ""])
    for idx, item in enumerate(TABLES, start=1):
        lines.extend([
            f"### {idx}. {item['title']}",
            f"- CSV：`{item['csv']}`",
            f"- Markdown：`{item['md']}`",
            f"- 论文用途：{item['usage']}",
            "",
        ])
    with open(INDEX_PATH, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def main():
    ensure_dirs()
    setup_style()
    data = load_data()
    df = get_community_df(data)

    figure_source_pie(data)
    figure_official_company_top(data)
    figure_scenario_top(data)
    figure_rating_distribution(df)
    figure_score_histogram(df)
    figure_score_box_by_scenario(df)
    figure_language_distribution(df)
    figure_stars_vs_score(df)
    figure_score_dimension_heatmap(df)
    figure_maintenance_distribution(df)
    figure_readme_vs_score(df)
    build_tables(data, df)
    write_index()

    print("论文图表生成完成。")
    print(f"图文件：{len(FIGURES)} 组，输出目录：{FIGURE_DIR}")
    print(f"表文件：{len(TABLES)} 组，输出目录：{TABLE_DIR}")
    print(f"图表索引：{INDEX_PATH}")


if __name__ == "__main__":
    main()