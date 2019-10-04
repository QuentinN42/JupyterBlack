from useful import get_json, write_json
import subprocess


def formatter(filename: str, tmpfile_name: str, args: list = None):
    """

    :param filename: name of the file to reformat
    :param tmpfile_name: name of the temp file
    :param args: arguments send to black
    :return: True if no errors else raise the error
    """
    if args is None:
        args = []
    json = get_json(filename)
    for i, cell in enumerate(json["cells"]):
        if cell["cell_type"] == "code":
            tmpfile_content = "".join(cell["source"])
            with open(tmpfile_name, "w") as f:
                f.write(tmpfile_content)

            # Black file tmpfile_name
            subprocess.call(["black", tmpfile_name, *args])

            # get content
            with open(tmpfile_name, "r") as f:
                tmpfile_content = f.read()

            # rewrite
            json["cells"][i]["source"] = [e + "\n" for e in tmpfile_content.split("\n")]

    write_json(filename, json)
    subprocess.call(["rm", tmpfile_name])
    return True
