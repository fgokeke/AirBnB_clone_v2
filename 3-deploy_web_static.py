#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""


from fabric.api import env, local, put, run
from datetime import datetime
import os
from os.path import isdir, exists

# Your servers' IP addresses
env.hosts = ['54.237.117.225', '34.207.156.91']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    if not isdir("versions"):
        os.mkdir("versions")
    date_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date_stamp)
    local("tar -cvzf {} web_static".format(archive_path))
    if exists(archive_path):
        return archive_path
    return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False
    file_name = archive_path.split("/")[-1]
    name_without_ext = file_name.split(".")[0]
    remote_tmp_path = "/tmp/{}".format(file_name)
    release_dir = "/data/web_static/releases/{}/".format(name_without_ext)
    try:
        put(archive_path, remote_tmp_path)
        run("mkdir -p {}".format(release_dir))
        run("tar -xzf {} -C {}".format(remote_tmp_path, release_dir))
        run("rm {}".format(remote_tmp_path))
        run("mv {}/web_static/* {}".format(release_dir, release_dir))
        run("rm -rf {}/web_static".format(release_dir))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_dir))
        return True
    except Exception as e:
        return False


def deploy():
    """
    Create and distribute an archive to the web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


# Run the script
if __name__ == "__main__":
    deploy()
