import polib
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            main()


def main():
    update_mo_file()
    run_shell_command("poetry run dotenv run ./scripts/generate.sh")


def update_mo_file():
    mo_file_path = (
        "/home/oskar/git/futurecoder/translations/locales/pl/LC_MESSAGES/futurecoder.mo"
    )
    po_file_path = "./pl.po"

    po = polib.pofile(po_file_path)
    po.save_as_mofile(mo_file_path)


def run_shell_command(command):
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="/home/oskar/git/futurecoder",
        )
        stdout, stderr = process.communicate()

        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")

        print("STDOUT:\n", stdout)
        print("STDERR:\n", stderr)

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    # Create a file change handler and start the observer
    file_path = "./pl.po"
    event_handler = FileChangeHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
