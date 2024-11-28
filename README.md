### Files in the Repository

Here is a list of all the files that should be included in the repository to ensure the project functions as intended:

---

#### **1. Python Script Files**
- `main.py`  
  - The primary script that initializes and runs the multi-agent system.

- `agent.py`  
  - Defines the `FileAgent` class and its methods.

- `multi_agent_manager.py`  
  - Handles the `MultiAgentFileReader` class and agent setup.

#### **2. Configuration and Patterns**
- `config.json`  
  - Configuration file specifying agent settings, patterns, and file limits.  
  Example:
  ```json
  [
      {
          "name": "EmailFinder",
          "search_pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
          "file_limit": 5
      },
      {
          "name": "UsernameFinder",
          "search_pattern": "\\buser[a-zA-Z0-9._-]+\\b",
          "file_limit": 5
      }
  ]
  ```

#### **3. Directory Structure**
- `input_files/`  
  - Directory containing files for processing.

- `output/`  
  - Directory where results, logs, and reports are stored.

#### **4. Additional Assets**
- `requirements.txt`  
  - Dependencies for the project (if any; currently, the standard library is sufficient).

- `.gitignore`  
  - Prevents unnecessary files (e.g., `__pycache__/`, `*.log`, `*.json`) from being added to the repository.

- `README.md`  
  - Documentation file for the repository (see below for content).

---

### README.md

```markdown
# Multi-Agent File Searcher

A Python-based multi-agent system that processes files to search for specific patterns and stores results in an organized manner. Each agent operates independently to maximize efficiency, with progress visually displayed in the CLI.

---

## Features

- **Multi-Agent System:** Each agent can process files with its own search pattern and limitations.
- **Detailed Logging:** Each agent maintains logs of its activities.
- **Final Report:** A summary of findings and logs for each agent is generated upon completion.
- **Progress Visualization:** Stunning loading bars for each agent showing current progress and line being processed.

---

## Requirements

This project only uses Python's standard library, so no additional dependencies are needed. Ensure Python 3.8+ is installed.

---

## File Structure

- **`main.py`**: The entry point of the program.
- **`agent.py`**: Defines the `FileAgent` class.
- **`multi_agent_manager.py`**: Manages multiple agents.
- **`config.json`**: Contains agent configurations (search patterns and file limits).
- **`input_files/`**: Directory for input files.
- **`output/`**: Directory for results, logs, and reports.

---

## Usage

1. **Setup Input Directory:**  
   Place files to be processed in the `input_files/` directory.

2. **Edit Configuration (Optional):**  
   Modify `config.json` to define agents, patterns, and file limits.

3. **Run the Program:**  
   Run the script using:
   ```bash
   python main.py
   ```

4. **View Output:**  
   Results, logs, and reports will be generated in the `output/` directory.

---

## Example Configuration

Below is an example of the `config.json` file:
```json
[
    {
        "name": "EmailFinder",
        "search_pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
        "file_limit": 5
    },
    {
        "name": "UsernameFinder",
        "search_pattern": "\\buser[a-zA-Z0-9._-]+\\b",
        "file_limit": 5
    }
]
```

---

## Customization

- **Adding Agents:** Add new configurations to the `config.json` file.
- **Search Patterns:** Use regular expressions to define new search patterns.

---

## License

This project is open source and available under the [MIT License](LICENSE).

```

This structure and README ensure the repository is well-documented and easy to use. Let me know if you need additional features or changes!
