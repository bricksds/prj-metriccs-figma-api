#!/usr/bin/env python3
"""
Script de Inicio para la Aplicación Web de Figma Analytics
=========================================================

Ejecuta la aplicación web Flask con configuración automática.
"""

import os
import sys
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    required_packages = ['flask', 'pandas', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Dependencias faltantes:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n💡 Instala las dependencias con:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def create_directories():
    """Crea los directorios necesarios"""
    directories = ['templates', 'temp', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Directorio creado/verificado: {directory}")

def start_application():
    """Inicia la aplicación web"""
    print("\n🚀 INICIANDO APLICACIÓN WEB DE FIGMA ANALYTICS")
    print("=" * 60)
    
    # Verificar que el archivo principal existe
    if not os.path.exists('app.py'):
        print("❌ Error: No se encontró app.py")
        print("💡 Asegúrate de estar en el directorio correcto")
        return False
    
    # Verificar que la plantilla existe
    if not os.path.exists('templates/index.html'):
        print("❌ Error: No se encontró templates/index.html")
        print("💡 Verifica que la estructura de archivos sea correcta")
        return False
    
    print("✅ Archivos verificados correctamente")
    
    try:
        # Importar y ejecutar la aplicación
        from app import app
        
        print("\n📱 Configuración de la aplicación:")
        print(f"   • Host: 0.0.0.0")
        print(f"   • Puerto: 5000")
        print(f"   • URL: http://localhost:5000")
        
        print("\n🌐 Abriendo navegador automáticamente en 3 segundos...")
        time.sleep(3)
        
        # Abrir navegador automáticamente
        webbrowser.open('http://localhost:5000')
        
        print("\n🎯 La aplicación está ejecutándose!")
        print("💡 Presiona Ctrl+C para detener la aplicación")
        print("=" * 60)
        
        # Ejecutar la aplicación
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Error importando la aplicación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 GENERADOR WEB DE FIGMA ANALYTICS")
    print("=" * 60)
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Crear directorios
    create_directories()
    
    # Iniciar aplicación
    start_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación detenida por el usuario")
        print("¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💡 Verifica la configuración y vuelve a intentar")
