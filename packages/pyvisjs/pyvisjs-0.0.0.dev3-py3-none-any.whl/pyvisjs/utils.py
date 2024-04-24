import subprocess
import os


def open_file(url):
    """
    :param url: web url or a file path on your computer
    >>> open_file("https://stackoverflow.com")
    >>> open_file("\\\\pyvisjs\\\\templates\\\\basic.html")  
    """

    #current_directory = os.getcwd()

    #if current_directory not in url:
    #    url = current_directory + url

    try: # should work on Windows
        os.startfile(url)
    except AttributeError:
        try: # should work on MacOS and most linux versions
            subprocess.call(['open', url])
        except:
            raise

def save_file(file_path: str, file_content: str) -> str:
    """
    if file_path is absolute then output_dir will be ignored
    """
    if os.path.isabs(file_path):
        output_dir, file_name = os.path.split(file_path)
    else:
        relative_path = os.path.join(os.getcwd(), file_path)
        output_dir, file_name = os.path.split(relative_path)

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w") as f:
        f.write(file_content)

    return file_path