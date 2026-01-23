#!/usr/bin/env python3
"""
CI/CD Integration Script for update-readme skill

This script provides CI/CD pipeline templates and utilities for
automatically updating documentation in CI/CD workflows.

Usage:
    python ci_cd.py generate --platform=github-actions  # Generate CI config
    python ci_cd.py validate --config=.github/workflows/ci.yml  # Validate config
    python ci_cd.py run --job=docs-update  # Run CI job locally
"""

import os
import sys
import argparse
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import logger, run_command


class CICDManager:
    """Manage CI/CD integration for documentation updates"""
    
    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path or Path.cwd()
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
    def generate_config(self, platform: str, output_path: Optional[Path] = None) -> bool:
        """Generate CI/CD configuration for a specific platform"""
        try:
            template = self._get_template(platform)
            if not template:
                logger.error(f"Unsupported platform: {platform}")
                return False
            
            if output_path is None:
                output_path = self._get_default_output_path(platform)
            
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write configuration
            with open(output_path, 'w', encoding='utf-8') as f:
                if platform == 'github-actions':
                    yaml.dump(template, f, default_flow_style=False, allow_unicode=True)
                elif platform == 'gitlab-ci':
                    yaml.dump(template, f, default_flow_style=False, allow_unicode=True)
                elif platform == 'azure-pipelines':
                    f.write(json.dumps(template, indent=2))
                else:
                    f.write(template)
            
            logger.info(f"Generated {platform} configuration at {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate CI/CD config: {e}")
            return False
    
    def validate_config(self, config_path: Path) -> bool:
        """Validate CI/CD configuration"""
        try:
            if not config_path.exists():
                logger.error(f"Config file not found: {config_path}")
                return False
            
            # Detect platform from file path/extension
            platform = self._detect_platform(config_path)
            
            if platform == 'github-actions':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                return self._validate_github_actions(config)
                
            elif platform == 'gitlab-ci':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                return self._validate_gitlab_ci(config)
                
            elif platform == 'azure-pipelines':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return self._validate_azure_pipelines(config)
                
            else:
                logger.warning(f"Unknown platform for config: {config_path}")
                return True  # Don't fail for unknown platforms
            
        except Exception as e:
            logger.error(f"Failed to validate config: {e}")
            return False
    
    def run_job(self, job_name: str, config_path: Optional[Path] = None) -> int:
        """Run a CI/CD job locally"""
        try:
            if config_path is None:
                config_path = self._find_ci_config()
                if not config_path:
                    logger.error("No CI/CD configuration found")
                    return 1
            
            platform = self._detect_platform(config_path)
            
            if platform == 'github-actions':
                return self._run_github_actions_job(job_name, config_path)
            elif platform == 'gitlab-ci':
                return self._run_gitlab_ci_job(job_name, config_path)
            elif platform == 'azure-pipelines':
                return self._run_azure_pipelines_job(job_name, config_path)
            else:
                logger.error(f"Unsupported platform: {platform}")
                return 1
                
        except Exception as e:
            logger.error(f"Failed to run job: {e}")
            return 1
    
    def _get_template(self, platform: str) -> Any:
        """Get CI/CD template for platform"""
        templates = {
            'github-actions': self._get_github_actions_template(),
            'gitlab-ci': self._get_gitlab_ci_template(),
            'azure-pipelines': self._get_azure_pipelines_template(),
            'circleci': self._get_circleci_template(),
            'jenkins': self._get_jenkins_template(),
        }
        return templates.get(platform)
    
    def _get_default_output_path(self, platform: str) -> Path:
        """Get default output path for platform"""
        paths = {
            'github-actions': self.project_path / '.github' / 'workflows' / 'docs-ci.yml',
            'gitlab-ci': self.project_path / '.gitlab-ci.yml',
            'azure-pipelines': self.project_path / 'azure-pipelines.yml',
            'circleci': self.project_path / '.circleci' / 'config.yml',
            'jenkins': self.project_path / 'Jenkinsfile',
        }
        return paths.get(platform, self.project_path / f'{platform}-ci.yml')
    
    def _detect_platform(self, config_path: Path) -> str:
        """Detect CI/CD platform from config path"""
        path_str = str(config_path)
        
        if '.github/workflows' in path_str:
            return 'github-actions'
        elif path_str.endswith('.gitlab-ci.yml'):
            return 'gitlab-ci'
        elif 'azure-pipelines' in path_str or path_str.endswith('.azure-pipelines.yml'):
            return 'azure-pipelines'
        elif '.circleci' in path_str:
            return 'circleci'
        elif 'Jenkinsfile' in path_str:
            return 'jenkins'
        else:
            # Try to detect from content
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)
                
                if 'uses:' in content and 'actions/' in content:
                    return 'github-actions'
                elif 'image:' in content and 'script:' in content:
                    return 'gitlab-ci'
                elif 'stages:' in content and 'pool:' in content:
                    return 'azure-pipelines'
            except:
                pass
            
            return 'unknown'
    
    def _find_ci_config(self) -> Optional[Path]:
        """Find CI/CD configuration file"""
        possible_paths = [
            self.project_path / '.github' / 'workflows' / 'ci.yml',
            self.project_path / '.github' / 'workflows' / 'docs.yml',
            self.project_path / '.gitlab-ci.yml',
            self.project_path / 'azure-pipelines.yml',
            self.project_path / '.circleci' / 'config.yml',
            self.project_path / 'Jenkinsfile',
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def _get_github_actions_template(self) -> Dict[str, Any]:
        """Generate GitHub Actions template"""
        return {
            'name': 'Documentation CI',
            'on': {
                'push': {
                    'branches': ['main', 'master'],
                    'paths': ['**/*.md', '**/*.py', '**/*.js', '**/*.ts', 'package.json', 'pyproject.toml']
                },
                'pull_request': {
                    'branches': ['main', 'master']
                },
                'schedule': [
                    {'cron': '0 0 * * 0'}  # Weekly on Sunday
                ]
            },
            'jobs': {
                'docs-check': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {
                            'name': 'Checkout',
                            'uses': 'actions/checkout@v4',
                            'with': {
                                'fetch-depth': 0
                            }
                        },
                        {
                            'name': 'Setup Python',
                            'uses': 'actions/setup-python@v4',
                            'with': {
                                'python-version': '3.11'
                            }
                        },
                        {
                            'name': 'Install dependencies',
                            'run': 'pip install -r requirements.txt || pip install -e .'
                        },
                        {
                            'name': 'Check documentation freshness',
                            'run': 'python -m scripts.analyze_project --check-only'
                        },
                        {
                            'name': 'Generate documentation',
                            'run': 'python -m scripts.generate_readme --check'
                        },
                        {
                            'name': 'Validate documentation',
                            'run': 'python -m scripts.integration.ci_cd validate --config=.github/workflows/docs-ci.yml'
                        }
                    ]
                },
                'docs-update': {
                    'runs-on': 'ubuntu-latest',
                    'if': "github.event_name == 'push' && github.ref == 'refs/heads/main'",
                    'needs': 'docs-check',
                    'steps': [
                        {
                            'name': 'Checkout',
                            'uses': 'actions/checkout@v4',
                            'with': {
                                'token': '${{ secrets.GITHUB_TOKEN }}',
                                'fetch-depth': 0
                            }
                        },
                        {
                            'name': 'Setup Python',
                            'uses': 'actions/setup-python@v4'
                        },
                        {
                            'name': 'Update documentation',
                            'run': 'python -m scripts.generate_readme --force'
                        },
                        {
                            'name': 'Commit and push updates',
                            'run': '|' + '''
                                git config --local user.email "action@github.com"
                                git config --local user.name "GitHub Action"
                                git add README.md AGENTS.md || true
                                if git diff --cached --quiet; then
                                    echo "No documentation updates needed"
                                else
                                    git commit -m "docs: auto-update documentation [skip ci]"
                                    git push
                                fi
                            '''
                        }
                    ]
                }
            }
        }
    
    def _get_gitlab_ci_template(self) -> Dict[str, Any]:
        """Generate GitLab CI template"""
        return {
            'stages': ['test', 'deploy'],
            'variables': {
                'PYTHON_VERSION': '3.11'
            },
            'docs-test': {
                'stage': 'test',
                'image': 'python:$PYTHON_VERSION',
                'script': [
                    'pip install -r requirements.txt || pip install -e .',
                    'python -m scripts.analyze_project --check-only',
                    'python -m scripts.generate_readme --check'
                ],
                'artifacts': {
                    'when': 'always',
                    'paths': ['README.md', 'AGENTS.md'],
                    'reports': {
                        'junit': 'test-reports/*.xml'
                    }
                }
            },
            'docs-update': {
                'stage': 'deploy',
                'image': 'python:$PYTHON_VERSION',
                'script': [
                    'pip install -r requirements.txt',
                    'python -m scripts.generate_readme --force',
                    'git config --global user.email "gitlab@example.com"',
                    'git config --global user.name "GitLab CI"',
                    'git add README.md AGENTS.md || true',
                    'if git diff --cached --quiet; then',
                    '  echo "No documentation updates needed"',
                    'else',
                    '  git commit -m "docs: auto-update documentation [skip ci]"',
                    '  git push https://gitlab-ci-token:${CI_JOB_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git HEAD:${CI_COMMIT_BRANCH}',
                    'fi'
                ],
                'rules': [
                    {
                        'if': '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "master"',
                        'when': 'on_success'
                    }
                ]
            }
        }
    
    def _get_azure_pipelines_template(self) -> Dict[str, Any]:
        """Generate Azure Pipelines template"""
        return {
            'trigger': {
                'branches': {
                    'include': ['main', 'master']
                },
                'paths': {
                    'include': ['**/*.md', '**/*.py', '**/*.js', '**/*.ts']
                }
            },
            'schedules': [
                {
                    'cron': '0 0 * * 0',
                    'branches': {
                        'include': ['main', 'master']
                    },
                    'always': True
                }
            ],
            'pool': {
                'vmImage': 'ubuntu-latest'
            },
            'stages': [
                {
                    'stage': 'Test',
                    'jobs': [
                        {
                            'job': 'DocsCheck',
                            'steps': [
                                {
                                    'task': 'UsePythonVersion@0',
                                    'inputs': {
                                        'versionSpec': '3.11'
                                    }
                                },
                                {
                                    'script': 'pip install -r requirements.txt || pip install -e .',
                                    'displayName': 'Install dependencies'
                                },
                                {
                                    'script': 'python -m scripts.analyze_project --check-only',
                                    'displayName': 'Check documentation freshness'
                                },
                                {
                                    'script': 'python -m scripts.generate_readme --check',
                                    'displayName': 'Generate documentation'
                                }
                            ]
                        }
                    ]
                },
                {
                    'stage': 'Deploy',
                    'dependsOn': ['Test'],
                    'condition': "and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))",
                    'jobs': [
                        {
                            'job': 'DocsUpdate',
                            'steps': [
                                {
                                    'task': 'UsePythonVersion@0',
                                    'inputs': {
                                        'versionSpec': '3.11'
                                    }
                                },
                                {
                                    'script': 'python -m scripts.generate_readme --force',
                                    'displayName': 'Update documentation'
                                },
                                {
                                    'script': '|' + '''
                                        git config --global user.email "azure-pipelines@example.com"
                                        git config --global user.name "Azure Pipelines"
                                        git add README.md AGENTS.md || true
                                        if git diff --cached --quiet; then
                                            echo "No documentation updates needed"
                                        else
                                            git commit -m "docs: auto-update documentation [skip ci]"
                                            git push origin HEAD:main
                                        fi
                                    ''',
                                    'displayName': 'Commit and push updates'
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    
    def _get_circleci_template(self) -> str:
        """Generate CircleCI template"""
        return '''version: 2.1

jobs:
  docs-check:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: pip install -r requirements.txt || pip install -e .
      - run:
          name: Check documentation
          command: python -m scripts.analyze_project --check-only
      - run:
          name: Generate documentation
          command: python -m scripts.generate_readme --check
      - store_artifacts:
          path: README.md
      - store_artifacts:
          path: AGENTS.md

  docs-update:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run:
          name: Update documentation
          command: python -m scripts.generate_readme --force
      - run:
          name: Commit updates
          command: |
            git config --global user.email "circleci@example.com"
            git config --global user.name "CircleCI"
            git add README.md AGENTS.md || true
            if git diff --cached --quiet; then
              echo "No documentation updates needed"
            else
              git commit -m "docs: auto-update documentation [skip ci]"
              git push origin $CIRCLE_BRANCH
            fi

workflows:
  version: 2
  docs:
    jobs:
      - docs-check
      - docs-update:
          requires:
            - docs-check
          filters:
            branches:
              only: main
'''
    
    def _get_jenkins_template(self) -> str:
        """Generate Jenkinsfile template"""
        return '''pipeline {
    agent any
    
    triggers {
        cron('H 0 * * 0')  // Weekly on Sunday
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh 'python3.11 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt || pip install -e .'
            }
        }
        
        stage('Check Documentation') {
            steps {
                sh '. venv/bin/activate && python -m scripts.analyze_project --check-only'
                sh '. venv/bin/activate && python -m scripts.generate_readme --check'
            }
        }
        
        stage('Update Documentation') {
            when {
                branch 'main'
            }
            steps {
                sh '. venv/bin/activate && python -m scripts.generate_readme --force'
                sh 'git config user.email "jenkins@example.com" && git config user.name "Jenkins"'
                sh 'git add README.md AGENTS.md || true'
                sh 'if git diff --cached --quiet; then echo "No documentation updates needed"; else git commit -m "docs: auto-update documentation [skip ci]" && git push origin main; fi'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'README.md, AGENTS.md', fingerprint: true
        }
    }
}
'''
    
    def _validate_github_actions(self, config: Dict[str, Any]) -> bool:
        """Validate GitHub Actions configuration"""
        required_keys = ['name', 'on', 'jobs']
        for key in required_keys:
            if key not in config:
                logger.error(f"Missing required key in GitHub Actions config: {key}")
                return False
        
        # Check for docs-related jobs
        jobs = config.get('jobs', {})
        if 'docs-check' not in jobs and 'docs-update' not in jobs:
            logger.warning("No documentation-related jobs found in GitHub Actions config")
        
        return True
    
    def _validate_gitlab_ci(self, config: Dict[str, Any]) -> bool:
        """Validate GitLab CI configuration"""
        if not isinstance(config, dict):
            logger.error("GitLab CI config must be a dictionary")
            return False
        
        # Check for docs-related jobs
        has_docs_job = any('docs' in job_name.lower() for job_name in config.keys())
        if not has_docs_job:
            logger.warning("No documentation-related jobs found in GitLab CI config")
        
        return True
    
    def _validate_azure_pipelines(self, config: Dict[str, Any]) -> bool:
        """Validate Azure Pipelines configuration"""
        required_keys = ['trigger', 'pool', 'stages']
        for key in required_keys:
            if key not in config:
                logger.error(f"Missing required key in Azure Pipelines config: {key}")
                return False
        
        return True
    
    def _run_github_actions_job(self, job_name: str, config_path: Path) -> int:
        """Run GitHub Actions job locally using act"""
        try:
            # Check if act is installed
            result = run_command(['which', 'act'])
            if not result['success']:
                logger.error("act is not installed. Install it from: https://github.com/nektos/act")
                return 1
            
            # Run the job
            cmd = ['act', '-j', job_name, '-W', str(config_path)]
            result = run_command(cmd, cwd=str(self.project_path))
            
            if result['success']:
                logger.info(f"Job {job_name} completed successfully")
                return 0
            else:
                logger.error(f"Job {job_name} failed: {result.get('error', 'Unknown error')}")
                return 1
                
        except Exception as e:
            logger.error(f"Error running GitHub Actions job: {e}")
            return 1
    
    def _run_gitlab_ci_job(self, job_name: str, config_path: Path) -> int:
        """Run GitLab CI job locally using gitlab-runner"""
        try:
            # Check if gitlab-runner is installed
            result = run_command(['which', 'gitlab-runner'])
            if not result['success']:
                logger.error("gitlab-runner is not installed")
                return 1
            
            # Run the job
            cmd = ['gitlab-runner', 'exec', 'docker', job_name]
            result = run_command(cmd, cwd=str(self.project_path))
            
            if result['success']:
                logger.info(f"Job {job_name} completed successfully")
                return 0
            else:
                logger.error(f"Job {job_name} failed: {result.get('error', 'Unknown error')}")
                return 1
                
        except Exception as e:
            logger.error(f"Error running GitLab CI job: {e}")
            return 1
    
    def _run_azure_pipelines_job(self, job_name: str, config_path: Path) -> int:
        """Run Azure Pipelines job locally"""
        logger.warning("Local execution of Azure Pipelines jobs is not fully supported")
        logger.info("Please run the pipeline in Azure DevOps or use the Azure DevOps CLI")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="CI/CD Integration for update-readme skill"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate CI/CD configuration')
    generate_parser.add_argument('--platform', required=True,
                                choices=['github-actions', 'gitlab-ci', 'azure-pipelines', 
                                        'circleci', 'jenkins'],
                                help='CI/CD platform')
    generate_parser.add_argument('--output', type=Path,
                                help='Output path for configuration')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate CI/CD configuration')
    validate_parser.add_argument('--config', type=Path, required=True,
                                help='Path to CI/CD configuration file')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run CI/CD job locally')
    run_parser.add_argument('--job', required=True,
                           help='Job name to run')
    run_parser.add_argument('--config', type=Path,
                           help='Path to CI/CD configuration file')
    
    args = parser.parse_args()
    
    manager = CICDManager()
    
    if args.command == 'generate':
        success = manager.generate_config(args.platform, args.output)
        sys.exit(0 if success else 1)
        
    elif args.command == 'validate':
        success = manager.validate_config(args.config)
        sys.exit(0 if success else 1)
        
    elif args.command == 'run':
        exit_code = manager.run_job(args.job, args.config)
        sys.exit(exit_code)
        
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()