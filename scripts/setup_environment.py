#!/usr/bin/env python3
"""
Script para configurar el entorno de desarrollo del framework de automatización QA
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import Config


def setup_logging():
    """Configurar logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logging.error(f"Python 3.8+ requerido. Versión actual: {version.major}.{version.minor}")
        return False
    
    logging.info(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def install_dependencies():
    """Instalar dependencias de Python"""
    try:
        logging.info("Instalando dependencias de Python...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        logging.info("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error instalando dependencias: {e}")
        return False


def install_webdrivers():
    """Instalar drivers de navegadores"""
    try:
        logging.info("Instalando drivers de navegadores...")
        
        # Chrome
        if platform.system() == "Windows":
            # Windows
            chrome_driver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            # Implementar descarga para Windows si es necesario
        elif platform.system() == "Darwin":
            # macOS
            subprocess.run(['brew', 'install', 'chromedriver'], check=True)
        else:
            # Linux
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'chromium-chromedriver'], check=True)
        
        # Firefox
        if platform.system() == "Windows":
            # Windows - descargar geckodriver
            pass
        elif platform.system() == "Darwin":
            # macOS
            subprocess.run(['brew', 'install', 'geckodriver'], check=True)
        else:
            # Linux
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'firefox-geckodriver'], check=True)
        
        logging.info("✅ Drivers de navegadores instalados")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.warning(f"Error instalando drivers: {e}")
        logging.info("Los drivers se instalarán automáticamente durante la ejecución de tests")
        return True


def create_directories():
    """Crear directorios necesarios"""
    try:
        logging.info("Creando directorios necesarios...")
        Config.ensure_directories()
        logging.info("✅ Directorios creados exitosamente")
        return True
    except Exception as e:
        logging.error(f"Error creando directorios: {e}")
        return False


def setup_git_hooks():
    """Configurar hooks de Git"""
    try:
        logging.info("Configurando hooks de Git...")
        
        # Crear directorio de hooks si no existe
        hooks_dir = Path('.git/hooks')
        hooks_dir.mkdir(exist_ok=True)
        
        # Pre-commit hook
        pre_commit_hook = hooks_dir / 'pre-commit'
        with open(pre_commit_hook, 'w') as f:
            f.write('''#!/bin/bash
# Pre-commit hook para el framework de automatización QA

echo "Ejecutando pre-commit checks..."

# Ejecutar linting
python -m flake8 pages/ utils/ tests/ --max-line-length=120 --ignore=E501,W503

# Ejecutar tests de humo
python scripts/run_tests.py --test-suite=smoke --browser=chrome --headless

echo "Pre-commit checks completados"
''')
        
        # Hacer ejecutable
        os.chmod(pre_commit_hook, 0o755)
        
        logging.info("✅ Hooks de Git configurados")
        return True
        
    except Exception as e:
        logging.warning(f"Error configurando hooks de Git: {e}")
        return True


def setup_ide_config():
    """Configurar archivos de IDE"""
    try:
        logging.info("Configurando archivos de IDE...")
        
        # VSCode settings
        vscode_dir = Path('.vscode')
        vscode_dir.mkdir(exist_ok=True)
        
        settings = {
            "python.defaultInterpreterPath": sys.executable,
            "python.linting.enabled": True,
            "python.linting.flake8Enabled": True,
            "python.linting.pylintEnabled": False,
            "python.formatting.provider": "black",
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": ["tests/"],
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                "reports/": True,
                "screenshots/": True
            }
        }
        
        import json
        with open(vscode_dir / 'settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
        
        logging.info("✅ Configuración de IDE completada")
        return True
        
    except Exception as e:
        logging.warning(f"Error configurando IDE: {e}")
        return True


def verify_installation():
    """Verificar que la instalación fue exitosa"""
    try:
        logging.info("Verificando instalación...")
        
        # Verificar imports
        import selenium
        import pytest
        import allure
        
        # Verificar configuración
        from config.config import Config
        from pages.base_page import BasePage
        
        logging.info("✅ Instalación verificada exitosamente")
        return True
        
    except ImportError as e:
        logging.error(f"Error de importación: {e}")
        return False
    except Exception as e:
        logging.error(f"Error verificando instalación: {e}")
        return False


def main():
    """Función principal"""
    setup_logging()
    
    logging.info("🚀 Configurando entorno de desarrollo del framework de automatización QA")
    
    steps = [
        ("Verificando versión de Python", check_python_version),
        ("Creando directorios necesarios", create_directories),
        ("Instalando dependencias de Python", install_dependencies),
        ("Instalando drivers de navegadores", install_webdrivers),
        ("Configurando hooks de Git", setup_git_hooks),
        ("Configurando IDE", setup_ide_config),
        ("Verificando instalación", verify_installation)
    ]
    
    success = True
    
    for step_name, step_func in steps:
        logging.info(f"📋 {step_name}...")
        if not step_func():
            logging.error(f"❌ Error en: {step_name}")
            success = False
        else:
            logging.info(f"✅ {step_name} completado")
    
    if success:
        logging.info("🎉 ¡Configuración completada exitosamente!")
        logging.info("📚 Para ejecutar tests, usa: python scripts/run_tests.py")
        logging.info("📖 Para más información, consulta el README.md")
    else:
        logging.error("❌ La configuración falló. Revisa los errores anteriores.")
        sys.exit(1)


if __name__ == '__main__':
    main()
