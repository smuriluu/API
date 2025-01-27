import logging
import os

print(os.path.join(os.getcwd(), 'api.log'))
# Configure the logging settings
logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'log/api.log'),
    level=logging.INFO,
    format="%(asctime)s: %(message)s"
)