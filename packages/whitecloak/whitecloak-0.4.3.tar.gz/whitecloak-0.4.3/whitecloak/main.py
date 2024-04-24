import time
import typing as T
import json
import uuid
from pathlib import Path

import httpx
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import track
from pydantic import BaseModel, TypeAdapter, Field

err_console = Console(stderr=True)
console = Console()


app = typer.Typer(no_args_is_help=True)


def valid_input(schema: dict, input: dict) -> bool:
    # TODO
    if False:
        console.print("[bold red]Error: invalid schema!")
        return False
    return True


class StepResponseError(BaseModel):
    exception_log: str | None = None
    raw_response_text: str | None = None


class StepResponse(BaseModel):
    # it must always return json? Make this a requirement
    body: dict | None
    headers: dict | None

    error: StepResponseError | None = None


class StepRun(BaseModel):
    id: str
    step_id: str
    step_version: int
    plugin_id: str

    step_input: dict
    execute_response: StepResponse
    execute_duration_ms: float

    started_at_ms: float
    ended_at_ms: float


class Step(BaseModel):
    id: str
    version: int = Field(ge=0)

    slug: str = Field(pattern=r"^[a-zA-Z0-9-]+$")
    plugin_id: str
    input: dict[str, T.Any]


class Plugin(BaseModel):
    input_schema: dict[str, T.Any]
    execute_url: str


class StepsInput(BaseModel):
    version: str
    steps: list[Step]
    plugins: dict[str, Plugin]


class StepsResponse(BaseModel):
    version: str
    runs: list[StepRun]


@app.command()
def run(
    *,
    json_file: T.Annotated[
        T.Optional[str], typer.Option(help="Path to the JSON file to run.")
    ] = None,
    json_string: T.Annotated[
        T.Optional[str], typer.Option(help="JSON string to run.")
    ] = None,
    output_file: T.Annotated[
        T.Optional[str], typer.Option(help="Path to the output file.")
    ] = None,
    return_json: T.Annotated[
        T.Optional[bool],
        typer.Option(
            help="True if stdout should only print the runs. This is headless mode."
        ),
    ] = None,
    output_length: T.Annotated[
        T.Optional[int],
        typer.Option(
            help="Number of characters to print for the output of each step. Ignored if --return-json is given."
        ),
    ] = 200,
):
    """
    Provide either a --json-file or a --json-string to run.
    If you would like the output to be json, use --return-json.
    Provide an optional --output-length for the length of the output of the run to display.
    """
    is_headless = bool(return_json)
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
            json_string = path.read_bytes()
        else:
            err_console.print(
                f"[bold red]Error:[/bold red] No file found at {json_file}"
            )
            return
    steps_input = StepsInput.model_validate_json(json_string)
    runs: list[StepRun] = []
    for step in track(
        steps_input.steps, description="Running steps...", disable=is_headless
    ):
        if not is_headless:
            console.log(f"running step {step.id}")
        step_started_at_ms = time.time() * 1_000
        plugin = steps_input.plugins[step.plugin_id]
        valid_input(schema=plugin.input_schema, input=step.input)  # TODO
        run_id = f"run_{uuid.uuid4()}"
        r = httpx.post(
            url=plugin.execute_url,
            json=step.input,
            headers={
                "x-whitecloak-run-id": str(run_id),
                "x-whitecloak-step-id": step.id,
            },
            timeout=60,
        )
        step_ended_at_ms = time.time() * 1_000
        try:
            step_response = StepResponse(body=r.json(), headers=r.headers)
        except Exception as e:
            step_response = StepResponse(
                body=None,
                headers=None,
                error=StepResponseError(exception_log=str(e), raw_response_text=r.text),
            )
        runs.append(
            StepRun(
                id=run_id,
                step_id=step.id,
                step_version=step.version,
                plugin_id=step.plugin_id,
                step_input=step.input,
                execute_response=step_response,
                execute_duration_ms=r.elapsed.total_seconds() * 1_000,
                started_at_ms=step_started_at_ms,
                ended_at_ms=step_ended_at_ms,
            )
        )
    table = Table("Run Id", "Step Id", "Latency (ms)", "Result")
    for _run in runs:
        table.add_row(
            _run.id,
            _run.step_id,
            str(round(_run.execute_duration_ms, 2)),
            json.dumps(_run.execute_response.body)[0:output_length],
        )
    if not is_headless:
        console.print(table)
    response = StepsResponse(version=steps_input.version, runs=runs)
    response_json = response.model_dump_json()
    if output_file is not None:
        path = Path(output_file)
        if not path.exists():
            # do this check just in case you do not have filesystem directory write access
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(response_json)
    if is_headless:
        console.print(response_json)


@app.command()
def hello():
    console.print("world")


if __name__ == "__main__":
    app()
