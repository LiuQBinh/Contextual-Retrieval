"""
Configuration file for LM Studio settings
Tập trung tất cả cấu hình LM Studio vào một nơi
"""

# Host
# HOST = "localhost"
HOST = "192.168.1.24"

# Port
# PORT = 1234
PORT = 2223

# URL LM Studio
LM_STUDIO_URL = f"""http://{HOST}:{PORT}/v1"""

# URL API
API_URL = f"""{LM_STUDIO_URL}/chat/completions"""

# LM Studio Server Configuration
LM_STUDIO_CONFIG = {
    "host": HOST,
    "port": PORT,
    "base_url": LM_STUDIO_URL,
    "timeout": 120,
    "model": "openai/gpt-oss-20b",
    "temperature": 0.1,
    "max_tokens": 2000,
    "stream": False
}

# API Endpoints
ENDPOINTS = {
    "chat_completions": "/chat/completions"
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "log_file": "agentic_chunking.log"
}

# Chunking Configuration
CHUNKING_CONFIG = {
    "max_chars_per_chunk": 4000,
    "output_dir": "agentic_chunking/output"
}

def get_lm_studio_url() -> str:
    """Get full LM Studio API URL"""
    return f"http://{LM_STUDIO_CONFIG['host']}:{LM_STUDIO_CONFIG['port']}/v1"

def get_api_endpoint(endpoint_name: str) -> str:
    """Get full API endpoint URL"""
    base = get_lm_studio_url()
    endpoint = ENDPOINTS.get(endpoint_name, "")
    return f"{base}{endpoint}"
