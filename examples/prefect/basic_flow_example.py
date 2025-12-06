#!/usr/bin/env python3
"""
Ejemplo básico de Prefect Flow
Demuestra los conceptos fundamentales de Prefect
"""

from prefect import flow, task
from typing import List
import time


@task(name="Add Numbers", description="Suma dos números")
def add_numbers(x: int, y: int) -> int:
    """Suma dos números con logging."""
    result = x + y
    print(f"✅ Sumando {x} + {y} = {result}")
    return result


@task(name="Multiply by Two", description="Multiplica un número por 2")
def multiply_by_two(x: int) -> int:
    """Multiplica un número por 2."""
    result = x * 2
    print(f"✅ Multiplicando {x} × 2 = {result}")
    return result


@task(name="Sum List", description="Suma todos los elementos de una lista")
def sum_list(numbers: List[int]) -> int:
    """Suma todos los elementos de una lista."""
    result = sum(numbers)
    print(f"✅ Sumando lista {numbers} = {result}")
    return result


@flow(name="Basic Math Flow", description="Flujo básico de operaciones matemáticas")
def basic_math_flow(x: int = 5, y: int = 3) -> int:
    """
    Flujo que demuestra operaciones matemáticas básicas con Prefect.

    Args:
        x: Primer número
        y: Segundo número

    Returns:
        Resultado final de las operaciones
    """
    print(f"🚀 Iniciando flujo con x={x}, y={y}")

    # Paso 1: Sumar números
    sum_result = add_numbers(x, y)

    # Paso 2: Multiplicar resultado por 2
    multiplied = multiply_by_two(sum_result)

    # Paso 3: Crear lista y sumar
    numbers_list = [x, y, sum_result, multiplied]
    final_result = sum_list(numbers_list)

    print(f"🎉 Flujo completado! Resultado final: {final_result}")
    return final_result


if __name__ == "__main__":
    # Ejecutar el flujo
    print("🔧 Ejecutando ejemplo básico de Prefect Flow")
    print("=" * 50)

    result = basic_math_flow(x=10, y=5)
    print(f"📊 Resultado final: {result}")

    print("\n💡 Conceptos demostrados:")
    print("  • @task - Funciones atómicas reutilizables")
    print("  • @flow - Orquestación de tareas")
    print("  • Dependencias automáticas entre tareas")
    print("  • Logging automático")
    print("  • Parámetros de flujo")
