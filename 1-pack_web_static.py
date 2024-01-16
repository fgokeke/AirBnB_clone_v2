#!/usr/bin/python3
"""
Write a Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB
Clone repo, using the function do_pack.
"""


from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    The function creates an archive named
    'web_static_<year><month><day><hour><minute><second>.tgz'.
    This archive contains all the files from the 'web_static'
    directory and is stored in a directory named 'versions'.
    If the 'versions' directory does not exist, it is created.

    Returns:
        The path to the archive if the archive has been successfully created.
        None otherwise.
    """
    # Create 'versions' directory if it doesn't exist
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    # Create a timestamped archive name
    date_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(date_stamp)
    archive_path = os.path.join("versions", archive_name)

    # Pack web_static contents into an archive
    local(f"tar -cvzf {archive_path} web_static")

    # Check if the archive was created successfully
    if os.path.exists(archive_path):
        return archive_path
    return None
