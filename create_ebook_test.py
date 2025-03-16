

import os
import sys
import argparse
import re
import requests
from datetime import datetime
import lyricsgenius as lg
from ebooklib import epub
from ebooklib.plugins.booktype import BooktypeFootnotes
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import html
from typing import List, Tuple, Dict, Optional

from unidecode import unidecode

def create_epub(output_format="azw3"):
    """Create an ebook from album data."""
    # Create a new EPUB book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier(f"album_test")
    book.set_title(f"test - Lyrics & Annotations")
    book.set_language('en')
    
    # Create chapters
    chapters = []
    spine = ['nav']


    
    # Add introduction chapter
    intro = epub.EpubHtml(title='Introduction', file_name='intro.xhtml')
    intro_content = f"""
    <html>
    <head>
        <title>Introduction</title>
    </head>
    <body>
        <p>This ebook contains lyrics and annotations for all songs in this album.</p>
        <p>All content is sourced from Genius.com.</p>
        <span id="InsertNoteID_1_marker1" class="InsertNoteMarker"><sup><a href="#InsertNoteID_1">1</a></sup></span>
        asdkjasjdklajsdljas
<span id="InsertNoteID_2_marker1" class="InsertNoteMarker"><sup><a href="#InsertNoteID_2">2</a></sup></span>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis eligendi tempore rerum velit nemo voluptatem in, delectus cupiditate a nihil animi officia molestias ducimus, suscipit odio, culpa optio? Error, ipsum.
Commodi harum voluptates neque alias enim a, dignissimos quidem quos aperiam. Quae, aperiam nesciunt velit maxime natus iusto facere hic alias quisquam explicabo! Reprehenderit optio inventore magni, maiores laudantium fuga!
Perspiciatis, recusandae voluptatibus labore corrupti repudiandae cum soluta quae, quia officiis explicabo qui doloribus, temporibus inventore error. Necessitatibus amet iste aspernatur. Dolore officiis, dolorum repellendus aliquid qui impedit asperiores amet.
Obcaecati illum molestias, in ipsam eaque rerum vel, totam enim odit voluptatibus inventore distinctio ratione expedita veritatis nobis? Ipsum, delectus veniam quidem ipsam magni suscipit necessitatibus velit voluptatem nulla omnis!
Autem, quod, earum maiores dignissimos nam eveniet ipsam nesciunt facere vitae corporis voluptate ipsa quis rem adipisci veniam facilis temporibus quaerat placeat commodi quae porro ea deleniti eligendi assumenda. Ipsam?
Consectetur consequatur temporibus, id natus quaerat ratione omnis. Perferendis sunt inventore nesciunt quod ab modi? Excepturi doloremque quaerat, laborum error, architecto eligendi aspernatur nisi porro et doloribus voluptatem molestiae deleniti.
Nisi, ab. Porro aut ullam molestias animi aspernatur modi dolor corrupti velit. Provident, obcaecati voluptatem quasi pariatur aut adipisci itaque quis corrupti. Ipsa molestias enim fugit culpa nostrum et! Perferendis.
Maiores, minima accusantium. Provident, recusandae quas illo corporis ea, nisi quia enim minus in debitis inventore vero quis eius beatae, totam natus ipsam alias quam quasi. Atque adipisci labore id?
Reiciendis dolorem veniam similique, minus, atque quae architecto velit nobis voluptatibus, doloremque non facilis doloribus ea. Necessitatibus impedit, facilis dolore pariatur facere unde quos adipisci in ea, non, quidem ullam!
Ad necessitatibus vitae deserunt, repudiandae sapiente, impedit ullam pariatur sint iste voluptatum, itaque ut? Ratione doloribus ipsam id non dolores dolorem ducimus, quae corrupti rem quidem sequi, enim eveniet accusamus.
Fuga, odio sed cum eius ipsum laudantium earum maxime voluptate aliquid voluptas consequatur hic possimus repellendus velit quidem assumenda minima alias repellat laboriosam necessitatibus dolorum mollitia? Qui ducimus beatae pariatur.
Ipsam, ad maxime reiciendis repellat quod laboriosam itaque, quos, minima pariatur consequatur incidunt dicta libero dolor illo labore vero perferendis deleniti. Laudantium quia natus neque vel ad aliquam veniam? Tempore.
Cupiditate architecto saepe voluptas, porro necessitatibus, eos modi sed at deserunt quaerat iusto placeat hic vitae voluptatum! Ipsum, exercitationem reiciendis illo aperiam, sed repudiandae, magnam commodi facilis officia culpa ducimus.
Omnis, aut eum. Ut, unde voluptatibus eius doloremque dolore corporis rem expedita in laboriosam voluptatem natus delectus, est tempore saepe? Aperiam assumenda rerum aliquid quam aliquam unde quo dolorem veniam!
Sed odit assumenda neque ullam, vero nemo ratione laudantium, ab voluptate doloremque distinctio earum beatae voluptas eos! Aliquid vitae, veniam sunt dolor minima aliquam? Iste omnis laborum nesciunt delectus doloremque.
Sapiente sed mollitia autem ad expedita culpa 
fuga nesciunt maiores voluptatem ex totam aspernatur saepe, similique nulla soluta sequi eligendi. Impedit cum dignissimos omnis et eligendi quos quisquam ducimus atque.
Temporibus, quae id quos consectetur maxime eius voluptates laboriosam explicabo at iusto molestiae nihil autem, earum deleniti? Animi, alias ea nostrum delectus similique ipsam tempora dolore fuga, iusto officia error.
Accusantium doloremque est placeat tempore unde inventore? Animi minus ut saepe accusantium quod vero vitae, officia qui reiciendis corporis quam aperiam? Totam, quod. Necessitatibus consequatur quas velit quam sunt modi.
Autem recusandae odio placeat illum vel libero soluta. Rem nisi vero tempore minima unde autem eligendi, debitis aut ad. Quam numquam a mollitia corporis animi nostrum perspiciatis? In, nesciunt minus!
Laboriosam dignissimos fugit est animi, numquam, ea consequatur libero architecto, enim voluptates illo eius qui assumenda! Repellat quos, impedit tempora rem voluptates, eum labore quibusdam consectetur quasi placeat architecto voluptas!
Possimus, et? Aliquid corrupti similique sit, alias autem corporis neque, cumque culpa voluptatum, harum eveniet doloremque aliquam quod reprehenderit fugiat eius vel quibusdam totam in laborum. Blanditiis vitae nostrum consectetur!
Quae magnam rerum molestiae consequatur 
placeat nesciunt hic, vitae esse at saepe facere cupiditate officia earum doloremque expedita possimus velit quia ut distinctio atque molestias aliquam repudiandae assumenda sint. Cumque?
Possimus et nisi debitis repellendus? Excepturi numquam modi, vero exercitationem maxime dicta, ab animi reprehenderit quo totam sint, id quaerat. Sint rerum, iusto facilis eaque dolorem eveniet distinctio mollitia laboriosam.
Nemo eligendi explicabo molestiae. Doloribus numquam illum veniam voluptatum. Quaerat dolores et qui explicabo debitis minus reprehenderit corrupti optio nobis, corporis earum aliquam! Voluptatem eaque illum facere qui rerum. Quod!
Quasi nostrum unde facilis officia asperiores delectus alias at nisi officiis aliquam, quod deserunt, laborum nemo ad architecto quas esse debitis saepe laudantium maxime molestiae cum! Dolorum adipisci quaerat amet.
Culpa error illum ipsam. Explicabo dicta repellat, officia quisquam quidem odit eos enim, nihil, quae minus temporibus nobis! Assumenda omnis cumque aspernatur inventore recusandae repellat tenetur iusto vel dolor earum!
Libero rerum totam laudantium. Pariatur ullam deleniti quaerat qui atque sed dolor, culpa ex. Quidem accusantium aut praesentium quasi laborum expedita voluptates. Repudiandae harum eum illum tenetur nostrum, incidunt odio!
Quod quaerat earum aperiam blanditiis reiciendis sit eligendi nam molestiae dolor explicabo in nesciunt quo maxime repellendus beatae ea ducimus, illo atque corrupti labore sint tenetur. Tempora saepe quis non.
Dolores sunt est, aperiam unde odio non molestias neque fugiat veniam quae sit asperiores aspernatur nihil laboriosam aliquam, vel porro rerum minima, qui saepe. Corrupti impedit nemo enim dicta amet?
Assumenda, enim quidem. Esse, doloremque. A neque possimus, architecto fugit nisi consectetur ullam sequi recusandae placeat porro non voluptatum magni ipsum voluptas ducimus? Necessitatibus nulla quasi neque hic ipsa asperiores!
Nesciunt, officia natus odit culpa, a doloribus eligendi repellat, asperiores nisi quibusdam hic voluptatibus veniam consequatur reiciendis non iure expedita eum tenetur voluptates aperiam eos modi placeat. Atque, similique nam.
Delectus doloribus commodi id, nostrum nam neque accusantium ducimus voluptatum suscipit praesentium nobis fugit sed. Itaque quaerat nesciunt, numquam modi aut minima cumque aperiam eum nulla esse tempore, non labore.
Possimus earum ut mollitia! Est unde natus aspernatur provident, id quae quam nostrum. Assumenda, non amet. Sed a quis laudantium doloribus repudiandae, doloremque enim voluptatibus non, ducimus quibusdam impedit ratione.
Assumenda autem excepturi eligendi veritatis vel eveniet, veniam porro officiis aliquid. Qui, sunt nobis sed ea iure cumque tempore. Deleniti, incidunt vel eveniet est aliquam qui excepturi voluptatum adipisci maxime!
Optio explicabo similique aspernatur odio rem itaque ratione atque reiciendis consectetur sapiente inventore reprehenderit, perspiciatis eligendi deserunt, perferendis pariatur non molestias a nulla consequuntur fuga maiores alias? Eligendi, dignissimos cum!
Vero quos fugit nobis illum ex quod quas assumenda quo ut alias similique, recusandae veritatis eius cum nam aspernatur! Dolores eaque excepturi voluptas deleniti dolorem quia, laboriosam quaerat aliquid reprehenderit!
Modi non sed nam, fugiat voluptatibus at vero pariatur quae aliquam molestiae illum voluptas beatae iste laborum numquam cupiditate mollitia maxime aspernatur, quidem sint. Facilis qui iste minus alias earum.
Distinctio ad commodi ut omnis et itaque dolore ea nobis fuga aliquid corrupti quidem necessitatibus veritatis minima aliquam asperiores, ex eaque sunt voluptatum. Atque illum voluptas adipisci quae veniam suscipit.
Adipisci deserunt delectus alias voluptatibus est odio, minima odit reprehenderit impedit, nisi asperiores. Totam atque sequi vero labore necessitatibus aliquid animi facere. Quae magni, alias repellendus rerum ea ab dignissimos!
Nesciunt numquam dolorum a culpa reiciendis voluptatum veritatis quod tempore dolores odio. Quae deleniti, sed nobis fugit neque doloribus porro molestias fugiat reprehenderit vitae, vero consequuntur, perspiciatis consequatur animi in?
Esse ad autem ab maiores nulla quas, velit numquam. Inventore voluptate harum beatae, recusandae ducimus a debitis. Maiores velit, dolorem exercitationem molestias harum quis maxime, eum et hic ea vel.
Quae officia non omnis eum, ipsa blanditiis eos, quam ut totam, sapiente accusantium soluta veritatis. Sunt repudiandae tempora, eum itaque error quasi hic fugit voluptate numquam dolor fuga ea. Recusandae!
Pariatur, laborum dolorem odio provident commodi hic consequuntur quod. Nemo consequuntur voluptatibus id repellendus dicta soluta minus vero aliquid veniam amet. Magnam officia voluptas, dolorem hic distinctio id doloremque error?
Natus consequuntur sequi ipsa magnam dignissimos, ullam velit alias iste laboriosam vero inventore ratione suscipit error doloribus commodi earum cumque? Cumque veniam neque, quam soluta repellendus nostrum adipisci eum corporis?
Perspiciatis pariatur consequuntur, odio sunt adipisci cupiditate qui quibusdam aperiam nulla alias dolore aspernatur rerum eligendi, perferendis quam. Neque, molestiae esse iusto laboriosam error labore id odio soluta nihil reprehenderit.
Unde soluta quae laudantium temporibus blanditiis nesciunt tempora fugit dignissimos, nulla necessitatibus officia debitis sint corrupti ab assumenda libero! Perferendis vel unde iure inventore excepturi hic sit nostrum, dolore sint!
Possimus autem aspernatur natus harum sunt explicabo inventore, temporibus totam odit fugiat ex voluptatum quibusdam omnis ea? Quam, sed assumenda similique temporibus adipisci laboriosam dolores qui, deserunt enim reprehenderit at!
Voluptate eius labore enim minima quos nisi eum mollitia maxime! Maiores quod tempora optio fugit nemo excepturi quisquam culpa tempore eligendi! Voluptatem inventore amet consequatur maiores labore nisi autem numquam?
Labore voluptatibus voluptatum facere modi accusamus vitae repellat provident mollitia laborum porro, cupiditate, aut unde! Voluptatibus error nesciunt eius temporibus dicta nisi molestias molestiae sequi, quisquam dolorem qui eum ducimus?
Quo consequatur odit voluptatum. Qui doloribus aperiam, quisquam maiores vero amet perspiciatis vitae eligendi dolores? Commodi, quis at explicabo reiciendis dolores impedit voluptas aliquid omnis earum labore qui, placeat cum?
<ol id="InsertNote_NoteList">
  <li id="InsertNoteID_1">Your footnote content here <span id="InsertNoteID_1_LinkBacks"><sup><a href="#InsertNoteID_1_marker1">^</a></sup></span></li>
    <li id="InsertNoteID_2">Second footnote content <span id="InsertNoteID_2_LinkBacks"><sup><a href="#InsertNoteID_2_marker1">^</a></sup></span></li>
</ol>
    </body>
    </html>
    """
    intro.content = intro_content
    book.add_item(intro)
    spine.append(intro)

    # Add navigation files
    book.toc = chapters
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create output filename
    filename_base = "test_file"
    
    # Save the ebook
    if output_format.lower() == "epub":
        epub_path = f"{filename_base}.epub"
        epub.write_epub(epub_path, book)
        return epub_path
    elif output_format.lower() == "azw3":
        # First save as EPUB
        epub_path = f"{filename_base}.epub"
        epub.write_epub(epub_path, book)
        
        # Then convert to AZW3 using Calibre's ebook-convert if available
        try:
            azw3_path = f"{filename_base}.azw3"
            os.system(f'ebook-convert "{epub_path}" "{azw3_path}"')
            # Remove temporary EPUB
            os.remove(epub_path)
            return azw3_path
        except Exception as e:
            print(f"Error converting to AZW3: {e}")
            print("Keeping EPUB format instead.")
            return epub_path
    else:
        print(f"Unsupported format: {output_format}. Using EPUB instead.")
        epub_path = f"{filename_base}.epub"
        epub.write_epub(epub_path, book, { "plugins" : [BooktypeFootnotes(booktype_book=book)] })
        return epub_path


create_epub()