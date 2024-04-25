import datetime
import json
import logging
import os
import pathlib
import typing

import click
import dotenv
import fabric

from np_upload_validation import hpc, models, npc, validation

dotenv.load_dotenv()


logger = logging.getLogger(__name__)

timestamp = datetime.datetime.now()
base_filename = f"np-upload-validation_{timestamp.strftime('%Y%m%d_%H%M%S')}"


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--log-to-file", default=False, is_flag=True)
def cli(debug: bool, log_to_file: bool) -> None:
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    if debug:
        validation.logger.setLevel(logging.DEBUG)
        hpc.logger.setLevel(logging.DEBUG)
        npc.logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    if log_to_file:
        log_path = f"{base_filename}.log"
        click.echo(f"Logging to file: {log_path}")
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        validation.logger.addHandler(file_handler)
        hpc.logger.addHandler(file_handler)
        npc.logger.addHandler(file_handler)
        logger.addHandler(file_handler)


@cli.command()
@click.argument(
    "session-id",
    type=str,
)
@click.argument(
    "exp-dir-root",
    type=pathlib.Path,
)
@click.option(
    "--output-path",
    type=pathlib.Path,
    default=None,
)
def validate_session(
    session_id: str,
    exp_dir_root: pathlib.Path,
    output_path: typing.Optional[pathlib.Path],
) -> None:
    try:
        result = validation.validate(session_id, exp_dir_root)
    except Exception as e:
        click.echo(message=f"Failed to validate: {e}", err=True)
        return None

    if result is None:
        return

    serialized = json.dumps([r.model_dump() for r in result], indent=4, sort_keys=True)

    if output_path is not None:
        output_path.write_text(serialized)
    else:
        click.echo(serialized)


def _trigger_hpc_job(
    entry_point: str,
    memsize: int,
) -> tuple[str, str]:
    username = os.environ["HPC_USERNAME"]
    with fabric.Connection(
        os.environ["HPC_HOST"],
        user=username,
        connect_kwargs={
            "password": os.environ["HPC_PASSWORD"],
        },
    ) as con:
        user_dir = f"/home/{username}"
        return hpc.run_hpc_job(
            con,
            hpc.HPCJob(
                email_address=os.environ["HPC_EMAIL_ADDRESS"],
                entry_point=entry_point,
                mem_size=memsize,
            ),
            f"{user_dir}/jobs",
            f"{user_dir}/job-logs",
            hpc.SIFContext(
                sif_loc_str=os.environ["HPC_SIF_PATH"],
                env_vars={
                    "CODE_OCEAN_API_TOKEN": os.environ["CODE_OCEAN_API_TOKEN"],
                    "CODE_OCEAN_DOMAIN": os.environ["CODE_OCEAN_DOMAIN"],
                    "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
                    "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
                    "AWS_DEFAULT_REGION": os.environ["AWS_DEFAULT_REGION"],
                },
            ),
            "npc_cleanup",
        )


@cli.command()
@click.argument(
    "session_id",
    type=str,
)
@click.option(
    "--output-path",
    type=pathlib.Path,
    default=None,
)
def validate_session_hpc(session_id: str, chunk_size: int, memsize: int) -> None:
    slurm_id, job_name = _trigger_hpc_job(
        (
            f"np-upload-validation --debug validate-npc-session {session_id} "
            f"--chunk-size={chunk_size}"
        ),
        memsize,
    )
    click.echo(f"Submitted job: {slurm_id} ({job_name})")


@cli.command()
@click.argument(
    "job_name",
    type=str,
)
def get_job_log(job_name: str) -> None:
    username = os.environ["HPC_USERNAME"]
    with fabric.Connection(
        os.environ["HPC_HOST"],
        user=username,
        connect_kwargs={
            "password": os.environ["HPC_PASSWORD"],
        },
    ) as con:
        user_dir = f"/home/{username}"
        log_content = hpc.get_remote_content(
            con,
            f"{user_dir}/job-logs/{job_name}.log",
        )
        click.echo(log_content)


@cli.command()
@click.argument(
    "exp-dir-root",
    type=pathlib.Path,
)
@click.option(
    "--output-dir",
    type=pathlib.Path,
    default=pathlib.Path("./"),
)
def batch_validate_sessions(
    exp_dir_root: pathlib.Path,
    output_dir: pathlib.Path,
) -> None:
    validation_results = []
    mismatches = []
    for validated in validation.batch_validate_sessions(exp_dir_root):
        for v in validated:
            if not v.associated.match:
                mismatches.append(v)
        validation_results.append(validated)

    (output_dir / f"{base_filename}.json").write_text(
        json.dumps(
            models.BatchValidationResult(
                exp_dir_root=exp_dir_root.as_posix(),
                timestamp=timestamp.isoformat(),
                validation=validation_results,
                mismatches=mismatches,
            ).model_dump(),
            indent=4,
            sort_keys=True,
        )
    )

    if mismatches:
        click.echo("Validation failed due to mismatches.", err=True)
    else:
        click.echo("Validation successful.")


@cli.command()
@click.argument(
    "exp-dir-root",
    type=pathlib.Path,
)
@click.option(
    "--output-dir",
    type=pathlib.Path,
    default=pathlib.Path("./"),
)
def batch_validate_sessions_hpc(exp_dir_root, output_dir, memsize: int) -> None:
    slurm_id, job_name = _trigger_hpc_job(
        " ".join(
            [
                "np-upload-validation",
                "--debug",
                "batch-validate-session",
                exp_dir_root.as_posix(),
                f"--output-dir={output_dir.as_posix()}",
            ]
        ),
        memsize,
    )
    click.echo(f"Submitted job: {slurm_id} ({job_name})")


if __name__ == "__main__":
    cli()
