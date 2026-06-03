# -*- coding: utf-8 -*-
"""
生成数据可视化与 Skill 推荐所需的数据文件。

输入：
    data/skills.json
    data/github_repo_metrics.json

输出：
    data/visualization_data.json

展示规则：
    推荐 skill 页面只展示：名称 + 星级 + 评级名 + 具体作用
    例如：AgriciDaniel/claude-seo ⭐⭐⭐⭐⭐ 夯 - 网站 SEO 分析与优化
"""

import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from urllib.parse import urlparse


SKILLS_PATH = "data/skills.json"
GITHUB_METRICS_PATH = "data/github_repo_metrics.json"
OUTPUT_PATH = "data/visualization_data.json"


SCENARIO_CATEGORIES = [
    # 先匹配更具体的行业/专业场景，避免被 Agent、开发、大模型等通用技术类抢走
    {
        "name": "网络安全",
        "keywords": ["security", "cyber", "audit", "vulnerability", "defense", "threat", "secure", "waf", "xss", "sql injection"],
    },
    {
        "name": "法律合同",
        "keywords": ["legal", "law", "contract", "compliance", "policy", "privacy", "gdpr"],
    },
    {
        "name": "金融分析",
        "keywords": ["finance", "financial", "cfo", "accounting", "market research", "business", "revenue", "pricing", "saas"],
    },
    {
        "name": "教育学习",
        "keywords": ["education", "tutor", "learning", "resume", "career", "interview", "study", "quiz"],
    },
    {
        "name": "医疗健康",
        "keywords": ["health", "medical", "clinic", "medicine", "wellness", "monitoring", "aiops", "alarm"],
    },
    {
        "name": "科研论文",
        "keywords": ["paper", "academic", "arxiv", "scientific", "citation", "literature", "research", "experiment", "hypothesis"],
    },
    {
        "name": "电商零售",
        "keywords": ["ecommerce", "e-com", "commerce", "shop", "shopping", "store", "retail", "product marketing", "product video", "sales", "customer journey"],
    },
    {
        "name": "增长广告",
        "keywords": ["seo", "growth", "ads", "advertising", "competitor", "landing page", "homepage audit", "conversion", "analytics", "programmatic seo"],
    },
    {
        "name": "社媒运营",
        "keywords": ["social", "twitter", "tweet", "x/", "linkedin", "threads", "bluesky", "mastodon", "whatsapp", "post", "publish", "scheduler", "giveaway"],
    },
    {
        "name": "邮件营销",
        "keywords": ["email", "cold email", "outreach", "newsletter", "courier", "notification", "message", "dm", "lifecycle email"],
    },
    {
        "name": "视频创作",
        "keywords": ["video", "youtube", "clip", "movie", "film", "summarization", "transcript", "frame"],
    },
    {
        "name": "图片生成",
        "keywords": ["image", "photo", "picture", "generate image", "image generate", "image edit", "upscaling", "background removal", "imagen"],
    },
    {
        "name": "语音音频",
        "keywords": ["voice", "tts", "asr", "speech", "audio", "transcription", "transcribe", "podcast", "music", "sound"],
    },
    {
        "name": "写作文案",
        "keywords": ["writing", "write", "copywriting", "copy-editing", "prose", "humanizer", "rewrite", "humanize", "article", "blog", "content strategy", "beautiful prose"],
    },
    {
        "name": "办公文档",
        "keywords": ["doc", "document", "pdf", "ppt", "slides", "presentation", "notion", "notebooklm", "knowledge", "meeting", "excel", "xlsx"],
    },
    {
        "name": "界面设计",
        "keywords": ["ui", "ux", "figma", "interface", "frontend design", "web design", "design system", "ui-ux"],
    },
    {
        "name": "编程开发",
        "keywords": ["typescript", "python", "java", "rust", "angular", "swift", "rails", "frontend", "code", "coding", "sdk", "api", "developer", "terraform", "playwright"],
    },
    {
        "name": "自动工作流",
        "keywords": ["workflow", "automation", "automate", "mcp", "n8n", "browser", "scraper", "extract", "agent workflow"],
    },
    {
        "name": "提示工程",
        "keywords": ["agent", "agents", "claude", "prompt", "context", "memory", "multi-agent", "parallel", "superpowers", "skill", "codex"],
    },
    {
        "name": "大模型",
        "keywords": ["llm", "nemo", "megatron", "tensorrt", "model", "training", "inference", "rl", "evaluator", "benchmark", "gpu", "optimizer"],
    },
    {
        "name": "数据检索",
        "keywords": ["data", "dataset", "qdrant", "vector", "rag", "search", "database", "embedding", "retrieval"],
    },
]


ACTION_WORDS = [
    "generate", "create", "analyze", "summarize", "optimize", "convert", "extract",
    "publish", "schedule", "monitor", "review", "debug", "automate", "train",
    "deploy", "search", "edit", "build", "detect", "rewrite", "translate"
]


EFFECT_RULES = [
    ("security", "安全审计与漏洞防护"),
    ("cyber", "网络安全与风险防护"),
    ("legal", "法律合规与政策文档处理"),
    ("contract", "合同与合规文档处理"),
    ("finance", "财务分析与商业决策"),
    ("financial", "财务分析与商业决策"),
    ("resume", "简历优化与求职准备"),
    ("interview", "面试准备与访谈整理"),
    ("health", "健康信息分析与系统监测"),
    ("medical", "医疗健康信息分析"),
    ("paper", "科研论文分析"),
    ("arxiv", "科研论文分析"),
    ("academic", "学术资料分析"),
    ("scientific", "科研资料分析"),
    ("research", "研究调研与资料分析"),
    ("seo", "网站搜索优化与增长分析"),
    ("ecommerce", "电商运营与商品营销"),
    ("commerce", "电商运营与商品营销"),
    ("product marketing", "产品营销与转化优化"),
    ("sales", "销售转化与客户运营"),
    ("email", "邮件营销与用户触达"),
    ("twitter", "社交平台内容发布与运营"),
    ("tweet", "社交平台内容发布与运营"),
    ("whatsapp", "即时通讯自动化与消息运营"),
    ("video", "视频生成、理解或处理"),
    ("youtube", "YouTube 视频处理与分析"),
    ("image", "图片生成与编辑"),
    ("audio", "音频生成、转录或处理"),
    ("voice", "语音合成与语音代理"),
    ("tts", "语音合成"),
    ("asr", "语音识别"),
    ("writing", "写作辅助与文本优化"),
    ("copywriting", "文案生成与优化"),
    ("humanizer", "AI 文本人性化改写"),
    ("markdown", "Markdown 转换与格式化"),
    ("ppt", "PPT 生成与演示文稿处理"),
    ("slides", "演示文稿生成与美化"),
    ("pdf", "PDF 文档处理与转换"),
    ("document", "文档处理与知识整理"),
    ("notion", "知识库管理与内容整理"),
    ("rag", "检索增强生成与知识问答"),
    ("qdrant", "向量搜索与数据库优化"),
    ("vector", "向量检索与数据搜索"),
    ("agent", "智能体工作流与任务协作"),
    ("prompt", "提示词设计与上下文优化"),
    ("mcp", "工具协议集成与自动化"),
    ("workflow", "自动化工作流搭建"),
    ("automation", "自动化流程处理"),
    ("typescript", "前端类型脚本开发辅助"),
    ("python", "编程开发辅助"),
    ("angular", "前端应用开发"),
    ("swiftui", "苹果界面开发实践"),
    ("llm", "大语言模型训练、推理或评估"),
    ("nemo", "大模型工程与训练优化"),
    ("megatron", "大模型训练工程"),
    ("tensorrt", "大模型推理加速优化"),
]


SCENARIO_DEFAULT_EFFECTS = {
    "网络安全": "安全审计与风险防护",
    "法律合同": "法律合规与政策文档处理",
    "金融分析": "财务分析与商业决策",
    "教育学习": "学习辅助与职业发展",
    "医疗健康": "健康信息分析与系统监测",
    "科研论文": "科研论文与学术资料分析",
    "电商零售": "电商运营与商品营销",
    "增长广告": "搜索优化、增长与广告投放",
    "社媒运营": "社媒内容运营与发布",
    "邮件营销": "邮件营销与用户触达",
    "视频创作": "视频创作、理解与处理",
    "图片生成": "图片生成与编辑处理",
    "语音音频": "语音音频处理与识别合成",
    "写作文案": "写作辅助与文本优化",
    "办公文档": "办公文档处理与知识管理",
    "界面设计": "界面设计与用户体验优化",
    "编程开发": "编程开发与框架实践",
    "自动工作流": "自动化工作流与工具集成",
    "提示工程": "智能体与提示词工程",
    "大模型": "大模型训练、推理与评估",
    "数据检索": "数据检索、向量搜索与知识问答",
    "其他 / 暂未明确": "综合型人工智能技能应用",
}


# 人工修正规则：用于修正关键词自动分类中明显不准确的个别 Skill。
# 后续如果发现某条推荐结果分类或中文作用不准，只需要在这里补一行。
MANUAL_CATEGORY_OVERRIDES = {
    "NVIDIA/NeMo-RL/launch-nemo-rl": "大模型",
    "NVIDIA/NemoClaw/nemoclaw-user-manage-policy": "法律合同",
    "NVIDIA/NeMo-RL/auto-research": "科研论文",
}


MANUAL_EFFECT_OVERRIDES = {
    "NVIDIA/NeMo-RL/launch-nemo-rl": "大模型强化学习训练启动与运行",
    "NVIDIA/NemoClaw/nemoclaw-user-manage-policy": "大模型系统策略管理与合规控制",
    "deanpeters/business-health-diagnostic": "商业健康度诊断与经营分析",
    "NVIDIA/NeMo-RL/auto-research": "自动化科研实验探索",
}


def load_json(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def parse_github_repo(link):
    parsed = urlparse(link or "")
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def is_official(skill):
    return "officialskills.sh" in (skill.get("link") or "")


def get_text(skill):
    return " ".join([
        skill.get("name") or "",
        skill.get("description") or "",
        skill.get("category") or "",
    ]).lower()


def get_core_text(skill):
    """只使用名称和描述，避免原始 category 干扰具体作用判断。"""
    return " ".join([
        skill.get("name") or "",
        skill.get("description") or "",
    ]).lower()


def classify_scenario(skill):
    name = skill_display_name(skill)
    if name in MANUAL_CATEGORY_OVERRIDES:
        return MANUAL_CATEGORY_OVERRIDES[name]

    text = get_text(skill)
    for category in SCENARIO_CATEGORIES:
        if any(keyword in text for keyword in category["keywords"]):
            return category["name"]
    return "其他 / 暂未明确"


def scenario_match_score(skill, scenario):
    text = get_text(skill)
    category = next((item for item in SCENARIO_CATEGORIES if item["name"] == scenario), None)
    if not category:
        return 8

    hits = sum(1 for keyword in category["keywords"] if keyword in text)
    if hits >= 3:
        return 25
    if hits == 2:
        return 18
    if hits == 1:
        return 12
    return 5


def github_popularity_score(metrics):
    stars = metrics.get("stars") or 0
    forks = metrics.get("forks") or 0

    if stars >= 5000:
        score = 18
    elif stars >= 1000:
        score = 15
    elif stars >= 200:
        score = 12
    elif stars >= 50:
        score = 8
    elif stars >= 10:
        score = 5
    else:
        score = 2

    if forks >= 50:
        score += 2
    elif forks >= 10:
        score += 1

    return min(score, 20)


def parse_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def maintenance_score(metrics):
    if metrics.get("archived"):
        return 0

    date = parse_datetime(metrics.get("pushed_at") or metrics.get("updated_at"))
    if not date:
        return 3

    days = (datetime.now(timezone.utc) - date.astimezone(timezone.utc)).days
    if days <= 30:
        return 20
    if days <= 90:
        return 16
    if days <= 180:
        return 12
    if days <= 365:
        return 8
    return 3


def documentation_score(metrics):
    if not metrics.get("has_readme"):
        return 0
    length = metrics.get("readme_length") or 0
    if length > 8000:
        return 15
    if length >= 2000:
        return 12
    if length >= 500:
        return 9
    return 5


def trust_score(metrics):
    score = 0
    if metrics.get("fetch_status") == "ok":
        score += 2
    if metrics.get("license"):
        score += 3
    if not metrics.get("archived") and not metrics.get("disabled"):
        score += 2
    if not metrics.get("is_fork"):
        score += 1
    if (metrics.get("related_skill_count") or 0) > 1:
        score += 2
    return min(score, 10)


def clarity_score(skill):
    description = (skill.get("description") or "").lower()
    if not description:
        return 0
    hits = sum(1 for word in ACTION_WORDS if word in description)
    if hits >= 2:
        return 10
    if hits == 1:
        return 7
    if len(description) >= 40:
        return 6
    return 3


def score_detail(skill, scenario, metrics):
    """返回推荐评分明细，便于论文解释和后续可视化。"""
    detail = {
        "scenario_match": scenario_match_score(skill, scenario),
        "github_popularity": github_popularity_score(metrics),
        "maintenance": maintenance_score(metrics),
        "documentation": documentation_score(metrics),
        "trust": trust_score(metrics),
        "clarity": clarity_score(skill),
    }
    detail["total"] = max(0, min(100, sum(detail.values())))
    return detail


def rating_from_score(score):
    if score >= 85:
        return "⭐⭐⭐⭐⭐", "夯"
    if score >= 70:
        return "⭐⭐⭐⭐", "顶级"
    if score >= 55:
        return "⭐⭐⭐", "人上人"
    if score >= 40:
        return "⭐⭐", "NPC"
    return "⭐", "拉完了"


def effect_from_skill(skill, scenario=None):
    name = skill_display_name(skill)
    if name in MANUAL_EFFECT_OVERRIDES:
        return MANUAL_EFFECT_OVERRIDES[name]

    text = get_core_text(skill)
    for keyword, effect in EFFECT_RULES:
        if keyword in text:
            return effect

    return SCENARIO_DEFAULT_EFFECTS.get(scenario, "综合型人工智能技能应用")


def recommended_count(total):
    if total <= 3:
        return total
    if total <= 10:
        return 3
    if total <= 30:
        return 5
    if total <= 80:
        return 8
    return 10


def skill_display_name(skill):
    return skill.get("name") or "未命名 Skill"


def build_visualization_data():
    skills_data = load_json(SKILLS_PATH)
    metrics_data = load_json(GITHUB_METRICS_PATH, {"repositories": {}})
    skills = skills_data.get("skills", [])
    repo_metrics = metrics_data.get("repositories", {})

    official_skills = [skill for skill in skills if is_official(skill)]
    community_skills = [skill for skill in skills if not is_official(skill)]

    official_by_company = defaultdict(list)
    for skill in official_skills:
        name = skill_display_name(skill)
        company = name.split("/")[0] if "/" in name else name
        official_by_company[company].append(skill)

    official_companies = []
    for company, items in sorted(official_by_company.items(), key=lambda item: len(item[1]), reverse=True):
        official_companies.append({
            "company": company,
            "count": len(items),
            "examples": [
                {
                    "name": skill_display_name(skill),
                    "effect": effect_from_skill(skill),
                    "link": skill.get("link"),
                }
                for skill in items[:5]
            ],
        })

    scenario_groups = defaultdict(list)
    enriched_skills = []
    for skill in community_skills:
        scenario = classify_scenario(skill)
        repo_id = parse_github_repo(skill.get("link"))
        metrics = repo_metrics.get(repo_id or "", {})
        detail = score_detail(skill, scenario, metrics)
        score = detail["total"]
        stars, rating_name = rating_from_score(score)
        effect = effect_from_skill(skill, scenario)
        item = {
            "name": skill_display_name(skill),
            "description": skill.get("description"),
            "link": skill.get("link"),
            "source_type": "community",
            "original_category": skill.get("category"),
            "scenario_category": scenario,
            "repo": repo_id,
            "recommend_score": score,
            "score_detail": detail,
            "rank_in_category": None,
            "rating_stars": stars,
            "rating_name": rating_name,
            "effect": effect,
            "display_text": f"{skill_display_name(skill)} {stars} {rating_name} - {effect}",
            "github_metrics": {
                "stars": metrics.get("stars"),
                "forks": metrics.get("forks"),
                "updated_at": metrics.get("updated_at"),
                "pushed_at": metrics.get("pushed_at"),
                "language": metrics.get("language"),
                "license": metrics.get("license"),
                "readme_length": metrics.get("readme_length"),
                "fetch_status": metrics.get("fetch_status"),
            },
        }
        scenario_groups[scenario].append(item)
        enriched_skills.append(item)

    community_categories = []
    scenario_order = [item["name"] for item in SCENARIO_CATEGORIES] + ["其他 / 暂未明确"]
    for scenario in scenario_order:
        items = scenario_groups.get(scenario, [])
        sorted_items = sorted(items, key=lambda item: item["recommend_score"], reverse=True)
        for rank, item in enumerate(sorted_items, start=1):
            item["rank_in_category"] = rank
        limit = recommended_count(len(sorted_items))
        community_categories.append({
            "category": scenario,
            "count": len(sorted_items),
            "recommended_count": limit,
            "recommended": sorted_items[:limit],
        })

    rating_distribution = Counter(item["rating_name"] for item in enriched_skills)

    result = {
        "generated_at": datetime.now().isoformat(),
        "overview": {
            "total": len(skills),
            "official_total": len(official_skills),
            "community_total": len(community_skills),
            "official_company_count": len(official_by_company),
            "community_category_count": len(community_categories),
        },
        "rating_labels": {
            "5": {"stars": "⭐⭐⭐⭐⭐", "name": "夯", "score_range": "85-100"},
            "4": {"stars": "⭐⭐⭐⭐", "name": "顶级", "score_range": "70-84"},
            "3": {"stars": "⭐⭐⭐", "name": "人上人", "score_range": "55-69"},
            "2": {"stars": "⭐⭐", "name": "NPC", "score_range": "40-54"},
            "1": {"stars": "⭐", "name": "拉完了", "score_range": "0-39"},
        },
        "score_model": {
            "total": 100,
            "dimensions": [
                {"name": "场景匹配度", "points": 25},
                {"name": "GitHub 热度", "points": 20},
                {"name": "维护活跃度", "points": 20},
                {"name": "文档质量", "points": 15},
                {"name": "项目可信度", "points": 10},
                {"name": "功能明确度", "points": 10},
            ],
        },
        "official_companies": official_companies,
        "community_categories": community_categories,
        "enriched_community_skills": sorted(
            enriched_skills,
            key=lambda item: (item["scenario_category"], item["rank_in_category"] or 999999),
        ),
        "community_rating_distribution": dict(rating_distribution),
        "manual_overrides": {
            "category_overrides": MANUAL_CATEGORY_OVERRIDES,
            "effect_overrides": MANUAL_EFFECT_OVERRIDES,
        },
    }
    save_json(OUTPUT_PATH, result)
    return result


def main():
    result = build_visualization_data()
    print(f"生成完成：{OUTPUT_PATH}")
    print(f"总数：{result['overview']['total']}")
    print(f"官方：{result['overview']['official_total']}，社区：{result['overview']['community_total']}")
    print(f"官方公司数：{result['overview']['official_company_count']}")
    print(f"社区分类数：{result['overview']['community_category_count']}")
    print("\n社区分类推荐预览：")
    for category in result["community_categories"][:5]:
        print(f"- {category['category']}：{category['count']} 个，推荐 {category['recommended_count']} 个")
        for item in category["recommended"][:3]:
            print(f"  {item['display_text']}")


if __name__ == "__main__":
    main()