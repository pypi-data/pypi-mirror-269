import re


def parse_pattern(pattern: str, line: str, name: str) -> str:
    regex = re.compile(pattern)
    match = regex.match(line)

    if not match:
        raise ValueError(f"Could not parse {name} from line")

    return match.group(1).strip()


def parse_indication(line: str) -> str:
    return parse_pattern(r"^.*Reason for Referral:(.*)<.*$", line, "indication")


def parse_ordering_md(line: str) -> str:
    return parse_pattern(r"^.*Physician Name:(.*?)(Reason|<).*$", line, "ordering MD")


def parse_sample_number(line: str) -> str:
    return parse_pattern(r"^.*Specimen #: (\d*) .*$", line, "sample number")


def parse_report_id(line: str) -> str:
    return parse_pattern(r"^.*Accession #: (.*) .*$", line, "report ID")
