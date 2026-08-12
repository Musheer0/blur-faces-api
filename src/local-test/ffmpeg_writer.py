import subprocess
import numpy as np

class FFmpegWriter:
    def __init__(
        self,
        output: str,
        width: int,
        height: int,
        fps: float,
        encoder: str = "libx264",
        pix_fmt: str = "bgr24",
        **extra: str,
    ):
        self._proc = subprocess.Popen(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-f",
                "rawvideo",
                "-pix_fmt",
                pix_fmt,
                "-s",
                f"{width}x{height}",
                "-r",
                str(fps),
                "-i",
                "-",
                "-an",
                "-c:v",
                encoder,
                "-pix_fmt",
                "yuv420p",
                *[arg for kv in extra.items() for arg in (f"-{kv[0]}", str(kv[1]))],
                output,
            ],
            stdin=subprocess.PIPE,
        )

    def write(self, frame: np.ndarray) -> None:
        self._proc.stdin.write(frame.tobytes())

    def release(self) -> None:
        if self._proc.stdin is not None:
            self._proc.stdin.close()
            self._proc.stdin = None
        self._proc.wait()
        if self._proc.returncode != 0:
            raise RuntimeError(f"ffmpeg exited with code {self._proc.returncode}")
