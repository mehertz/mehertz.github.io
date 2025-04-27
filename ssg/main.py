#!/usr/bin/env python3

import os
import shutil
import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader
import json


def load_config(base_dir):
    config_path = os.path.join(base_dir, '..', 'config.json')  # Assumes config.json is in the parent directory
    defaults = {
        'site_title': 'My Default Blog Title',
        'year': 2024,
        'site_description': 'A default site description.'
    }
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Merge defaults with loaded config
        defaults.update(config)
        return defaults
    except FileNotFoundError:
        print(f"Warning: config.json not found at {config_path}. Using default values.")
        return defaults
    except json.JSONDecodeError:
        print(f"Warning: config.json at {config_path} is invalid. Using default values.")
        return defaults
    except Exception as e:
        print(f"Error loading config.json: {e}. Using default values.")
        return defaults

class StaticSiteGenerator:
    def __init__(self, content_dir, template_dir, static_dir, output_dir):
        self.content_dir = content_dir
        self.template_dir = template_dir
        self.static_dir = static_dir
        self.output_dir = output_dir
        
        print(f"Content directory: {self.content_dir}")
        print(f"Template directory: {self.template_dir}")
        print(f"Static directory: {self.static_dir}")
        print(f"Output directory: {self.output_dir}")
        
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        self.pages = []  # Will store all page information for navigation
        
        # Load configuration
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config = load_config(script_dir)
        print(f"Loaded config: {self.config}")
        
    def clean_output_dir(self):
        """Remove and recreate the output directory"""
        print(f"Cleaning output directory: {self.output_dir}")
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        print(f"Created output directory: {self.output_dir}")
    
    def copy_static_files(self):
        """Copy static files to the output directory"""
        if os.path.exists(self.static_dir):
            print(f"Copying static files from {self.static_dir}")
            static_output = os.path.join(self.output_dir, 'static')
            if os.path.exists(static_output):
                shutil.rmtree(static_output)
            shutil.copytree(self.static_dir, static_output)
            print(f"Static files copied to {static_output}")
        else:
            print(f"Static directory not found: {self.static_dir}")
    
    def render_markdown(self, content_path):
        """Convert markdown content to HTML with frontmatter metadata"""
        print(f"Processing Markdown file: {content_path}")
        with open(content_path, 'r') as f:
            post = frontmatter.load(f)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(post.content)
        
        # Return metadata and HTML content
        return post.metadata, html_content
    
    def collect_pages(self):
        """Collect information about all pages for navigation"""
        print("Collecting page information for navigation")
        self.pages = []
        
        if not os.path.exists(self.content_dir):
            print(f"Content directory does not exist: {self.content_dir}")
            return
            
        content_files = os.listdir(self.content_dir)
        
        for filename in content_files:
            if filename.endswith('.md'):
                content_path = os.path.join(self.content_dir, filename)
                with open(content_path, 'r') as f:
                    post = frontmatter.load(f)
                
                output_filename = os.path.splitext(filename)[0] + '.html'
                nav_order = post.metadata.get('nav_order', 999)
                
                url = output_filename
                print(f"Adding page: {output_filename} with URL: {url}")
                
                self.pages.append({
                    'title': post.metadata.get('title', os.path.splitext(filename)[0].capitalize()),
                    'url': url,
                    'nav_order': nav_order,
                    'safe_url': output_filename,  # This will be a guaranteed URL without leading slash
                    'date': post.metadata.get('date', ''),
                    'description': post.metadata.get('description', '')
                })
        
        # Sort pages by nav_order
        self.pages.sort(key=lambda x: x['nav_order'])
        print(f"Collected {len(self.pages)} pages for navigation")
    
    def generate_pages(self):
        """Generate HTML pages from markdown content"""
        print(f"Generating pages from {self.content_dir}")
        if not os.path.exists(self.content_dir):
            print(f"Content directory does not exist: {self.content_dir}")
            return
        
        # First collect all pages for navigation
        self.collect_pages()
        
        # Fix any URLs that might have slashes prepended by Jinja2
        for page in self.pages:
            if page['url'].startswith('/'):
                page['url'] = page['url'][1:]
        
        # Sort pages by date for prev/next post navigation
        blog_posts = []
        for filename in os.listdir(self.content_dir):
            if filename.endswith('.md'):
                content_path = os.path.join(self.content_dir, filename)
                with open(content_path, 'r') as f:
                    post = frontmatter.load(f)
                    output_filename = os.path.splitext(filename)[0] + '.html'
                    blog_posts.append({
                        'filename': filename,
                        'title': post.metadata.get('title'),
                        'date': post.metadata.get('date'),
                        'nav_order': post.metadata.get('nav_order', 999),
                        'url': output_filename,
                        'description': post.metadata.get('description', '')
                    })
        
        # Sort blog posts by date (or nav_order if date not available)
        blog_posts = sorted(blog_posts, key=lambda x: (x.get('nav_order', 999), x.get('date', '')))
            
        content_files = os.listdir(self.content_dir)
        print(f"Found {len(content_files)} files in content directory")
        
        # Process all markdown files as posts
        for filename in content_files:
            if filename.endswith('.md'):
                content_path = os.path.join(self.content_dir, filename)
                print(f"Processing {filename}")
                metadata, html_content = self.render_markdown(content_path)
                
                # Always use post.html template
                template_name = 'post.html'
                print(f"Using template: {template_name}")
                
                try:
                    template = self.jinja_env.get_template(template_name)
                except Exception as e:
                    print(f"Error loading template {template_name}: {e}")
                    continue
                
                # Add navigation to the template context
                metadata['pages'] = self.pages
                
                # Add site title and year from config
                metadata['site_title'] = self.config['site_title']
                metadata['year'] = self.config['year']
                
                # Find current post index for navigation
                current_post_index = next((i for i, post in enumerate(blog_posts) if post['filename'] == filename), None)
                
                if current_post_index is not None:
                    # Add previous post if it exists
                    if current_post_index > 0:
                        metadata['prev_post'] = blog_posts[current_post_index - 1]
                    
                    # Add next post if it exists
                    if current_post_index < len(blog_posts) - 1:
                        metadata['next_post'] = blog_posts[current_post_index + 1]
                
                # Render the template with content and metadata
                output_html = template.render(
                    content=html_content,
                    **metadata
                )
                
                # Determine output filename
                output_filename = os.path.splitext(filename)[0] + '.html'
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Write the output file
                with open(output_path, 'w') as f:
                    f.write(output_html)
                    
                print(f"Generated {output_path}")
        
        # Create index.html directly from index template
        index_path = os.path.join(self.output_dir, 'index.html')
        print("Generating index.html from template...")
        try:
            # Get the index template
            template = self.jinja_env.get_template('index.html')
            
            # Prepare metadata for the index page
            metadata = {
                'title': 'Home',
                'site_title': self.config['site_title'],
                'year': self.config['year'],
                'pages': self.pages,
                'site_description': self.config['site_description']
            }
            
            # Render the template
            output_html = template.render(**metadata)
            
            # Write the index file
            with open(index_path, 'w') as f:
                f.write(output_html)
                
            print(f"Generated {index_path}")
        except Exception as e:
            print(f"Error generating index.html: {e}")
            
            # If the index.html template doesn't exist, create a basic one from page.html
            try:
                template = self.jinja_env.get_template('page.html')
                
                # Prepare metadata for the index page (fallback)
                metadata = {
                    'title': 'Home',
                    'site_title': self.config['site_title'],
                    'year': self.config['year'],
                    'is_homepage': True,
                    'pages': self.pages,
                    'site_description': self.config['site_description'],
                    'content': ''  # Empty content since we're just listing pages
                }
                
                # Render the template
                output_html = template.render(**metadata)
                
                # Write the index file
                with open(index_path, 'w') as f:
                    f.write(output_html)
                    
                print(f"Generated {index_path} using page.html template")
            except Exception as e:
                print(f"Error generating index.html with page.html template: {e}")
    
    def build(self):
        """Build the static site"""
        print("🔨 Building static site...")
        self.clean_output_dir()
        self.copy_static_files()
        self.generate_pages()
        print("✅ Site built successfully!")

if __name__ == "__main__":
    # Define paths relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, 'content')
    template_dir = os.path.join(base_dir, 'ssg', 'templates')
    static_dir = os.path.join(base_dir, 'ssg', 'static')
    output_dir = os.path.join(base_dir, 'html')
    
    ssg = StaticSiteGenerator(content_dir, template_dir, static_dir, output_dir)
    ssg.build() 