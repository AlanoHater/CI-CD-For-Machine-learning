#!/usr/bin/env python3
"""
Demo completo de pipeline ML
Ejemplo para testing y validación en CI/CD
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_utils import generate_sample_data, preprocess_data, validate_data_integrity
from src.model import MLModel, create_and_train_model
import numpy as np


def main():
    """Ejecutar demo completo del pipeline ML."""
    print("🚀 Iniciando demo del pipeline ML...")
    print("=" * 50)

    # Inicializar variables
    accuracy = 0.0
    final_status = "FAILED"

    # Paso 1: Generar datos
    print("\n📊 Paso 1: Generación de datos")
    df = generate_sample_data(n_samples=500, n_features=6, random_state=42)
    print(f"✅ Generados {len(df)} samples con {len(df.columns)-1} features")

    # Paso 2: Validar integridad
    print("\n🔍 Paso 2: Validación de datos")
    validation = validate_data_integrity(df)
    print(f"✅ Validación completa: {validation['n_rows']} filas, {validation['n_cols']} columnas")
    print(f"   📈 Balance de clases: {validation['class_balance']}")

    # Paso 3: Preprocesamiento
    print("\n⚙️ Paso 3: Preprocesamiento")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    print(f"✅ Datos preprocesados: Train {X_train.shape}, Test {X_test.shape}")

    # Paso 4: Entrenamiento de modelo
    print("\n🏋️ Paso 4: Entrenamiento de modelo")
    model = create_and_train_model(X_train, y_train, model_type='random_forest')
    print("✅ Modelo entrenado exitosamente")

    # Paso 5: Evaluación
    print("\n📊 Paso 5: Evaluación del modelo")
    results = model.evaluate(X_test, y_test)
    accuracy = results['accuracy']
    print(f"📊 Accuracy del modelo: {accuracy:.4f}")
    
    # Paso 6: Validación de calidad
    print("\n🎯 Paso 6: Validación de calidad")
    min_accuracy_threshold = 0.5  # Threshold mínimo para considerar el modelo válido
    if accuracy >= min_accuracy_threshold:
        print(f"✅ Modelo aprobado - Accuracy {accuracy:.4f} >= {min_accuracy_threshold}")
        status = "SUCCESS"
    else:
        print(f"❌ Modelo rechazado - Accuracy insuficiente ({accuracy:.4f} < {min_accuracy_threshold})")
        status = "FAILED"

    # Paso 7: Guardado de modelo
    if status == "SUCCESS":
        print("\n💾 Paso 7: Guardado de modelo")
        model.save_model('models/demo_model.pkl')
        print("✅ Modelo guardado exitosamente")

        # Paso 8: Validación de carga
        print("\n🔄 Paso 8: Validación de carga")
        new_model = MLModel()
        new_model.load_model('models/demo_model.pkl')
        is_valid = new_model.validate_model_loading()

        if is_valid:
            print("✅ Modelo válido después de carga")
            final_status = "SUCCESS"
        else:
            print("❌ Error en validación de carga")
            final_status = "FAILED"
    else:
        final_status = "FAILED"

    # Resultado final
    print("\n" + "=" * 50)
    if final_status == "SUCCESS":
        print("🎉 ¡PIPELINE ML COMPLETADO EXITOSAMENTE!")
        print(f"📊 Accuracy final: {accuracy:.4f}")
        print("📈 El modelo está listo para producción")
        return 0
    else:
        print("💥 PIPELINE ML FALLÓ")
        print(f"📊 Accuracy final: {accuracy:.4f}")
        print("🔧 Revisar configuración y datos")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
