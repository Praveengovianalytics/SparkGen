#!/bin/bash

# This script sets up the directory structure for the genai-cookiecutter template

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

# Create the cookiecutter.json file at the root of the template
touch cookiecutter.json

# Create the root directory for the template using the Cookiecutter variable
mkdir -p "{{cookiecutter.project_slug}}"
cd "{{cookiecutter.project_slug}}"

# Create .github/workflows directory and CI/CD workflow files
mkdir -p .github/workflows
touch .github/workflows/ci.yml
touch .github/workflows/cd.yml

# Create notebooks directory
mkdir notebooks

# Create docs directory and responsible_ai.md
mkdir docs
touch docs/responsible_ai.md

# Create ResponsibleAI directory and files
mkdir ResponsibleAI
touch ResponsibleAI/bias_detection.py
touch ResponsibleAI/privacy_preservation.py
touch ResponsibleAI/explainability.py

# Create the inner project directory (this will be replaced with the actual project slug)
mkdir "{{cookiecutter.project_slug}}"
cd "{{cookiecutter.project_slug}}"

# Create subdirectories and their respective files
mkdir agents
touch agents/agent.py

mkdir prompt
touch prompt/prompt_template.py

mkdir llms
touch llms/base_llm.py

mkdir embeddings
touch embeddings/embedder.py

mkdir vectordatabase
touch vectordatabase/vector_store.py

mkdir tools
touch tools/tools.py

mkdir memory
touch memory/memory.py

mkdir callbacks
touch callbacks/callback_handler.py

mkdir utils
touch utils/utils.py

mkdir telemetry
touch telemetry/telemetry.py

mkdir config
touch config/config_loader.py

mkdir data_loaders
touch data_loaders/data_loader.py

mkdir retrievers
touch retrievers/retriever.py

mkdir reranker
touch reranker/reranker.py

# Create the __init__.py and main.py files
touch __init__.py
touch main.py

# Navigate back to the outer project directory
cd ..

# Create ci_cd directory and its subdirectories and files
mkdir -p ci_cd/deployment/helm-chart
mkdir -p ci_cd/bamboo
touch ci_cd/Dockerfile
touch ci_cd/docker-compose.yml
touch ci_cd/deployment/kubernetes.yml
touch ci_cd/bamboo/bamboo-spec.yaml
touch ci_cd/bamboo/push_eventhub_logs.py

# Create logs and tests directories, and test_sample.py
mkdir logs
mkdir tests
touch tests/test_sample.py

# Create other files at the project root
touch .gitignore
touch LICENSE
touch README.md
touch Makefile
touch pyproject.toml
touch poetry.lock
