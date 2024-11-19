from abc import ABC, abstractmethod
from pathlib import Path


class LineTransformation(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def apply(self, line: str) -> str:
        pass


def applyTransformation(path: Path, line_transform: LineTransformation) -> Path:
    out_path = path.with_stem(path.stem + "_" + line_transform.name())
    with open(out_path, "w", encoding="utf-8") as out_handle:
        with open(path, "r", encoding="utf-8") as in_handle:
            actual_line_index = 0
            verbatim = False
            for line in in_handle:
                byte_order_mark = line.startswith("\uFEFF")

                if verbatim or line[byte_order_mark:].startswith("#"):
                    out_handle.write(line)
                elif line[byte_order_mark:].startswith("["):  # Potentially go into verbatim
                    if not line[byte_order_mark:].startswith("[Map"):
                        verbatim = True
                    out_handle.write(line)
                else:  # content line
                    if actual_line_index % 2 == 1:
                        line = line_transform.apply(line)
                    out_handle.write(line)
                    actual_line_index += 1
    return out_path


class EllipsisSpacing(LineTransformation):
    def name(self) -> str:
        return "ellipses"

    def apply(self, line: str) -> str:
        return line.replace(" ...", "...")


class QuoteTransform(LineTransformation):
    def name(self) -> str:
        return "quotes"

    def apply(self, line: str) -> str:
        line = line.replace("'", "’")

        n_quotes = line.count('"')
        if n_quotes == 0:
            return line

        if n_quotes % 2 != 0:
            print(line)
            return line

        seen = 0
        for i,c in enumerate(line):
            if c == '"':
                line = substitute(line, i, "“" if seen % 2 == 0 else "”")
                seen += 1

        return line


def substitute(s: str, index: int, c: str) -> str:
    return s[:index] + c + s[index+1:]


# if __name__ == "__main__":
    # applyTransformation(, EllipsisSpacing())
    # applyTransformation(, QuoteTransform())
