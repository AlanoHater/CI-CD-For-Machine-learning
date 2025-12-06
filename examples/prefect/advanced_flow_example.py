#!/usr/bin/env python3
"""
Ejemplo avanzado de Prefect Flow
Demuestra manejo de estados, errores y reintentos
"""

from prefect import flow, task
from prefect.states import Completed, Failed
from typing import Dict, Any
import random
import time


@task(name="Unstable Task", description="Tarea que puede fallar aleatoriamente")
def unstable_task(task_id: str, failure_rate: float = 0.3) -> str:
    """
    Tarea que falla aleatoriamente para demostrar reintentos.

    Args:
        task_id: Identificador de la tarea
        failure_rate: Probabilidad de fallo (0-1)
    """
    print(f"🎲 Ejecutando tarea inestable {task_id}...")

    if random.random() < failure_rate:
        raise Exception(f"💥 Tarea {task_id} falló aleatoriamente!")

    result = f"✅ Tarea {task_id} completada exitosamente"
    print(result)
    return result


@task(name="Process Data", description="Procesa datos con validación")
def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa datos con validación y transformación.

    Args:
        data: Datos a procesar

    Returns:
        Datos procesados
    """
    print(f"⚙️ Procesando datos: {data}")

    # Validación
    if 'value' not in data:
        raise ValueError("❌ Datos inválidos: falta campo 'value'")

    if not isinstance(data['value'], (int, float)):
        raise TypeError("❌ Tipo de dato inválido para 'value'")

    # Procesamiento
    processed = data.copy()
    processed['processed_value'] = data['value'] * 2
    processed['status'] = 'processed'
    processed['timestamp'] = time.time()

    print(f"✅ Datos procesados: {processed}")
    return processed


@task(name="Save Results", description="Guarda resultados en 'base de datos'")
def save_results(results: Dict[str, Any]) -> str:
    """
    Simula guardar resultados en una base de datos.

    Args:
        results: Resultados a guardar

    Returns:
        ID de guardado simulado
    """
    print(f"💾 Guardando resultados: {results}")

    # Simular operación de BD
    save_id = f"save_{int(time.time())}_{random.randint(1000, 9999)}"

    print(f"✅ Resultados guardados con ID: {save_id}")
    return save_id


@flow(name="Advanced Flow with Error Handling",
      description="Flujo avanzado con manejo de errores y reintentos")
def advanced_flow_with_error_handling(num_tasks: int = 3) -> Dict[str, Any]:
    """
    Flujo que demuestra manejo avanzado de errores y estados.

    Args:
        num_tasks: Número de tareas inestables a ejecutar

    Returns:
        Resultado del flujo con información de ejecución
    """
    print(f"🚀 Iniciando flujo avanzado con {num_tasks} tareas")
    print("=" * 60)

    results = {
        'successful_tasks': [],
        'failed_tasks': [],
        'processed_data': [],
        'saved_ids': []
    }

    try:
        # Paso 1: Ejecutar tareas inestables (algunas pueden fallar)
        print("\n📋 Paso 1: Ejecutando tareas inestables")
        for i in range(num_tasks):
            try:
                result = unstable_task(f"task_{i+1}", failure_rate=0.4)
                results['successful_tasks'].append(f"task_{i+1}")
                print(f"✅ Task {i+1} completada")
            except Exception as e:
                results['failed_tasks'].append(f"task_{i+1}")
                print(f"❌ Task {i+1} falló: {e}")
                # Continuar con otras tareas

        # Paso 2: Procesar datos si al menos una tarea fue exitosa
        print("
📋 Paso 2: Procesando datos"        if len(results['successful_tasks']) > 0:
            for i, task_name in enumerate(results['successful_tasks']):
                data = {
                    'task': task_name,
                    'value': (i + 1) * 10,
                    'metadata': {'attempt': i + 1}
                }

                try:
                    processed = process_data(data)
                    results['processed_data'].append(processed)
                    print(f"✅ Datos de {task_name} procesados")
                except Exception as e:
                    print(f"❌ Error procesando datos de {task_name}: {e}")
        else:
            print("⚠️ No hay tareas exitosas para procesar")

        # Paso 3: Guardar resultados si hay datos procesados
        print("
📋 Paso 3: Guardando resultados"        if len(results['processed_data']) > 0:
            for data in results['processed_data']:
                try:
                    save_id = save_results(data)
                    results['saved_ids'].append(save_id)
                    print(f"✅ Datos guardados con ID: {save_id}")
                except Exception as e:
                    print(f"❌ Error guardando datos: {e}")
        else:
            print("⚠️ No hay datos procesados para guardar")

        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL FLUJO")
        print("=" * 60)
        print(f"✅ Tareas exitosas: {len(results['successful_tasks'])}")
        print(f"❌ Tareas fallidas: {len(results['failed_tasks'])}")
        print(f"📦 Datos procesados: {len(results['processed_data'])}")
        print(f"💾 Registros guardados: {len(results['saved_ids'])}")

        if len(results['saved_ids']) > 0:
            print("\n🎉 ¡Flujo completado exitosamente!")
            return results
        else:
            print("\n⚠️ Flujo completado con limitaciones")
            return results

    except Exception as e:
        print(f"\n💥 Error crítico en el flujo: {e}")
        raise


@flow(name="Retry Flow", description="Flujo que demuestra reintentos automáticos")
def retry_flow(max_attempts: int = 3) -> str:
    """
    Flujo que demuestra reintentos automáticos en caso de fallo.

    Args:
        max_attempts: Número máximo de intentos

    Returns:
        Resultado del flujo
    """
    print(f"🔄 Iniciando flujo con reintentos (máx {max_attempts} intentos)")

    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        print(f"🎯 Intento {attempt}/{max_attempts}")

        try:
            result = unstable_task("retry_task", failure_rate=0.7)
            print(f"✅ Éxito en intento {attempt}")
            return f"Completado en intento {attempt}: {result}"

        except Exception as e:
            print(f"❌ Intento {attempt} falló: {e}")
            if attempt < max_attempts:
                wait_time = attempt * 2  # Espera incremental
                print(f"⏳ Esperando {wait_time}s antes del siguiente intento...")
                time.sleep(wait_time)
            else:
                print("💥 Todos los intentos fallaron")
                raise Exception(f"Falló después de {max_attempts} intentos")


if __name__ == "__main__":
    print("🚀 Ejecutando ejemplos avanzados de Prefect")
    print("=" * 60)

    # Ejemplo 1: Flujo con manejo de errores
    print("\n🎭 EJEMPLO 1: Flujo con Manejo de Errores")
    print("-" * 40)
    result1 = advanced_flow_with_error_handling(num_tasks=5)

    print(f"\n📊 Resultados: {len(result1['successful_tasks'])} exitosas, {len(result1['failed_tasks'])} fallidas")

    # Ejemplo 2: Flujo con reintentos
    print("\n🔄 EJEMPLO 2: Flujo con Reintentos")
    print("-" * 40)
    result2 = retry_flow(max_attempts=3)

    print(f"📊 Resultado: {result2}")

    print("\n" + "=" * 60)
    print("🎉 ¡Ejemplos avanzados completados!")
    print("\n💡 Conceptos demostrados:")
    print("  • Manejo de errores y excepciones")
    print("  • Estados de tareas (éxito/fallo)")
    print("  • Reintentos automáticos")
    print("  • Logging detallado")
    print("  • Flujos robustos y fault-tolerant")
