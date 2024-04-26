import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set default log level to DEBUG

# Create a handler that outputs log messages to standard error
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)  # Set handler level

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set formatter for handler
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
