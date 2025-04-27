#!/usr/bin/env python3

import os
import argparse
import sys
from .main import StaticSiteGenerator

def main():
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument('--content', help='Content directory', default='content')
    parser.add_argument('--templates', help='Templates directory', default='ssg/templates')
    parser.add_argument('--static', help='Static files directory', default='ssg/static')
    parser.add_argument('--output', help='Output directory', default='html')
    
    args = parser.parse_args()
    
    # Get the current working directory
    base_dir = os.getcwd()
    
    # Set up paths
    content_dir = os.path.join(base_dir, args.content)
    template_dir = os.path.join(base_dir, args.templates)
    static_dir = os.path.join(base_dir, args.static)
    output_dir = os.path.join(base_dir, args.output)
    
    # Validate directories
    if not os.path.exists(content_dir):
        print(f"Error: Content directory '{content_dir}' does not exist.")
        sys.exit(1)
    
    if not os.path.exists(template_dir):
        print(f"Error: Templates directory '{template_dir}' does not exist.")
        sys.exit(1)
    
    # Build the site
    ssg = StaticSiteGenerator(content_dir, template_dir, static_dir, output_dir)
    ssg.build()

if __name__ == "__main__":
    main() 