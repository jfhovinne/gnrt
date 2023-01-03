"""
Run tests for multiple Python versions concurrently.
"""

import sys
import anyio
import dagger


async def test():
    versions = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12-rc"]

    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory(".")

        async def test_version(version: str):
            python = (
                client.container().from_(f"python:{version}-slim-buster")
                .with_mounted_directory("/src", src)
                .with_workdir("/src")
                .with_exec(["./vendor/bin/task", "build"])
                .with_exec(["./vendor/bin/task", "qa"])
                .with_exec(["./vendor/bin/task", "test"])
            )

            print(f"Starting tests for Python {version}")

            await python.exit_code()

            print(f"Tests for Python {version} succeeded!")

        async with anyio.create_task_group() as tg:
            for version in versions:
                tg.start_soon(test_version, version)

    print("All tasks have finished")


if __name__ == "__main__":
    anyio.run(test)
