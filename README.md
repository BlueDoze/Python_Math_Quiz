# Python Math Quiz

This is a small Python math-quiz project.
The main script is `Pedro_Aguiar_Python_Math_Quiz_Code.py` and it uses only the Python standard library (random, time, math).

## Repository structure

- `Pedro_Aguiar_Python_Math_Quiz_Code.py` — the game code.
- `Dockerfile` — Docker image definition to run the game.
- `docker-compose.yml` — Compose service for running the game interactively.
- `requirements.txt` — dependency file (currently empty / placeholder).
- `leaderboard.txt` — file used to persist scores (created/mounted by Compose).

## Requirements

- Docker Engine installed
- Docker Compose (bundled with Docker Desktop or `docker-compose` separately)
- Windows PowerShell (examples below use PowerShell)

## Run with Docker Compose (recommended)

Open PowerShell in the project folder (`c:\Users\pedri\OneDrive\Desktop\python_math\Python_Math_Quiz`) and run:

```powershell
# Build the image
docker-compose build

# Run the container interactively (recommended for answering prompts)
docker-compose run --rm quiz
```

Notes:

- `docker-compose run --rm quiz` creates a container from the `quiz` service, attaches a TTY and keeps STDIN open so you can answer prompts.
- `--rm` removes the container when it exits.

You can also use `docker-compose up --build`, but for interactive sessions `run` is often more convenient.

## Run with Docker CLI (alternative)

```powershell
# Build with docker
docker build -t python-math-quiz:latest .

# Run interactively (mount the host leaderboard file)
# In PowerShell use $(pwd).Path for the absolute path
$hostPath = "$(pwd).Path\\leaderboard.txt"
docker run -it --rm -v ${hostPath}:/app/leaderboard.txt python-math-quiz:latest
```

If `leaderboard.txt` does not exist on the host, Docker will create an empty file when mounting.

## Leaderboard persistence

The `docker-compose.yml` mounts `./leaderboard.txt` to `/app/leaderboard.txt` inside the container, so scores persist between runs.

## Development (hot-reload / edit without rebuild)

Currently the Compose setup copies files into the image at build time (`COPY . /app`). For a development workflow where you want live edits without rebuilding the image, modify `docker-compose.yml` to mount the project directory into the container:

```yaml
services:
  quiz:
    build: .
    volumes:
      - ./:/app
      - ./leaderboard.txt:/app/leaderboard.txt
    stdin_open: true
    tty: true
    working_dir: /app
    command: python Pedro_Aguiar_Python_Math_Quiz_Code.py
```

This will reflect changes made on the host immediately inside the container.

## Adding dependencies

If you start using third-party libraries, add them to `requirements.txt` (one per line). Then run:

```powershell
docker-compose build --no-cache
```

Or, if you prefer `docker build`:

```powershell
docker build -t python-math-quiz:latest .
```

## Troubleshooting

- Permission error mounting `leaderboard.txt` on Windows: create the file on the host first with `New-Item -Path . -Name "leaderboard.txt" -ItemType "file"` and retry.
- Interactive/TTY issues: prefer `docker-compose run --rm quiz` for interactive sessions.

## License

Feel free to use or modify this code. No formal license is specified in this repository.
