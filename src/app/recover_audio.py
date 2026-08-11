import subprocess


def recover_audio(input: str, audio_video: str, output: str):
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", input,
        "-i", audio_video,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output,
    ], check=True)

    return output