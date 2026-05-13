import os
import re
from pathlib import Path
from html.parser import HTMLParser

class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.warnings = []
        self.tag_stack = []
        self.line_num = 1
        
    def handle_starttag(self, tag, attrs):
        if tag not in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']:
            self.tag_stack.append((tag, self.line_num))
            
    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1][0] == tag:
            self.tag_stack.pop()
        elif tag not in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']:
            self.errors.append(f"Line {self.line_num}: Unexpected closing tag </{tag}>")
            
    def handle_data(self, data):
        self.line_num += data.count('\n')
        
    def error(self, message):
        self.errors.append(f"Line {self.line_num}: {message}")
        
    def get_unclosed_tags(self):
        return [(tag, line) for tag, line in self.tag_stack]

def validate_css(css_content):
    """验证CSS语法"""
    errors = []
    warnings = []
    
    # 检查括号匹配
    brace_count = css_content.count('{') - css_content.count('}')
    if brace_count != 0:
        errors.append(f"CSS括号不匹配: {brace_count} 个未闭合的括号")
    
    # 检查常见CSS错误
    lines = css_content.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line and not line.startswith('/*') and not line.endswith('*/'):
            # 检查属性声明
            if ':' in line and not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                if not any(keyword in line for keyword in ['@media', '@import', '@keyframes']):
                    warnings.append(f"Line {i}: CSS属性可能缺少分号: {line}")
    
    return errors, warnings

def validate_html_file(file_path):
    """验证单个HTML文件"""
    try:
        # 尝试多种编码读取文件
        content = None
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            return ["无法读取文件 - 编码错误"], [], []
        
        # HTML结构验证
        validator = HTMLValidator()
        try:
            validator.feed(content)
        except Exception as e:
            validator.errors.append(f"HTML解析错误: {str(e)}")
        
        # 检查未闭合的标签
        unclosed_tags = validator.get_unclosed_tags()
        for tag, line in unclosed_tags:
            validator.errors.append(f"Line {line}: 未闭合的标签 <{tag}>")
        
        # CSS验证
        css_errors = []
        css_warnings = []
        
        # 提取<style>标签中的CSS
        style_pattern = r'<style[^>]*>(.*?)</style>'
        style_matches = re.findall(style_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for css_content in style_matches:
            errors, warnings = validate_css(css_content)
            css_errors.extend(errors)
            css_warnings.extend(warnings)
        
        # 检查基本HTML结构
        structure_errors = []
        if '<!DOCTYPE html>' not in content and '<!doctype html>' not in content.lower():
            structure_errors.append("缺少DOCTYPE声明")
        
        if '<html' not in content.lower():
            structure_errors.append("缺少<html>标签")
            
        if '<head>' not in content.lower():
            structure_errors.append("缺少<head>标签")
            
        if '<body>' not in content.lower():
            structure_errors.append("缺少<body>标签")
        
        # 检查iframe标签
        iframe_pattern = r'<iframe[^>]*class=["\']game-iframe["\'][^>]*>'
        if not re.search(iframe_pattern, content, re.IGNORECASE):
            structure_errors.append("缺少game-iframe类的iframe标签")
        
        all_errors = validator.errors + css_errors + structure_errors
        all_warnings = validator.warnings + css_warnings
        
        return all_errors, all_warnings, []
        
    except Exception as e:
        return [f"文件处理错误: {str(e)}"], [], []

def main():
    """主函数 - 验证所有游戏页面"""
    games_dir = Path('games')
    
    total_files = 0
    files_with_errors = 0
    files_with_warnings = 0
    
    print("开始验证HTML文件...\n")
    
    # 遍历所有HTML文件
    for html_file in sorted(games_dir.glob('*.html')):
        if html_file.name in ['index.html', 'play.html', 'game_template.html']:
            continue
            
        total_files += 1
        print(f"验证文件: {html_file.name}")
        
        errors, warnings, info = validate_html_file(html_file)
        
        if errors:
            files_with_errors += 1
            print(f"  ❌ 发现 {len(errors)} 个错误:")
            for error in errors:
                print(f"    - {error}")
        
        if warnings:
            files_with_warnings += 1
            print(f"  ⚠️  发现 {len(warnings)} 个警告:")
            for warning in warnings:
                print(f"    - {warning}")
        
        if not errors and not warnings:
            print("  ✅ 文件格式正确")
        
        print()
    
    # 总结报告
    print("=" * 50)
    print("验证总结:")
    print(f"总文件数: {total_files}")
    print(f"有错误的文件: {files_with_errors}")
    print(f"有警告的文件: {files_with_warnings}")
    print(f"完全正确的文件: {total_files - files_with_errors - files_with_warnings}")
    
    if files_with_errors == 0:
        print("\n🎉 所有文件都没有严重错误!")
    else:
        print(f"\n⚠️  需要修复 {files_with_errors} 个文件的错误")

if __name__ == '__main__':
    main()