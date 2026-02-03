# Qwen3-TTS Studio

A professional interface for [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) with automated podcast generation, multi-language support, and flexible LLM integration.

![Qwen3-TTS Studio Screenshot](docs/screenshot.png)

## Features

### Voice Generation
- **Voice Clone**: Clone any voice from a 3-second audio sample
- **Custom Voices**: 9 preset voices (Vivian, Serena, Ryan, etc.)
- **Voice Design**: Describe your desired voice in natural language
- **10 Languages**: English, Chinese, Korean, Japanese, German, French, Spanish, Portuguese, Russian, Italian

### Podcast Generation

**Two Ways to Create Podcasts:**

1. **AI-Generated** - Provide a topic, AI creates outline and script
   - Uses OpenAI, Gemini, Claude, or local LLMs (Ollama/LM Studio)
   - Automatic speaker assignment
   - Custom personas support

2. **Import Existing Transcript** - Upload or paste your own script
   - Simple format: `Speaker Name:\n[timecode]\ntext`
   - Auto-maps speakers to voices
   - Skip AI generation entirely

### Quality of Life
- Parameter presets (Fast/Balanced/Quality)
- Generation history with search
- Auto-save settings
- Real-time progress tracking

## Quick Start

### Installation

```bash
# 1. Clone and setup
git clone https://github.com/bc-dunia/qwen3-TTS-studio.git
cd qwen3-TTS-studio
conda create -n qwen3-tts python=3.12 -y
conda activate qwen3-tts

# 2. Install dependencies
pip install -U qwen-tts
pip install gradio soundfile numpy moviepy openai

# 3. Download TTS models (required)
pip install -U "huggingface_hub[cli]"
huggingface-cli download Qwen/Qwen3-TTS-Tokenizer-12Hz --local-dir ./Qwen3-TTS-Tokenizer-12Hz
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base --local-dir ./Qwen3-TTS-12Hz-1.7B-Base
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --local-dir ./Qwen3-TTS-12Hz-1.7B-CustomVoice

# 4. Configure LLM (choose one option below)
cp .env.example .env
# Edit .env with your chosen provider
```

### LLM Provider Setup

**Option 1: OpenAI (Easiest)**
```bash
# In .env file:
OPENAI_API_KEY=sk-proj-your-key
```

**Option 2: Local LLM (Free, Private, Recommended)**
```bash
# Install Ollama
brew install ollama  # or download from ollama.ai

# Pull a model
ollama pull qwen2.5:3b

# In .env file:
LLM_PROVIDER=localllm
LLM_MODEL=qwen2.5:3b
```

**Option 3: Portkey (Production, Multi-Provider)**
```bash
# In .env file:
LLM_PROVIDER=portkey
LLM_MODEL=gemini-1.5-pro  # or claude-3-5-sonnet, etc.
PORTKEY_API_KEY=sk-portkey-your-key
```
Sign up at [portkey.ai](https://app.portkey.ai/), configure provider in dashboard

### Run

```bash
python qwen_tts_ui.py
```

Open `http://127.0.0.1:7860` in your browser.

## Podcast Creation Methods

### Method 1: AI-Generated

1. Go to **Podcast** tab
2. Select **"Generate with AI"** mode
3. Enter topic (e.g., "The future of AI in music production")
4. Optional: Add key points and style preferences
5. Select 2-4 speaker voices
6. Click **Generate Podcast**

AI will create outline, write dialogue, and synthesize audio.

### Method 2: Import Transcript

1. Go to **Podcast** tab
2. Select **"Import Transcript"** mode
3. Upload `.txt` file or paste transcript:

```
Speaker 1:
00:00
Welcome to the show. Today we're discussing AI.

Speaker 2:
00:05
Thanks for having me. I'm excited to talk about this.
```

4. Select voices (order matches Speaker 1, Speaker 2, etc.)
5. Click **Generate Podcast**

Skips AI generation, goes straight to audio synthesis.

**Transcript Format:**
- Speaker name + colon (`:`)
- Optional timecode (ignored for TTS)
- Dialogue text
- Blank line between speakers
- Any speaker names work (`Speaker 1`, `Marco`, `Host`, etc.)

## LLM Provider Comparison

| Provider | Cost | Speed | Quality | Privacy | Setup |
|----------|------|-------|---------|---------|-------|
| **Local (Ollama)** | Free | Fast | Good | 100% Private | Easy |
| **Local (LM Studio)** | Free | Fast | Good | 100% Private | Medium |
| **OpenAI** | Paid | Very Fast | Excellent | Cloud | Easiest |
| **Portkey (Gemini)** | Paid | Fast | Excellent | Cloud | Medium |
| **Portkey (Claude)** | Paid | Fast | Excellent | Cloud | Medium |

**Recommended:** Start with **Ollama + qwen2.5:3b** for free, private, high-quality podcast generation.

### Best Local Models

| Model | Quality | Speed | JSON Reliability |
|-------|---------|-------|------------------|
| `qwen2.5:3b` | ⭐⭐⭐⭐ | Very Fast | Excellent |
| `qwen2.5:7b` | ⭐⭐⭐⭐⭐ | Fast | Excellent |
| `llama3.2:3b` | ⭐⭐⭐ | Very Fast | Good |
| `mistral:7b` | ⭐⭐⭐⭐ | Medium | Good |

**Tip:** Qwen models excel at structured JSON output, making them ideal for podcast generation.

## Requirements

- **Python**: 3.12+
- **OS**: macOS (MPS) or Linux (CUDA)
- **RAM**: 16GB+
- **For Podcast Feature**:
  - OpenAI API key OR
  - Portkey account OR
  - Local LLM (Ollama/LM Studio)
- **For Voice Clone**: OpenAI API key (Whisper transcription)

## Available TTS Models

| Model | Features | Size | Use Case |
|-------|----------|------|----------|
| 1.7B-CustomVoice | 9 preset voices | 4.2GB | Recommended |
| 1.7B-Base | Voice cloning | 4.2GB | Custom voices |
| 1.7B-VoiceDesign | Natural language voice | 4.2GB | Voice description |
| 0.6B-CustomVoice | 9 preset voices | 2.3GB | Lightweight |
| 0.6B-Base | Voice cloning | 2.3GB | Lightweight |

## Troubleshooting

### Local LLM Issues

**"Connection refused" or "Cannot connect"**
- Ollama: Check if running with `ollama list`
- LM Studio: Verify local server is started (port 1234)
- Check `.env` has correct `LLM_LOCAL_BASE_URL`

**"Invalid JSON" or "JSON Schema" errors**
- Switch to `qwen2.5:3b` (best for JSON)
- Use larger model (`qwen2.5:7b`)
- In LM Studio: Set "Max Tokens" to 2000+

**Model too slow**
- Use smaller model (`qwen2.5:3b` instead of `7b`)
- Reduce number of podcast segments
- Ensure enough RAM available

### OpenAI/Portkey Issues

**"OPENAI_API_KEY not found"**
- Create `.env` file: `cp .env.example .env`
- Add your key: `OPENAI_API_KEY=sk-proj-...`

**"PORTKEY_API_KEY not found"**
- Set `LLM_PROVIDER=portkey` in `.env`
- Add Portkey key: `PORTKEY_API_KEY=sk-portkey-...`
- Configure provider in Portkey dashboard

### Voice Clone Whisper Error

Audio transcription always requires `OPENAI_API_KEY`, even when using Portkey or local LLMs (Whisper is OpenAI-only).

### Audio Generation Issues

- Ensure 16GB+ RAM available
- For CUDA: Install flash-attn: `pip install -U flash-attn --no-build-isolation`
- Verify models fully downloaded
- Check sufficient disk space

## Configuration Files

**.env** - Your configuration (create from .env.example)
```bash
# Required for Podcast AI generation (pick one)
LLM_PROVIDER=localllm
LLM_MODEL=qwen2.5:3b

# Required for Voice Clone transcription
OPENAI_API_KEY=sk-proj-...
```

**See `.env.example`** for all configuration options and detailed setup instructions.

**See `PORTKEY_INTEGRATION.md`** for advanced Portkey configuration, observability, and multi-provider setup.

## Project Structure

```
qwen3-TTS-studio/
├── qwen_tts_ui.py              # Main entry point
├── config.py                   # LLM provider configuration
├── podcast/
│   ├── orchestrator.py         # Podcast workflow
│   ├── transcript_parser.py    # Import transcript support
│   ├── outline.py              # AI outline generation
│   └── transcript.py           # AI script generation
├── audio/
│   ├── generator.py            # TTS synthesis
│   └── combiner.py             # Audio merging
├── ui/
│   └── content_input.py        # Podcast input UI
└── storage/
    ├── persona.py              # Speaker personas
    └── history.py              # Generation history
```

## Advanced Usage

### Custom Personas

Create speaker personalities in the Persona tab:
- Define character traits
- Set speaking style
- Add expertise areas
- Use in podcast generation

### Quality Presets

- **Fast**: Lower quality, faster generation
- **Balanced**: Good quality, reasonable speed (recommended)
- **Quality**: Best quality, slower generation

### Multi-Language

Change language in Podcast tab dropdown. Affects:
- AI script generation language
- TTS voice synthesis
- Natural pronunciation

## Acknowledgments

Built on [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) by Alibaba Qwen team.

- [HuggingFace Models](https://huggingface.co/collections/Qwen/qwen3-tts)
- [Research Paper](https://arxiv.org/abs/2601.15621)
- [Official Blog](https://qwen.ai/blog?id=qwen3tts-0115)

## License

This project uses Qwen3-TTS models. See [Qwen3-TTS License](https://github.com/QwenLM/Qwen3-TTS/blob/main/LICENSE) for terms.
