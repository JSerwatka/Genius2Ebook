#!/usr/bin/env python3
"""
Album Lyrics to Ebook Generator

This script creates an ebook (EPUB or MOBI) containing lyrics and annotations
from a specified album using the Genius API.

Requirements:
- lyricsgenius
- ebooklib
- argparse
"""

import os
import sys
import argparse
import re
import requests
from datetime import datetime
import lyricsgenius as lg
from ebooklib import epub
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def clean_html(html_text):
    """Remove unwanted HTML elements and clean up text."""
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text


def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)


def get_album_data(artist_name, album_name, api_key):
    """Fetch album data from Genius."""
    genius = lg.Genius(api_key, 
                      skip_non_songs=True, 
                      excluded_terms=["(Remix)", "(Live)"],
                      remove_section_headers=False,
                      verbose=True,
                      retries=3)
    
    try:
        print(f"Searching for album '{album_name}' by '{artist_name}'...")
        
        # Search for the album directly rather than going through artist
        album = genius.search_album(album_name, artist_name)
        if not album:
            # Try a more general search approach
            print("Direct album search failed, trying alternative methods...")
            
            # Try searching for songs by the artist first to verify the artist exists
            artist_search = genius.search_artist(artist_name, max_songs=1)
            if not artist_search:
                print(f"Artist '{artist_name}' not found on Genius.")
                return None
                
            # Try direct album search with found artist name (might be slightly different)
            album = genius.search_album(album_name, artist_search.name)
            
            if not album:
                print(f"Album '{album_name}' not found.")
                return None
        
        # Fetch all tracks with lyrics
        print(f"Found album: {album.name} by {album.artist.name}")
        print("Fetching track lyrics...")
        
        for track in album.tracks:
            if not hasattr(track, 'song') or not track.song:
                continue
                
            print(f"Fetching lyrics for: {track.song.title}")
            try:
                # Fetch the song with lyrics
                song = genius.search_song(track.song.title, album.artist.name)
                
                if song:
                    annotations = genius.song_annotations(song.id)
                    
                    # Attach the song object with lyrics to the track
                    track.song = song
                    track.annotations = annotations 
                    
                    break # DEBUG: TODO: remove
            except Exception as e:
                print(f"Error fetching lyrics for {track.song.title}: {e}")
        
        # Count tracks with lyrics
        tracks_with_lyrics = sum(1 for track in album.tracks if hasattr(track, 'song') and 
                                track.song and hasattr(track.song, 'lyrics') and track.song.lyrics)
        print(f"Number of tracks: {len(album.tracks)}")
        print(f"Tracks with lyrics: {tracks_with_lyrics}")
        
        return album
    
    except Exception as e:
        print(f"Error: {e}")
        print("Try checking the spelling of the artist and album names.")
        return None


def create_epub(album, output_format="epub"):
    """Create an ebook from album data."""
    # Create a new EPUB book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier(f"album_{album.id}")
    book.set_title(f"{album.name} - Lyrics & Annotations")
    book.set_language('en')
    book.add_author(album.artist.name)
    book.add_metadata('DC', 'description', f"Lyrics and annotations for the album {album.name} by {album.artist.name}")
    book.add_metadata('DC', 'publisher', 'Generated with Album Lyrics to Ebook Generator')
    book.add_metadata('DC', 'date', datetime.now().strftime("%Y-%m-%d"))
    
    # Create chapters
    chapters = []
    spine = ['nav']

    # Add cover
    if hasattr(album, 'cover_art_url') and album.cover_art_url:
        try:
            # Download cover image
            response = requests.get(album.cover_art_url)
            if response.status_code == 200:
                # Create cover image
                book.set_cover("cover.jpg", response.content)
                print("Added album cover to ebook")
            else:
                print(f"Failed to download cover image: HTTP status {response.status_code}")
        except Exception as e:
            print(f"Error adding cover image: {e}")
            print("Continuing without cover image")
    
    # Add introduction chapter
    intro = epub.EpubHtml(title='Introduction', file_name='intro.xhtml')
    intro_content = f"""
    <html>
    <head>
        <title>Introduction</title>
    </head>
    <body>
        <h1>{album.name}</h1>
        <h2>by {album.artist.name}</h2>
        <p>Released: {album.release_date_components.strftime("%d %B %Y") if hasattr(album, 'release_date_components') else 'Unknown'} <!-- Annotation: This is a note. --></p>
        <p>This ebook contains lyrics and annotations for all songs in this album.</p>
        <p>All content is sourced from Genius.com.</p>
    </body>
    </html>
    """
    intro.content = intro_content
    book.add_item(intro)
    spine.append(intro)
    
    # Create a chapter for each song
    for track_num, track in enumerate(album.tracks, 1):
        # Skip if no song or no lyrics
        if not hasattr(track, 'song') or not track.song or not hasattr(track.song, 'lyrics') or not track.song.lyrics:
            print(f"Skipping track {track_num} - no lyrics available")
            continue
        
        # Create chapter
        chapter = epub.EpubHtml(title=track.song.title, file_name=f'song_{track_num}.xhtml')
        
        # Get annotations if available
        annotations = []
        # TODO handle annotations
        # try:
        #     # Get song annotations from Genius
        #     song_info = track.song
        #     referents = song_info.referents if hasattr(song_info, 'referents') else []
            
        #     for ref in referents:
        #         for annotation in ref.annotations:
        #             if hasattr(annotation, 'body') and annotation.body and annotation.body.get('plain'):
        #                 fragment = ref.fragment if hasattr(ref, 'fragment') else "Unknown lyric"
        #                 body = annotation.body.get('plain', 'No annotation text')
        #                 annotations.append({
        #                     'fragment': fragment,
        #                     'body': clean_html(body)
        #                 })
        # except Exception as e:
        #     print(f"Error getting annotations for {track.song.title}: {e}")
        
        # Build chapter content
        chapter_content = f"""
        <html>
        <head>
            <title>{track.song.title}</title>
        </head>
        <body>
            <h1>{track_num}. {track.song.title}</h1>
        """
        
        # Add lyrics
        lyrics = track.song.lyrics if hasattr(track.song, 'lyrics') else ""
        clean_lyrics = lyrics.replace('Lyrics', '', 1).strip()  # Remove the "Lyrics" header
        lyrics_html = f"""
            <div class="lyrics">
                <pre>{clean_lyrics}</pre>
            </div>
        """
        chapter_content += lyrics_html
        
        # TODO: check if needed: Add annotations section if there are any
        # if annotations:
        #     chapter_content += """
        #     <h2>Annotations</h2>
        #     <div class="annotations">
        #     """
            
        #     for i, annotation in enumerate(annotations, 1):
        #         chapter_content += f"""
        #         <div class="annotation">
        #             <h3>Note {i}: "{annotation['fragment']}"</h3>
        #             <p>{annotation['body']}</p>
        #         </div>
        #         """
            
        #     chapter_content += "</div>"
        
        chapter_content += """
        </body>
        </html>
        """
        
        chapter.content = chapter_content
        book.add_item(chapter)
        chapters.append(chapter)
        spine.append(chapter)
    
    # Add default CSS
    style = """
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
        margin: 5%;
        text-align: justify;
    }
    h1 {
        text-align: center;
        page-break-before: always;
    }
    h2 {
        text-align: center;
        margin-top: 1em;
    }
    h3 {
        margin-top: 1.5em;
        background-color: #f5f5f5;
        padding: 5px;
    }
    pre {
        font-family: inherit;
        white-space: pre-wrap;
        margin: 1em 0;
        line-height: 1.5;
    }
    .annotations {
        margin-top: 2em;
        border-top: 1px solid #ccc;
        padding-top: 1em;
    }
    .annotation {
        margin-bottom: 1.5em;
        padding-bottom: 1em;
        border-bottom: 1px dotted #ddd;
    }
    """
    
    css = epub.EpubItem(uid="style_default", file_name="style/default.css", 
                        media_type="text/css", content=style)
    book.add_item(css)
    
    # Add navigation files
    book.toc = chapters
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create output filename
    filename_base = sanitize_filename(f"{album.artist.name} - {album.name}")
    
    # Save the ebook
    if output_format.lower() == "epub":
        epub_path = f"{filename_base}.epub"
        epub.write_epub(epub_path, book)
        return epub_path
    elif output_format.lower() == "mobi":
        # First save as EPUB
        epub_path = f"{filename_base}.epub"
        epub.write_epub(epub_path, book)
        
        # Then convert to MOBI using Calibre's ebook-convert if available
        try:
            mobi_path = f"{filename_base}.mobi"
            os.system(f'ebook-convert "{epub_path}" "{mobi_path}"')
            # Remove temporary EPUB
            os.remove(epub_path)
            return mobi_path
        except Exception as e:
            print(f"Error converting to MOBI: {e}")
            print("Keeping EPUB format instead.")
            return epub_path
    else:
        print(f"Unsupported format: {output_format}. Using EPUB instead.")
        epub_path = f"{filename_base}.epub"
        epub.write_epub(epub_path, book)
        return epub_path


def main():
    load_dotenv() 
    parser = argparse.ArgumentParser(description="Generate an ebook of album lyrics and annotations")
    parser.add_argument("artist", help="Artist name")
    parser.add_argument("album", help="Album name")
    parser.add_argument("--api-key", help="Genius API key", default= os.getenv("GENIUS_API_KEY"))
    parser.add_argument("--format", choices=["epub", "mobi"], default="epub", 
                        help="Output format (epub or mobi)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("ERROR: Genius API key is required. Provide it with --api-key or set GENIUS_API_KEY environment variable.")
        sys.exit(1)
    
    # Set LyricsGenius verbose mode if debug is enabled
    if args.debug:
        print("Debug mode enabled.")
    
    album_data = get_album_data(args.artist, args.album, args.api_key)
    
    if album_data:
        print("Creating ebook...")
        output_file = create_epub(album_data, args.format)
        print(f"Ebook created successfully: {output_file}")
    else:
        print("Failed to create ebook.")
        print("\nTroubleshooting tips:")
        print("1. Check that your Genius API key is correct")
        print("2. Try with the exact artist and album name as listed on Genius.com")
        print("3. Some albums might not be available on Genius or might be listed differently")
        print("4. Run with --debug flag for more information")


if __name__ == "__main__":
    main()