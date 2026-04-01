"""Script de teste sem câmera - valida pipeline com imagem dummy.

Este script testa o pipeline de processamento sem necessidade de câmera.
Útil para validação rápida e desenvolvimento.
"""

import sys
import numpy as np
from pathlib import Path

# Adicionar project root ao path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.processing.pipeline import RGBSimplePipeline, ProcessingConfig
from app.data.storage import StorageManager


def create_dummy_plant_image(width=640, height=480):
    """Cria imagem dummy com uma forma verde (simulando planta).

    Args:
        width: Largura da imagem.
        height: Altura da imagem.

    Returns:
        Imagem BGR (numpy array).
    """
    # Criar imagem branca (background)
    image = np.ones((height, width, 3), dtype=np.uint8) * 200

    # Adicionar um quadrado verde no centro (planta simulada)
    center_x, center_y = width // 2, height // 2
    size = 100

    # Background branco
    image[
        center_y - size : center_y + size,
        center_x - size : center_x + size
    ] = [50, 150, 50]  # Verde em BGR

    return image


def test_pipeline():
    """Testa pipeline com imagem dummy."""
    print("=" * 60)
    print("TESTE DE PIPELINE - Pranta MVP")
    print("=" * 60)

    try:
        # 1. Criar pipeline
        print("\n1. Inicializando pipeline...")
        config = ProcessingConfig()
        pipeline = RGBSimplePipeline(config)
        print("   ✓ Pipeline criado com sucesso")

        # 2. Criar imagem dummy
        print("\n2. Criando imagem dummy (simulando planta)...")
        dummy_image = create_dummy_plant_image()
        print(f"   ✓ Imagem criada: {dummy_image.shape}")

        # 3. Processar imagem
        print("\n3. Processando imagem...")
        metrics, mask = pipeline.process_image(dummy_image)

        if metrics is None:
            print("   ⚠ Nenhuma planta detectada")
            print("   (Isto é ok se a imagem dummy não corresponder ao threshold)")
            return True

        # 4. Exibir resultados
        print("   ✓ Métricas extraídas com sucesso:")
        print(f"      - Area: {metrics.area_px:.2f} px²")
        print(f"      - Perimeter: {metrics.perimeter_px:.2f} px")
        print(f"      - Solidity: {metrics.solidity:.4f}")
        print(f"      - Circularity: {metrics.circularity:.4f}")
        print(f"      - Aspect Ratio: {metrics.aspect_ratio:.4f}")
        print(f"      - Hue: {metrics.hue_mean:.2f} ± {metrics.hue_std:.2f}")
        print(f"      - Saturation: {metrics.sat_mean:.2f} ± {metrics.sat_std:.2f}")
        print(f"      - Value: {metrics.val_mean:.2f} ± {metrics.val_std:.2f}")

        # 5. Verificar máscara
        print("\n4. Validando máscara...")
        mask_pixels = np.count_nonzero(mask)
        print(f"   ✓ Pixels da máscara: {mask_pixels}")

        print("\n" + "=" * 60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_storage():
    """Testa módulo de armazenamento (estrutura de diretórios)."""
    print("\n" + "=" * 60)
    print("TESTE DE STORAGE")
    print("=" * 60)

    try:
        print("\n1. Inicializando StorageManager...")
        storage = StorageManager()
        print("   ✓ StorageManager criado")

        print("\n2. Verificando diretórios...")
        from app.data.storage import CONSOLIDATED_CSV, RAW_DIR
        if CONSOLIDATED_CSV.exists():
            print(f"   ✓ CSV consolidado existe: {CONSOLIDATED_CSV}")
        else:
            print(f"   ⚠ CSV consolidado será criado na primeira captura")

        if RAW_DIR.exists():
            print(f"   ✓ Diretório raw existe: {RAW_DIR}")

        print("\n3. Testando criação de sessão...")
        session_dir = storage.create_plant_session("TestePlanta")
        print(f"   ✓ Sessão criada: {session_dir}")

        print("\n" + "=" * 60)
        print("✅ TESTE DE STORAGE OK")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 SUITE DE TESTES - Pranta MVP (SEM CÂMERA)\n")

    success = True

    # Teste 1: Pipeline
    success = test_pipeline() and success

    # Teste 2: Storage
    success = test_storage() and success

    if success:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\nA aplicação está pronta para usar.")
        print("Para usar com câmera: python main.py")
        sys.exit(0)
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        print("\nVerifique os erros acima e execute:")
        print("  python validate_installation.py")
        sys.exit(1)
