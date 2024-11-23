![image](https://github.com/user-attachments/assets/d442f52b-4c3d-4d50-99df-1bdf130e018d)


# SparkGen ✨
A GenAI Cookiecutter template for rapidly creating robust, scalable, and modular Generative AI projects with best practices in mind.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/Praveengovianalytics/SparkGen)](https://github.com/Praveengovianalytics/SparkGen/issues)
[![GitHub release](https://img.shields.io/github/release/Praveengovianalytics/SparkGen)](https://github.com/Praveengovianalytics/SparkGen/releases)
<a href="https://colab.research.google.com/drive/1h9E0Q5Fema9TkOiv0asyaSaHin1R0UN5?usp=sharing">
<img alt="Open In Colab" src="https://colab.research.google.com/assets/colab-badge.svg">
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
SparkGen✨  is an open-source GenAI Cookiecutter template designed to streamline the creation of Generative AI projects. It provides a comprehensive and modular project structure that integrates best practices in software development, deployment, and responsible AI considerations.

Whether you're building a conversational agent, multi-model agent, AI-powered application, or experimenting with large language models, this template provides a solid foundation to accelerate your development process.

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

Generate a new project using the GenAI Cookiecutter template:
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

The generated project will have the following structure:
```plaintext
your_project_slug/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── notebooks/
├── docs/
│   └── responsible_ai.md
├── ResponsibleAI/
│   ├── bias_detection.py
│   ├── privacy_preservation.py
│   └── explainability.py
├── your_project_slug/
│   ├── agents/
│   ├── prompt/
│   ├── llms/
│   ├── embeddings/
│   ├── vectordatabase/
│   ├── tools/
│   ├── memory/
│   ├── callbacks/
│   ├── utils/
│   ├── telemetry/
│   ├── config/
│   ├── data_loaders/
│   ├── retrievers/
│   ├── reranker/
│   ├── __init__.py
│   └── main.py
├── ci_cd/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── deployment/
│       ├── kubernetes.yml
│       └── helm-chart/
├── logs/
├── tests/
├── .gitignore
├── LICENSE
├── README.md
├── Makefile
├── pyproject.toml
├── poetry.lock
```

### 🕹️ Key Directories and Files
- **`agents/`**: Contains agent logic and orchestration.
- **`prompt/`**: Manages prompt engineering and templates.
- **`llms/`**: Integration with Large Language Models.
- **`embeddings/`**: Handling of embedding generation.
- **`vectordatabase/`**: Operations related to vector databases.
- **`tools/`**: Custom tools for tasks like web scraping.
- **`memory/`**: Memory management for agent context.
- **`callbacks/`**: Custom callbacks for various processes.
- **`utils/`**: Utility functions used across the project.
- **`telemetry/`**: Monitoring and logging functionalities.
- **`config/`**: Configuration files and loaders.
- **`data_loaders/`**: Scripts for data loading and preprocessing.
- **`retrievers/`**: Logic for data retrieval.
- **`reranker/`**: Algorithms for reranking retrieved results.
- **`main.py`**: The main entry point for running the project.
- **`tests/`**: Contains unit and integration tests.
- **`ci_cd/`**: CI/CD configurations and deployment scripts.
- **`ResponsibleAI/`**: Modules focusing on Responsible AI practices.

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
- **Project Repository**: [GenAI Cookiecutter](https://github.com/Praveengovianalytics/SparkGen)

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
   - Open an issue on the [GitHub Issues](https://github.com/yourusername/genai-cookiecutter/issues) page.
4. **How can I extend the template to suit my needs?**
   - Modify the template files in the generated project or customize the Cookiecutter template itself by forking the repository.

---

## ⌛ Change Log
See the `CHANGELOG.md` file for details on version changes.

---

By using SparkGen ✨, you're accelerating your Gen AI development with a solid foundation and best practices. 🚀 Happy coding!
