import typer
from typing import Annotated, Optional
from ..shell import shell_retry
from ..typer import command_mixin, annotation

app = typer.Typer(add_completion=False)


@command_mixin(app)
def retry(args, retry_times: Annotated[Optional[int], annotation.Option('--times')] = -1):
    shell_retry(args, retry_times if retry_times >= 0 else None)
