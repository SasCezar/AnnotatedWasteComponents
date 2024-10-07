<p align="center">
  <h1 align="center">WasteAnnotator: Automated Component Annotation Pipeline</h1>
</p>

## Table of Contents

- [About the Project](#about-the-project)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
    - [Running the Pipeline](#running-the-pipeline)
    - [Configuration](#configuration)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## About the Project

WasteAnnotator is an automated pipeline designed to extract and annotate components from abandoned GitHub projects. By
analyzing the project's dependency graph, the tool identifies components and labels them based on the files they
contain. The final output is a structured file detailing the components and their associated files, providing a
comprehensive view of the project's architecture.

---

## Architecture Overview

The WasteAnnotator tool consists of several key modules:

- **Finder**: Retrieves projects from a repository service (currently GitHub only) based on specified criteria.
- **GraphExtractor**: Parses the project's dependency graph to identify potential components (currently uses [Arcan](https://www.arcan.tech/)).
- **Annotator**: Uses semantic techniques to label and annotate components based on their file contents (currently uses
  [AutoFL](https://github.com/SasCezar/autofl)).
- **CommunityExtractor**: Identifies communities within the component structure for further insights (via customizable
  algorithms from [cdlib](https://cdlib.readthedocs.io/en/latest/)).
- **Exporter**: Outputs the processed information in configurable formats (e.g., JSON).

Configurations for each module are defined in YAML files located in the `config` folder, allowing for easy customization
of behavior and parameters.
For each module new classes can be added by extending the base classes in the directory.
---

## Getting Started

### Prerequisites

- [Docker v4.25](https://www.docker.com/get-started) or higher for containerization.
- [Git](https://git-scm.com/) for repository cloning.
- (Optional) [Python 3.10](https://www.python.org/downloads/) if running the application outside of Docker.

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/WasteAnnotator.git
   cd WasteAnnotator
   ```

2. **Set Up Environment Variables**
    - (Optional) Create a `.env` file in the project root to define any necessary environment variables (e.g., GitHub
      tokens, paths).

3. **Build and Start Services with Docker**
   ```bash
   docker compose up --build
   ```

This will initialize all required services and set up the necessary environment for running the WasteAnnotator pipeline.

---

## Usage

### Running the Pipeline

The main entry point for the WasteAnnotator pipeline is `src/main.py`. The pipeline can be executed either using Docker
or directly via Python.

#### Using Docker

1. **Ensure Services are Running**
   ```bash
   docker compose up
   ```

2. **Run the Main Pipeline**
    - The default service automatically runs `main.py` within the Docker container, which initiates the component
      extraction and annotation process.

#### Running Locally (Without Docker)

1. **Install Dependencies with Poetry**
    ```bash
    poetry install
    ```

2. **Activate the Poetry Environment**
   ```bash
   poetry shell
   ```

3. **Execute the Script**
   ```bash
   python src/main.py
   ```

### Configuration

Configuration files are located in the `config` directory, which contains settings for different modules (e.g.,
`annotator`, `community`, `exporter`). Each YAML file can be customized to alter the behavior of the pipeline
components:

- `config/main.yaml`: The primary configuration file, referencing all module-specific settings.
- Module-specific YAML files: Adjust parameters for finer control, such as `finder/github_archived_java.yaml` to change
  GitHub project retrieval criteria.

The pipeline uses [Hydra](https://hydra.cc/) for configuration management, allowing runtime configuration overrides. For
example:

```bash
python src/main.py finder=custom_finder.yaml graphextractor=arcan.yaml
```

---

## Contributing

Contributions are welcome! Please fork the repository and use a feature branch to work on your changes. When ready,
submit a pull request for review.

---

## License

This repository was previously licensed under the MIT License. However, it includes code that is licensed under the GNU
General Public License (GPL). As a result, the entire project is now licensed under the GPL 3. All previous and future
versions must comply with this license.

---

Thank you for using and contributing to WasteAnnotator! If you have any questions or need support, please open an issue
or contact the maintainers.
