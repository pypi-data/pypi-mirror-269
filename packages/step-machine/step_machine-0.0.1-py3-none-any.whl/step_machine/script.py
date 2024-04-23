import hashlib
import subprocess
import sys

import time

from step_machine.types import StepExecutionOutput


def calculate_checksum(file_path: str) -> str:
    """
    Calculate the SHA-256 checksum of a file.

    :param file_path: The path to the file for which to calculate the checksum.
    :return: The hexadecimal SHA-256 checksum of the file.
    """
    # Initialize a SHA-256 hasher
    sha256_hash = hashlib.sha256()

    # Open the file in binary mode and read chunks to calculate the hash
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    # Return the hexadecimal representation of the digest
    return sha256_hash.hexdigest()


def run_script(entry_point, script_path) -> StepExecutionOutput:
    # Start the subprocess and specify stdout and stderr to be piped
    with subprocess.Popen(
            [entry_point, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line-buffered
    ) as proc:
        # Variables to store captured outputs
        stdout_capture = []
        stderr_capture = []

        # Stream stdout and stderr line by line
        while True:
            output = proc.stdout.readline()
            if output:
                print(output, end='')  # Stream to the current stdout channel
                stdout_capture.append(output)
            err = proc.stderr.readline()
            if err:
                print(err, end='', file=sys.stderr)  # Stream to the current stderr channel
                stderr_capture.append(err)

            # Break if process is done and no more output
            if output == '' and err == '' and proc.poll() is not None:
                break

        # Make sure to capture any remaining output after the loop has finished
        stdout_capture.extend(proc.stdout.readlines())
        stderr_capture.extend(proc.stderr.readlines())

        # Gather the final parts of stdout and stderr
        final_stdout = ''.join(stdout_capture)
        final_stderr = ''.join(stderr_capture)

    # Get the exit code
    exit_code = proc.returncode

    # Get the signature and timestamp
    signature = calculate_checksum(script_path)
    current_unix_timestamp = int(time.time())

    # Construct the final output object
    output = StepExecutionOutput(
        signature=signature,
        timestamp=current_unix_timestamp,
        exit_code=exit_code,
        stdout=final_stdout,
        stderr=final_stderr,
    )
    return output
