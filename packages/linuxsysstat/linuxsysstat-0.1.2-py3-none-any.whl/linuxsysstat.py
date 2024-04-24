#!/usr/bin/env python3

import psutil
import logging
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_linux_distribution():
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME'):
                    return line.split('=')[1].strip().strip('"')
    except Exception as e:
        logger.error(f"Error reading distribution information: {e}")
        sys.exit(1)

def main():
    # Check if the system is Linux
    if sys.platform != 'linux':
        logger.error("This script is only supported on Linux systems.")
        sys.exit(1)

    # Get Linux distribution name
    distribution = get_linux_distribution()
    logger.info(f"Linux Distribution: {distribution}")

    # Get free memory
    memory = psutil.virtual_memory().free / (1024 * 1024)
    logger.info(f"Free Memory: {memory:.2f} MB")

    # Get number of CPUs
    num_cpus = psutil.cpu_count()
    logger.info(f"Number of CPUs: {num_cpus}")

if __name__ == "__main__":
    main ()


