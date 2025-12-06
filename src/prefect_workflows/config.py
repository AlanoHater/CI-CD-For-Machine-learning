"""
Configuración de Prefect para diferentes entornos
Incluye configuración para desarrollo, staging y producción
"""

import os
from typing import Dict, Any
from prefect.blocks.system import Secret


# =============================================================================
# CONFIGURACIONES POR ENTORNO
# =============================================================================


def get_dev_config() -> Dict[str, Any]:
    """Configuración para desarrollo local."""
    return {
        "environment": "development",
        "prefect_api_url": "http://127.0.0.1:4200/api",
        "log_level": "INFO",
        "data_dir": "data/",
        "models_dir": "models/",
        "logs_dir": "logs/",
        "cache_dir": ".cache/",
        "mlflow_tracking_uri": None,
        "database_url": "sqlite:///dev.db",
        "batch_size": 32,
        "random_seed": 42,
        "model_params": {
            "n_estimators": 50,  # Más rápido para desarrollo
            "max_depth": 10,
            "random_state": 42,
        },
    }


def get_staging_config() -> Dict[str, Any]:
    """Configuración para staging/testing."""
    return {
        "environment": "staging",
        "prefect_api_url": os.getenv("PREFECT_API_URL", "https://api.prefect.cloud"),
        "log_level": "INFO",
        "data_dir": "/app/data/",
        "models_dir": "/app/models/",
        "logs_dir": "/app/logs/",
        "cache_dir": "/app/.cache/",
        "mlflow_tracking_uri": os.getenv("MLFLOW_TRACKING_URI"),
        "database_url": os.getenv(
            "DATABASE_URL", "postgresql://user:pass@localhost/staging"
        ),
        "batch_size": 64,
        "random_seed": 42,
        "model_params": {"n_estimators": 100, "max_depth": None, "random_state": 42},
    }


def get_prod_config() -> Dict[str, Any]:
    """Configuración para producción."""
    return {
        "environment": "production",
        "prefect_api_url": os.getenv("PREFECT_API_URL", "https://api.prefect.cloud"),
        "log_level": "WARNING",
        "data_dir": "/app/data/",
        "models_dir": "/app/models/",
        "logs_dir": "/app/logs/",
        "cache_dir": "/app/.cache/",
        "mlflow_tracking_uri": os.getenv("MLFLOW_TRACKING_URI"),
        "database_url": os.getenv("DATABASE_URL"),
        "batch_size": 128,
        "random_seed": 42,
        "model_params": {
            "n_estimators": 200,
            "max_depth": None,
            "random_state": 42,
            "n_jobs": -1,  # Usar todos los cores
        },
    }


# =============================================================================
# FUNCIONES DE CONFIGURACIÓN
# =============================================================================


def get_config(environment: str = None) -> Dict[str, Any]:
    """
    Obtiene la configuración según el entorno.

    Args:
        environment: Entorno deseado (dev, staging, prod)

    Returns:
        Diccionario con configuración
    """
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")

    environment = environment.lower()

    if environment == "development" or environment == "dev":
        config = get_dev_config()
    elif environment == "staging":
        config = get_staging_config()
    elif environment == "production" or environment == "prod":
        config = get_prod_config()
    else:
        raise ValueError(f"Entorno desconocido: {environment}")

    # Override con variables de entorno si existen
    config.update(_get_env_overrides())

    return config


def _get_env_overrides() -> Dict[str, Any]:
    """Obtiene overrides desde variables de entorno."""
    overrides = {}

    # Mapping de variables de entorno a config keys
    env_mapping = {
        "PREFECT_API_URL": "prefect_api_url",
        "LOG_LEVEL": "log_level",
        "DATA_DIR": "data_dir",
        "MODELS_DIR": "models_dir",
        "LOGS_DIR": "logs_dir",
        "CACHE_DIR": "cache_dir",
        "MLFLOW_TRACKING_URI": "mlflow_tracking_uri",
        "DATABASE_URL": "database_url",
        "BATCH_SIZE": "batch_size",
        "RANDOM_SEED": "random_seed",
    }

    for env_var, config_key in env_mapping.items():
        value = os.getenv(env_var)
        if value is not None:
            # Convertir tipos básicos
            if config_key in ["batch_size", "random_seed"]:
                try:
                    value = int(value)
                except ValueError:
                    pass
            overrides[config_key] = value

    return overrides


def setup_environment(config: Dict[str, Any] = None):
    """
    Configura el entorno según la configuración.

    Args:
        config: Configuración a usar (opcional)
    """
    if config is None:
        config = get_config()

    # Crear directorios necesarios
    directories = [
        config["data_dir"],
        config["models_dir"],
        config["logs_dir"],
        config["cache_dir"],
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Configurar variables de entorno
    os.environ["PREFECT_API_URL"] = config["prefect_api_url"]
    os.environ["PREFECT_LOGGING_LEVEL"] = config["log_level"]

    if config.get("mlflow_tracking_uri"):
        os.environ["MLFLOW_TRACKING_URI"] = config["mlflow_tracking_uri"]

    print(f"🔧 Entorno configurado: {config['environment']}")
    print(f"📁 Directorios creados: {', '.join(directories)}")


def get_secret_value(secret_name: str, default: str = None) -> str:
    """
    Obtiene el valor de un secreto de Prefect.

    Args:
        secret_name: Nombre del secreto
        default: Valor por defecto si no se encuentra

    Returns:
        Valor del secreto
    """
    try:
        secret = Secret.load(secret_name)
        return secret.get()
    except Exception:
        if default is not None:
            return default
        raise ValueError(
            f"Secreto '{secret_name}' no encontrado y no hay valor por defecto"
        )


# =============================================================================
# CONFIGURACIONES PREDEFINIDAS PARA DIFERENTES CASOS DE USO
# =============================================================================

# Configuración para CI/CD
CI_CONFIG = {
    "environment": "ci",
    "log_level": "INFO",
    "data_dir": "data/",
    "models_dir": "models/",
    "logs_dir": "logs/",
    "cache_dir": ".cache/",
    "model_params": {
        "n_estimators": 10,  # Muy rápido para CI
        "max_depth": 5,
        "random_state": 42,
    },
}

# Configuración para experimentación rápida
EXPERIMENT_CONFIG = {
    "environment": "experiment",
    "log_level": "DEBUG",
    "data_dir": "data/",
    "models_dir": "models/",
    "logs_dir": "logs/",
    "cache_dir": ".cache/",
    "model_params": {"n_estimators": 25, "max_depth": 8, "random_state": 42},
}


# =============================================================================
# UTILIDADES PARA TESTING
# =============================================================================


def create_test_config(**overrides) -> Dict[str, Any]:
    """
    Crea una configuración de test con overrides personalizados.

    Args:
        **overrides: Valores a overridear

    Returns:
        Configuración de test
    """
    config = get_dev_config()
    config.update(
        {
            "environment": "test",
            "data_dir": "test_data/",
            "models_dir": "test_models/",
            "logs_dir": "test_logs/",
            "cache_dir": "test_cache/",
            "model_params": {
                "n_estimators": 5,  # Muy pequeño para tests
                "random_state": 42,
            },
        }
    )
    config.update(overrides)
    return config


if __name__ == "__main__":
    # Demo de configuración
    print("🔧 Demo de configuración de Prefect")
    print("=" * 50)

    # Configuración de desarrollo
    dev_config = get_config("development")
    print(f"📊 Configuración desarrollo: {dev_config['environment']}")
    print(f"🏠 Directorios: {dev_config['data_dir']}, {dev_config['models_dir']}")

    # Setup del entorno
    setup_environment(dev_config)

    print("\n✅ Configuración completada!")
    print("💡 Ejecuta 'prefect server start' para iniciar el servidor UI")
