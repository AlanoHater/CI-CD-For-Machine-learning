#!/usr/bin/env python3
"""
Script para validar la estructura del proyecto MLOps GHA Learning.
Se ejecuta como pre-commit hook.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class ProjectValidator:
    """Validador de estructura del proyecto."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_file_exists(self, file_path: str, description: str) -> bool:
        """Validar que un archivo existe."""
        full_path = self.root / file_path
        if not full_path.exists():
            self.errors.append(f"❌ Falta {description}: {file_path}")
            return False
        return True

    def validate_directory_exists(self, dir_path: str, description: str) -> bool:
        """Validar que un directorio existe."""
        full_path = self.root / dir_path
        if not full_path.exists() or not full_path.is_dir():
            self.errors.append(f"❌ Falta {description}: {dir_path}")
            return False
        return True

    def validate_python_files(self, dir_path: str, min_files: int = 1) -> bool:
        """Validar que un directorio tiene archivos Python."""
        full_path = self.root / dir_path
        if not full_path.exists():
            return False

        py_files = list(full_path.glob("**/*.py"))
        if len(py_files) < min_files:
            self.errors.append(f"❌ {dir_path} debe tener al menos {min_files} archivo(s) Python")
            return False
        return True

    def validate_init_files(self) -> bool:
        """Validar archivos __init__.py."""
        init_files = [
            "src/__init__.py",
            "tests/__init__.py"
        ]

        for init_file in init_files:
            if not self.validate_file_exists(init_file, f"archivo __init__.py en {init_file}"):
                return False
        return True

    def validate_test_files(self) -> bool:
        """Validar archivos de test."""
        test_dir = self.root / "tests"
        if not test_dir.exists():
            self.errors.append("❌ Falta directorio tests/")
            return False

        test_files = list(test_dir.glob("test_*.py"))
        if len(test_files) == 0:
            self.errors.append("❌ No hay archivos de test en tests/")
            return False

        # Verificar que cada módulo tenga test correspondiente
        src_modules = [f.stem for f in (self.root / "src").glob("*.py") if f.name != "__init__.py"]
        test_modules = [f.stem.replace("test_", "") for f in test_files]

        missing_tests = set(src_modules) - set(test_modules)
        if missing_tests:
            self.warnings.append(f"⚠️ Módulos sin tests: {', '.join(missing_tests)}")

        return True

    def validate_requirements(self) -> bool:
        """Validar archivos de dependencias."""
        req_files = ["requirements.txt", "pyproject.toml"]

        for req_file in req_files:
            if not self.validate_file_exists(req_file, f"archivo de dependencias {req_file}"):
                return False

        # Validar que requirements.txt tenga dependencias básicas
        try:
            with open(self.root / "requirements.txt", "r") as f:
                content = f.read().lower()
                basic_deps = ["numpy", "pandas", "scikit-learn"]
                missing_deps = [dep for dep in basic_deps if dep not in content]

                if missing_deps:
                    self.warnings.append(f"⚠️ Dependencias faltantes en requirements.txt: {', '.join(missing_deps)}")
        except FileNotFoundError:
            pass

        return True

    def validate_workflows(self) -> bool:
        """Validar workflows de GitHub Actions."""
        workflow_dir = self.root / ".github" / "workflows"
        if not workflow_dir.exists():
            self.errors.append("❌ Falta directorio .github/workflows/")
            return False

        yml_files = list(workflow_dir.glob("*.yml"))
        yaml_files = list(workflow_dir.glob("*.yaml"))

        if len(yml_files) + len(yaml_files) == 0:
            self.errors.append("❌ No hay archivos de workflow en .github/workflows/")
            return False

        return True

    def validate_scripts(self) -> bool:
        """Validar scripts de utilidad."""
        script_dir = self.root / "scripts"
        if not script_dir.exists():
            self.warnings.append("⚠️ Falta directorio scripts/ (útil para automatización)")
            return True

        sh_files = list(script_dir.glob("*.sh"))
        py_files = list(script_dir.glob("*.py"))

        if len(sh_files) + len(py_files) == 0:
            self.warnings.append("⚠️ No hay scripts en scripts/")
            return True

        return True

    def validate_documentation(self) -> bool:
        """Validar documentación."""
        docs = ["README.md", "LEARNING-ROADMAP.md", "START-HERE.md"]

        for doc in docs:
            if not self.validate_file_exists(doc, f"documento {doc}"):
                return False

        return True

    def run_validation(self) -> Tuple[bool, List[str], List[str]]:
        """Ejecutar todas las validaciones."""
        print("🔍 Validando estructura del proyecto MLOps GHA Learning...")
        print("=" * 60)

        # Ejecutar todas las validaciones
        validations = [
            ("Estructura básica", self.validate_init_files),
            ("Archivos de test", self.validate_test_files),
            ("Dependencias", self.validate_requirements),
            ("Workflows GHA", self.validate_workflows),
            ("Scripts", self.validate_scripts),
            ("Documentación", self.validate_documentation),
        ]

        all_passed = True
        for name, validation_func in validations:
            try:
                passed = validation_func()
                status = "✅" if passed else "❌"
                print("15")
                if not passed:
                    all_passed = False
            except Exception as e:
                print("15"                self.errors.append(f"Error en {name}: {e}")
                all_passed = False

        # Mostrar resumen
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE VALIDACIÓN")
        print("=" * 60)

        if self.errors:
            print(f"❌ ERRORES ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
        else:
            print("✅ No hay errores críticos")

        if self.warnings:
            print(f"\n⚠️ ADVERTENCIAS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")

        if all_passed and not self.errors:
            print("\n🎉 ¡Estructura del proyecto válida!")
            return True, self.errors, self.warnings
        else:
            print(f"\n💥 Se encontraron {len(self.errors)} errores que deben corregirse")
            return False, self.errors, self.warnings


def main():
    """Función principal."""
    validator = ProjectValidator()
    success, errors, warnings = validator.run_validation()

    # Exit code para pre-commit
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
