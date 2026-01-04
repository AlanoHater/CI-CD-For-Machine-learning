"""
Tests para el módulo data_utils.py
Ejemplos de tests unitarios para el aprendizaje de CI/CD
"""
import os # <--- AGREGAR
import shutil # <--- AGREGAR
import tempfile # <--- AGREGAR
import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from src.data_utils import (
    generate_sample_data,
    preprocess_data,
    validate_data_integrity,
)


class TestGenerateSampleData:
    """Tests para la función generate_sample_data."""

    def test_generate_sample_data_basic(self):
        """Test generación básica de datos."""
        df = generate_sample_data(n_samples=100, n_features=4)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100
        assert "target" in df.columns
        assert len(df.columns) == 5  # 4 features + 1 target

    def test_generate_sample_data_reproducibility(self):
        """Test que los datos sean reproducibles con misma semilla."""
        df1 = generate_sample_data(n_samples=50, random_state=42)
        df2 = generate_sample_data(n_samples=50, random_state=42)

        pd.testing.assert_frame_equal(df1, df2)

    def test_generate_sample_data_target_values(self):
        """Test que target tenga valores binarios."""
        df = generate_sample_data(n_samples=100)

        assert df["target"].isin([0, 1]).all()
        assert (
            len(df["target"].unique()) <= 2
        )  # Puede tener solo una clase en datasets pequeños


class TestPreprocessData:
    """Tests para la función preprocess_data."""

    def test_preprocess_data_output_shapes(self):
        """Test que las formas de los arrays sean correctas."""
        df = generate_sample_data(n_samples=100, n_features=4)

        X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

        # Verificar formas
        assert X_train.shape[0] == y_train.shape[0]  # Mismas filas
        assert X_test.shape[0] == y_test.shape[0]  # Mismas filas
        assert X_train.shape[1] == X_test.shape[1] == 4  # Mismas columnas
        assert isinstance(scaler, StandardScaler)

    def test_preprocess_data_split_ratio(self):
        """Test que el split train/test sea correcto."""
        df = generate_sample_data(n_samples=100)

        X_train, X_test, y_train, y_test, _ = preprocess_data(df)

        # Verificar proporción aproximada 80/20
        total_samples = len(df)
        expected_train = int(total_samples * 0.8)
        expected_test = total_samples - expected_train

        assert abs(len(X_train) - expected_train) <= 1  # Tolerancia de 1
        assert abs(len(X_test) - expected_test) <= 1

    def test_preprocess_data_scaling(self):
        """Test que los datos estén escalados correctamente."""
        df = generate_sample_data(n_samples=100, n_features=2)

        X_train, X_test, _, _, scaler = preprocess_data(df)

        # Verificar que la media sea aproximadamente 0 y std aproximadamente 1
        assert abs(X_train.mean()) < 0.1  # Media cercana a 0
        assert abs(X_train.std() - 1.0) < 0.1  # Std cercana a 1


class TestValidateDataIntegrity:
    """Tests para la función validate_data_integrity."""

    def test_validate_data_integrity_complete_data(self):
        """Test validación de datos completos."""
        df = generate_sample_data(n_samples=50, n_features=3)

        result = validate_data_integrity(df)

        # Verificar estructura del resultado
        required_keys = [
            "n_rows",
            "n_cols",
            "missing_values",
            "duplicate_rows",
            "data_types",
            "infinite_values",
        ]
        for key in required_keys:
            assert key in result

        # Verificar valores
        assert result["n_rows"] == 50
        assert result["n_cols"] == 4  # 3 features + 1 target
        assert result["missing_values"] == 0
        assert result["duplicate_rows"] == 0
        assert result["infinite_values"] == 0

    def test_validate_data_integrity_with_target(self):
        """Test validación incluye información de clases cuando hay target."""
        df = generate_sample_data(n_samples=100)

        result = validate_data_integrity(df)

        assert "class_balance" in result
        assert "min_class_ratio" in result
        assert isinstance(result["class_balance"], dict)
        assert 0 < result["min_class_ratio"] <= 1

    def test_validate_data_integrity_missing_values(self):
        """Test detección de valores faltantes."""
        df = generate_sample_data(n_samples=50)
        df.loc[0, "feature_0"] = np.nan  # Agregar valor faltante

        result = validate_data_integrity(df)

        assert result["missing_values"] == 1

    def test_validate_data_integrity_duplicates(self):
        """Test detección de filas duplicadas."""
        df = generate_sample_data(n_samples=50)
        # Agregar fila duplicada
        duplicate_row = df.iloc[0].copy()
        df = pd.concat([df, pd.DataFrame([duplicate_row])], ignore_index=True)

        result = validate_data_integrity(df)

        assert result["duplicate_rows"] >= 1  # Al menos una fila duplicada


# Tests de integración
class TestDataUtilsIntegration:
    """Tests de integración para el flujo completo de data_utils."""

    def test_complete_data_pipeline(self):
        """Test del pipeline completo de procesamiento de datos."""
        # Generar datos
        df = generate_sample_data(n_samples=200, n_features=4, random_state=42)

        # Validar integridad
        validation = validate_data_integrity(df)
        assert validation["missing_values"] == 0
        assert validation["n_rows"] == 200

        # Preprocesar
        X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

        # Verificar consistencia
        assert len(X_train) + len(X_test) == len(df)
        assert len(y_train) + len(y_test) == len(df)
        assert X_train.shape[1] == X_test.shape[1] == 4

        # Verificar escalado
        assert abs(X_train.mean()) < 0.1
        assert abs(X_train.std() - 1.0) < 0.1

    def test_data_pipeline_reproducibility(self):
        """Test que el pipeline completo sea reproducible."""
        # Ejecutar pipeline dos veces
        df1 = generate_sample_data(n_samples=100, random_state=123)
        X_train1, X_test1, y_train1, y_test1, _ = preprocess_data(df1)

        df2 = generate_sample_data(n_samples=100, random_state=123)
        X_train2, X_test2, y_train2, y_test2, _ = preprocess_data(df2)

        # Verificar que los resultados sean idénticos
        np.testing.assert_array_equal(X_train1, X_train2)
        np.testing.assert_array_equal(X_test1, X_test2)
        np.testing.assert_array_equal(y_train1, y_train2)
        np.testing.assert_array_equal(y_test1, y_test2)

class TestSaveProcessedData:
    """Tests para la función save_processed_data."""

    def setup_method(self):
        """Generar datos de ejemplo y crear directorio temporal."""
        from src.data_utils import generate_sample_data, preprocess_data

        self.df = generate_sample_data(n_samples=20, n_features=3, random_state=1)
        self.X_train, self.X_test, self.y_train, self.y_test, self.scaler = preprocess_data(self.df)

        self.temp_dir = tempfile.mkdtemp()
        self.output_path = self.temp_dir + os.sep 

    def teardown_method(self):
        """Eliminar el directorio temporal."""
        shutil.rmtree(self.temp_dir)

    def test_save_processed_data_creates_files(self):
        """Test que la función guarda todos los archivos esperados."""
        from src.data_utils import save_processed_data

        save_processed_data(
            self.X_train, self.X_test, self.y_train, self.y_test, self.scaler, self.output_path
        )

        expected_files = [
            "X_train.npy",
            "X_test.npy",
            "y_train.npy",
            "y_test.npy",
            "scaler.pkl",
        ]

        for filename in expected_files:
            file_path = os.path.join(self.output_path, filename)
            assert os.path.exists(file_path)

    def test_saved_data_can_be_loaded_correctly(self):
        """Test que los archivos guardados pueden ser cargados y mantienen sus formas."""
        from src.data_utils import save_processed_data
        from sklearn.preprocessing import StandardScaler

        save_processed_data(
            self.X_train, self.X_test, self.y_train, self.y_test, self.scaler, self.output_path
        )

        X_train_loaded = np.load(os.path.join(self.output_path, "X_train.npy"))
        scaler_loaded = joblib.load(os.path.join(self.output_path, "scaler.pkl"))

        np.testing.assert_array_equal(self.X_train, X_train_loaded)
        assert isinstance(scaler_loaded, StandardScaler)
if __name__ == "__main__":
    # Ejecutar tests si se corre directamente
    pytest.main([__file__, "-v"])
