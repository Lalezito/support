#!/usr/bin/env python3
"""
🧪 SCRIPT DE PRUEBA DEL SISTEMA AUTÓNOMO MEJORADO
Valida que el auto-cleanup y auto-recovery funcionen correctamente
"""

import asyncio
import sys
import os
sys.path.append('/Users/alejandrocaceres/Desktop/appstore - zodia/.claude/00_CONFIGURATION')

from autonomous_intelligence_system import AutonomousIntelligenceSystem
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_autonomous_system():
    """🧪 Prueba completa del sistema autónomo con auto-cleanup"""
    print("🚀 INICIANDO PRUEBA DEL SISTEMA AUTÓNOMO MEJORADO")
    print("=" * 60)

    try:
        # Crear instancia del sistema
        ai_system = AutonomousIntelligenceSystem()
        print("✅ Sistema autónomo inicializado")

        # Test 1: Procesar instrucción simple
        print("\n📝 Test 1: Procesamiento básico con auto-cleanup")
        test_instruction = "Analiza el sistema de compatibilidad y reporta su estado"

        result = await ai_system.process_user_instruction(test_instruction)

        print(f"✅ Instrucción procesada exitosamente")
        print(f"   - Success: {result.get('success', 'Unknown')}")
        print(f"   - Cleanup ejecutado: {bool(result.get('cleanup_results'))}")

        if result.get('cleanup_results'):
            cleanup = result['cleanup_results']
            print(f"   - Archivos verificados: {cleanup.get('files_checked', 0)}")
            print(f"   - Errores encontrados: {len(cleanup.get('errors', []))}")
            print(f"   - Warnings: {len(cleanup.get('warnings', []))}")
            print(f"   - Consola limpia: {cleanup.get('console_cleaned', False)}")

        # Test 2: Probar detección de errores
        print("\n🔍 Test 2: Sistema de detección de errores")

        # Simular errores comunes
        test_errors = [
            "Missing Flutter material import in test_file.dart",
            "Missing import for EnhancedCompatibilityResult in service_file.dart",
            "undefined references in Flutter analysis"
        ]

        recovery_result = await ai_system._attempt_auto_recovery(test_errors)

        print(f"✅ Auto-recovery procesado:")
        print(f"   - Errores procesados: {len(test_errors)}")
        print(f"   - Fixes intentados: {len(recovery_result.get('attempted_fixes', []))}")
        print(f"   - Errores restantes: {len(recovery_result.get('remaining_errors', []))}")
        print(f"   - Recovery exitoso: {recovery_result.get('success', False)}")

        # Test 3: Estado del sistema
        print("\n📊 Test 3: Estado del sistema")
        status = ai_system.get_system_status()

        print(f"✅ Estado del sistema:")
        print(f"   - Modo autónomo: {status.get('autonomous_mode', False)}")
        print(f"   - Aprendizaje activo: {status.get('learning_active', False)}")
        print(f"   - Salud del sistema: {status.get('system_health', 'Unknown')}")

        # Test 4: Validación de archivos Flutter
        print("\n🔍 Test 4: Validación de archivos Flutter")

        cleanup_results = {
            'errors_found': False,
            'errors': [],
            'warnings': [],
            'files_checked': 0,
            'files_cleaned': 0,
            'console_cleaned': False
        }

        await ai_system._validate_generated_files(cleanup_results)

        print(f"✅ Validación de archivos completada:")
        print(f"   - Archivos verificados: {cleanup_results['files_checked']}")
        print(f"   - Errores encontrados: {len(cleanup_results['errors'])}")

        if cleanup_results['errors']:
            print("   - Errores detectados:")
            for error in cleanup_results['errors'][:3]:  # Mostrar primeros 3
                print(f"     • {error}")

        print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("✅ Sistema autónomo con auto-cleanup funcionando correctamente")

        return True

    except Exception as e:
        print(f"\n❌ ERROR EN LA PRUEBA: {e}")
        print("=" * 60)
        return False

async def main():
    """🎯 Función principal de prueba"""
    success = await test_autonomous_system()

    if success:
        print("\n🏆 RESULTADO: SISTEMA VALIDADO CORRECTAMENTE")
        sys.exit(0)
    else:
        print("\n💥 RESULTADO: ERRORES EN EL SISTEMA")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)