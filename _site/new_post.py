import os
from datetime import datetime

import begin
from slugify import slugify

template = """---
title: "{}"
date: {}
author: {}
tags:
categories: 
comments: true
excerpt: "Escribe aquí un buen resumen de tu artículo"
header:
  overlay_image: #image
  teaser: #image
  overlay_filter: rgba(0, 0, 0, 0.5)
---"""


@begin.start(auto_convert=True)
def main(draft=False, author="Héctor Patricio", *names):
    """ Creates a new file with today's date and title as slug in _posts dir """

    t = datetime.today()
    date = f"{t.year}-{t.month:02d}-{t.day:02d}"
    directory = "_drafts" if draft else "_posts"

    if not os.path.exists(directory):
        os.makedirs(directory)

    for name in names:
        date_string = (date + "-") * (not draft)
        file_name = f"{directory}/{date_string}{slugify(name)}.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(template.format(name, date, author))
