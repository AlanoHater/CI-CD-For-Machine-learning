"""
Tests para el módulo model.py
Tests de modelos ML para el aprendizaje de CI/CD
"""

import pytest
import numpy as np
import os
import tempfile
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from src.model import MLModel, create_and_train_model
from src.data_utils import generate_sample_data, preprocess_data


class TestMLModel:
    """Tests para la clase MLModel."""

    def setup_method(self):
        """Setup antes de cada test."""
        self.X_train = np.random.randn(50, 4)
        self.y_train = np.random.randint(0, 2, 50)
        self.X_test = np.random.randn(20, 4)
        self.y_test = np.random.randint(0, 2, 20)

    def test_init_random_forest(self):
        """Test inicialización de modelo Random Forest."""
        model = MLModel(model_type='random_forest', n_estimators=50)

        assert isinstance(model.model, RandomForestClassifier)
        assert model.model.n_estimators == 50
        assert not model.is_trained

    def test_init_logistic_regression(self):
        """Test inicialización de modelo Logistic Regression."""
        model = MLModel(model_type='logistic_regression', max_iter=500)

        assert isinstance(model.model, LogisticRegression)
        assert model.model.max_iter == 500
        assert not model.is_trained

    def test_init_invalid_model_type(self):
        """Test que modelo inválido lance error."""
        with pytest.raises(ValueError, match="Modelo .* no soportado"):
            MLModel(model_type='invalid_model')

    def test_train_model(self):
        """Test entrenamiento básico del modelo."""
        model = MLModel(model_type='random_forest')

        model.train(self.X_train, self.y_train)

        assert model.is_trained

    def test_predict_without_training(self):
        """Test que predict lance error si modelo no está entrenado."""
        model = MLModel()

        with pytest.raises(ValueError, match="no ha sido entrenado"):
            model.predict(self.X_test)

    def test_predict_after_training(self):
        """Test predicciones después del entrenamiento."""
        model = MLModel()
        model.train(self.X_train, self.y_train)

        predictions = model.predict(self.X_test)

        assert len(predictions) == len(self.X_test)
        assert all(pred in [0, 1] for pred in predictions)

    def test_evaluate_without_training(self):
        """Test que evaluate lance error si modelo no está entrenado."""
        model = MLModel()

        with pytest.raises(ValueError, match="no ha sido entrenado"):
            model.evaluate(self.X_test, self.y_test)

    def test_evaluate_after_training(self):
        """Test evaluación completa del modelo."""
        model = MLModel()
        model.train(self.X_train, self.y_train)

        results = model.evaluate(self.X_test, self.y_test)

        # Verificar estructura del resultado
        required_keys = ['accuracy', 'confusion_matrix', 'classification_report', 'predictions', 'true_values']
        for key in required_keys:
            assert key in results

        # Verificar valores
        assert isinstance(results['accuracy'], float)
        assert 0 <= results['accuracy'] <= 1
        assert isinstance(results['confusion_matrix'], list)
        assert len(results['predictions']) == 10  # Primeras 10 predicciones
        assert len(results['true_values']) == 10   # Primeros 10 valores reales

    def test_save_model_without_training(self):
        """Test que save lance error si modelo no está entrenado."""
        model = MLModel()

        with pytest.raises(ValueError, match="no ha sido entrenado"):
            model.save_model('test_model.pkl')

    def test_save_and_load_model(self):
        """Test guardar y cargar modelo."""
        model = MLModel()
        model.train(self.X_train, self.y_train)

        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp:
            model.save_model(tmp.name)

            # Verificar que archivo existe
            assert os.path.exists(tmp.name)

            # Cargar modelo
            new_model = MLModel()
            new_model.load_model(tmp.name)

            # Verificar que está entrenado
            assert new_model.is_trained

            # Verificar que hace predicciones
            predictions = new_model.predict(self.X_test)
            assert len(predictions) == len(self.X_test)

            # Limpiar
            os.unlink(tmp.name)

    def test_load_nonexistent_model(self):
        """Test cargar modelo que no existe."""
        model = MLModel()

        with pytest.raises(FileNotFoundError):
            model.load_model('nonexistent_model.pkl')

    def test_validate_model_loading(self):
        """Test validación de carga de modelo."""
        model = MLModel()
        model.train(self.X_train, self.y_train)

        is_valid = model.validate_model_loading()

        assert isinstance(is_valid, bool)
        assert is_valid  # Debería ser válido

    def test_validate_model_loading_untrained(self):
        """Test validación falla con modelo no entrenado."""
        model = MLModel()

        is_valid = model.validate_model_loading()

        assert isinstance(is_valid, bool)
        assert not is_valid  # Debería fallar


class TestHelperFunctions:
    """Tests para funciones helper del módulo."""

    def test_create_and_train_model(self):
        """Test función helper para crear y entrenar modelo."""
        X_train = np.random.randn(50, 4)
        y_train = np.random.randint(0, 2, 50)

        model = create_and_train_model(X_train, y_train, model_type='random_forest')

        assert isinstance(model, MLModel)
        assert model.is_trained
        assert model.model_type == 'random_forest'


class TestModelIntegration:
    """Tests de integración con datos reales."""

    def test_complete_ml_pipeline(self):
        """Test pipeline completo con datos reales."""
        # Generar datos
        df = generate_sample_data(n_samples=100, n_features=4, random_state=42)
        X_train, X_test, y_train, y_test, _ = preprocess_data(df)

        # Crear y entrenar modelo
        model = create_and_train_model(X_train, y_train)

        # Evaluar
        results = model.evaluate(X_test, y_test)

        # Verificar que accuracy sea razonable (> 0.5)
        assert results['accuracy'] > 0.5

        # Guardar y recargar
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp:
            model.save_model(tmp.name)

            new_model = MLModel()
            new_model.load_model(tmp.name)

            # Verificar funcionamiento
            predictions = new_model.predict(X_test)
            assert len(predictions) == len(X_test)

            os.unlink(tmp.name)

    def test_model_comparison(self):
        """Test comparación entre diferentes tipos de modelo."""
        df = generate_sample_data(n_samples=150, random_state=42)
        X_train, X_test, y_train, y_test, _ = preprocess_data(df)

        # Entrenar Random Forest
        rf_model = create_and_train_model(X_train, y_train, model_type='random_forest')
        rf_results = rf_model.evaluate(X_test, y_test)

        # Entrenar Logistic Regression
        lr_model = create_and_train_model(X_train, y_train, model_type='logistic_regression')
        lr_results = lr_model.evaluate(X_test, y_test)

        # Ambos deberían tener accuracy > 0.4 (umbral bajo para test)
        assert rf_results['accuracy'] > 0.4
        assert lr_results['accuracy'] > 0.4

        # Verificar que las métricas sean números
        assert isinstance(rf_results['accuracy'], (int, float))
        assert isinstance(lr_results['accuracy'], (int, float))


# Benchmarks de performance
class TestModelPerformance:
    """Tests de performance para asegurar eficiencia."""

    def test_training_performance(self):
        """Test que el entrenamiento sea razonablemente rápido."""
        import time

        X_train = np.random.randn(100, 4)
        y_train = np.random.randint(0, 2, 100)

        model = MLModel(model_type='random_forest', n_estimators=10)  # Modelo pequeño

        start_time = time.time()
        model.train(X_train, y_train)
        training_time = time.time() - start_time

        # Entrenamiento debería tomar menos de 1 segundo
        assert training_time < 1.0

    def test_prediction_performance(self):
        """Test que las predicciones sean rápidas."""
        import time

        X_train = np.random.randn(50, 4)
        y_train = np.random.randint(0, 2, 50)
        X_test = np.random.randn(1000, 4)  # Muchas predicciones

        model = MLModel()
        model.train(X_train, y_train)

        start_time = time.time()
        predictions = model.predict(X_test)
        prediction_time = time.time() - start_time

        # 1000 predicciones deberían tomar menos de 0.1 segundos
        assert prediction_time < 0.1
        assert len(predictions) == 1000


if __name__ == "__main__":
    # Ejecutar tests si se corre directamente
    pytest.main([__file__, "-v"])
