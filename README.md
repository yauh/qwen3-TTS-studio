# Qwen3-TTS Studio

A professional-grade interface for [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS), designed to unlock the model's full potential with fine-grained control and intuitive workflows.

![Qwen3-TTS Studio Screenshot](docs/screenshot.png)

## Why This Project?

Qwen3-TTS is a powerful text-to-speech model, but using it directly requires dealing with complex parameters, manual prompt engineering, and repetitive boilerplate code. **Qwen3-TTS Studio** was created to solve these problems:

- **Fine-tuned Control**: Easily adjust temperature, top-k, top-p, and other parameters with real-time presets (Fast / Balanced / Quality)
- **Better Results**: Optimized default settings and automatic token management to avoid common issues like silent audio or distorted output
- **Intuitive UI/UX**: Clean, modern interface that makes voice generation accessible to everyone
- **Automated Podcasts**: Generate complete podcasts from just a topic - AI writes the script, assigns voices, and synthesizes audio automatically

## Features

### Voice Generation
- **Voice Clone**: Clone any voice with just a 3-second audio sample
- **Custom Voice**: 9 preset voices with style control (Vivian, Serena, Ryan, etc.)
- **Voice Design**: Describe your desired voice in natural language
- **10 Language Support**: Korean, English, Chinese, Japanese, German, French, Russian, Portuguese, Spanish, Italian

### Podcast Generation
- **One-Click Podcasts**: Enter a topic, get a complete podcast
- **AI Script Writing**: Outline and transcript generation (supports OpenAI, Gemini, Claude via Portkey)
- **Multi-Speaker Support**: Assign different voices to each speaker
- **Custom Personas**: Create and save speaker personalities

### Quality of Life
- **Parameter Presets**: Quick presets for different use cases
- **Generation History**: Browse, search, and replay past generations
- **Auto-Save Settings**: Your preferences persist across sessions
- **Real-time Feedback**: Character count, generation time, and status indicators

## Requirements

- Python 3.12+
- macOS (MPS) / Linux (CUDA)
- 16GB+ RAM
- API Key for Podcast feature (choose one):
  - OpenAI (quick start)
  - Portkey (production, multi-provider)
  - Local LLM via Ollama/LM Studio (free, private)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/bc-dunia/qwen3-TTS-studio.git
cd qwen3-TTS-studio
```

### 2. Create Virtual Environment

```bash
conda create -n qwen3-tts python=3.12 -y
conda activate qwen3-tts
```

### 3. Install Dependencies

```bash
pip install -U qwen-tts
pip install gradio soundfile numpy moviepy openai
```

For CUDA users:
```bash
pip install -U flash-attn --no-build-isolation
```

### 4. Download Models

Download models from **HuggingFace** or **ModelScope**.

#### HuggingFace (Recommended)

```bash
pip install -U "huggingface_hub[cli]"

# Required models
huggingface-cli download Qwen/Qwen3-TTS-Tokenizer-12Hz --local-dir ./Qwen3-TTS-Tokenizer-12Hz
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base --local-dir ./Qwen3-TTS-12Hz-1.7B-Base
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --local-dir ./Qwen3-TTS-12Hz-1.7B-CustomVoice

# Optional models
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-Base --local-dir ./Qwen3-TTS-12Hz-0.6B-Base
huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./Qwen3-TTS-12Hz-0.6B-CustomVoice
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign --local-dir ./Qwen3-TTS-12Hz-1.7B-VoiceDesign
```

#### ModelScope (For users in China)

```bash
pip install -U modelscope

modelscope download --model Qwen/Qwen3-TTS-Tokenizer-12Hz --local_dir ./Qwen3-TTS-Tokenizer-12Hz
modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-Base --local_dir ./Qwen3-TTS-12Hz-1.7B-Base
modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --local_dir ./Qwen3-TTS-12Hz-1.7B-CustomVoice
```

### 5. Configure LLM Provider

Create a `.env` file and configure your LLM provider:

```bash
cp .env.example .env
```

#### Quick Start Options:

**OpenAI (Easiest):**
```bash
OPENAI_API_KEY=sk-proj-your-key
```
Get your key: https://platform.openai.com/api-keys

**Portkey (Production - Gemini, Claude, GPT, etc.):**
```bash
LLM_PROVIDER=portkey
LLM_MODEL=gemini-1.5-pro  # or claude-3-5-sonnet, gpt-4-turbo, etc.
PORTKEY_API_KEY=sk-portkey-your-key
```
1. Sign up at [Portkey](https://app.portkey.ai/)
2. Configure provider credentials in dashboard
3. Benefits: Observability, caching, cost tracking, multi-provider

**Local LLM (Free & Private - Ollama):**
```bash
LLM_PROVIDER=localllm
LLM_MODEL=llama3.2:3b  # or qwen2.5:3b, mistral:7b, etc.
```
1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama3.2:3b`
3. No API key needed - runs locally!

**Local LLM (Free & Private - LM Studio):**
```bash
LLM_PROVIDER=localllm
LLM_MODEL=qwen2.5-3b-instruct
LLM_LOCAL_BASE_URL=http://localhost:1234/v1
```
1. Install [LM Studio](https://lmstudio.ai/)
2. Download and load a model
3. Start local server in LM Studio

**Important:** Voice Clone audio transcription requires `OPENAI_API_KEY` (uses Whisper), even when using Portkey or Local LLM.

**Recommended Local Models for Stability:**
- ✅ Best: `qwen2.5:3b` or `qwen2.5:7b` (excellent JSON output)
- ✅ Good: `llama3.2:3b` (reliable, fast)
- ✅ Good: `mistral:7b` (higher quality, slower)
- ⚠️ Variable: `ministral-3b` (may struggle with complex JSON)

**Tips for Local LLM Success:**
- Use models 3B or larger for better reliability
- Qwen models typically perform best at JSON generation
- If you get JSON errors, try a different model or increase model size

See [PORTKEY_INTEGRATION.md](PORTKEY_INTEGRATION.md) for detailed configuration.

## Usage

### Start Server

```bash
python qwen_tts_ui.py
```

Open `http://127.0.0.1:7860` in your browser.

### Available Models

| Model | Features | Size |
|-------|----------|------|
| 1.7B-CustomVoice | 9 preset voices + style control | 4.2GB |
| 1.7B-Base | Voice Clone (3-sec sample) | 4.2GB |
| 1.7B-VoiceDesign | Natural language voice design | 4.2GB |
| 0.6B-CustomVoice | 9 preset voices (lightweight) | 2.3GB |
| 0.6B-Base | Voice Clone (lightweight) | 2.3GB |

### Preset Voices

| Speaker | Description | Native Language |
|---------|-------------|-----------------|
| Vivian | Bright, slightly sharp young female | Chinese |
| Serena | Warm, soft young female | Chinese |
| Ryan | Dynamic male with strong rhythm | English |
| Aiden | Bright American male, clear midrange | English |
| Ono_Anna | Lively Japanese female | Japanese |
| Sohee | Warm Korean female, rich emotion | Korean |

## Project Structure

```
qwen3-TTS-studio/
├── qwen_tts_ui.py              # Main entry point
├── config.py                   # LLM provider configuration
│
├── ui/                         # UI Components
│   ├── content_input.py        # Content input section
│   ├── draft_editor.py         # Draft editing
│   ├── draft_preview.py        # Outline/transcript preview
│   ├── persona.py              # Persona management UI
│   ├── progress.py             # Progress indicators
│   └── voice_cards.py          # Voice selection cards
│
├── podcast/                    # Podcast Generation
│   ├── orchestrator.py         # Main orchestration
│   ├── models.py               # Pydantic models
│   ├── outline.py              # AI outline generation
│   ├── transcript.py           # AI transcript generation
│   ├── prompts.py              # LLM prompts
│   └── session.py              # Session management
│
├── audio/                      # Audio Processing
│   ├── generator.py            # TTS generation
│   ├── batch.py                # Batch processing
│   ├── combiner.py             # Audio concatenation
│   └── model_loader.py         # Model loading
│
└── storage/                    # Data Persistence
    ├── history.py              # Podcast history
    ├── persona.py              # Persona storage
    ├── persona_models.py       # Persona models
    └── voice.py                # Voice management
```

## Troubleshooting

### Common Issues

#### "OPENAI_API_KEY not found in environment"
- Ensure you have a `.env` file in the project root
- Verify `OPENAI_API_KEY` is set in `.env`
- Check that `LLM_PROVIDER=openai` (or not set, as it's the default)

#### "PORTKEY_API_KEY not found in environment"
- Verify `LLM_PROVIDER=portkey` is set in `.env`
- Ensure `PORTKEY_API_KEY` is configured
- Configure your provider credentials in the Portkey dashboard

#### Whisper Transcription Error (Voice Clone)
- Audio transcription requires `OPENAI_API_KEY` even when using Portkey or Local LLM
- Whisper is OpenAI-specific and cannot be routed through other providers
- Set `OPENAI_API_KEY` in your `.env` file

#### Local LLM Connection Issues
- Ensure Ollama is running: `ollama serve` (usually starts automatically)
- For LM Studio: Start the local server in the app (default port 1234)
- Check model is loaded: `ollama list` (for Ollama)
- Verify base URL matches your setup (Ollama: 11434, LM Studio: 1234)

#### Local LLM JSON Errors
- **Problem**: Model outputs invalid JSON or JSON Schema instead of data
- **Solution 1**: Try a different model (qwen2.5:3b recommended)
- **Solution 2**: Use a larger model size (7B instead of 3B)
- **Solution 3**: In LM Studio, adjust "Max Tokens" to 2000+ in settings
- Models like Ministral may struggle - switch to Qwen or Llama for reliability

#### Audio Generation Issues
- Ensure sufficient RAM (16GB+ recommended)
- For CUDA users, verify flash-attn is properly installed
- Check that model files are completely downloaded

#### Model Loading Errors
- Verify all required models are downloaded to the correct directories
- Check that model paths match the directory structure
- Ensure sufficient disk space for models

For more detailed troubleshooting, see [PORTKEY_INTEGRATION.md](PORTKEY_INTEGRATION.md).

## Acknowledgments

This project is built on top of the excellent [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) model by Alibaba Qwen team.

- **HuggingFace**: https://huggingface.co/collections/Qwen/qwen3-tts
- **ModelScope**: https://modelscope.cn/collections/Qwen/Qwen3-TTS
- **Paper**: https://arxiv.org/abs/2601.15621
- **Blog**: https://qwen.ai/blog?id=qwen3tts-0115

## License

This project uses Qwen3-TTS models. Please refer to the [Qwen3-TTS License](https://github.com/QwenLM/Qwen3-TTS/blob/main/LICENSE) for model usage terms.
