import datetime
import os

from dotenv import load_dotenv


def get_log_output_path():
    load_dotenv()  # Load environment variables from .env

    today_date = datetime.datetime.today().date()

    output_folder_base = os.getenv("OUTPUT_FOLDER", "")  # Get from .env
    output_folder = os.path.join(output_folder_base, str(today_date.year))
    os.makedirs(output_folder, exist_ok=True)

    log_filename = "log.txt"
    log_paths = [os.path.join(output_folder, log_filename), log_filename]
    
    return log_paths

def update_log(message) -> None:
    """
    Update the log file with a message.
    """
    log_paths = get_log_output_path()
    for log_path in log_paths:
        with open(log_path, "a") as log_file:
            log_file.write(f"{datetime.datetime.now().isoformat()} --- {message}\n")

