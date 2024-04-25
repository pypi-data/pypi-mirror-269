import logging
import re
import tempfile
import typing
import uuid

import fabric
import pydantic

logging.basicConfig()
logger = logging.getLogger(__name__)


class SIFContext(pydantic.BaseModel):

    sif_loc_str: str
    env_vars: typing.Optional[dict[str, str]]


class HPCJob(pydantic.BaseModel):

    email_address: str
    entry_point: str
    mem_size: int = 12


def _build_env_file(env_dict: dict[str, str]) -> str:
    return "\n".join([f"{k}={v}" for k, v in env_dict.items()])


def _build_singularity_exec(
    context: SIFContext,
    env_file: typing.Optional[str],
) -> str:
    _cmd = [
        "singularity",
        "exec",
        "--cleanenv",
    ]
    if env_file is not None:
        _cmd.append(f"--env-file {env_file}")

    _cmd.append(context.sif_loc_str)

    return " ".join(_cmd)


def _build_hpc_batch_job(
    job: HPCJob,
    job_name: str,
    output_path: str,
    singularity_exec: typing.Optional[str],
) -> str:
    if singularity_exec is not None:
        _exec = f"{singularity_exec} {job.entry_point}"
    else:
        _exec = job.entry_point

    # parsing is highly succeptible to newline characters causing errors, TODO: use a list?
    return f"""#!/bin/bash
#SBATCH --job-name={job_name}                               # Job name
#SBATCH --mail-type=END,FAIL                                # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user={job.email_address}                         # Where to send mail
#SBATCH --ntasks=1                                          # Run on a single CPU
#SBATCH --mem={job.mem_size}gb                                           # Job memory request (per node)
#SBATCH --time=10:00:00                                     # Time limit hrs:min:sec
#SBATCH --output='{output_path}'                            # Standard output and error log
#SBATCH --partition braintv                                 # Partition used for processing
#SBATCH --tmp=100M                                          # Request the amount of space your jobs needs on /scratch/fast

pwd; hostname; date

echo 'Running {job_name} job on a single thread'

{_exec}

date
    """


def _write_to_host(
    con: fabric.Connection,
    content: str,
    remote_path: str,
) -> None:
    """
    Notes
    -----
    - windows isnt supported?, no posixpath
    """
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        temp.write(content)
        temp.seek(0)
        result = con.put(temp.name, remote_path)

    if not result:
        raise Exception(f"Failed to transfer to host: {result}")


def run_hpc_job(
    con: fabric.Connection,
    job: HPCJob,
    jobs_dir: str,
    logs_dir: str,
    sif_context: typing.Optional[SIFContext],
    name_prefix: typing.Optional[str],
) -> tuple[str, str]:
    job_id = uuid.uuid4().hex
    logger.debug(f"job_id: {job_id}")

    if name_prefix is not None:
        job_name = f"{name_prefix}-{job_id}"
    else:
        job_name = job_id
    logger.debug(f"job_name: {job_name}")

    if sif_context is not None:
        if sif_context.env_vars is not None:
            env_file_content = _build_env_file(sif_context.env_vars)
            env_file = f"{jobs_dir}/{job_name}.env"
            sif_exec = _build_singularity_exec(sif_context, env_file)
        else:
            env_file_content = None
            env_file = None
            sif_exec = _build_singularity_exec(sif_context, None)
    else:
        env_file_content = None
        env_file = None
        sif_exec = None

    job_content = _build_hpc_batch_job(
        job,
        job_name,
        f"{logs_dir}/{job_name}.log",
        sif_exec,
    )

    if env_file is not None and env_file_content is not None:
        logger.info("Writing env file to host...")
        logger.debug("env_file_content: %s" % env_file_content)
        _write_to_host(
            con,
            env_file_content,
            env_file,
        )

    logger.info("Writing job to host...")
    logger.debug(f"job_content: {job_content}")
    job_script = f"{jobs_dir}/{job_name}.sh"
    _write_to_host(
        con,
        job_content,
        job_script,
    )

    logger.info("Triggering job...")
    result = con.run(f"sbatch {job_script}")

    result_output = result.stdout.strip()
    matches = re.match(r"Submitted batch job (\d+)", result_output)
    if matches is None or len(matches.groups()) < 1:
        raise Exception("Failed to find job id: %s" % result_output)
    slurm_job_id = matches.group(1)
    logger.debug("Parsed slurm_job_id: %s" % slurm_job_id)

    return slurm_job_id, job_name


def get_remote_content(
    con: fabric.Connection,
    file_path: str,
) -> str:
    return con.run(f"cat {file_path}", hide=True).stdout.strip()
