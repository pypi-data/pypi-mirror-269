import time
import typing as T
import json
import uuid
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import track
import httpx
from pydantic import BaseModel

err_console = Console(stderr=True)
console = Console()


app = typer.Typer(no_args_is_help=True)


def valid_input(schema: dict, input: dict) -> bool:
    # TODO
    if False:
        console.print("[bold red]Error: invalid schema!")
        return False
    return True


class StepResponse(BaseModel):
    duration_ms: float

    output: dict | None = None

    exception_str: str | None = None
    response_text: str | None = None


class StepRun(BaseModel):
    response: StepResponse
    started_at_ms: float
    ended_at_ms: float


@app.command()
def run(
    *,
    json_file: T.Annotated[
        T.Optional[str], typer.Option(help="Path to the JSON file to run.")
    ] = None,
    json_string: T.Annotated[
        T.Optional[str], typer.Option(help="JSON string to run.")
    ] = None,
    output_file: T.Annotated[str, typer.Option(help="Path to the output file.")],
    output_length: T.Annotated[
        T.Optional[int],
        typer.Option(help="Number of characters to print for the output of each step."),
    ] = 200,
):
    """
    Provide either a --json_file or a --json_string to run.
    Provide an optional --output-length for the length of the output of the run to display.
    """
    if not json_file and not json_string:
        err_console.print(
            "[bold red]Error:[/bold red] Please provide either [green]--json_file[/green] or [green]--json_string[/green]."
        )
        return
    if json_file and json_string:
        err_console.print(
            "[bold red]Error:[/bold red] Please provide either [green]--json_file[/green] or [green]--json_string[/green], not both."
        )
        return
    if json_file:
        path = Path(json_file)
        if path.exists():
            with path.open("r") as f:
                steps_j = json.load(f)
        else:
            err_console.print(
                f"[bold red]Error:[/bold red] No file found at {json_file}"
            )
            return
    else:
        steps_j = json.loads(json_string)
    result_by_step: dict[str, StepRun] = {}
    for step in track(steps_j["steps"], description="Running steps..."):
        console.log(f"running step {step['id']}")
        step_started_at_ms = time.time() * 1_000
        # confirm the input types conform to the plugins inputSchema
        input = step["input"]
        plugin = steps_j["plugins"][step["pluginId"]]
        input_schema = plugin["inputSchema"]
        valid_input(schema=input_schema, input=input)
        r = httpx.post(
            url=plugin["execute"],
            json=input,
            headers={
                "x-whitecloak-run-id": str(uuid.uuid4()),
                "x-whitecloak-step-id": step["id"],
            },
            timeout=60,
        )
        duration_ms = r.elapsed.total_seconds() * 1_000
        step_ended_at_ms = time.time() * 1_000
        try:
            step_j = r.json()
            step_response = StepResponse(duration_ms=duration_ms, output=step_j)
        except Exception as e:
            step_response = StepResponse(
                duration_ms=duration_ms, response_text=r.text, exception_str=str(e)
            )
        result_by_step[step["id"]] = StepRun(
            response=step_response,
            started_at_ms=step_started_at_ms,
            ended_at_ms=step_ended_at_ms,
        )
    table = Table("Step Id", "Latency (ms)", "Result")
    output_rows: list[dict] = []
    for step_id, step_result in result_by_step.items():
        table.add_row(
            step_id,
            str(round(step_result.response.duration_ms, 2)),
            json.dumps(step_result.response.output)[0:output_length],
        )
        output_rows.append(
            {
                "step_id": step_id,
                "result": step_result.model_dump(mode="json"),
            }
        )
    console.print(table)
    path = Path(output_file)
    if not path.exists():
        # do this check just in case you do not have filesystem directory write access
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output_rows))


@app.command()
def hi():
    console.print("hi")


if __name__ == "__main__":
    app()
