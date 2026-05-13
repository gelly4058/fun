#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏页面生成脚本
用于从GameMonetize API获取游戏数据并为每个游戏生成独立的HTML页面
"""

import requests
import json
import os
import re
from urllib.parse import quote
from datetime import datetime

class GamePageGenerator:
    def __init__(self):
        self.feed_url = 'https://gamemonetize.com/feed.php?format=0&name=traffic&num=50&page=1'
        self.games_dir = 'games'
        self.template_file = 'games/game_template.html'
        
    def fetch_games_data(self):
        """获取游戏数据"""
        try:
            print("正在获取游戏数据...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://gamemonetize.com/'
            }
            response = requests.get(self.feed_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            games_data = response.json()
            print(f"成功获取 {len(games_data)} 个游戏数据")
            
            # 保存原始数据用于分析
            with open('games_data.json', 'w', encoding='utf-8') as f:
                json.dump(games_data, f, indent=2, ensure_ascii=False)
            
            return games_data
            
        except Exception as e:
            print(f"获取游戏数据失败: {e}")
            return []
    
    def analyze_game_structure(self, games_data):
        """分析游戏数据结构"""
        if not games_data:
            return
            
        print("\n=== 游戏数据结构分析 ===")
        sample_game = games_data[0]
        
        print("游戏对象包含的字段:")
        for key, value in sample_game.items():
            print(f"  {key}: {type(value).__name__} - {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
        
        # 分析关键字段
        print("\n=== 关键字段分析 ===")
        key_fields = ['title', 'description', 'url', 'thumb', 'category', 'tags']
        for field in key_fields:
            if field in sample_game:
                print(f"✓ {field}: {sample_game[field]}")
            else:
                print(f"✗ {field}: 字段不存在")
    
    def sanitize_filename(self, title):
        """清理文件名，移除特殊字符"""
        # 移除或替换特殊字符
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '-', filename.strip())
        filename = filename.lower()
        return filename[:50]  # 限制长度
    
    def create_game_template(self):
        """创建游戏页面模板"""
        template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Traffic Jam 3D Games</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{title} - Traffic Jam 3D Games">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{thumb}">
    <meta property="og:url" content="{page_url}">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} - Traffic Jam 3D Games">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{thumb}">
    
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-3SXS6THN83"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        
        gtag('config', 'G-3SXS6THN83');
    </script>
    
    <link rel="stylesheet" href="../style.css">
    <style>
        .game-container 
            padding: 2rem;
            text-align: center;
            max-width: 1000px;
            margin: 0 auto;
        
        .game-iframe {
            width: 100%;
            max-width: 800px;
            height: 600px;
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            margin: 2rem 0;
        }
        .game-info {
            background: rgba(26, 26, 26, 0.8);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: left;
        }
        .game-info h2 {
            color: #FFD700;
            margin-bottom: 1rem;
        }
        .game-info p {
            color: #c0c0c0;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        .back-link {
            display: inline-block;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            color: #1a1a1a;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 1rem;
            transition: all 0.3s ease;
        }
        .back-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
        }
        @media (max-width: 768px) {
            .game-iframe {
                height: 400px;
            }
            .game-container {
                padding: 1rem;
            }
        }
    </style>
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Game",
        "name": "{title}",
        "description": "{description}",
        "image": "{thumb}",
        "url": "{page_url}",
        "genre": "{category}",
        "gamePlatform": "Web Browser",
        "operatingSystem": "Any",
        "applicationCategory": "Game",
        "offers": {{
             "@type": "Offer",
             "price": "0",
             "priceCurrency": "USD"
         }}
     }}
    </script>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                <h1><a href="../index.html">Traffic Jam 3D</a></h1>
            </div>
            <nav class="nav">
                <ul>
                    <li><a href="../index.html" class="nav-link">Home</a></li>
                    <li><a href="index.html" class="nav-link">More Games</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <main class="main">
        <div class="container">
            <div class="game-container">
                <h1>{title}</h1>
                <iframe class="game-iframe" src="{game_url}" allowfullscreen></iframe>
                
                <div class="game-info">
                    <h2>About This Game</h2>
                    <p>{description}</p>
                    {category_info}
                    <a href="index.html" class="back-link">← Back to Games</a>
                </div>
            </div>
        </div>
    </main>
</body>
</html>'''
        
        os.makedirs(self.games_dir, exist_ok=True)
        with open(self.template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"游戏页面模板已创建: {self.template_file}")
    
    def run_generation(self):
        """运行生成模式"""
        if not os.path.exists('games_data.json'):
            print(f"游戏数据文件不存在: games_data.json")
            print("请先运行分析模式")
            return
        
        if not os.path.exists(self.template_file):
            print(f"模板文件不存在: {self.template_file}")
            print("请先运行分析模式")
            return
        
        # 加载游戏数据
        with open('games_data.json', 'r', encoding='utf-8') as f:
            games_data = json.load(f)
        
        # 加载模板
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        print(f"=== 开始生成 {len(games_data)} 个游戏页面 ===")
        
        generated_games = []
        for i, game in enumerate(games_data):
            try:
                # 生成文件名
                filename = self.sanitize_filename(game['title'])
                filepath = os.path.join('games', f'{filename}.html')
                
                # 准备模板变量
                template_vars = {
                    'title': game['title'],
                    'description': game['description'][:160] + '...' if len(game['description']) > 160 else game['description'],
                    'keywords': game.get('tags', '') + ', traffic games, html5 games',
                    'thumb': game['thumb'],
                    'page_url': f'https://yourdomain.com/games/{filename}.html',  # 需要替换为实际域名
                    'game_url': game['url'],
                    'category': game.get('category', 'Game'),
                    'category_info': f'<p><strong>Category:</strong> {game.get("category", "Game")}</p>' if game.get('category') else ''
                }
                
                # 替换模板变量
                html_content = template
                for key, value in template_vars.items():
                    html_content = html_content.replace(f'{{{key}}}', str(value))
                
                # 写入文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                generated_games.append({
                    'title': game['title'],
                    'filename': filename,
                    'filepath': filepath,
                    'id': game.get('id', i)
                })
                
                print(f"✓ 已生成: {filepath}")
                
            except Exception as e:
                print(f"✗ 生成失败 {game['title']}: {e}")
        
        # 保存生成的游戏列表
        with open('games/generated_games.json', 'w', encoding='utf-8') as f:
            json.dump(generated_games, f, ensure_ascii=False, indent=2)
        
        print(f"\n=== 生成完成 ===")
        print(f"成功生成 {len(generated_games)} 个游戏页面")
        print(f"游戏列表已保存到: games/generated_games.json")
        print("\n下一步需要更新 games/index.html 中的链接")

if __name__ == '__main__':
    import sys
    
    generator = GamePageGenerator()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'generate':
        generator.run_generation()
    else:
        generator.run_analysis()
