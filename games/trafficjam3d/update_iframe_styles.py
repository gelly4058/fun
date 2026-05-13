#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新游戏页面的iframe CSS样式
"""

import os
import re
import glob

def update_iframe_styles():
    # 定义新的CSS样式
    old_game_container = r'        \.game-container \{\s*padding: 2rem;\s*text-align: center;\s*max-width: 1000px;\s*margin: 0 auto;\s*\}'
    new_game_container = '''        .game-container {
            padding: 1.5rem;
            text-align: center;
            max-width: 1200px;
            margin: 0 auto;
        }'''
    
    old_game_iframe = r'        \.game-iframe \{\s*width: 100%;\s*max-width: 800px;\s*height: 600px;\s*border: none;\s*border-radius: 15px;\s*box-shadow: 0 8px 25px rgba\(0, 0, 0, 0\.3\);\s*margin: 2rem 0;\s*\}'
    new_game_iframe = '''        .game-iframe {
            width: 100%;
            max-width: 1000px;
            height: 700px;
            border: none;
            border-radius: 20px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
            margin: 1.5rem 0 3rem 0;
            background: #000;
            transition: all 0.3s ease;
        }
        .game-iframe:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
        }'''
    
    old_media_query = r'        @media \(max-width: 768px\) \{\s*\.game-iframe \{\s*height: 400px;\s*\}\s*\.game-container \{\s*padding: 1rem;\s*\}\s*\}'
    new_media_query = '''        @media (max-width: 1024px) {
            .game-iframe {
                max-width: 900px;
                height: 600px;
            }
        }
        @media (max-width: 768px) {
            .game-iframe {
                height: 450px;
                margin: 1rem 0 2rem 0;
                border-radius: 15px;
            }
            .game-container {
                padding: 1rem;
            }
        }
        @media (max-width: 480px) {
            .game-iframe {
                height: 350px;
                border-radius: 12px;
            }
        }'''
    
    # 获取所有游戏HTML文件
    games_dir = 'games'
    html_files = glob.glob(os.path.join(games_dir, '*.html'))
    
    # 排除不需要更新的文件
    exclude_files = ['index.html', 'play.html']
    html_files = [f for f in html_files if os.path.basename(f) not in exclude_files]
    
    updated_files = []
    
    for file_path in html_files:
        try:
            # 尝试不同的编码方式
            content = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                print(f"Could not decode {file_path} with any encoding")
                continue
                
            original_content = content
            
            # 更新game-container样式
            content = re.sub(
                r'        \.game-container \{[^}]*\}',
                new_game_container,
                content,
                flags=re.DOTALL
            )
            
            # 更新game-iframe样式
            content = re.sub(
                r'        \.game-iframe \{[^}]*\}',
                new_game_iframe,
                content,
                flags=re.DOTALL
            )
            
            # 更新媒体查询
            content = re.sub(
                r'        @media \(max-width: 768px\) \{[^}]*\}[^}]*\}',
                new_media_query,
                content,
                flags=re.DOTALL
            )
            
            # 如果内容有变化，写入文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
                updated_files.append(os.path.basename(file_path))
                print(f"Updated: {file_path}")
            
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
    
    print(f"\nTotal files updated: {len(updated_files)}")
    print("Updated files:")
    for file in updated_files:
        print(f"  - {file}")

if __name__ == '__main__':
    update_iframe_styles()