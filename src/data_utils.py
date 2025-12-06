"""
Utilidades para procesamiento de datos en Machine Learning.
Módulo de ejemplo para el aprendizaje de GitHub Actions.
"""

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def generate_sample_data(
    n_samples: int = 1000, n_features: int = 4, random_state: int = 42
) -> pd.DataFrame:
    """
    Genera datos sintéticos para testing de ML.

    Args:
        n_samples: Número de muestras
        n_features: Número de features
        random_state: Semilla para reproducibilidad

    Returns:
        DataFrame con datos sintéticos
    """
    np.random.seed(random_state)

    # Generar features
    X = np.random.randn(n_samples, n_features)

    # Crear target basado en features (con algo de ruido)
    y = (X[:, 0] + X[:, 1] * 0.5 + np.random.randn(n_samples) * 0.1 > 0).astype(int)

    # Crear DataFrame
    columns = [f"feature_{i}" for i in range(n_features)]
    df = pd.DataFrame(X, columns=columns)
    df["target"] = y

    return df


def preprocess_data(
    df: pd.DataFrame, target_col: str = "target"
) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocesa datos para ML: split y escalado.

    Args:
        df: DataFrame con datos
        target_col: Nombre de la columna target

    Returns:
        Tuple de (X_train, X_test, y_train, y_test, scaler)
    """
    # Separar features y target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Escalar features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train.values, y_test.values, scaler


def validate_data_integrity(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Valida la integridad de los datos.

    Args:
        df: DataFrame a validar

    Returns:
        Dict con resultados de validación
    """
    validation_results = {
        "n_rows": len(df),
        "n_cols": len(df.columns),
        "missing_values": df.isnull().sum().sum(),
        "duplicate_rows": df.duplicated().sum(),
        "data_types": df.dtypes.to_dict(),
    }

    # Validar que no hay valores infinitos
    validation_results["infinite_values"] = (
        np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
    )

    # Validar balance de clases (si hay columna target)
    if "target" in df.columns:
        class_counts = df["target"].value_counts()
        validation_results["class_balance"] = class_counts.to_dict()
        validation_results["min_class_ratio"] = class_counts.min() / class_counts.max()

    return validation_results

import os
def save_processed_data(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    scaler: StandardScaler,
    # 📝 CAMBIO FORZADO PARA CI
    os.makedirs(output_path, exist_ok=True)
    output_path: str = "data/processed/",
) -> None:
    """
    Guarda datos procesados en archivos.

    Args:
        X_train: Features de entrenamiento
        X_test: Features de test
        y_train: Target de entrenamiento
        y_test: Target de test
        scaler: Scaler fitted
        output_path: Directorio de salida
    """
    import os

    os.makedirs(output_path, exist_ok=True)

    # Guardar arrays
    np.save(f"{output_path}X_train.npy", X_train)
    np.save(f"{output_path}X_test.npy", X_test)
    np.save(f"{output_path}y_train.npy", y_train)
    np.save(f"{output_path}y_test.npy", y_test)

    # Guardar scaler
    import joblib

    joblib.dump(scaler, f"{output_path}scaler.pkl")

    print(f"✅ Datos guardados en {output_path}")


if __name__ == "__main__":
    # Demo del módulo
    print("🔄 Generando datos de ejemplo...")
    df = generate_sample_data(n_samples=100)

    print("🔍 Validando integridad...")
    validation = validate_data_integrity(df)
    print(
        f"✅ Validación completa: {validation['n_rows']} filas, {validation['n_cols']} columnas"
    )

    print("⚙️ Preprocesando datos...")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    print(f"📊 Datos procesados: Train {X_train.shape}, Test {X_test.shape}")

    print("💾 Guardando datos...")
    save_processed_data(X_train, X_test, y_train, y_test, scaler)
