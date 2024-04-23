from os import PathLike
from google_ai_studio_utils.config import google_ai_studio_html_template


def parse_csv_to_conversation(file_path: PathLike) -> list[tuple[str, str]]:
    import sys
    import csv

    csv.field_size_limit(sys.maxsize)
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        # next(reader)  # Skip the header
        conversation = [(row[0].replace(":", ""), row[1]) for row in reader]
    return conversation


def format_dunder_keys(s: str, **kwargs):
    for k, v in kwargs.items():
        k_ = f"__{k}__"
        s = s.replace(k_, v)
    return s


def conversation_to_html(
    conversation: list[tuple[str, str]],
    font: str = "sans-serif",
    title: str = "Google AI Studio Exported Conversation",
) -> str:
    import markdown

    html_template = google_ai_studio_html_template.read_text()

    content = ""
    for index, (role, message) in enumerate(conversation):
        if role == "Model":
            content += f'<div id="convo-item-{index}" class="model-content">{markdown.markdown(message, extensions=['footnotes', 'meta', 'toc', 'admonition', 'fenced_code', 'tables'])}</div><hr>'
        else:
            content += f'<div id="convo-item-{index}" class="user-content"><pre>{message}</pre></div><hr>'

    return format_dunder_keys(html_template, content=content, font=font, title=title)


def conversation_to_html(
    conversation: list[tuple[str, str]],
    font: str = "sans-serif",
    title: str = "Google AI Studio Exported Conversation",
) -> str:
    import markdown

    html_template = google_ai_studio_html_template.read_text()

    content = ""
    for index, (role, message) in enumerate(conversation):
        if role == "Model":
            content += f'<a id="convo-item-{index}" class="anchor-button" href="#convo-item-{index}"># </a><div class="model-content">{markdown.markdown(message, extensions=['footnotes', 'meta', 'toc', 'admonition', 'fenced_code', 'tables'])}</div><hr>'
        else:
            content += f'<a id="convo-item-{index}" class="anchor-button" href="#convo-item-{index}"># </a><div class="user-content"><pre>{message}</pre></div><hr>'

    return format_dunder_keys(html_template, content=content, font=font, title=title)


def gist_create(p: PathLike) -> str:
    import subprocess

    # gh gist create p
    return subprocess.run(
        ["gh", "gist", "create", str(p)], capture_output=True, text=True
    ).stdout.strip()


def gist_url_to_gtm(gist_url: str, strip_tddschn: bool = True) -> str:
    to_replace = "https://gist.github.com/"
    if strip_tddschn and (to_replace + "tddschn/") in gist_url:
        to_replace += "tddschn/"
    url = gist_url.replace(to_replace, "https://g.teddysc.me/")
    return url
