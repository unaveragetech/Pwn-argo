import os
import re
import shutil
import threading
from datetime import datetime
import json
import sys
import time

class FileAgent:
    def __init__(self, name, search_pattern, output_dir, file_limit):
        self.name = name
        self.search_pattern = search_pattern
        self.output_dir = output_dir
        self.file_limit = file_limit
        self.processed_files = 0
        self.total_matches = 0
        self.working_dir = os.path.join(output_dir, self.name)
        self.results_file = os.path.join(self.working_dir, "results.json")
        self.logs_file = os.path.join(self.working_dir, "logs.txt")
        self.current_file_copy = None

        # Initialize the agent's working directory
        self._setup_working_directory()

    def _setup_working_directory(self):
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
        # Ensure the results and logs files are blank
        open(self.results_file, 'w').close()
        open(self.logs_file, 'w').close()

    def log(self, message):
        with open(self.logs_file, 'a') as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    def progress_bar(self, current, total, line_number, file_name):
        percent = (current / total) * 100
        bar = '#' * int(percent // 5) + '-' * (20 - int(percent // 5))
        sys.stdout.write(
            f"\r[{self.name}] Processing file: {file_name} | Line: {line_number} | Matches: {self.total_matches} | [{bar}] {percent:.2f}%"
        )
        sys.stdout.flush()

    def process_file(self, file_path):
        try:
            self.log(f"Starting to process file: {file_path}")
            # Copy the file to the agent's working directory
            self.current_file_copy = os.path.join(self.working_dir, os.path.basename(file_path))
            shutil.copy(file_path, self.current_file_copy)

            matches = []
            total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore'))

            # Read the file line by line
            with open(self.current_file_copy, 'r', encoding='utf-8', errors='ignore') as f:
                for line_number, line in enumerate(f, start=1):
                    self.progress_bar(line_number, total_lines, line_number, os.path.basename(file_path))
                    for match in re.finditer(self.search_pattern, line):
                        matches.append({
                            "line": line_number,
                            "content": match.group(),
                            "file": os.path.basename(file_path)
                        })
                        self.total_matches += 1
            sys.stdout.write("\n")  # Move to the next line after processing the file

            # Write matches to the results file
            if matches:
                with open(self.results_file, 'a') as results:
                    json.dump(matches, results, indent=4)
                self.log(f"Found {len(matches)} matches in {file_path}")
            else:
                self.log(f"No matches found in {file_path}")

        except Exception as e:
            self.log(f"Error processing file {file_path}: {e}")
        finally:
            # Cleanup: Delete the copied file
            if self.current_file_copy and os.path.exists(self.current_file_copy):
                os.remove(self.current_file_copy)
            self.log(f"Finished processing file: {file_path}")
            self.processed_files += 1

    def generate_final_report(self):
        report_file = os.path.join(self.working_dir, "final_report.txt")
        try:
            with open(report_file, 'w') as report:
                report.write(f"Agent Name: {self.name}\n")
                report.write(f"Search Pattern: {self.search_pattern}\n")
                report.write(f"Files Processed: {self.processed_files}\n")
                report.write(f"Total Matches: {self.total_matches}\n")
                report.write(f"Results File: {self.results_file}\n")
                report.write(f"Logs File: {self.logs_file}\n")
                report.write(f"Report Generated: {datetime.now()}\n")
            self.log("Final report generated.")
        except Exception as e:
            self.log(f"Error generating final report: {e}")

    def run(self, files):
        for file_path in files[:self.file_limit]:
            self.process_file(file_path)
        self.generate_final_report()

class MultiAgentFileReader:
    def __init__(self, input_dir, output_dir, agent_configs):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.agent_configs = agent_configs
        self.agents = []

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def setup_agents(self):
        for config in self.agent_configs:
            agent = FileAgent(
                name=config['name'],
                search_pattern=config['search_pattern'],
                output_dir=self.output_dir,
                file_limit=config['file_limit']
            )
            self.agents.append(agent)

    def get_files(self):
        files = []
        for root, _, filenames in os.walk(self.input_dir):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files

    def distribute_files(self, files):
        # Distribute files evenly among agents
        file_batches = [files[i::len(self.agents)] for i in range(len(self.agents))]
        return file_batches

    def run(self):
        self.setup_agents()
        files = self.get_files()
        file_batches = self.distribute_files(files)

        threads = []
        for agent, file_batch in zip(self.agents, file_batches):
            thread = threading.Thread(target=agent.run, args=(file_batch,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("All agents have completed their tasks.")

if __name__ == "__main__":
    # Example usage
    input_directory = "./input_files"  # Directory containing files to process
    output_directory = "./output"      # Directory to store agent outputs

    # Define agents and their configurations
    agent_configs = [
        {"name": "EmailFinder", "search_pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", "file_limit": 5},
        {"name": "UsernameFinder", "search_pattern": r"\\buser[a-zA-Z0-9._-]+\\b", "file_limit": 5}
    ]

    # Initialize and run the system
    system = MultiAgentFileReader(input_directory, output_directory, agent_configs)
    system.run()
