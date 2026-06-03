# -*- coding: utf-8 -*-
"""
AI Agent Skills 数据爬取入口

只爬取 VoltAgent/awesome-agent-skills 的 README 列表数据，
并保存为本地 JSON，供后续数据可视化页面使用。
不会下载任何 skill 仓库或 skill 文件夹。
"""

import argparse
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import LOG_DIR, LOG_FILE
from crawler import SkillCrawler
from data_manager import DataManager


def setup_logging(verbose: bool = False):
    """配置日志系统"""
    os.makedirs(LOG_DIR, exist_ok=True)

    log_level = logging.DEBUG if verbose else logging.INFO
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    return root_logger


def crawl_and_save() -> bool:
    """执行一次数据爬取，并保存 JSON 数据"""
    crawler = SkillCrawler()
    data_manager = DataManager()

    skills = crawler.crawl()
    if not skills:
        print("爬取失败：没有获取到技能数据")
        return False

    valid_skills = crawler.filter_valid_skills(skills)
    if not valid_skills:
        print("爬取失败：没有有效技能数据")
        return False

    data_manager.save_skills(valid_skills)
    data_manager.save_summary(valid_skills)
    data_manager.save_update_time()

    print(f"爬取完成：共保存 {len(valid_skills)} 条技能数据")
    print("数据文件：data/skills.json")
    print("汇总文件：data/skills_summary.json")
    return True


def show_stats():
    """显示当前本地 JSON 数据统计"""
    data_manager = DataManager()
    skills = data_manager.load_skills()
    if not skills:
        print("暂无技能数据，请先运行：python main.py --crawl")
        return

    categories = {}
    for skill in skills:
        category = skill.get('category', '未分类')
        categories[category] = categories.get(category, 0) + 1

    print("\n技能数据统计")
    print(f"总计：{len(skills)} 个技能")
    print(f"分类数：{len(categories)}")
    print("\n各分类技能数：")
    for category, count in sorted(categories.items(), key=lambda item: item[1], reverse=True):
        print(f"  {category}: {count}")

    last_update = data_manager.get_last_update_time()
    if last_update:
        print(f"\n最后更新：{last_update.strftime('%Y-%m-%d %H:%M:%S')}")


def export_csv(output_path: str):
    """导出技能数据为 CSV"""
    data_manager = DataManager()
    skills = data_manager.load_skills()
    if not skills:
        print("暂无技能数据，请先运行：python main.py --crawl")
        return

    if data_manager.export_to_csv(skills, output_path):
        print(f"成功导出 {len(skills)} 条数据到：{output_path}")
    else:
        print("导出失败")


def main():
    parser = argparse.ArgumentParser(
        description='AI Agent Skills 数据爬取工具（只保存 JSON，不下载 skill 文件夹）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python main.py --crawl
  python main.py --stats
  python main.py --export skills.csv
        """
    )
    parser.add_argument('--crawl', action='store_true', help='爬取最新技能数据并保存为 JSON')
    parser.add_argument('--stats', action='store_true', help='显示当前数据统计')
    parser.add_argument('--export', metavar='FILE', help='导出技能数据为 CSV 文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细日志')

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.crawl:
        success = crawl_and_save()
        if not success:
            sys.exit(1)
    elif args.stats:
        show_stats()
    elif args.export:
        export_csv(args.export)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()