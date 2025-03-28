import html
from typing import List, Tuple, Dict, Optional


class LyricsAnnotator:
    def __init__(self, annotations: List[Tuple[str, List[str]]], full_lyrics: str):
        self.annotations = annotations
        self.full_lyrics = full_lyrics
        self.footnotes = '<ol id="InsertNote_NoteList">'
        self.current_id = 1
        
    def annotate_lyrics(self) -> str:
        for annotation in self.annotations:
            fragment = annotation[0]
            note = annotation[1][0]
            
            if not fragment or not note:
                print("Skipping annotation with empty fragment or notes")
                continue
            
            self.full_lyrics.replace(fragment, f'<span class="annotated" id="annotated_{self.current_id}">{fragment}</span>')
            self.footnotes += f'<li id="InsertNoteID_{self.current_id}">{note}</li>'

        self.footnotes += '</ol>'
        return self.full_lyrics + self.footnotes