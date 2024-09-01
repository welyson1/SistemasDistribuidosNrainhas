# logger.py
import os
import json
import logging
from datetime import datetime

class NQueensLogger:
    def __init__(self):
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"nqueens_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(message)s')

    def log_result(self, n, solver_type, solutions, time):
        log_entry = {
            "n": n,
            "solver_type": solver_type,
            "num_solutions": len(solutions),
            "time": time,
            "solutions": solutions
        }
        logging.info(json.dumps(log_entry))

    def get_latest_log_file(self):
        return max([os.path.join(self.log_dir, f) for f in os.listdir(self.log_dir)], key=os.path.getctime)