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
- **AI Script Writing**: GPT-powered outline and transcript generation
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
- OpenAI API Key or Portkey Account (for Podcast feature)

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

The Podcast feature requires an LLM provider for AI-powered outline and transcript generation. You can choose between **OpenAI** (direct) or **Portkey** (with observability and advanced features).

#### Option A: OpenAI (Default)

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

#### Option B: Portkey (Recommended for Production)

Portkey provides observability, caching, fallbacks, and cost management while maintaining full OpenAI compatibility.

1. Sign up at [Portkey](https://app.portkey.ai/)
2. Create a virtual key for OpenAI in the Portkey dashboard
3. Configure `.env`:

```bash
LLM_PROVIDER=portkey
PORTKEY_API_KEY=sk-portkey-your-portkey-api-key
PORTKEY_VIRTUAL_KEY=openai-virtual-your-virtual-key
```

**Benefits of Portkey:**
- 📊 Real-time observability and analytics
- 💰 Cost tracking and management
- ⚡ Semantic caching to reduce costs
- 🔄 Automatic fallbacks and load balancing
- 📈 Detailed usage metrics

#### Optional: Custom Model

You can override the default model (gpt-5.2) by adding:

```bash
LLM_MODEL=gpt-4-turbo
```

For complete configuration options, see [Portkey Integration Guide](PORTKEY_INTEGRATION.md).

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

## LLM Provider Configuration

This project supports multiple LLM providers for the Podcast generation feature:

| Provider | Setup Difficulty | Features | Best For |
|----------|-----------------|----------|----------|
| **OpenAI** | Easy | Direct API access | Quick setup, development |
| **Portkey** | Medium | Observability, caching, fallbacks, analytics | Production, cost management, monitoring |

**Quick Switch:** Change providers by updating a single environment variable in `.env`:
```bash
LLM_PROVIDER=openai  # or 'portkey'
```

For detailed setup and configuration, see [PORTKEY_INTEGRATION.md](PORTKEY_INTEGRATION.md).

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
- Ensure both `PORTKEY_API_KEY` and `PORTKEY_VIRTUAL_KEY` are configured
- Check that your virtual key is properly set up in the Portkey dashboard

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
