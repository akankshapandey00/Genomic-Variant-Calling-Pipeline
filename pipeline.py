#!/usr/bin/env python3
import subprocess
import logging
import datetime
import sys

def main():
    # Setup logging
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"pipeline_{timestamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )

    scripts = [
        "getGenome.sh",
        "getReads.sh",
        "trimReads.sh",
        "indexGenome.sh",
        "alignReads.sh",
        "sort.sh",
        "indexReads.sh",
        "runDeepVariant.sh"
    ]

    logging.info("=== Starting variant-calling pipeline ===")
    for script in scripts:
        logging.info(f"▶ Running {script}")
        try:
            subprocess.run(["bash", script], check=True)
            logging.info(f"✔ {script} completed successfully")
        except subprocess.CalledProcessError as e:
            logging.error(f"✖ {script} failed (exit {e.returncode})")
            logging.error("Pipeline aborted.")
            sys.exit(e.returncode)

    logging.info("✅ All steps finished without errors.")
    logging.info(f"Log saved to {log_filename}")

if __name__ == "__main__":
    main()
