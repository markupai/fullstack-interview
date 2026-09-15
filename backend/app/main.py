"""Process entrypoint. One image, one package, selected by role: `api` or `worker`."""

import asyncio
import sys

import uvicorn

from app.config import settings

ROLES = ("api", "worker")


def run_api() -> None:
    uvicorn.run(
        "app.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )


def run_worker() -> None:
    from app.workers.main import main

    asyncio.run(main())


def main(argv: list[str]) -> None:
    role = argv[0] if argv else "api"
    if role == "api":
        run_api()
    elif role == "worker":
        run_worker()
    else:
        print(f"unknown role {role!r}; expected one of {ROLES}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
