import subprocess
import tempfile
import os
import dotenv

dotenv.load_dotenv()

PIPER_EXE = os.getenv("PIPER_EXE_PATH")
VOICE_MODEL = os.getenv("VOICE_MODEL_PATH")

def speak(text):
    print("\nAssistant:\n")
    print(text)

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as wav_file:

        output_path = wav_file.name

    result = subprocess.run(
        [
            PIPER_EXE,
            "--model",
            VOICE_MODEL,
            "--output_file",
            output_path
        ],
        input=text,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        print("Piper Error:")
        print(result.stderr)
        return

    if not os.path.exists(output_path):
        print("Audio file missing")
        return

    if os.path.getsize(output_path) == 0:
        print("Audio file empty")
        return

    subprocess.run(
        [
            "powershell",
            "-c",
            f'(New-Object Media.SoundPlayer "{output_path}").PlaySync();'
        ]
    )