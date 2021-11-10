import os
import sys
import click
import random
from jina import Flow, Document, DocumentArray
from jina.logging.predefined import default_logger as logger


def config():
    os.environ["JINA_DATA_FILE"] = os.environ.get(
        "JINA_DATA_FILE", "data/national-climate-change-response-white-paper.txt"
    )
    os.environ["JINA_PORT"] = os.environ.get("JINA_PORT", str(45678))
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ.setdefault("JINA_WORKSPACE", os.path.join(cur_dir, "workspace"))
    os.environ.setdefault(
        "JINA_WORKSPACE_MOUNT",
        f'{os.environ.get("JINA_WORKSPACE")}:/workspace/workspace',
    )


def input_generator(filepath: str):
    with open(filepath) as file:
        lines = file.readlines()
    # num_lines = len(lines)
    num_lines = 60
    for i in range(num_lines):
        yield Document(text=lines[i])


def print_topk(resp, sentence):
    for doc in resp.data.docs:
        print(f"\n\n\nTa-Dah🔮, here's what we found for: {sentence}")
        for idx, match in enumerate(doc.matches):
            score = match.scores["cosine"].value
            print(f"> {idx:>2d}({score:.2f}). {match.text}")


def index():
    flow = Flow().load_config("flows/flow.yml")

    filepath = os.environ.get("JINA_DATA_FILE")
    with flow:
        flow.post(
            on="/index",
            inputs=input_generator(filepath),
            show_progress=True,
            on_done=lambda resp: print(resp.docs[0].embedding),
        )


def query(top_k=5):
    flow = Flow().load_config("flows/flow.yml")
    with flow:
        text = input("Please type a sentence: ")
        doc = Document(content=text)

        result = flow.post(
            on="/search",
            inputs=DocumentArray([doc]),
            parameters={"top_k": top_k},
            line_format="text",
            return_results=True,
        )
        print_topk(result[0], text)


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query"], case_sensitive=False),
)
@click.option("--top_k", "-k", default=5)
def main(task, top_k):
    config()
    if task == "index":
        if os.path.exists(os.environ.get("JINA_WORKSPACE")):
            logger.error(
                f'\n +---------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                        | \
                    \n | The directory {os.environ.get("JINA_WORKSPACE")} already exists. Please remove it before indexing again. | \
                    \n |                                   🤖🤖🤖                                        | \
                    \n +---------------------------------------------------------------------------------+'
            )
            sys.exit(1)
        index()
    elif task == "query":
        query(top_k)


if __name__ == "__main__":
    main()
