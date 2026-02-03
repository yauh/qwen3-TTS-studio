# Portkey Integration Guide

This document explains the Portkey integration that has been added to Qwen3-TTS Studio, allowing you to use either OpenAI directly or route your requests through Portkey for enhanced observability and features.

## What Changed?

### Modified Files

1. **`config.py`** - Enhanced configuration system
   - Added `get_llm_provider()` - Select between 'openai' or 'portkey'
   - Added `get_llm_model()` - Configure model name via environment
   - Added `get_portkey_api_key()` - Portkey API key management
   - Added `get_portkey_virtual_key()` - Portkey virtual key for OpenAI
   - Added `get_portkey_base_url()` - Portkey endpoint configuration
   - Added `get_llm_client_config()` - Unified client configuration

2. **`podcast/outline.py`** - Dynamic client initialization
   - Now uses `get_llm_client_config()` for flexible provider support
   - Model name now configurable via `get_llm_model()`

3. **`podcast/transcript.py`** - Dynamic client initialization
   - Now uses `get_llm_client_config()` for flexible provider support
   - Model name now configurable via `get_llm_model()`

4. **`qwen_tts_ui.py`** - Updated Whisper transcription
   - Whisper audio transcription now uses `get_llm_client_config()`

5. **`.env.example`** - Configuration template
   - Comprehensive documentation for both OpenAI and Portkey setup
   - Example configurations and setup instructions

## Quick Start

### Using OpenAI (Default)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your OpenAI API key:
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

3. Run the application as usual.

### Using Portkey

1. Sign up at [Portkey](https://app.portkey.ai/)

2. Create a virtual key for OpenAI in the Portkey dashboard:
   - Go to Virtual Keys section
   - Create a new virtual key
   - Select OpenAI as the provider
   - Add your OpenAI API key

3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your Portkey credentials:
   ```bash
   LLM_PROVIDER=portkey
   PORTKEY_API_KEY=sk-portkey-your-key-here
   PORTKEY_VIRTUAL_KEY=openai-virtual-your-key-here
   ```

5. Run the application - all LLM requests will now route through Portkey!

## Configuration Options

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | No | `openai` | Provider to use: `openai` or `portkey` |
| `LLM_MODEL` | No | `gpt-5.2` | Model name to use for completions |
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key (*required when using OpenAI) |
| `PORTKEY_API_KEY` | Yes** | - | Portkey API key (**required when using Portkey) |
| `PORTKEY_VIRTUAL_KEY` | Yes** | - | Portkey virtual key for OpenAI (**required when using Portkey) |
| `PORTKEY_BASE_URL` | No | `https://api.portkey.ai/v1` | Portkey API endpoint |

## Benefits of Using Portkey

### Observability
- Track all LLM requests in real-time
- Monitor token usage, costs, and latency
- View detailed request/response logs
- Analyze usage patterns and trends

### Caching
- Semantic caching to reduce costs
- Faster response times for similar requests
- Configurable cache TTL

### Reliability
- Automatic fallbacks to alternative providers
- Load balancing across multiple endpoints
- Retry logic with exponential backoff
- Circuit breaker patterns

### Cost Management
- Set rate limits per user/team
- Budget alerts and controls
- Cost attribution and tracking
- Detailed cost analytics

### Prompt Management
- Version control for prompts
- A/B testing capabilities
- Centralized prompt library
- Template management

## Technical Details

### How It Works

The integration uses the standard OpenAI Python SDK but configures it differently based on the provider:

**For OpenAI:**
```python
client = OpenAI(api_key="sk-proj-...")
```

**For Portkey:**
```python
client = OpenAI(
    api_key="sk-portkey-...",
    base_url="https://api.portkey.ai/v1",
    default_headers={
        "x-portkey-api-key": "sk-portkey-...",
        "x-portkey-virtual-key": "openai-virtual-...",
        "x-portkey-provider": "openai"
    }
)
```

### Backward Compatibility

All changes are **100% backward compatible**:
- Existing `.env` files with `OPENAI_API_KEY` continue to work
- Default provider is `openai` if not specified
- No code changes required for existing deployments
- All existing functionality preserved

### Type Safety

The implementation maintains type safety through Python Protocols:
- Client initialization is type-checked
- Configuration returns properly typed dictionaries
- No runtime type errors

## Troubleshooting

### "OPENAI_API_KEY not found in environment"
- Make sure you have a `.env` file in the project root
- Verify `OPENAI_API_KEY` is set in `.env`
- Check that `LLM_PROVIDER=openai` (or not set, as it's the default)

### "PORTKEY_API_KEY not found in environment"
- Verify `LLM_PROVIDER=portkey` is set
- Ensure `PORTKEY_API_KEY` is set in `.env`
- Ensure `PORTKEY_VIRTUAL_KEY` is set in `.env`

### "Unknown LLM provider"
- Check that `LLM_PROVIDER` is either `openai` or `portkey`
- Variable names are case-insensitive but values are case-sensitive

### Requests failing with Portkey
- Verify your Portkey API key is valid
- Ensure your virtual key is correctly configured in Portkey dashboard
- Check that your virtual key has OpenAI credentials configured
- Review Portkey dashboard for error logs

## Testing

You can test the configuration without running the full application:

```python
# Test OpenAI configuration
from config import get_llm_provider, get_llm_client_config
print(f"Provider: {get_llm_provider()}")
print(f"Config: {get_llm_client_config()}")
```

## Migration Checklist

If you're migrating from OpenAI to Portkey:

- [ ] Sign up for Portkey account
- [ ] Create virtual key for OpenAI in Portkey dashboard
- [ ] Add OpenAI API key to virtual key configuration
- [ ] Copy Portkey API key
- [ ] Copy virtual key identifier
- [ ] Update `.env` with Portkey credentials
- [ ] Set `LLM_PROVIDER=portkey`
- [ ] Test outline generation
- [ ] Test transcript generation
- [ ] Test Whisper transcription
- [ ] Verify requests appear in Portkey dashboard
- [ ] Check token usage and costs in Portkey

## Support

For issues related to:
- **Qwen3-TTS Studio**: Open an issue in this repository
- **Portkey**: Visit [Portkey Documentation](https://docs.portkey.ai/) or contact Portkey support
- **OpenAI API**: Visit [OpenAI Platform](https://platform.openai.com/)

## Additional Resources

- [Portkey Documentation](https://docs.portkey.ai/)
- [Portkey Dashboard](https://app.portkey.ai/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Portkey Virtual Keys Guide](https://docs.portkey.ai/docs/product/ai-gateway/virtual-keys)
