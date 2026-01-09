#!/usr/bin/env python3
"""
Bulk Upload Script for Handwritten Journal Entries

This script processes handwritten journal entry images and converts them
to markdown blog posts using Google's Gemini API.

Usage:
    python bulk_upload.py --input <directory> --api-key <gemini-api-key>

Requirements:
    - google-generativeai
    - Pillow
"""

import os
import sys

# Suppress warnings before importing google.generativeai
if not sys.warnoptions:
    import warnings
    warnings.filterwarnings('ignore')

import argparse
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

try:
    import google.generativeai as genai
    from PIL import Image
except ImportError:
    print("Error: Required packages not installed.")
    print("Please install them with:")
    print("  pip install google-generativeai Pillow")
    sys.exit(1)


class JournalEntryProcessor:
    """Processes handwritten journal entries and converts them to markdown posts."""
    
    def __init__(self, api_key: str, output_dir: str = "posts"):
        """
        Initialize the processor.
        
        Args:
            api_key: Google Gemini API key
            output_dir: Directory to save converted markdown files
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def _create_conversion_prompt(self) -> str:
        """Create the prompt for Gemini to convert handwritten entries."""
        return """You are converting a handwritten journal entry into a markdown blog post.

Please analyze this handwritten journal entry and:
1. Extract the date (if visible)
2. Identify or create a title based on the content
3. Convert the handwritten text into clean, readable markdown format
4. Preserve paragraph breaks and formatting

Return ONLY a JSON object with this exact structure:
{
  "title": "Title of the entry",
  "date": "YYYY-MM-DD",
  "content": "# Title\\n\\nMarkdown content here..."
}

Important notes:
- If no date is visible, use today's date
- If no clear title exists, create one that captures the main theme (max 5-7 words)
- The content should be properly formatted markdown
- Do not include the frontmatter (---) in the content, just the markdown body
- Preserve the original writing style and voice
- Use proper markdown formatting (headings, lists, bold, italic, etc.)
"""

    def process_image(self, image_path: Path) -> Optional[Dict[str, str]]:
        """
        Process a single image and convert it to markdown format.
        
        Args:
            image_path: Path to the handwritten journal entry image
            
        Returns:
            Dictionary with title, date, and content, or None if processing fails
        """
        try:
            print(f"Processing {image_path.name}...")
            
            # Load the image
            image = Image.open(image_path)
            
            # Generate content using Gemini
            prompt = self._create_conversion_prompt()
            response = self.model.generate_content([prompt, image])
            
            # Parse the response
            response_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON directly
                json_str = response_text
            
            # Parse the JSON
            result = json.loads(json_str)
            
            # Validate required fields
            if not all(key in result for key in ['title', 'date', 'content']):
                print(f"Warning: Missing required fields in response for {image_path.name}")
                return None
            
            # Validate date format
            try:
                datetime.strptime(result['date'], '%Y-%m-%d')
            except ValueError:
                print(f"Warning: Invalid date format for {image_path.name}, using today's date")
                result['date'] = datetime.now().strftime('%Y-%m-%d')
            
            return result
            
        except Exception as e:
            print(f"Error processing {image_path.name}: {e}")
            return None
    
    def _create_filename(self, title: str) -> str:
        """
        Create a safe filename from the title.
        
        Args:
            title: Post title
            
        Returns:
            Safe filename
        """
        # Convert to lowercase and replace spaces with hyphens
        filename = title.lower()
        # Remove special characters
        filename = re.sub(r'[^a-z0-9\s-]', '', filename)
        # Replace spaces with hyphens
        filename = re.sub(r'\s+', '-', filename)
        # Remove multiple consecutive hyphens
        filename = re.sub(r'-+', '-', filename)
        # Trim hyphens from ends
        filename = filename.strip('-')
        
        # Limit length
        if len(filename) > 50:
            filename = filename[:50].rsplit('-', 1)[0]
        
        return f"{filename}.md"
    
    def save_post(self, post_data: Dict[str, str]) -> Optional[Path]:
        """
        Save the converted post as a markdown file.
        
        Args:
            post_data: Dictionary with title, date, and content
            
        Returns:
            Path to the saved file, or None if save fails
        """
        try:
            filename = self._create_filename(post_data['title'])
            filepath = self.output_dir / filename
            
            # Check if file already exists
            if filepath.exists():
                print(f"Warning: {filename} already exists, adding timestamp...")
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                filename = f"{filepath.stem}-{timestamp}.md"
                filepath = self.output_dir / filename
            
            # Create the markdown content with frontmatter
            frontmatter = f"""---
title: {post_data['title']}
date: {post_data['date']}
---

{post_data['content']}
"""
            
            # Write to file
            filepath.write_text(frontmatter, encoding='utf-8')
            print(f"✓ Saved: {filename}")
            
            return filepath
            
        except Exception as e:
            print(f"Error saving post: {e}")
            return None
    
    def process_directory(self, input_dir: Path, 
                         extensions: List[str] = None) -> Dict[str, int]:
        """
        Process all images in a directory.
        
        Args:
            input_dir: Directory containing handwritten entry images
            extensions: List of image extensions to process
            
        Returns:
            Dictionary with processing statistics
        """
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        
        stats = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0
        }
        
        # Find all image files
        image_files = []
        for ext in extensions:
            image_files.extend(input_dir.glob(f"*{ext}"))
            image_files.extend(input_dir.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"No image files found in {input_dir}")
            return stats
        
        print(f"\nFound {len(image_files)} image(s) to process\n")
        
        for image_path in sorted(image_files):
            stats['processed'] += 1
            
            # Process the image
            post_data = self.process_image(image_path)
            
            if post_data:
                # Save the post
                saved_path = self.save_post(post_data)
                if saved_path:
                    stats['successful'] += 1
                else:
                    stats['failed'] += 1
            else:
                stats['failed'] += 1
        
        return stats


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Bulk upload handwritten journal entries to markdown blog posts"
    )
    parser.add_argument(
        '--input',
        '-i',
        type=str,
        required=True,
        help="Directory containing handwritten entry images"
    )
    parser.add_argument(
        '--api-key',
        '-k',
        type=str,
        help="Google Gemini API key (or set GEMINI_API_KEY environment variable)"
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        default='posts',
        help="Output directory for markdown files (default: posts)"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Process images without saving (for testing)"
    )
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Error: Gemini API key required")
        print("Provide via --api-key or set GEMINI_API_KEY environment variable")
        sys.exit(1)
    
    # Validate input directory
    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    if not input_dir.is_dir():
        print(f"Error: Input path is not a directory: {input_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("Handwritten Journal Entry Bulk Upload")
    print("=" * 60)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {args.output}")
    print(f"Dry run: {args.dry_run}")
    print("=" * 60)
    print()
    
    # Initialize processor
    processor = JournalEntryProcessor(api_key, args.output)
    
    # Process directory
    stats = processor.process_directory(input_dir)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Processing Summary")
    print("=" * 60)
    print(f"Total processed: {stats['processed']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Skipped: {stats['skipped']}")
    print("=" * 60)
    
    if stats['successful'] > 0 and not args.dry_run:
        print("\n✓ Posts have been created in the posts/ directory")
        print("✓ Commit and push the changes to trigger the GitHub Action")
        print("  that will update posts.json and publish your posts!")
        print("\nCommands:")
        print("  git add posts/*.md")
        print("  git commit -m 'Add bulk uploaded journal entries'")
        print("  git push")
    
    sys.exit(0 if stats['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
