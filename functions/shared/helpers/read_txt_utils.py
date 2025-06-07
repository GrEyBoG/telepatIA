from functools import lru_cache
from pathlib import Path

PROMPTS_DIR = Path("shared/assets/prompts")

@lru_cache(maxsize=None)
def _read_prompt_sync(path: Path) -> str:
    #---------------------------------------------------------------------------
    # *                           _read_prompt_sync
    # ?  Read and cache the content of a prompt file synchronously
    # @param path Path  The full path to the prompt file
    # @return str       The content of the prompt
    #---------------------------------------------------------------------------
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found at path: {path}")
    except Exception as e:
        raise RuntimeError(f"Failed to read prompt from {path}: {e}") from e
    
async def _load_prompt(filename: str, base_dir: Path = PROMPTS_DIR) -> str:
    #---------------------------------------------------------------------------
    # *                           _load_prompt
    # ?  Loads a prompt file from the prompts directory
    # @param filename str  The name of the prompt file
    # @return str          The content of the prompt
    #---------------------------------------------------------------------------
    try:
        return _read_prompt_sync(base_dir / filename)
    except Exception as e:
        raise RuntimeError(f"Error loading prompt '{filename}' from '{base_dir}': {e}") from e