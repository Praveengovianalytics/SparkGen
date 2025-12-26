<img src="https://github.com/user-attachments/assets/d442f52b-4c3d-4d50-99df-1bdf130e018d" alt="Image Description" width="800">


[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/Praveengovianalytics/SparkGen)](https://github.com/Praveengovianalytics/SparkGen/issues)
[![GitHub release](https://img.shields.io/github/release/Praveengovianalytics/SparkGen)](https://github.com/Praveengovianalytics/SparkGen/releases)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/Praveengovianalytics/SparkGen/releases)
</a>
<a href="https://www.python.org/">
<img alt="Build" src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg?color=green">
</a>

<h4 align="center">
    <p>
        <a href="#shield-installation">Installation</a> |
        <a href="#fire-quickstart">Quickstart</a> |
    <p>
</h4>

---
## ⚛ Introduction
SparkGen✨  is an open-source GenAI accelerator template designed to streamline the creation of Generative AI projects. It provides a comprehensive and modular project structure that integrates best practices in software development, deployment, and responsible AI considerations.

Whether you're building a conversational agent, multi-model agent, AI-powered application, or experimenting with large language models, this template provides a solid foundation to accelerate your development process.

# Story of SparkGen 🎸✨

## How SparkGen Was Created

*The story of **SparkGen** began in Bangkok, during a recent business trip that led me to the vibrant **Hard Rock Cafe**. Amidst the electrifying music and creative energy, I reflected on how small sparks of inspiration can create extraordinary compositions—whether in music or technology.*
*Sitting in that dynamic atmosphere, it struck me: what if we had a "hard rock" foundation for Generative AI? A toolkit designed to ignite innovation and help teams seamlessly create impactful AI solutions. By the end of the night, the name **SparkGen** was developed—a fusion of creativity, simplicity, and the generative power of AI.*
*SparkGen is built to inspire, accelerate, and empower AI creators to turn ideas into reality. Just like music brings people together to create something extraordinary, SparkGen helps you compose your own AI ideas to reality.*

---
## :fire: Quickstart

### 🔍 Prerequisites
- Python 3.9+
- Cookiecutter: For generating projects from templates.
- Poetry: For dependency management.
- Git
- Docker (optional): For containerization.
- Kubernetes (optional): For orchestration.

## :shield: Installation

**Install Cookiecutter**
```bash
pip install cookiecutter
```

**Install Poetry**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### ⚙️ Generating a New Project

Generate a new project using the Multiagentic Cookiecutter template:
```bash
cookiecutter https://github.com/Praveengovianalytics/SparkGen.git
```
You will be prompted to enter various details:
- `project_name`: The name of your new project.
- `project_slug`: [Automatically generated based on `project_name`]
- `author_name`: Your name.
- `description`: A short description of your project.
- `version`: Initial version number.
- `open_source_license`: Choose a license.
- `ci_cd_tool`: Choose a CI/CD tool (e.g., GitHub Actions).
- `deployment_platform`: Choose a deployment platform (e.g., Docker, Kubernetes).
- `multi_agent_mode`: Choose between router-manager, planner-builder, or single-agent.
- `api_framework`: Pick FastAPI to bootstrap an API surface or None for CLI-first.
- `observability`: Choose Logging only or OpenTelemetry-ready wiring.
- `openai_agent_sdk`: Enable to scaffold OpenAI Agents SDK usage (router and planner flows can delegate to Agents).
- MCP connectivity and A2A protocol scaffolds are included to accelerate
  multi-agent interoperability and context sharing out of the box.

If you select **FastAPI**, the generated project includes `api/app.py` with
`/health` and `/agent/invoke` endpoints; run with:
```bash
uvicorn {{cookiecutter.project_slug}}.api.app:app --reload
```

### 🧭 Usage Steps
1. **Generate** a project with Cookiecutter.
2. **Install deps** inside the generated folder:
   ```bash
   cd your_project_slug
   poetry install
   ```
3. **Run CLI entrypoint** (single-agent by default):
   ```bash
   poetry run python your_project_slug/main.py
   ```
4. **Run FastAPI service** (if selected):
   ```bash
   uvicorn your_project_slug.api.app:app --reload
   ```
5. **Call the API**:
   ```bash
   curl -X POST http://localhost:8000/agent/invoke -H "Content-Type: application/json" -d '{"query":"hello","pattern":"single-agent"}'
   ```
6. **Switch orchestration patterns** by changing `pattern` (e.g., `router-manager`, `sequential`, `planner-executor`, `hierarchical`, `broadcast-reduce`, `critic-review`, `tool-first`).

---

## 🔬 Table of Contents
- [✨ Features](#features)
- [🏃‍♂️ Quickstart](#quickstart)
  - [🔍 Prerequisites](#prerequisites)
  - [📝 Installation](#installation)
  - [⚙️ Generating a New Project](#generating-a-new-project)
- [🔮 Project Structure](#project-structure)
  - [🕹️ Key Directories and Files](#key-directories-and-files)
- [🌐 Usage](#usage)
  - [🚀 Running the Application](#running-the-application)
- [🔄 Examples](#examples)
- [🚨 Development](#development)
  - [🔧 Testing](#testing)
  - [♻️ Continuous Integration](#continuous-integration)
- [🚧 Deployment](#deployment)
  - [🛠️ Docker Deployment](#docker-deployment)
  - [🚀 Kubernetes Deployment](#kubernetes-deployment)
- [👁‍□️ Responsible AI Practices](#responsible-ai-practices)
- [📊 Contributing](#contributing)
- [🌐 License](#license)
- [📞 Contact](#contact)
- [🔗 Acknowledgments](#acknowledgments)
- [🔍 Frequently Asked Questions](#frequently-asked-questions)
- [⌛ Change Log](#change-log)

---

## ✨ Features
- **Modular Project Structure**: Organized directories and modules for scalability and maintainability.
- **LLM Integration**: Seamless integration with Large Language Models (LLMs) like OpenAI GPT.
- **Prompt Engineering**: Template-based prompt management using Jinja2.
- **Embeddings Support**: Efficient handling of embeddings for semantic similarity.
- **Vector Databases**: Integration with vector databases for storing and retrieving embeddings.
- **Custom Tools and Utilities**: Extendable tools for specific tasks.
- **Memory Management**: Contextual memory for conversational agents.
- **Callbacks and Telemetry**: Hooks and monitoring for various stages of processing.
- **CI/CD Integration**: Ready-to-use GitHub Actions workflows for continuous integration and deployment.
- **Responsible AI Modules**: Components for bias detection, privacy preservation, and explainability.
- **Docker and Kubernetes Support**: Containerization and orchestration for scalable deployments.
- **Poetry for Dependency Management**: Simplified dependency management and virtual environment handling.

---

## 🔮 Project Structure

The cookiecutter generates a single, production-ready layout with clear separation between orchestration, interfaces, and infrastructure. Optional components (e.g., FastAPI, Kubernetes) appear only when selected during project generation.

```plaintext
your_project_slug/
├── your_project_slug/
│   ├── agents/
│   ├── prompt/
│   ├── llms/
│   ├── tools/
│   ├── memory/
│   ├── callbacks/
│   ├── utils/
│   ├── telemetry/
│   ├── config/
│   ├── data_loaders/
│   ├── retrievers/
│   ├── embeddings/
│   ├── vectordatabase/
│   ├── orchestration/
│   ├── guardrails/
│   ├── protocols/
│   ├── connectors/
│   ├── __init__.py
│   └── main.py
├── api/                     # FastAPI surface (if selected)
├── ResponsibleAI/
├── docs/
├── notebooks/
├── tests/
├── ci_cd/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── deployment/
│       ├── kubernetes.yml
│       └── helm-chart/
├── .github/
│   └── workflows/
├── logs/
├── pyproject.toml
├── poetry.lock
├── LICENSE
├── README.md
├── Makefile
└── .gitignore
```

### 🕹️ Key Directories and Files
- **`your_project_slug/agents/`**: Agent definitions and orchestration flows.
- **`your_project_slug/prompt/`**: Prompt templates and Jinja2 assets.
- **`your_project_slug/tools/`**: Tool specs/functions for external actions.
- **`your_project_slug/memory/`**: State and memory abstractions.
- **`your_project_slug/telemetry/`**: Logging, tracing, and monitoring hooks.
- **`your_project_slug/orchestration/`**: Coordination patterns (planner, router, sequential, etc.).
- **`your_project_slug/guardrails/`**: Safety and policy enforcement utilities.
- **`your_project_slug/protocols/`**: Agent-to-agent or service communication protocols.
- **`your_project_slug/connectors/`**: Integrations such as MCP client stubs.
- **`your_project_slug/data_loaders/`, `retrievers/`, `embeddings/`, `vectordatabase/`**: Data ingestion and retrieval building blocks.
- **`your_project_slug/main.py`**: CLI entrypoint for running the selected orchestration mode.
- **`api/`**: FastAPI surface for `/health` and `/agent/invoke` (generated when FastAPI is chosen).
- **`ResponsibleAI/`**: Bias detection, privacy preservation, and explainability modules.
- **`ci_cd/`**: Docker, Compose, and Kubernetes deployment scaffolds.
- **`tests/`**: Unit and integration tests for agents, protocols, and tools.
- **`docs/` & `notebooks/`**: Extended documentation and runnable examples.

---

## 🌐 Usage

### 🚀 Running the Application

Navigate to the project directory:
```bash
cd your_project_slug
```

Install dependencies using Poetry:
```bash
poetry install
```

Activate the virtual environment:
```bash
poetry shell
```

Run the application:
```bash
poetry run python your_project_slug/main.py
```

---

## 🔄 Examples
- **Jupyter Notebooks**: Explore the `notebooks/` directory for example notebooks demonstrating usage of different components.
- **Command-Line Arguments**: Modify `main.py` to accept command-line arguments for different modes or functionalities.

---

## 🚨 Development

### 🔧 Testing
Run tests using Pytest:
```bash
poetry run pytest tests/
```
Ensure that you have adequate test coverage for all modules.

### ♻️ Continuous Integration
- **GitHub Actions**: The template includes CI workflows for automated testing and deployment.
- **Code Quality**: Integrate tools like `flake8`, `black`, and `isort` for code linting and formatting.

---

## 🚧 Deployment

### 🛠️ Docker Deployment
Build and run the Docker image:
```bash
docker build -t your_project_slug .
docker run -p 8000:8000 your_project_slug
```

### 🚀 Kubernetes Deployment
Apply the Kubernetes manifest:
```bash
kubectl apply -f ci_cd/deployment/kubernetes.yml
```

---

## 👁‍□️ Responsible AI Practices
We are committed to building AI responsibly:

- **Bias Detection**: Implemented in `ResponsibleAI/bias_detection.py`.
  - Regularly audits model outputs for fairness.
- **Privacy Preservation**: Data anonymization techniques in `ResponsibleAI/privacy_preservation.py`.
  - Compliance with data protection regulations.
- **Explainability**: Model interpretability methods in `ResponsibleAI/explainability.py`.
  - Use of SHAP values for feature importance.

For more details, refer to `docs/responsible_ai.md`.

---

## 📊 Contributing

### 🌈 How to Contribute
1. **Fork the Repository.**
2. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit Your Changes:**
   ```bash
   git commit -m "Add YourFeature"
   ```
4. **Push to the Branch:**
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request.**

### 🔜 Code of Conduct
Please read our Code of Conduct before contributing.

---

## 🌐 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 📞 Contact
- **Author**: Praveen Govindaraj   
- **Email**: praveengovi@gmail.com
- **GitHub**: [link](https://github.com/Praveengovianalytics)
- **Project Repository**: [SparkGen](https://github.com/Praveengovianalytics/SparkGen)

---

## 🔗 Acknowledgments
- **Contributors**: Thanks to all the contributors who have helped improve this project.
- **Libraries and Tools**: This project leverages open-source libraries like Cookiecutter, Poetry, OpenAI API, Jinja2, and others.

---

## 🔍 Frequently Asked Questions
1. **How do I change the LLM model used?**
   - Configure the LLM model in `config/config_loader.py` or set it via environment variables.
2. **Can I use this project for commercial purposes?**
   - Yes, this project is licensed under the MIT License, which allows commercial use. Refer to the `LICENSE` file for details.
3. **How do I report bugs or request features?**
   - Open an issue on the [GitHub Issues](https://github.com/Praveengovianalytics/SparkGen/issues) page.
4. **How can I extend the template to suit my needs?**
   - Modify the template files in the generated project or customize the Cookiecutter template itself by forking the repository.

---

## ⌛ Change Log

To be Updated

---

By using SparkGen ✨, you're accelerating your Gen AI development with a solid foundation and best practices. 🚀 Happy coding!
