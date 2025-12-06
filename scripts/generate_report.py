#!/usr/bin/env python3
"""
Script para generar reportes de análisis del proyecto.
Útil para CI/CD y monitoreo de calidad.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import subprocess


class ProjectReporter:
    """Genera reportes comprehensivos del proyecto."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.report: Dict[str, Any] = {}

    def count_lines_of_code(self) -> Dict[str, int]:
        """Cuenta líneas de código por lenguaje."""
        loc = {
            'python': 0,
            'yaml': 0,
            'markdown': 0,
            'bash': 0,
            'dockerfile': 0,
            'other': 0
        }

        extensions = {
            '.py': 'python',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.md': 'markdown',
            '.sh': 'bash',
            'Dockerfile': 'dockerfile'
        }

        for file_path in self.root.rglob('*'):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                ext = file_path.suffix
                if file_path.name == 'Dockerfile':
                    ext = 'Dockerfile'

                category = extensions.get(ext, 'other')

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        loc[category] += lines
                except:
                    pass

        return loc

    def analyze_code_quality(self) -> Dict[str, Any]:
        """Analiza calidad del código."""
        quality = {
            'tests_exist': False,
            'test_count': 0,
            'linting_tools': [],
            'documentation_exists': False,
            'ci_configured': False
        }

        # Verificar tests
        test_dir = self.root / 'tests'
        if test_dir.exists():
            test_files = list(test_dir.glob('test_*.py'))
            quality['tests_exist'] = len(test_files) > 0
            quality['test_count'] = len(test_files)

        # Verificar herramientas de linting
        lint_tools = ['black', 'flake8', 'mypy', 'isort']
        for tool in lint_tools:
            if (self.root / f'.{tool}').exists() or any((self.root / f).exists() for f in ['pyproject.toml', 'setup.cfg', 'tox.ini']):
                quality['linting_tools'].append(tool)

        # Verificar documentación
        docs = ['README.md', 'docs']
        quality['documentation_exists'] = any((self.root / doc).exists() for doc in docs)

        # Verificar CI
        ci_paths = ['.github/workflows', '.gitlab-ci.yml', 'Jenkinsfile']
        quality['ci_configured'] = any((self.root / ci).exists() for ci in ci_paths)

        return quality

    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analiza dependencias del proyecto."""
        deps = {
            'python_requirements': False,
            'requirements_count': 0,
            'dev_dependencies': False,
            'has_pyproject': False
        }

        # Verificar requirements.txt
        req_file = self.root / 'requirements.txt'
        if req_file.exists():
            deps['python_requirements'] = True
            try:
                with open(req_file, 'r') as f:
                    deps['requirements_count'] = len([line.strip() for line in f if line.strip() and not line.startswith('#')])
            except:
                pass

        # Verificar pyproject.toml
        pyproject = self.root / 'pyproject.toml'
        deps['has_pyproject'] = pyproject.exists()

        # Verificar dependencias de desarrollo
        dev_files = ['requirements-dev.txt', 'dev-requirements.txt']
        deps['dev_dependencies'] = any((self.root / f).exists() for f in dev_files)

        return deps

    def analyze_ml_specific(self) -> Dict[str, Any]:
        """Analiza aspectos específicos de ML."""
        ml_analysis = {
            'has_ml_code': False,
            'ml_libraries': [],
            'has_data_processing': False,
            'has_model_training': False,
            'has_evaluation': False
        }

        # Verificar código ML
        src_dir = self.root / 'src'
        if src_dir.exists():
            for py_file in src_dir.glob('*.py'):
                try:
                    with open(py_file, 'r') as f:
                        content = f.read().lower()

                        # Verificar librerías ML
                        ml_libs = ['sklearn', 'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy']
                        for lib in ml_libs:
                            if lib in content:
                                if lib not in ml_analysis['ml_libraries']:
                                    ml_analysis['ml_libraries'].append(lib)

                        # Verificar funcionalidades
                        if any(term in content for term in ['preprocess', 'clean', 'transform']):
                            ml_analysis['has_data_processing'] = True
                        if any(term in content for term in ['fit', 'train', 'model']):
                            ml_analysis['has_model_training'] = True
                        if any(term in content for term in ['accuracy', 'precision', 'recall', 'evaluate']):
                            ml_analysis['has_evaluation'] = True

                except:
                    pass

        ml_analysis['has_ml_code'] = len(ml_analysis['ml_libraries']) > 0

        return ml_analysis

    def generate_report(self) -> Dict[str, Any]:
        """Genera reporte completo."""
        print("📊 Generando reporte del proyecto...")

        self.report = {
            'timestamp': datetime.now().isoformat(),
            'project_name': 'MLOps GHA Learning',
            'version': '0.1.0',
            'lines_of_code': self.count_lines_of_code(),
            'code_quality': self.analyze_code_quality(),
            'dependencies': self.analyze_dependencies(),
            'ml_analysis': self.analyze_ml_specific()
        }

        # Calcular métricas agregadas
        total_loc = sum(self.report['lines_of_code'].values())
        self.report['summary'] = {
            'total_lines_of_code': total_loc,
            'has_tests': self.report['code_quality']['tests_exist'],
            'has_ci': self.report['code_quality']['ci_configured'],
            'has_docs': self.report['code_quality']['documentation_exists'],
            'is_ml_project': self.report['ml_analysis']['has_ml_code'],
            'quality_score': self._calculate_quality_score()
        }

        return self.report

    def _calculate_quality_score(self) -> float:
        """Calcula score de calidad del proyecto (0-100)."""
        score = 0

        # Tests (30 puntos)
        if self.report['code_quality']['tests_exist']:
            score += 20
            if self.report['code_quality']['test_count'] >= 3:
                score += 10

        # CI/CD (20 puntos)
        if self.report['code_quality']['ci_configured']:
            score += 20

        # Documentación (15 puntos)
        if self.report['code_quality']['documentation_exists']:
            score += 15

        # Linting (15 puntos)
        if len(self.report['code_quality']['linting_tools']) >= 2:
            score += 15
        elif len(self.report['code_quality']['linting_tools']) >= 1:
            score += 7

        # Dependencias (10 puntos)
        if self.report['dependencies']['python_requirements']:
            score += 5
        if self.report['dependencies']['has_pyproject']:
            score += 5

        # ML específico (10 puntos)
        if self.report['ml_analysis']['has_ml_code']:
            score += 5
        if all([
            self.report['ml_analysis']['has_data_processing'],
            self.report['ml_analysis']['has_model_training'],
            self.report['ml_analysis']['has_evaluation']
        ]):
            score += 5

        return min(score, 100)  # Máximo 100

    def save_report(self, output_file: str = 'project_report.json') -> None:
        """Guarda reporte en archivo JSON."""
        output_path = self.root / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        print(f"💾 Reporte guardado en {output_path}")

    def print_summary(self) -> None:
        """Imprime resumen del reporte."""
        if not self.report:
            self.generate_report()

        print("\n" + "="*60)
        print("📊 REPORTE DEL PROYECTO - MLOps GHA Learning")
        print("="*60)

        # Líneas de código
        loc = self.report['lines_of_code']
        print("
📝 LÍNEAS DE CÓDIGO:"        print(f"  Python: {loc['python']}")
        print(f"  YAML: {loc['yaml']}")
        print(f"  Markdown: {loc['markdown']}")
        print(f"  Bash: {loc['bash']}")
        print(f"  Total: {sum(loc.values())}")

        # Calidad de código
        quality = self.report['code_quality']
        print("
🧹 CALIDAD DE CÓDIGO:"        print(f"  Tests: {'✅' if quality['tests_exist'] else '❌'} ({quality['test_count']} archivos)")
        print(f"  CI/CD: {'✅' if quality['ci_configured'] else '❌'}")
        print(f"  Documentación: {'✅' if quality['documentation_exists'] else '❌'}")
        print(f"  Linting: {', '.join(quality['linting_tools']) or 'Ninguno'}")

        # ML específico
        ml = self.report['ml_analysis']
        print("
🤖 ANÁLISIS ML:"        print(f"  Es proyecto ML: {'✅' if ml['has_ml_code'] else '❌'}")
        print(f"  Librerías ML: {', '.join(ml['ml_libraries']) or 'Ninguna'}")
        print(f"  Data Processing: {'✅' if ml['has_data_processing'] else '❌'}")
        print(f"  Model Training: {'✅' if ml['has_model_training'] else '❌'}")
        print(f"  Evaluation: {'✅' if ml['has_evaluation'] else '❌'}")

        # Score final
        summary = self.report['summary']
        score = summary['quality_score']
        print("
🎯 SCORE DE CALIDAD:"        print(".1f"        if score >= 80:
            print("  Estado: 🏆 Excelente")
        elif score >= 60:
            print("  Estado: ✅ Bueno")
        elif score >= 40:
            print("  Estado: ⚠️ Mejorable")
        else:
            print("  Estado: 💥 Necesita atención")

        print("="*60)


def main():
    """Función principal."""
    reporter = ProjectReporter()
    report = reporter.generate_report()
    reporter.print_summary()
    reporter.save_report()

    # Exit code basado en score
    score = report['summary']['quality_score']
    if score >= 60:
        print("\n✅ Proyecto aprobado!")
        sys.exit(0)
    else:
        print(f"\n⚠️ Score de calidad bajo ({score:.1f}). Considera mejoras.")
        sys.exit(1)


if __name__ == "__main__":
    main()
