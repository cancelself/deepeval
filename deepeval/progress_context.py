from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from contextlib import contextmanager
from typing import Optional, Generator
import sys
from tqdm import tqdm as tqdm_bar
import tqdm

from deepeval.telemetry import capture_synthesizer_run


@contextmanager
def progress_context(
    description: str, total: int = 9999, transient: bool = True
):
    console = Console(file=sys.stderr)  # Direct output to standard error
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,  # Use the custom console
        transient=transient,
    ) as progress:
        progress.add_task(description=description, total=total)
        yield


@contextmanager
def synthesizer_progress_context(
    method: str,
    evaluation_model: str,
    embedder: Optional[str] = None,
    max_generations: str = None,
    use_case: str = "QA",
    progress_bar: Optional[tqdm.std.tqdm] = None,
) -> Generator[Optional[tqdm.std.tqdm], None, None]:
    with capture_synthesizer_run(max_generations, method):
        if embedder is None:
            description = f"✨ 🍰 ✨ You're generating up to {max_generations} goldens using DeepEval's latest Synthesizer (using {evaluation_model}, use case={use_case}, method={method})! This may take a while..."
        else:
            description = f"✨ 🍰 ✨ You're generating up to {max_generations} goldens using DeepEval's latest Synthesizer (using {evaluation_model} and {embedder}, use case={use_case}, method={method})! This may take a while..."
        # Direct output to stderr, using TQDM progress bar for visual feedback
        if not progress_bar:
            with tqdm_bar(total=max_generations, desc=description, file=sys.stderr) as progress_bar:
                yield progress_bar  # Pass progress bar to use in outer loop
        else:
            yield progress_bar