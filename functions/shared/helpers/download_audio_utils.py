from pathlib import Path
import httpx

AUDIO_DIR = Path("shared/assets/audio")


#---------------------------
#     FILE UTILITIES
#---------------------------

def _ensure_audio_directory() -> None:
    #---------------------------------------------------------------------------
    # *                     _ensure_audio_directory
    # ?  Ensures that the audio directory exists; creates it if necessary.
    # @param None
    # @return None
    #---------------------------------------------------------------------------
    try:
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create audio directory '{AUDIO_DIR}': {e}") from e


async def download_audio(url: str, filename: str | None = None) -> Path:
    #---------------------------------------------------------------------------
    # *                      download_audio
    # ?  Download an audio file from a URL and save it locally.
    # @param url str           The URL of the audio file to download.
    # @param filename str|None Optional custom filename (with extension). If None, uses name from URL.
    # @return Path             The path to the saved audio file.
    #---------------------------------------------------------------------------
    _ensure_audio_directory()

    if filename:
        dest_name = filename
    else:
        try:
            dest_name = Path(url).name
            if not dest_name:
                raise ValueError("URL does not contain a valid filename.")
        except Exception:
            raise ValueError(f"Cannot infer filename from URL: {url}")

    dest_path = AUDIO_DIR / dest_name

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Failed to download audio from {url}: {e}") from e

        try:
            dest_path.write_bytes(response.content)
        except Exception as e:
            raise RuntimeError(f"Failed to save audio file to {dest_path}: {e}") from e

    return dest_path


def delete_audio_file(file_path: Path) -> None:
    #---------------------------------------------------------------------------
    # *                      delete_audio_file
    # ?  Delete a local audio file given its Path.
    # @param file_path Path  The full path to the audio file to delete.
    # @return None
    #---------------------------------------------------------------------------
    try:
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
        else:
            raise FileNotFoundError(f"Audio file not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to delete audio file '{file_path}': {e}") from e
