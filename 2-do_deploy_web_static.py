#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""


from fabric.api import env, put, run
from os.path import exists


env.hosts = ['54.237.117.225', '34.207.156.91']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    Args:
        archive_path (str): the path to the archive to be deployed
    Returns:
        True if all operations were successful, otherwise returns False
    """
    print("Starting the deployment process.")

    # Check if the archive_path exists
    if exists(archive_path) is False:
        print(f"Archive path {archive_path} does not exist.")
        return False

    # Extract the file name and the name without extension
    file_name = archive_path.split("/")[-1]
    name_without_ext = file_name.split(".")[0]

    # Define the directory paths
    remote_tmp_path = f"/tmp/{file_name}"
    release_dir = f"/data/web_static/releases/{name_without_ext}/"

    try:
        print(f"Uploading the archive {archive_path} to {remote_tmp_path}.")
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, remote_tmp_path)
        print(f"Archive uploaded.")
        # Uncompress the archive in the release directory on the web server
        run(f"mkdir -p {release_dir}")
        run(f"tar -xzf {remote_tmp_path} -C {release_dir}")

        # Delete the archive from the web server
        run(f"rm {remote_tmp_path}")

        # Move content out from web_static folder to the release dir
        run(f"mv {release_dir}web_static/* {release_dir}")

        # Remove the empty directory after moving its content
        run(f"rm -rf {release_dir}web_static")

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release dir
        run(f"ln -s {release_dir} /data/web_static/current")

        print("New version deployed!")

        return True
    except Exception as e:
        print(e)
        return False
