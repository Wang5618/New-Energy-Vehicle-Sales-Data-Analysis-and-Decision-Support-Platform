#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
汽车之家车型数据爬虫 (纯requests方案 v3)
爬取字段：品牌、车型、价格、续航、电池容量、用户评分
数据源：/grade/carhtml/ + /k.autohome.com.cn/
输出：autohome_cars.csv

用法：python autohome_spider.py

说明：
  - 品牌/车型/价格：从汽车之家车型大全字母页提取，覆盖率~100%
  - 用户评分：从口碑页提取（前N款）
  - 续航/电池容量：配置页为JS动态渲染，纯requests提取受限，
    建议使用Selenium版本获取（见autohome_spider_selenium.py）
"""

import csv
import os
import re
import sys
import time
import random
import traceback
import requests

# ============================================================
# 配置
# ============================================================
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autohome_cars.csv")
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
MAX_SCORE_FETCH = 7000
DELAY = (1.0, 2.5)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.autohome.com.cn/car/",
}


def safe_get(url, timeout=15):
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout)
            resp.encoding = resp.apparent_encoding or "utf-8"
            if resp.status_code == 200:
                return resp.text
        except Exception:
            pass
        time.sleep(2 * (attempt + 1))
    return None


# ============================================================
# 阶段1：从字母页提取基础数据
# ============================================================
def parse_letter_page(html, letter):
    cars = []
    # 提取品牌名
    brand_pattern = re.compile(
        r"<a\s+href=\"//car\.autohome\.com\.cn/price/brand-\d+-\d+\.html[^\"]*\"[^>]*>([^<]+)</a>"
    )
    brands = brand_pattern.findall(html)
    current_brand = brands[0] if brands else letter

    # 按 <li id="sXXXX"> 块解析
    li_pattern = re.compile(r"<li\s+id=\"s(\d+)\"[^>]*>(.*?)</li>", re.DOTALL)
    for li_m in li_pattern.finditer(html):
        sid = li_m.group(1)
        block = li_m.group(2)
        h4_m = re.search(r"<h4[^>]*>(.*?)</h4>", block, re.DOTALL)
        if not h4_m:
            continue
        model = re.sub(r"<[^>]*>", "", h4_m.group(1)).strip()
        if not model or len(model) < 2:
            continue
        price_m = re.search(r"指导价[：:]\s*<a[^>]*class='red'[^>]*>(.*?)</a>", block)
        price = price_m.group(1).strip() if price_m else "暂无"
        cars.append({
            "series_id": sid,
            "brand": current_brand,
            "model": model,
            "price": price,
        })
    return cars


def fetch_letter(letter):
    url = f"https://www.autohome.com.cn/grade/carhtml/{letter}.html"
    html = safe_get(url)
    if not html:
        return []
    return parse_letter_page(html, letter)


# ============================================================
# 阶段2：口碑评分
# ============================================================
def fetch_score(series_id):
    """从口碑页提取评分。HTML结构: <h4>口碑评分</h4>...<em>4.44</em>"""
    url = f"https://k.autohome.com.cn/{series_id}/"
    html = safe_get(url, timeout=10)
    if not html:
        return ""
    # 匹配: 口碑评分</h4>...<em>4.44</em>
    m = re.search(r'口碑评分</h4>.*?<em[^>]*>\s*([\d.]+)\s*</em>', html, re.DOTALL)
    if m:
        return m.group(1)
    # 备用: 直接去除标签后匹配
    plain = re.sub(r'<[^>]*>', ' ', html)
    m = re.search(r'口碑评分\s+([\d.]+)', plain)
    return m.group(1) if m else ""


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 60)
    print("汽车之家车型数据爬虫 v3")
    print("=" * 60)

    # ---- 阶段1：基础数据 ----
    print("\n[阶段1] 爬取基础数据 (A-Z)...")
    all_cars = []
    for letter in LETTERS:
        print(f"  [{letter}]", end=" ", flush=True)
        cars = fetch_letter(letter)
        all_cars.extend(cars)
        print(f"{len(cars)}款")
        time.sleep(random.uniform(*DELAY))
    print(f"\n[+] 共提取 {len(all_cars)} 款车型")

    # 去重
    seen = {}
    for c in all_cars:
        key = c["model"]
        if key not in seen or (c["price"] != "暂无" and seen[key]["price"] == "暂无"):
            seen[key] = c
    unique_cars = list(seen.values())
    print(f"[+] 去重后 {len(unique_cars)} 款")

    # ---- 阶段2：口碑评分 ----
    print(f"\n[阶段2] 获取口碑评分 (前{MAX_SCORE_FETCH}款)...")
    sample = [c for c in unique_cars if c.get("series_id")][:MAX_SCORE_FETCH]
    score_map = {}
    for i, car in enumerate(sample):
        sid = car.get("series_id", "")
        score = fetch_score(sid)
        if score:
            score_map[sid] = score
            print(f"  [{i+1}/{len(sample)}] {car['model'][:25]} → {score}分")
        else:
            print(f"  [{i+1}/{len(sample)}] {car['model'][:25]} → (无评分)")
        time.sleep(random.uniform(0.5, 1.5))
    print(f"[+] 获取到 {len(score_map)} 个评分")

    # ---- 阶段3：汇总输出 ----
    print(f"\n[阶段3] 汇总输出...")
    results = []
    for car in unique_cars:
        sid = car.get("series_id", "")
        results.append({
            "品牌": car.get("brand", ""),
            "车型": car["model"],
            "价格": car["price"],
            "续航(km)": "",   # 配置页为JS渲染，纯requests方案受限
            "电池容量(kWh)": "",
            "用户评分": score_map.get(sid, ""),
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["品牌", "车型", "价格", "续航(km)", "电池容量(kWh)", "用户评分"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{'=' * 60}")
    print(f"[DONE] {len(results)} 条记录 → {OUTPUT_FILE}")
    print(f"  品牌/车型/价格: 完整提取")
    print(f"  用户评分: {len(score_map)} 条")
    print(f"  续航/电池容量: 需Selenium方案 (配置页JS动态渲染)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
    except Exception as e:
        print(f"\n[!] 错误: {e}")
        traceback.print_exc()
