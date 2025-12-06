# Prefect workflows for MLOps
# Workflow orchestration for Machine Learning pipelines

from prefect.blocks.system import Secret
import os

__version__ = "0.1.0"


# Configuración global de Prefect
def setup_prefect():
    """Configura el entorno de Prefect para desarrollo."""
    # Configurar para desarrollo local
    os.environ.setdefault("PREFECT_API_URL", "http://127.0.0.1:4200/api")

    # Configurar logging
    import logging

    logging.basicConfig(level=logging.INFO)

    print("🚀 Prefect configurado para desarrollo local")
    print("💡 Ejecuta 'prefect server start' para iniciar el servidor UI")


# Funciones helper para workflows
def get_secret(name: str, default: str = None) -> str:
    """Obtiene un secreto de Prefect blocks."""
    try:
        secret = Secret.load(name)
        return secret.get()
    except Exception:
        if default:
            return default
        raise ValueError(f"Secret '{name}' no encontrado")


def log_ml_metrics(metrics: dict, step_name: str = "ML Step"):
    """Registra métricas de ML en los logs de Prefect."""
    from prefect import get_run_logger

    logger = get_run_logger()
    logger.info(f"📊 {step_name} - Métricas:")

    for key, value in metrics.items():
        if isinstance(value, float):
            logger.info(f"   {key}: {value:.4f}")
        else:
            logger.info(f"   {key}: {value}")
