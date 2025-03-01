# Get Genius API token from https://genius.com/api-clients
GENIUS_API_TOKEN = "oAk9mtXcLEkXbEO2s3-ihSXV6Mm_YpdBJK0OdNCi-eZOUaJs7loxGmq0ADxYJPf0"

import lyricsgenius
from ebooklib import epub
import subprocess


def create_chapter(track, stylesheet):
    chapter = epub.EpubHtml(title=track.song.title,
                           file_name=f"{track.song.title.replace(' ', '_')}.xhtml",
                           lang='en')
    content = f"""<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{stylesheet.file_name}"/>
    </head>
    <body>
        <h2>{track.song.title}</h2>
        <pre>{track.song.lyrics}</pre>
    </body></html>"""
    chapter.content = content
    return chapter

def main():
    artist = input("Enter artist name: ")
    album_title = input("Enter album title: ")
    file_format = input("Output format (epub/mobi): ").lower()

    genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
    genius.remove_section_headers = True  # Add this for cleaner lyrics
    genius.language = 'en'  

    try:
        album = genius.search_album(artist, album_title)
        if not album:
            print("Album not found!")
            return

        # Save lyrics to ensure we have them loaded
        album.save_lyrics()
        
        book = epub.EpubBook()
        book.set_title(f"{album_title} by {artist}")
        book.add_author(artist)
        book.set_language('en')

        # Create stylesheet
        style = '''
        pre {
            white-space: pre-wrap;
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        '''
        stylesheet = epub.EpubItem(uid="style", 
                                  file_name="style/styles.css", 
                                  media_type="text/css", 
                                  content=style)
        book.add_item(stylesheet)

        # Create chapters
        chapters = []
        for track in album.tracks:
            try:
                if hasattr(track.song, 'lyrics') and track.song.lyrics:
                    chapter = create_chapter(track, stylesheet)
                    book.add_item(chapter)
                    chapters.append(chapter)
            except Exception as e:
                # Safe title access
                title = getattr(track.song, 'title', f"Track {track.number}")
                print(f"Error processing {title}: {str(e)}")

        # Add structure
        book.toc = chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = ['nav'] + chapters

        # Save and convert
        filename = f"{artist}_{album_title}.epub".replace(' ', '_')
        epub.write_epub(filename, book, {})

        if file_format == 'mobi':
            try:
                subprocess.run(['ebook-convert', filename, filename.replace('.epub', '.mobi')])
                print(f"Created {filename.replace('.epub', '.mobi')}")
            except FileNotFoundError:
                print("Calibre required for MOBI conversion")
        else:
            print(f"Created {filename}")

    except Exception as e:
        print(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main()