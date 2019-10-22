import argparse
from useful import get_json


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("paths", help="The path(s) of the file(s).")

        self.black_arguments_names: list = []
        for arg in get_json("arguments.json"):  # TODO : set up the bools params
            self.black_arguments_names.append(arg["long"].replace("-", "_"))
            if "short" in arg.keys():
                parser.add_argument(
                    "-" + arg["short"],
                    "--" + arg["long"],
                    help=arg["help"],
                    default=None,
                )
            else:
                parser.add_argument("--" + arg["long"], help=arg["help"], default=None)
        self.args = parser.parse_args()

    @property
    def files(self):
        return self.args.paths

    @property
    def for_black(self):
        return " ".join(
            [
                f"--{name.replace('_', '-')} {vars(self.args)[name]}"
                for name in self.black_arguments_names
                if vars(self.args)[name] is not None
            ]
        )

    def run(self):
        print(">>" + self.for_black + "<<")


def main():
    args = Args()
    args.run()


if __name__ == "__main__":
    pass
