from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

# Database configuration
DATABASE_URL = config("DATABASE_URL", cast=Secret)

# Gmail configuration
GMAIL_SMTP_SERVER = config("GMAIL_SMTP_SERVER", default="smtp.gmail.com", cast=str)
GMAIL_SMTP_PORT = config("GMAIL_SMTP_PORT", default=587, cast=int)
GMAIL_USERNAME = config("GMAIL_USERNAME", cast=str)
GMAIL_PASSWORD = config("GMAIL_PASSWORD", cast=Secret)

# Kafka configuration
KAFKA_PRODUCT_TOPIC = config("KAFKA_PRODUCT_TOPIC", cast=str)
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT", cast=str)

# Test database configuration
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

# OpenAI API key
OPENAI_API_KEY = config("OPENAI_API_KEY", cast=Secret)
