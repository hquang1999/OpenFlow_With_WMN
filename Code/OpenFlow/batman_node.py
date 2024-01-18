import socket
import subprocess
from time import sleep
from typing import Literal
from batman_config import PORT, CONTROLLER_IP


def get_batman_table(table_id: Literal["oj", "nj"]) -> str:
    completed_process = subprocess.run(
        ["sudo", "batctl", "meshif", "bat0", table_id],
        capture_output=True,
        encoding="utf8",
    )
    # return json.loads(completed_process.stdout)
    return completed_process.stdout.strip()


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # send tables to controller every second
    while True:
        s.sendto(get_batman_table("oj").encode("utf8"), (CONTROLLER_IP, PORT))
        sleep(60)
