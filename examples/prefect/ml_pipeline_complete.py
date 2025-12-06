#!/usr/bin/env python3
"""
Ejemplo completo: Integración de Prefect con ML Pipeline
Demuestra cómo usar Prefect para orquestar un pipeline completo de ML
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.states import Completed, Failed

# Importar módulos del proyecto
from src.data_utils import generate_sample_data, preprocess_data, validate_data_integrity
from src.model import create_and_train_model
from src.prefect_workflows.config import get_config, setup_environment


@task(name="Generate Sample Data", description="Genera datos de ejemplo para ML")
def generate_sample_data_task(n_samples: int = 1000, n_features: int = 8) -> str:
    """
    Genera datos de ejemplo y los guarda en archivo.

    Args:
        n_samples: Número de muestras
        n_features: Número de features

    Returns:
        Ruta del archivo generado
    """
    logger = get_run_logger()
    logger.info(f"📊 Generando {n_samples} muestras con {n_features} features")

    # Generar datos
    df = generate_sample_data(n_samples=n_samples, n_features=n_features, random_state=42)

    # Crear directorio si no existe
    os.makedirs('data', exist_ok=True)
    file_path = 'data/sample_ml_data.csv'

    # Guardar datos
    df.to_csv(file_path, index=False)
    logger.info(f"💾 Datos guardados en {file_path}")

    # Validación básica
    if len(df) != n_samples:
        raise ValueError(f"❌ Número de muestras incorrecto: esperado {n_samples}, obtenido {len(df)}")

    return file_path


@task(name="Quality Assurance", description="Validación completa de calidad de datos")
def quality_assurance(data_path: str) -> dict:
    """
    Realiza validación completa de calidad de datos.

    Args:
        data_path: Ruta al archivo de datos

    Returns:
        Resultados de validación
    """
    logger = get_run_logger()
    logger.info("🔍 Ejecutando Quality Assurance")

    # Cargar datos
    import pandas as pd
    df = pd.read_csv(data_path)

    # Ejecutar validaciones
    validation_results = validate_data_integrity(df)

    # Criterios de calidad
    quality_checks = {
        'has_minimum_samples': len(df) >= 100,
        'has_target_column': 'target' in df.columns,
        'low_missing_data': validation_results['missing_values'] < len(df) * 0.1,  # < 10%
        'no_duplicate_data': validation_results['duplicates'] < len(df) * 0.05,  # < 5%
        'balanced_classes': validation_results.get('min_class_ratio', 0) > 0.1  # > 10% balance
    }

    # Calcular score de calidad
    passed_checks = sum(quality_checks.values())
    total_checks = len(quality_checks)
    quality_score = passed_checks / total_checks

    results = {
        'quality_score': quality_score,
        'passed_checks': passed_checks,
        'total_checks': total_checks,
        'checks': quality_checks,
        'validation_details': validation_results
    }

    # Logging detallado
    logger.info(".2%"
    for check_name, passed in quality_checks.items():
        status = "✅" if passed else "❌"
        logger.info(f"   {status} {check_name}: {passed}")

    # Artifact con reporte de calidad
    qa_report = f"""
# 📊 Quality Assurance Report

## Overall Quality Score: {quality_score:.2%}

## Quality Checks ({passed_checks}/{total_checks} passed)

| Check | Status |
|-------|--------|
"""

    for check_name, passed in quality_checks.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        qa_report += f"| {check_name.replace('_', ' ').title()} | {status} |\n"

    qa_report += f"""
## Data Summary
- **Samples**: {validation_results['shape'][0]:,}
- **Features**: {validation_results['shape'][1]:,}
- **Missing Values**: {validation_results['missing_values']:,}
- **Duplicates**: {validation_results['duplicates']:,}

## Recommendations
{'✅ Data quality is excellent! Ready for ML pipeline.' if quality_score >= 0.8 else '⚠️ Data quality needs attention before proceeding.'}
"""

    create_markdown_artifact(qa_report, "quality-assurance-report")

    if quality_score < 0.6:
        raise ValueError(f"❌ Calidad de datos insuficiente: {quality_score:.2%}")

    return results


@task(name="Model Training with Validation", description="Entrenamiento y validación de modelo")
def train_and_validate_model(data_path: str, config: dict) -> dict:
    """
    Entrena y valida un modelo de ML.

    Args:
        data_path: Ruta a los datos
        config: Configuración del modelo

    Returns:
        Resultados del entrenamiento
    """
    logger = get_run_logger()
    logger.info("🏋️ Iniciando entrenamiento de modelo")

    # Cargar y preprocesar datos
    import pandas as pd
    df = pd.read_csv(data_path)
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    # Entrenar modelo
    model = create_and_train_model(X_train, y_train, model_params=config['model_params'])

    # Evaluar modelo
    evaluation_results = model.evaluate(X_test, y_test)
    accuracy = evaluation_results['accuracy']

    # Validar performance mínima
    min_accuracy = config.get('min_accuracy', 0.7)
    if accuracy < min_accuracy:
        raise ValueError(".4f"
    # Preparar resultados
    results = {
        'accuracy': accuracy,
        'model_params': config['model_params'],
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'evaluation_details': evaluation_results,
        'passed_validation': accuracy >= min_accuracy
    }

    logger.info(".4f"
    return results


@task(name="Model Deployment", description="Despliegue del modelo entrenado")
def deploy_model(data_path: str, training_results: dict, config: dict) -> dict:
    """
    Simula el despliegue del modelo.

    Args:
        data_path: Ruta a los datos
        training_results: Resultados del entrenamiento
        config: Configuración de despliegue

    Returns:
        Información de despliegue
    """
    logger = get_run_logger()
    logger.info("🚀 Iniciando despliegue de modelo")

    # Simular proceso de despliegue
    import time
    time.sleep(2)  # Simular tiempo de despliegue

    # Información de despliegue
    deployment_info = {
        'model_version': f"v1.0.{int(time.time())}",
        'accuracy': training_results['accuracy'],
        'deployment_timestamp': time.time(),
        'environment': config.get('environment', 'staging'),
        'endpoint_url': f"https://api.mlops.dev/models/{training_results.get('model_id', 'default')}",
        'status': 'deployed'
    }

    logger.info(f"✅ Modelo desplegado exitosamente en {deployment_info['environment']}")
    logger.info(f"🔗 Endpoint: {deployment_info['endpoint_url']}")

    return deployment_info


@flow(name="Complete ML Pipeline with Prefect",
      description="Pipeline completo de ML orquestado con Prefect")
def complete_ml_pipeline(
    n_samples: int = 1000,
    n_features: int = 8,
    min_accuracy: float = 0.75,
    environment: str = "development"
) -> dict:
    """
    Pipeline completo de ML usando Prefect para orquestación.

    Args:
        n_samples: Número de muestras para datos de ejemplo
        n_features: Número de features
        min_accuracy: Accuracy mínima requerida
        environment: Entorno de ejecución

    Returns:
        Resultados completos del pipeline
    """
    logger = get_run_logger()
    logger.info("🚀 Iniciando Pipeline Completo de ML con Prefect")
    logger.info(f"📊 Configuración: {n_samples} samples, {n_features} features, min_accuracy={min_accuracy}")

    # Configuración
    config = get_config(environment)
    config['min_accuracy'] = min_accuracy

    # Setup del entorno
    setup_environment(config)

    try:
        # Paso 1: Generar datos
        logger.info("📋 Paso 1: Generación de datos")
        data_path = generate_sample_data_task(n_samples, n_features)

        # Paso 2: Quality Assurance
        logger.info("📋 Paso 2: Quality Assurance")
        qa_results = quality_assurance(data_path)

        # Paso 3: Entrenamiento y validación
        logger.info("📋 Paso 3: Entrenamiento del modelo")
        training_results = train_and_validate_model(data_path, config)

        # Paso 4: Despliegue (solo si accuracy es suficiente)
        logger.info("📋 Paso 4: Despliegue del modelo")
        deployment_results = deploy_model(data_path, training_results, config)

        # Resultado final
        final_results = {
            'status': 'success',
            'data_path': data_path,
            'quality_score': qa_results['quality_score'],
            'model_accuracy': training_results['accuracy'],
            'deployment_info': deployment_results,
            'execution_time': None,  # Se calcula después
            'config': config
        }

        # Artifact final con resumen completo
        summary_report = f"""
# 🎉 ML Pipeline Execution Summary

## Pipeline Status: ✅ SUCCESS

## Key Metrics
- **Data Quality Score**: {qa_results['quality_score']:.2%}
- **Model Accuracy**: {training_results['accuracy']:.4f}
- **Samples Processed**: {n_samples:,}
- **Features Used**: {n_features}

## Quality Checks
- ✅ Minimum samples requirement
- ✅ Target column present
- ✅ Low missing data
- ✅ Acceptable duplicates
- ✅ Class balance

## Model Performance
- **Training Samples**: {training_results['training_samples']:,}
- **Test Samples**: {training_results['test_samples']:,}
- **Accuracy Threshold**: {min_accuracy:.2%} (✅ Met)

## Deployment
- **Environment**: {deployment_results['environment']}
- **Version**: {deployment_results['model_version']}
- **Endpoint**: {deployment_results['endpoint_url']}

---
*Pipeline ejecutado exitosamente con Prefect*
"""

        create_markdown_artifact(summary_report, "pipeline-execution-summary")

        logger.info("🎉 ¡Pipeline de ML completado exitosamente!")
        return final_results

    except Exception as e:
        logger.error(f"💥 Error en pipeline: {e}")

        # Artifact de error
        error_report = f"""
# ❌ ML Pipeline Execution Failed

## Error Details
**Error Message**: {str(e)}
**Error Type**: {type(e).__name__}

## Partial Results
- Data generation: ✅ Completed
- Quality assurance: {'✅' if 'qa_results' in locals() else '❌'} Failed
- Model training: {'✅' if 'training_results' in locals() else '❌'} Failed
- Deployment: ❌ Not attempted

## Recommendations
1. Check data quality and integrity
2. Verify model configuration
3. Review error logs for detailed information
4. Consider adjusting quality thresholds
"""

        create_markdown_artifact(error_report, "pipeline-error-report")

        raise  # Re-lanzar la excepción


@flow(name="ML Experiment Runner", description="Ejecuta múltiples experimentos de ML")
def run_ml_experiments(experiments: list = None) -> list:
    """
    Ejecuta múltiples experimentos de ML en paralelo.

    Args:
        experiments: Lista de configuraciones de experimentos

    Returns:
        Resultados de todos los experimentos
    """
    if experiments is None:
        experiments = [
            {'n_samples': 500, 'n_features': 4, 'min_accuracy': 0.7},
            {'n_samples': 1000, 'n_features': 6, 'min_accuracy': 0.75},
            {'n_samples': 1500, 'n_features': 8, 'min_accuracy': 0.8},
        ]

    logger = get_run_logger()
    logger.info(f"🧪 Ejecutando {len(experiments)} experimentos de ML")

    results = []

    # Ejecutar experimentos (en Prefect 2.0, esto se puede paralelizar)
    for i, exp_config in enumerate(experiments, 1):
        logger.info(f"🔬 Experimento {i}/{len(experiments)}: {exp_config}")

        try:
            result = complete_ml_pipeline(**exp_config)
            result['experiment_id'] = i
            results.append(result)
            logger.info(f"✅ Experimento {i} completado")
        except Exception as e:
            logger.error(f"❌ Experimento {i} falló: {e}")
            results.append({
                'experiment_id': i,
                'status': 'failed',
                'error': str(e),
                'config': exp_config
            })

    # Resumen de experimentos
    successful = len([r for r in results if r.get('status') == 'success'])
    logger.info(f"📊 Experimentos completados: {successful}/{len(experiments)}")

    return results


if __name__ == "__main__":
    print("🚀 Ejecutando Pipeline Completo de ML con Prefect")
    print("=" * 60)

    # Configurar entorno de desarrollo
    from src.prefect_workflows import setup_prefect
    setup_prefect()

    # Ejecutar pipeline completo
    print("\n🎯 Ejecutando pipeline completo...")
    results = complete_ml_pipeline(
        n_samples=500,  # Más pequeño para demo rápido
        n_features=6,
        min_accuracy=0.7
    )

    print("
✅ Pipeline completado!"    print(".4f"    print(f"📊 Calidad de datos: {results['quality_score']:.2%}")

    print("\n🧪 Ejecutando experimentos múltiples...")
    exp_results = run_ml_experiments()

    successful_experiments = len([r for r in exp_results if r.get('status') == 'success'])
    print(f"📊 Experimentos exitosos: {successful_experiments}/{len(exp_results)}")

    print("\n" + "=" * 60)
    print("🎉 ¡Demo completado!")
    print("\n💡 Este ejemplo demuestra:")
    print("  • Orquestación completa de ML con Prefect")
    print("  • Manejo de estados y errores")
    print("  • Logging y artifacts detallados")
    print("  • Quality assurance integrada")
    print("  • Despliegue simulado")
    print("  • Experimentos múltiples")
