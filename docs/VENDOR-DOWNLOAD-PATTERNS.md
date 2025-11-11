# Vendor Download Patterns - Guia de Uso

## Descrição

O arquivo `vendor_download_patterns.json` contém padrões de URLs de download dos principais fabricantes de hardware. Este guia ajuda a encontrar e construir URLs de download direto para drivers.

## Estrutura do Arquivo

```json
{
  "vendors": [
    {
      "name": "Nome do Fabricante",
      "website": "Site oficial",
      "patterns": {
        "tipo_dispositivo": {
          "search_page": "Página de busca",
          "direct_download_pattern": "Padrão de URL com placeholders",
          "example": "Exemplo de URL real",
          "notes": "Notas importantes"
        }
      }
    }
  ]
}
```

## Fabricantes Incluídos

### Hardware Principal
- **AMD** - Graphics, Chipset
- **Intel** - Graphics, Network, Chipset, Management Engine, Wireless, Bluetooth
- **NVIDIA** - Graphics (GeForce), Studio Drivers

### Áudio e Rede
- **Realtek** - Audio, Network, Card Reader
- **Broadcom** - Wireless, Bluetooth

### Placas-Mãe
- **ASUS** - Motherboard, Utilities
- **MSI** - Motherboard, Graphics
- **Gigabyte** - Motherboard
- **ASRock** - Motherboard

### Storage
- **Samsung** - SSD/NVMe
- **Western Digital** - Storage/NVMe
- **ADATA** - SSD/NVMe
- **Corsair** - Storage, Peripherals

### Periféricos
- **Logitech** - Gaming Peripherals
- **Razer** - Gaming Peripherals

## Como Usar

### 1. Busca Manual no Site

Para cada driver no `drivers.json`, visite a `search_page` correspondente:

**Exemplo - Intel Network Driver:**
```
Search Page: https://www.intel.com/content/www/us/en/download/18293/intel-network-adapter-driver-for-windows-10.html
```

### 2. Construir URL Direta

Use o `direct_download_pattern` substituindo os placeholders:

**Placeholders Comuns:**
- `{version}` - Versão do driver (ex: 25.10.2, 566.03)
- `{id}` - ID do download no site do fabricante
- `{model}` - Modelo do hardware
- `{filename}` - Nome do arquivo
- `{month}` - Mês (ex: oct, nov, dec)
- `{category}` - Categoria do driver

**Exemplo - AMD Graphics:**
```
Pattern: https://drivers.amd.com/drivers/whql-amd-software-adrenalin-edition-{version}-win10-win11-{month}-rdna.exe

Substituindo:
- {version} = 25.10.2
- {month} = oct

URL Final: https://drivers.amd.com/drivers/whql-amd-software-adrenalin-edition-25.10.2-win10-win11-oct-rdna.exe
```

**Exemplo - Intel Graphics:**
```
Pattern: https://downloadmirror.intel.com/{id}/graphics-windows-{version}.exe

Substituindo:
- {id} = 785597 (encontrado na search_page)
- {version} = 101.5593

URL Final: https://downloadmirror.intel.com/785597/graphics-windows-101.5593.exe
```

**Exemplo - NVIDIA GeForce:**
```
Pattern: https://us.download.nvidia.com/Windows/{version}/{version}-desktop-win10-win11-64bit-international-dch-whql.exe

Substituindo:
- {version} = 566.03 (aparece duas vezes)

URL Final: https://us.download.nvidia.com/Windows/566.03/566.03-desktop-win10-win11-64bit-international-dch-whql.exe
```

### 3. Usando o Helper Script

```python
from utils.download_url_helper import suggest_download_url, print_vendor_info

# Ver informações de um fabricante
print_vendor_info("Intel")

# Obter sugestão de URL
suggestion = suggest_download_url("AMD", "graphics")
print(f"Search Page: {suggestion['search_page']}")
print(f"Example: {suggestion['example']}")
```

### 4. Gerar Relatório de Sugestões

```bash
python -c "
from utils.download_url_helper import generate_download_suggestions_report
import json

# Carregar drivers do JSON
with open('drivers.json', 'r') as f:
    data = json.load(f)
    drivers = []
    for mfr in data['manufacturers']:
        drivers.extend(mfr['drivers'])

# Gerar relatório
generate_download_suggestions_report(drivers, 'download_suggestions.txt')
"
```

## Notas Importantes por Fabricante

### AMD
- **Graphics**: Versão e mês no nome do arquivo
- **RDNA**: Para GPUs modernas (RX 6000/7000 series)
- Exemplo: `25.10.2` = versão, `oct` = outubro

### Intel
- **Precisa do ID**: Cada driver tem um ID único no site
- **Encontrar ID**: Está na URL da página de download
- Exemplo: `https://www.intel.com/content/www/us/en/download/785597/` → ID = 785597

### NVIDIA
- **Versão duplicada**: A versão aparece duas vezes na URL
- **DCH vs Standard**: DCH para Windows 10/11 moderno
- **Studio vs Game Ready**: Studio para criadores, Game Ready para gamers

### Realtek
- **FileId necessário**: Precisa do FileId específico do site
- **Geralmente ZIP**: Drivers vêm compactados
- **Difícil automação**: Site não tem padrão consistente

### Broadcom
- **Estrutura variável**: Cada driver tem estrutura diferente
- **Busca manual recomendada**: Difícil automatizar
- **Docs.broadcom.com**: Maioria dos downloads

### ASUS/MSI/Gigabyte
- **Modelo específico**: Precisa do modelo exato da placa-mãe
- **Categorias**: Chipset, LAN, Audio, Utilities, etc.
- **Exemplo ASUS**: `PRIME_Z590M-PLUS` no caminho da URL

## Fluxo de Trabalho Recomendado

1. **Executar scan**:
   ```bash
   python detect-drivers.py --action scan
   ```

2. **Revisar drivers.json** gerado

3. **Para cada driver sem URL**:
   - Consultar `vendor_download_patterns.json`
   - Visitar a `search_page` do fabricante
   - Encontrar a versão mais recente
   - Copiar URL de download direto
   - Colar no `drivers.json`

4. **Baixar drivers**:
   ```bash
   # Criar pasta para downloads
   mkdir downloads_work
   
   # Baixar manualmente ou usar wget/curl
   wget -P downloads_work "URL_DO_DRIVER"
   ```

5. **Calcular SHA256**:
   ```bash
   # Windows PowerShell
   Get-FileHash -Algorithm SHA256 downloads_work\driver.exe
   
   # Linux
   sha256sum downloads_work/driver.exe
   ```

6. **Atualizar drivers.json** com hash

7. **Testar**:
   ```bash
   python setup-drivers.py --manifest drivers.json --dry-run
   ```

## Exemplos Práticos

### Exemplo 1: Driver Intel LAN

1. **Driver detectado**:
   ```json
   {
     "name": "Intel(R) Ethernet Connection (14) I219-V",
     "manufacturer": "Intel Corporation",
     "deviceType": "Network",
     "version": "12.19.1.37"
   }
   ```

2. **Consultar padrão**:
   - Fabricante: Intel
   - Tipo: Network
   - Search Page: https://www.intel.com/content/www/us/en/download/18293/

3. **Visitar página e encontrar**:
   - ID: 18293
   - Arquivo: PROWinx64.exe

4. **Construir URL**:
   ```
   https://downloadmirror.intel.com/18293/PROWinx64.exe
   ```

### Exemplo 2: Driver AMD Radeon

1. **Driver detectado**:
   ```json
   {
     "name": "AMD Radeon RX 6650 XT",
     "manufacturer": "AMD / ATI",
     "deviceType": "Graphics",
     "version": "32.0.12033.1030"
   }
   ```

2. **Consultar padrão**:
   - Fabricante: AMD
   - Tipo: Graphics
   - Pattern: `whql-amd-software-adrenalin-edition-{version}-win10-win11-{month}-rdna.exe`

3. **Visitar site AMD**:
   - Versão mais recente: 25.10.2
   - Mês: October (oct)

4. **Construir URL**:
   ```
   https://drivers.amd.com/drivers/whql-amd-software-adrenalin-edition-25.10.2-win10-win11-oct-rdna.exe
   ```

### Exemplo 3: Driver NVIDIA GeForce

1. **Driver detectado**:
   ```json
   {
     "name": "NVIDIA GeForce RTX 3060",
     "manufacturer": "NVIDIA Corporation",
     "deviceType": "Graphics"
   }
   ```

2. **Visitar NVIDIA**:
   - https://www.nvidia.com/Download/index.aspx
   - Selecionar GPU e buscar
   - Versão mais recente: 566.03

3. **Construir URL**:
   ```
   https://us.download.nvidia.com/Windows/566.03/566.03-desktop-win10-win11-64bit-international-dch-whql.exe
   ```

## Dicas

- **Sempre verifique a versão mais recente** no site oficial
- **Links diretos podem mudar** - use search_page como fallback
- **Teste o link** antes de adicionar ao drivers.json
- **Alguns fabricantes bloqueiam downloads diretos** - pode precisar baixar manualmente
- **Mantenha o arquivo atualizado** com novos padrões descobertos

## Contribuindo

Se você descobrir novos padrões ou atualizações, adicione ao `vendor_download_patterns.json`:

1. Identifique o padrão da URL
2. Adicione exemplo real
3. Documente placeholders usados
4. Adicione notas importantes

## Suporte

Para fabricantes não listados:
1. Visite o site oficial de suporte
2. Procure pela seção de downloads/drivers
3. Identifique o padrão de URL (se houver)
4. Adicione ao arquivo de padrões
