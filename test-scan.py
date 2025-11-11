#!/usr/bin/env python3
"""
Script de teste para demonstrar a funcionalidade de scan do detect-drivers.py
"""

import json
from pathlib import Path
from utils.driver_detector import list_installed_drivers, export_driver_list

def test_scan_functionality():
    """Testa a funcionalidade de scan e criação do drivers.json"""
    
    print("=" * 60)
    print("Teste de Varredura de Drivers")
    print("=" * 60)
    print()
    
    # 1. Detectar drivers instalados
    print("1. Detectando drivers instalados no sistema...")
    installed_drivers = list_installed_drivers()
    print(f"   ✓ Encontrados {len(installed_drivers)} drivers")
    print()
    
    # 2. Mostrar alguns exemplos
    print("2. Exemplos de drivers detectados:")
    for i, driver in enumerate(installed_drivers[:5], 1):
        print(f"   {i}. {driver.get('name', 'Unknown')}")
        print(f"      Versão: {driver.get('version', 'unknown')}")
        print(f"      Device ID: {driver.get('deviceId', 'N/A')}")
        print()
    
    if len(installed_drivers) > 5:
        print(f"   ... e mais {len(installed_drivers) - 5} drivers")
        print()
    
    # 3. Converter para formato de manifesto
    print("3. Convertendo para formato de manifesto...")
    manifest_entries = []
    for driver in installed_drivers:
        entry = {
            'name': driver.get('name', 'Unknown Driver'),
            'version': driver.get('version', 'unknown'),
            'deviceId': driver.get('deviceId', ''),
            'url': '',  # A ser preenchido manualmente
            'fileName': '',  # A ser preenchido manualmente
            'sha256': '',  # A ser preenchido manualmente
            'type': 'exe',  # Tipo padrão
            'os': 'windows',  # Detectar automaticamente
            'silentArgs': ''  # A ser preenchido manualmente
        }
        manifest_entries.append(entry)
    print(f"   ✓ {len(manifest_entries)} entradas criadas")
    print()
    
    # 4. Exportar para arquivo de teste
    test_output = 'drivers-test.json'
    print(f"4. Exportando para {test_output}...")
    if export_driver_list(manifest_entries, test_output):
        print(f"   ✓ Arquivo criado com sucesso!")
        print()
        
        # 5. Verificar conteúdo
        print("5. Verificando conteúdo do arquivo...")
        with open(test_output, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"   ✓ JSON válido com {len(data.get('drivers', []))} drivers")
            print()
        
        # 6. Mostrar exemplo de entrada
        print("6. Exemplo de entrada no manifesto:")
        if manifest_entries:
            example = manifest_entries[0]
            print(json.dumps(example, indent=2))
            print()
        
        print("=" * 60)
        print("Teste concluído com sucesso!")
        print("=" * 60)
        print()
        print(f"Arquivo gerado: {test_output}")
        print()
        print("Próximos passos:")
        print("  1. Revisar o arquivo gerado")
        print("  2. Adicionar URLs de download dos fabricantes")
        print("  3. Adicionar nomes de arquivo")
        print("  4. Calcular e adicionar hashes SHA256")
        print("  5. Ajustar tipos de instalador (exe, msi, zip)")
        print("  6. Adicionar argumentos de instalação silenciosa")
        print()
        
        return True
    else:
        print("   ✗ Falha ao criar arquivo")
        return False

if __name__ == "__main__":
    test_scan_functionality()
