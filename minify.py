#!/usr/bin/env python3
"""
Code Minification Script for Karachuonyo Website
Minifies HTML, CSS, and JavaScript for better performance
"""

import re
import os
import shutil
from pathlib import Path

def minify_html(html_content):
    """Minify HTML content by removing unnecessary whitespace and comments"""
    # Remove HTML comments (but keep conditional comments)
    html_content = re.sub(r'<!--(?!\s*(?:\[if|<!|>)).*?-->', '', html_content, flags=re.DOTALL)
    
    # Remove extra whitespace between tags
    html_content = re.sub(r'>\s+<', '><', html_content)
    
    # Remove leading/trailing whitespace from lines
    lines = html_content.split('\n')
    minified_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            minified_lines.append(stripped)
    
    return '\n'.join(minified_lines)

def minify_css(css_content):
    """Minify CSS content by removing comments and unnecessary whitespace"""
    # Remove CSS comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove extra whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # Remove whitespace around specific characters
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
    
    # Remove trailing semicolons before closing braces
    css_content = re.sub(r';\s*}', '}', css_content)
    
    return css_content.strip()

def minify_js(js_content):
    """Basic JavaScript minification (removes comments and extra whitespace)"""
    # Remove single-line comments (but preserve URLs)
    js_content = re.sub(r'(?<!:)//(?![^\n]*["\'])[^\n]*', '', js_content)
    
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    
    # Remove extra whitespace
    js_content = re.sub(r'\s+', ' ', js_content)
    
    # Remove whitespace around operators and punctuation
    js_content = re.sub(r'\s*([{}();,=+\-*/<>!&|])\s*', r'\1', js_content)
    
    return js_content.strip()

def process_html_file(file_path):
    """Process HTML file and minify embedded CSS and JavaScript"""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content)
    
    # Minify CSS within <style> tags
    def minify_style_content(match):
        css_content = match.group(1)
        minified_css = minify_css(css_content)
        return f'<style>{minified_css}</style>'
    
    content = re.sub(r'<style[^>]*>(.*?)</style>', minify_style_content, content, flags=re.DOTALL)
    
    # Minify JavaScript within <script> tags (excluding external scripts)
    def minify_script_content(match):
        full_tag = match.group(0)
        if 'src=' in full_tag:
            return full_tag  # Don't minify external scripts
        
        js_content = match.group(1)
        minified_js = minify_js(js_content)
        return f'<script{match.group(0).split(">")[0].split("<script")[1]}>{minified_js}</script>'
    
    content = re.sub(r'<script([^>]*)>(.*?)</script>', minify_script_content, content, flags=re.DOTALL)
    
    # Minify the HTML structure
    minified_content = minify_html(content)
    
    # Create minified version
    minified_path = file_path.replace('.html', '.min.html')
    
    with open(minified_path, 'w', encoding='utf-8') as f:
        f.write(minified_content)
    
    new_size = len(minified_content)
    reduction = ((original_size - new_size) / original_size) * 100
    
    print(f"Original size: {original_size:,} bytes")
    print(f"Minified size: {new_size:,} bytes")
    print(f"Size reduction: {reduction:.1f}%")
    print(f"Minified file saved as: {minified_path}")
    
    return minified_path

def create_production_build():
    """Create a production-ready build with minified files"""
    print("Creating production build...")
    
    # Create build directory
    build_dir = Path('build')
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    # Process HTML files
    html_files = list(Path('.').glob('*.html'))
    
    for html_file in html_files:
        if '.min.' not in html_file.name:
            minified_path = process_html_file(str(html_file))
            
            # Copy minified file to build directory
            build_file = build_dir / html_file.name
            shutil.copy2(minified_path, build_file)
            
            print(f"Copied {minified_path} to {build_file}")
    
    # Copy other assets
    asset_extensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico']
    
    for ext in asset_extensions:
        for asset_file in Path('.').glob(f'*{ext}'):
            if not asset_file.name.startswith('.'):
                dest_file = build_dir / asset_file.name
                shutil.copy2(asset_file, dest_file)
                print(f"Copied asset: {asset_file} -> {dest_file}")
    
    print(f"\nProduction build completed in '{build_dir}' directory")
    print("Files are optimized for deployment")

if __name__ == '__main__':
    print("Karachuonyo Website Minification Tool")
    print("=====================================")
    
    # Check if index.html exists
    if not os.path.exists('index.html'):
        print("Error: index.html not found in current directory")
        exit(1)
    
    try:
        # Process individual file
        process_html_file('index.html')
        
        print("\n" + "="*50)
        
        # Create production build
        create_production_build()
        
        print("\nMinification completed successfully!")
        print("\nFiles created:")
        print("- index.min.html (minified version)")
        print("- build/ directory (production build)")
        
    except Exception as e:
        print(f"Error during minification: {e}")
        exit(1)