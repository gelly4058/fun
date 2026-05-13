import os
import re
from pathlib import Path

def fix_iframe_styles():
    """修复所有游戏页面的iframe居中样式问题"""
    games_dir = Path('games')
    
    # 新的清理后的CSS样式
    new_styles = '''    <style>
        /* Override main styles for better game display */
        .game-container {
            padding: 1.5rem !important;
            text-align: center !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }
        
        .game-iframe {
            width: 100% !important;
            max-width: 1000px !important;
            height: 700px !important;
            border: none !important;
            border-radius: 20px !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4) !important;
            margin: 1.5rem auto 3rem auto !important;
            background: #000 !important;
            transition: all 0.3s ease !important;
            display: block !important;
            aspect-ratio: unset !important;
        }
        
        .game-iframe:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5) !important;
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
        
        /* Responsive Design */
        @media (max-width: 1024px) {
            .game-iframe {
                max-width: 900px !important;
                height: 600px !important;
            }
        }
        
        @media (max-width: 768px) {
            .game-iframe {
                height: 450px !important;
                margin: 1rem auto 2rem auto !important;
                border-radius: 15px !important;
            }
            .game-container {
                padding: 1rem !important;
            }
        }
        
        @media (max-width: 480px) {
            .game-iframe {
                height: 350px !important;
                border-radius: 12px !important;
            }
        }
    </style>'''
    
    updated_files = []
    error_files = []
    
    # 遍历所有HTML文件
    for html_file in games_dir.glob('*.html'):
        if html_file.name in ['index.html', 'play.html', 'game_template.html']:
            continue
            
        try:
            # 尝试多种编码方式读取文件
            content = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    with open(html_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                error_files.append(f"{html_file.name} - 无法读取文件")
                continue
            
            # 查找并替换<style>标签内容
            # 使用正则表达式匹配从<style>到</style>的所有内容
            style_pattern = r'<style>.*?</style>'
            
            if re.search(style_pattern, content, re.DOTALL):
                # 替换样式内容
                new_content = re.sub(style_pattern, new_styles, content, flags=re.DOTALL)
                
                # 写入文件
                with open(html_file, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(new_content)
                
                updated_files.append(html_file.name)
            else:
                error_files.append(f"{html_file.name} - 未找到<style>标签")
                
        except Exception as e:
            error_files.append(f"{html_file.name} - {str(e)}")
    
    print(f"成功更新 {len(updated_files)} 个文件:")
    for file in updated_files:
        print(f"  - {file}")
    
    if error_files:
        print(f"\n处理失败 {len(error_files)} 个文件:")
        for error in error_files:
            print(f"  - {error}")
    
    return len(updated_files), len(error_files)

if __name__ == '__main__':
    updated, errors = fix_iframe_styles()
    print(f"\n总计: 更新 {updated} 个文件, 失败 {errors} 个文件")