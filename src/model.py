"""
Módulo de modelo de Machine Learning.
Ejemplo práctico para testing y CI/CD.
"""

import os
from typing import Any, Dict, Union

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


class MLModel:
    """Clase wrapper para modelos de ML con funcionalidades de evaluación."""

    def __init__(self, model_type: str = "random_forest", **kwargs):
        """
        Inicializa el modelo.

        Args:
            model_type: Tipo de modelo ('random_forest' o 'logistic_regression')
            **kwargs: Parámetros del modelo
        """
        self.model_type = model_type
        self.model_params = kwargs

        if model_type == "random_forest":
            default_params = {"n_estimators": 100, "random_state": 42}
            default_params.update(kwargs)
            self.model = RandomForestClassifier(**default_params)
        elif model_type == "logistic_regression":
            default_params = {"random_state": 42, "max_iter": 1000}
            default_params.update(kwargs)
            self.model = LogisticRegression(**default_params)
        else:
            raise ValueError(f"Modelo {model_type} no soportado")

        self.is_trained = False

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Entrena el modelo.

        Args:
            X_train: Features de entrenamiento
            y_train: Target de entrenamiento
        """
        print(f"🏋️ Entrenando modelo {self.model_type}...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("✅ Modelo entrenado exitosamente")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Realiza predicciones.

        Args:
            X: Features para predecir

        Returns:
            Predicciones del modelo
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado aún")

        return self.model.predict(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """
        Evalúa el modelo en datos de test.

        Args:
            X_test: Features de test
            y_test: Target de test

        Returns:
            Dict con métricas de evaluación
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado aún")

        y_pred = self.predict(X_test)

        # Calcular métricas
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, output_dict=True)

        results = {
            "accuracy": accuracy,
            "confusion_matrix": conf_matrix.tolist(),
            "classification_report": class_report,
            "predictions": y_pred.tolist()[:10],  # Primeras 10 predicciones
            "true_values": y_test.tolist()[:10],  # Primeros 10 valores reales
        }

        print(f"📊 Accuracy del modelo: {accuracy:.4f}")
        return results

    def save_model(self, filepath: str) -> None:
        """
        Guarda el modelo entrenado.

        Args:
            filepath: Ruta donde guardar el modelo
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado aún")

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Guardar modelo
        joblib.dump(self.model, filepath)
        print(f"💾 Modelo guardado en {filepath}")

    def load_model(self, filepath: str) -> None:
        """
        Carga un modelo guardado.

        Args:
            filepath: Ruta del modelo guardado
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Archivo {filepath} no encontrado")

        self.model = joblib.load(filepath)
        self.is_trained = True
        print(f"📂 Modelo cargado desde {filepath}")

    def validate_model_loading(self) -> bool:
        """
        Valida que el modelo se puede cargar correctamente.

        Returns:
            True si el modelo está operativo
        """
        try:
            # Crear datos dummy para test
            X_dummy = np.random.randn(10, 4)
            predictions = self.predict(X_dummy)
            return len(predictions) == 10
        except Exception as e:
            print(f"❌ Error validando modelo: {e}")
            return False


def create_and_train_model(
    X_train: np.ndarray, y_train: np.ndarray, model_type: str = "random_forest"
) -> MLModel:
    """
    Función helper para crear y entrenar un modelo.

    Args:
        X_train: Features de entrenamiento
        y_train: Target de entrenamiento
        model_type: Tipo de modelo

    Returns:
        Modelo entrenado
    """
    model = MLModel(model_type=model_type)
    model.train(X_train, y_train)
    return model


if __name__ == "__main__":
    # Demo del módulo
    print("🚀 Demo del módulo de modelo ML")

    # Crear datos de ejemplo
    from data_utils import generate_sample_data, preprocess_data

    df = generate_sample_data(n_samples=200)
    X_train, X_test, y_train, y_test, _ = preprocess_data(df)

    # Crear y entrenar modelo
    model = create_and_train_model(X_train, y_train, model_type="random_forest")

    # Evaluar modelo
    results = model.evaluate(X_test, y_test)
    print(f"🎯 Accuracy final: {results['accuracy']:.4f}")

    # Guardar modelo
    model.save_model("models/demo_model.pkl")

    # Validar carga
    new_model = MLModel()
    new_model.load_model("models/demo_model.pkl")
    is_valid = new_model.validate_model_loading()
    print(f"✅ Modelo válido después de carga: {is_valid}")
