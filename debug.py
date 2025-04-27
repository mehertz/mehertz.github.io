#!/usr/bin/env python3

from ssg.main import StaticSiteGenerator
import os

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.join(base_dir, 'content')
    template_dir = os.path.join(base_dir, 'ssg', 'templates')
    static_dir = os.path.join(base_dir, 'ssg', 'static')
    output_dir = os.path.join(base_dir, 'html')
    
    print(f"Base directory: {base_dir}")
    print(f"Content directory: {content_dir}")
    print(f"Template directory: {template_dir}")
    print(f"Static directory: {static_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Test if output directory is writable
    test_file = os.path.join(output_dir, 'test.txt')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        print(f"Successfully wrote to {test_file}")
        os.remove(test_file)
    except Exception as e:
        print(f"Error writing to output directory: {e}")
    
    # Check if template directory exists and list templates
    if os.path.exists(template_dir):
        print(f"Template directory exists: {template_dir}")
        print("Templates available:")
        for filename in os.listdir(template_dir):
            print(f" - {filename}")
    else:
        print(f"Template directory does not exist: {template_dir}")
    
    # Initialize SSG
    ssg = StaticSiteGenerator(content_dir, template_dir, static_dir, output_dir)
    
    # Run the build
    try:
        ssg.build()
        print("Build completed successfully")
    except Exception as e:
        print(f"Build failed: {e}")
    
    # Check output directory contents
    if os.path.exists(output_dir):
        print(f"Output directory contents: {output_dir}")
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            file_size = os.path.getsize(filepath)
            print(f" - {filename} ({file_size} bytes)")
    else:
        print(f"Output directory does not exist: {output_dir}") 