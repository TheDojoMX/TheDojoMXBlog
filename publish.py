import os
from datetime import datetime

import begin

@begin.start(auto_convert=True)
def main(file_name):
    """
    Moves a file to the _posts directory, adds the date to the file and renames it,
    adding the date
    """

    t = datetime.today()
    date = f"{t.year}-{t.month:02d}-{t.day:02d}"

    with open(file_name, "r+") as f:
        content = f.read()
        content = content.replace("date: {date}", f"date: {date}")
        f.seek(0)
        f.write(content)

    new_name = file_name.replace("_drafts/", f"_posts/{date}-}")
    os.rename(file_name, new_name)
