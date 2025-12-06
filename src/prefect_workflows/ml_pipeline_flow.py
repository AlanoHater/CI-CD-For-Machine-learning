"""
ML Pipeline Flow usando Prefect
Basado en el tutorial de DataCamp: ML Workflow Orchestration with Prefect

Este módulo demuestra cómo crear un flujo completo de ML usando Prefect para:
- Carga y preparación de datos
- Entrenamiento de modelo
- Evaluación y validación
- Logging y monitoreo
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Dict, Any, Tuple
import joblib
import os
from datetime import datetime

from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from . import log_ml_metrics


# =============================================================================
# TASKS INDIVIDUALES (Funciones atómicas reutilizables)
# =============================================================================

@task(name="Load Data", description="Carga datos desde archivo CSV")
def load_data(file_path: str) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV.

    Args:
        file_path: Ruta al archivo CSV

    Returns:
        DataFrame con los datos cargados
    """
    logger = get_run_logger()

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    logger.info(f"📂 Cargando datos desde {file_path}")
    df = pd.read_csv(file_path)

    logger.info(f"✅ Datos cargados: {len(df)} filas, {len(df.columns)} columnas")
    log_ml_metrics({
        "rows": len(df),
        "columns": len(df.columns),
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
    }, "Data Loading")

    return df


@task(name="Explore Data", description="Análisis exploratorio básico de datos")
def explore_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Realiza análisis exploratorio básico de los datos.

    Args:
        df: DataFrame a explorar

    Returns:
        Diccionario con estadísticas exploratorias
    """
    logger = get_run_logger()
    logger.info("🔍 Realizando análisis exploratorio de datos")

    # Estadísticas básicas
    stats = {
        "shape": df.shape,
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
    }

    # Información de clases (si hay columna target)
    if 'target' in df.columns:
        class_counts = df['target'].value_counts()
        stats['class_distribution'] = class_counts.to_dict()
        stats['class_balance_ratio'] = class_counts.min() / class_counts.max()

    log_ml_metrics({
        "total_samples": len(df),
        "features": len(df.columns) - ('target' in df.columns),
        "missing_pct": (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
        "duplicates_pct": (stats['duplicates'] / len(df)) * 100
    }, "Data Exploration")

    # Crear artifact de Markdown con resumen
    # Generar distribución de clases si existe
    class_dist_text = ""
    if 'class_distribution' in stats and stats['class_distribution']:
        class_dist_text = '\n'.join(
            f"- **Class {k}**: {v:,} samples ({v/stats['shape'][0]*100:.1f}%)" 
            for k, v in stats['class_distribution'].items()
        )
    else:
        class_dist_text = "- No class distribution available"

    # Calcular porcentajes de calidad de datos
    total_cells = len(df) * len(df.columns)
    missing_pct = (sum(stats['missing_values'].values()) / total_cells) * 100 if total_cells > 0 else 0.0
    duplicates_pct = (stats['duplicates'] / len(df)) * 100 if len(df) > 0 else 0.0

    summary_md = f"""
# 📊 Data Exploration Summary

## Dataset Overview
- **Samples**: {stats['shape'][0]:,}
- **Features**: {stats['shape'][1]:,}
- **Missing Values**: {sum(stats['missing_values'].values()):,}
- **Duplicates**: {stats['duplicates']:,}

## Class Distribution
{class_dist_text}

## Data Quality
- **Missing %**: {missing_pct:.2f}%
- **Duplicates %**: {duplicates_pct:.2f}%
"""

    create_markdown_artifact(summary_md, "data-exploration-summary")

    logger.info("✅ Análisis exploratorio completado")
    return stats


@task(name="Preprocess Data", description="Preprocesamiento y limpieza de datos")
def preprocess_data(df: pd.DataFrame, target_col: str = "target") -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocesa los datos para ML.

    Args:
        df: DataFrame a procesar
        target_col: Nombre de la columna target

    Returns:
        Tuple de (X_train, X_test, y_train, y_test, scaler)
    """
    logger = get_run_logger()
    logger.info("⚙️ Preprocesando datos para ML")

    # Separar features y target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    logger.info(f"📊 Split realizado: Train {len(X_train)}, Test {len(X_test)}")

    # Escalar features numéricas
    scaler = StandardScaler()
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns

    if len(numeric_cols) > 0:
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()

        X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
        X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

        logger.info(f"🔧 Features escaladas: {len(numeric_cols)} columnas numéricas")
    else:
        X_train_scaled = X_train
        X_test_scaled = X_test
        logger.warning("⚠️ No se encontraron columnas numéricas para escalar")

    log_ml_metrics({
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "scaled_features": len(numeric_cols),
        "total_features": X_train.shape[1]
    }, "Data Preprocessing")

    return (
        X_train_scaled.values,
        X_test_scaled.values,
        y_train.values,
        y_test.values,
        scaler
    )


@task(name="Train Model", description="Entrenamiento del modelo de ML")
def train_model(X_train: np.ndarray, y_train: np.ndarray,
                model_params: Dict[str, Any] = None) -> RandomForestClassifier:
    """
    Entrena un modelo de Random Forest.

    Args:
        X_train: Features de entrenamiento
        y_train: Target de entrenamiento
        model_params: Parámetros del modelo

    Returns:
        Modelo entrenado
    """
    logger = get_run_logger()

    # Parámetros por defecto
    default_params = {
        'n_estimators': 100,
        'random_state': 42,
        'max_depth': None,
        'min_samples_split': 2
    }

    if model_params:
        default_params.update(model_params)

    logger.info(f"🏋️ Entrenando Random Forest con parámetros: {default_params}")

    model = RandomForestClassifier(**default_params)
    model.fit(X_train, y_train)

    logger.info("✅ Modelo entrenado exitosamente")
    log_ml_metrics({
        "n_estimators": model.n_estimators,
        "max_depth": model.max_depth,
        "n_features": model.n_features_in_,
        "training_score": model.score(X_train, y_train)
    }, "Model Training")

    return model


@task(name="Evaluate Model", description="Evaluación completa del modelo")
def evaluate_model(model: RandomForestClassifier, X_test: np.ndarray,
                  y_test: np.ndarray) -> Dict[str, Any]:
    """
    Evalúa el modelo en datos de test.

    Args:
        model: Modelo entrenado
        X_test: Features de test
        y_test: Target de test

    Returns:
        Diccionario con métricas de evaluación
    """
    logger = get_run_logger()
    logger.info("📊 Evaluando modelo en datos de test")

    # Predicciones
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

    # Métricas principales
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Classification report como dict
    class_report = classification_report(y_test, y_pred, output_dict=True)

    # Feature importance (para Random Forest)
    feature_importance = {}
    if hasattr(model, 'feature_importances_'):
        for i, importance in enumerate(model.feature_importances_):
            feature_importance[f'feature_{i}'] = importance

    results = {
        'accuracy': accuracy,
        'confusion_matrix': conf_matrix.tolist(),
        'classification_report': class_report,
        'feature_importance': feature_importance,
        'predictions_sample': y_pred[:10].tolist(),  # Primeras 10 predicciones
        'true_values_sample': y_test[:10].tolist()   # Primeros 10 valores reales
    }

    logger.info(f"Accuracy: {accuracy:.4f}")
    
    # Formatear top features para el artifact
    top_features_text = ""
    if feature_importance:
        top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
        top_features_text = '\n'.join(
            f"- **{name}**: {importance:.4f}" 
            for name, importance in top_features
        )
    else:
        top_features_text = "- No feature importance available"
    
    # Crear artifact con métricas detalladas
    metrics_md = f"""
# 📈 Model Evaluation Results

## Overall Metrics
- **Accuracy**: {accuracy:.4f}
- **Precision (weighted)**: {class_report['weighted avg']['precision']:.4f}
- **Recall (weighted)**: {class_report['weighted avg']['recall']:.4f}
- **F1-Score (weighted)**: {class_report['weighted avg']['f1-score']:.4f}

## Confusion Matrix
```
{conf_matrix}
```

## Top 5 Most Important Features
{top_features_text}
"""

    create_markdown_artifact(metrics_md, "model-evaluation-results")

    log_ml_metrics({
        "accuracy": accuracy,
        "precision": class_report['weighted avg']['precision'],
        "recall": class_report['weighted avg']['recall'],
        "f1_score": class_report['weighted avg']['f1-score']
    }, "Model Evaluation")

    return results


@task(name="Save Model", description="Guarda el modelo y scaler entrenados")
def save_model(model: RandomForestClassifier, scaler: StandardScaler,
               model_path: str = "models", model_name: str = None) -> str:
    """
    Guarda el modelo y scaler en archivos.

    Args:
        model: Modelo entrenado
        scaler: Scaler ajustado
        model_path: Directorio donde guardar
        model_name: Nombre base del modelo (opcional)

    Returns:
        Ruta del modelo guardado
    """
    logger = get_run_logger()

    # Crear directorio si no existe
    os.makedirs(model_path, exist_ok=True)

    # Generar nombre único si no se proporciona
    if model_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"rf_model_{timestamp}"

    model_file = f"{model_path}/{model_name}.pkl"
    scaler_file = f"{model_path}/{model_name}_scaler.pkl"

    # Guardar modelo
    joblib.dump(model, model_file)
    logger.info(f"💾 Modelo guardado: {model_file}")

    # Guardar scaler
    joblib.dump(scaler, scaler_file)
    logger.info(f"💾 Scaler guardado: {scaler_file}")

    # Verificar que se pueden cargar
    try:
        loaded_model = joblib.load(model_file)
        loaded_scaler = joblib.load(scaler_file)

        # Quick validation
        test_pred = loaded_model.predict(np.random.randn(5, model.n_features_in_))
        logger.info("✅ Modelo y scaler guardados y validados correctamente")
    except Exception as e:
        logger.error(f"❌ Error al validar archivos guardados: {e}")
        raise

    return model_file


# =============================================================================
# FLOWS PRINCIPALES (Orquestación de tareas)
# =============================================================================

@flow(name="ML Training Pipeline", description="Pipeline completo de entrenamiento de ML")
def ml_training_pipeline(data_path: str, model_name: str = None,
                        model_params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Flow principal para entrenamiento completo de ML.

    Args:
        data_path: Ruta al archivo CSV con datos
        model_name: Nombre del modelo (opcional)
        model_params: Parámetros del modelo (opcional)

    Returns:
        Diccionario con resultados del pipeline
    """
    logger = get_run_logger()
    logger.info("🚀 Iniciando pipeline de entrenamiento ML")

    # Paso 1: Cargar datos
    df = load_data(data_path)

    # Paso 2: Explorar datos
    exploration_results = explore_data(df)

    # Paso 3: Preprocesar datos
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    # Paso 4: Entrenar modelo
    model = train_model(X_train, y_train, model_params)

    # Paso 5: Evaluar modelo
    evaluation_results = evaluate_model(model, X_test, y_test)

    # Paso 6: Guardar modelo
    model_path = save_model(model, scaler, model_name=model_name)

    # Resultado final
    pipeline_results = {
        'model_path': model_path,
        'evaluation': evaluation_results,
        'exploration': exploration_results,
        'training_info': {
            'samples': len(df),
            'features': X_train.shape[1],
            'test_split': len(X_test) / (len(X_train) + len(X_test))
        }
    }

    logger.info("🎉 Pipeline de entrenamiento completado exitosamente!")
    log_ml_metrics({
        "final_accuracy": evaluation_results['accuracy'],
        "model_saved": model_path,
        "total_samples": len(df)
    }, "Pipeline Completion")

    return pipeline_results


@flow(name="ML Batch Prediction", description="Pipeline para predicciones por lotes")
def batch_prediction_pipeline(model_path: str, data_path: str,
                            output_path: str = "predictions") -> str:
    """
    Flow para realizar predicciones por lotes.

    Args:
        model_path: Ruta al modelo guardado
        data_path: Ruta a los datos para predecir
        output_path: Directorio donde guardar predicciones

    Returns:
        Ruta del archivo de predicciones
    """
    logger = get_run_logger()
    logger.info("🔮 Iniciando pipeline de predicciones por lotes")

    # Cargar modelo y scaler
    model = joblib.load(model_path)
    scaler_path = model_path.replace('.pkl', '_scaler.pkl')
    scaler = joblib.load(scaler_path)

    # Cargar datos
    df = load_data(data_path)

    # Preprocesar (sin target si no existe)
    if 'target' in df.columns:
        X = df.drop(columns=['target'])
    else:
        X = df

    # Escalar
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        X_scaled = X.copy()
        X_scaled[numeric_cols] = scaler.transform(X[numeric_cols])
    else:
        X_scaled = X

    # Predecir
    predictions = model.predict(X_scaled.values)
    probabilities = model.predict_proba(X_scaled.values) if hasattr(model, 'predict_proba') else None

    # Crear DataFrame de resultados
    results_df = df.copy()
    results_df['prediction'] = predictions

    if probabilities is not None:
        for i, class_prob in enumerate(probabilities.T):
            results_df[f'probability_class_{i}'] = class_prob

    # Guardar resultados
    os.makedirs(output_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_path}/predictions_{timestamp}.csv"
    results_df.to_csv(output_file, index=False)

    logger.info(f"💾 Predicciones guardadas: {output_file}")
    logger.info(f"📊 Total predicciones: {len(predictions)}")

    log_ml_metrics({
        "predictions_count": len(predictions),
        "output_file": output_file,
        "has_probabilities": probabilities is not None
    }, "Batch Prediction")

    return output_file


# =============================================================================
# UTILITIES PARA DESARROLLO
# =============================================================================

if __name__ == "__main__":
    # Configuración para desarrollo local
    from . import setup_prefect
    setup_prefect()

    # Crear datos de ejemplo si no existen
    example_data = "data/sample_data.csv"
    if not os.path.exists(example_data):
        from src.data_utils import generate_sample_data
        os.makedirs("data", exist_ok=True)
        df = generate_sample_data(n_samples=1000, n_features=8, random_state=42)
        df.to_csv(example_data, index=False)
        print(f"📄 Datos de ejemplo creados: {example_data}")

    # Ejecutar flujo de ejemplo
    print("🚀 Ejecutando flujo de ejemplo...")
    results = ml_training_pipeline(data_path=example_data, model_name="example_model")

    print("✅ Flujo completado!")
    print(f"📊 Accuracy final: {results['evaluation']['accuracy']:.4f}")
    print(f"💾 Modelo guardado: {results['model_path']}")