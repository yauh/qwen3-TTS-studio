"""Transcript file parser for importing existing podcast transcripts."""

from __future__ import annotations

import re
from typing import List, Dict, Tuple


def parse_transcript_text(content: str) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Parse transcript text in the format:

    Speaker Name:
    [optional timecode]
    dialogue text

    Args:
        content: Raw transcript text

    Returns:
        Tuple of (dialogues, unique_speakers)
        - dialogues: List of {"speaker": "Speaker 1", "text": "..."}
        - unique_speakers: List of unique speaker names found

    Examples:
        >>> content = '''
        ... Speaker 1:
        ... 00:00
        ... Hello world
        ...
        ... Speaker 2:
        ... 00:05
        ... Hi there
        ... '''
        >>> dialogues, speakers = parse_transcript_text(content)
        >>> len(dialogues)
        2
        >>> speakers
        ['Speaker 1', 'Speaker 2']
    """
    dialogues: List[Dict[str, str]] = []
    unique_speakers: List[str] = []

    lines = content.split('\n')

    current_speaker = None
    current_text_lines: List[str] = []

    # Regex patterns
    # Matches: "Speaker 1:", "Marco:", "Dylan:", etc.
    speaker_pattern = re.compile(r'^([^:]+):\s*$')
    # Matches timecodes like "00:00", "01:23", "12:34:56"
    timecode_pattern = re.compile(r'^\d{1,2}:\d{2}(:\d{2})?\s*$')

    def save_current_dialogue():
        """Save the current dialogue if we have both speaker and text."""
        nonlocal current_speaker, current_text_lines
        if current_speaker and current_text_lines:
            text = ' '.join(current_text_lines).strip()
            if text:  # Only save if there's actual text
                dialogues.append({
                    "speaker": current_speaker,
                    "text": text
                })
                if current_speaker not in unique_speakers:
                    unique_speakers.append(current_speaker)
        current_text_lines = []

    for line in lines:
        line_stripped = line.strip()

        # Skip empty lines
        if not line_stripped:
            continue

        # Check if this is a speaker line
        speaker_match = speaker_pattern.match(line_stripped)
        if speaker_match:
            # Save previous dialogue
            save_current_dialogue()
            # Start new dialogue
            current_speaker = speaker_match.group(1).strip()
            continue

        # Check if this is a timecode (skip it)
        if timecode_pattern.match(line_stripped):
            continue

        # Otherwise, it's dialogue text
        if current_speaker:
            current_text_lines.append(line_stripped)

    # Save the last dialogue
    save_current_dialogue()

    return dialogues, unique_speakers


def parse_transcript_file(file_path: str) -> Tuple[List[Dict[str, str]], List[str]]:
    """
    Parse a transcript file.

    Args:
        file_path: Path to the transcript file

    Returns:
        Tuple of (dialogues, unique_speakers)

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty or cannot be parsed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Transcript file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading transcript file: {e}")

    if not content.strip():
        raise ValueError("Transcript file is empty")

    dialogues, speakers = parse_transcript_text(content)

    if not dialogues:
        raise ValueError(
            "No dialogues found in transcript. "
            "Expected format:\n"
            "Speaker Name:\n"
            "[optional timecode]\n"
            "dialogue text"
        )

    return dialogues, speakers


def create_speaker_mapping(
    unique_speakers: List[str],
    voice_selections: List[Dict[str, str]]
) -> Dict[str, str]:
    """
    Create a mapping from transcript speaker names to voice IDs.

    Args:
        unique_speakers: List of speaker names from transcript
        voice_selections: List of {"name": "...", "voice_id": "...", "role": "..."} from UI

    Returns:
        Dict mapping speaker name to voice ID

    Example:
        >>> unique_speakers = ["Speaker 1", "Speaker 2"]
        >>> voices = [
        ...     {"name": "Marco", "voice_id": "vivian", "role": "Host"},
        ...     {"name": "Daniel", "voice_id": "ryan", "role": "Guest"}
        ... ]
        >>> mapping = create_speaker_mapping(unique_speakers, voices)
        >>> mapping
        {'Speaker 1': 'vivian', 'Speaker 2': 'ryan'}
    """
    mapping = {}

    # Simple mapping: transcript speaker order -> voice selection order
    for idx, speaker in enumerate(unique_speakers):
        if idx < len(voice_selections):
            mapping[speaker] = voice_selections[idx]["voice_id"]
        else:
            # If more speakers than voices, reuse voices
            mapping[speaker] = voice_selections[idx % len(voice_selections)]["voice_id"]

    return mapping


def apply_speaker_mapping(
    dialogues: List[Dict[str, str]],
    speaker_mapping: Dict[str, str]
) -> List[Dict[str, str]]:
    """
    Apply speaker mapping to dialogues, replacing speaker names with voice IDs.

    Args:
        dialogues: List of {"speaker": "Speaker 1", "text": "..."}
        speaker_mapping: Dict mapping speaker names to voice IDs

    Returns:
        List of dialogues with speakers replaced by voice IDs
    """
    mapped_dialogues = []

    for dialogue in dialogues:
        speaker_name = dialogue["speaker"]
        voice_id = speaker_mapping.get(speaker_name)

        if not voice_id:
            # If no mapping found, keep original speaker name
            voice_id = speaker_name

        mapped_dialogues.append({
            "speaker": voice_id,
            "text": dialogue["text"]
        })

    return mapped_dialogues


def validate_transcript(
    dialogues: List[Dict[str, str]],
    min_dialogues: int = 2
) -> Tuple[bool, str]:
    """
    Validate a parsed transcript.

    Args:
        dialogues: Parsed dialogues
        min_dialogues: Minimum number of dialogues required

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not dialogues:
        return False, "No dialogues found in transcript"

    if len(dialogues) < min_dialogues:
        return False, f"Transcript must contain at least {min_dialogues} dialogues (found {len(dialogues)})"

    # Check that all dialogues have text
    for idx, dialogue in enumerate(dialogues):
        if not dialogue.get("text", "").strip():
            return False, f"Dialogue {idx + 1} has no text"

    return True, ""


if __name__ == "__main__":
    # Test with sample file
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            dialogues, speakers = parse_transcript_file(file_path)
            print(f"✓ Parsed {len(dialogues)} dialogues")
            print(f"✓ Found {len(speakers)} unique speakers: {', '.join(speakers)}")
            print("\nFirst 3 dialogues:")
            for i, d in enumerate(dialogues[:3], 1):
                print(f"{i}. {d['speaker']}: {d['text'][:80]}...")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        # Run doctests
        import doctest
        doctest.testmod()
        print("✓ All tests passed")
