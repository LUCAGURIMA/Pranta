"""Script de validação de instalação - testa se todas as dependências estão disponíveis."""

import sys
from pathlib import Path

# Adicionar caminho do projeto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_imports():
    """Testa importação de todas as dependências."""
    print("=" * 60)
    print("Testando Importações - Pranta MVP")
    print("=" * 60)

    tests = []

    # Teste 1: Bibliotecas externas
    print("\n1. Testando bibliotecas externas...")
    try:
        import cv2
        print(f"   ✓ OpenCV {cv2.__version__}")
        tests.append(True)
    except ImportError as e:
        print(f"   ✗ OpenCV: {e}")
        tests.append(False)

    try:
        import PyQt5
        from PyQt5.QtCore import PYQT_VERSION_STR
        print(f"   ✓ PyQt5 {PYQT_VERSION_STR}")
        tests.append(True)
    except ImportError as e:
        print(f"   ✗ PyQt5: {e}")
        tests.append(False)
    except AttributeError:
        try:
            import PyQt5
            print(f"   ✓ PyQt5 (versão não detectada, mas importada)")
            tests.append(True)
        except ImportError as e:
            print(f"   ✗ PyQt5: {e}")
            tests.append(False)

    try:
        import pandas
        print(f"   ✓ Pandas {pandas.__version__}")
        tests.append(True)
    except (ImportError, AttributeError) as e:
        try:
            import pandas
            print(f"   ✓ Pandas (versão não detectada, mas importada)")
            tests.append(True)
        except ImportError:
            print(f"   ✗ Pandas: {e}")
            tests.append(False)

    try:
        import matplotlib
        print(f"   ✓ Matplotlib {matplotlib.__version__}")
        tests.append(True)
    except (ImportError, AttributeError) as e:
        try:
            import matplotlib
            print(f"   ✓ Matplotlib (versão não detectada, mas importada)")
            tests.append(True)
        except ImportError:
            print(f"   ✗ Matplotlib: {e}")
            tests.append(False)

    try:
        import numpy
        print(f"   ✓ NumPy {numpy.__version__}")
        tests.append(True)
    except (ImportError, AttributeError) as e:
        try:
            import numpy
            print(f"   ✓ NumPy (versão não detectada, mas importada)")
            tests.append(True)
        except ImportError:
            print(f"   ✗ NumPy: {e}")
            tests.append(False)

    try:
        import plantcv
        print(f"   ✓ PlantCV {plantcv.__version__}")
        tests.append(True)
    except (ImportError, AttributeError) as e:
        try:
            import plantcv
            print(f"   ✓ PlantCV (versão não detectada, mas importada)")
            tests.append(True)
        except ImportError:
            print(f"   ✗ PlantCV: {e}")
            tests.append(False)

    # Teste 2: Módulos do projeto
    print("\n2. Testando módulos do projeto...")
    try:
        from app.capture.camera_manager import CameraManager
        print(f"   ✓ camera_manager.CameraManager")
        tests.append(True)
    except ImportError as e:
        print(f"   ✗ camera_manager: {e}")
        tests.append(False)

    try:
        from app.processing.pipeline import RGBSimplePipeline, ProcessingConfig
        print(f"   ✓ pipeline.RGBSimplePipeline e ProcessingConfig")
        tests.append(True)
    except ImportError as e:
        print(f"   ✗ pipeline: {e}")
        tests.append(False)

    try:
        from app.data.storage import StorageManager
        print(f"   ✓ storage.StorageManager")
        tests.append(True)
    except ImportError as e:
        print(f"   ✗ storage: {e}")
        tests.append(False)

    try:
        from app.analytics.metrics import MetricsAnalyzer
        print(f"   ✓ metrics.MetricsAnalyzer")
        tests.append(True)
    except ImportError as e:
        print(f"   ✗ metrics: {e}")
        tests.append(False)

    try:
        from app.ui.main_window import PrantaMainWindow
        print(f"   ✓ main_window.PrantaMainWindow")
        tests.append(True)
    except ImportError as e:
        print(f"   ✗ main_window: {e}")
        tests.append(False)

    # Teste 3: Estrutura de diretórios
    print("\n3. Testando estrutura de diretórios...")
    required_dirs = [
        "app",
        "app/capture",
        "app/processing",
        "app/data",
        "app/analytics",
        "app/ui",
        "data",
        "data/raw",
        "data/processed",
        "data/results",
        "data/results/index",
    ]

    all_dirs_exist = True
    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            print(f"   ✓ {dir_name}/")
        else:
            print(f"   ✗ {dir_name}/ NÃO ENCONTRADO")
            all_dirs_exist = False
    tests.append(all_dirs_exist)

    # Teste 4: Arquivos de configuração
    print("\n4. Testando arquivos de configuração...")
    required_files = [
        "requirements.txt",
        "README.md",
        "main.py",
        "CHECKLIST_ACEITE.md",
    ]

    all_files_exist = True
    for file_name in required_files:
        file_path = PROJECT_ROOT / file_name
        if file_path.exists():
            print(f"   ✓ {file_name}")
        else:
            print(f"   ✗ {file_name} NÃO ENCONTRADO")
            all_files_exist = False
    tests.append(all_files_exist)

    # Resultado final
    print("\n" + "=" * 60)
    passed = sum(tests)
    total = len(tests)

    if all(tests):
        print(f"✅ TODOS OS TESTES PASSARAM ({passed}/{total})")
        print("=" * 60)
        print("\nA instalação está completa! Você pode executar:")
        print("  python main.py")
        return 0
    else:
        print(f"❌ ALGUNS TESTES FALHARAM ({passed}/{total})")
        print("=" * 60)
        print("\nPor favor:")
        print("1. Reinstale dependências: pip install -r requirements.txt")
        print("2. Verifique estrutura de diretórios")
        print("3. Execute novamente: python validate_installation.py")
        return 1


if __name__ == "__main__":
    sys.exit(test_imports())
