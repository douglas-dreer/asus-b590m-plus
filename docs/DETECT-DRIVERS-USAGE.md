# Uso do detect-drivers.py

## Descrição

O script `detect-drivers.py` permite fazer uma varredura completa do sistema e criar automaticamente um arquivo `drivers.json` com todos os drivers instalados detectados.

## Varredura do Sistema e Criação do drivers.json

Para fazer uma varredura completa e criar o arquivo `drivers.json`:

```bash
python detect-drivers.py --action scan
```

Isso irá:
1. Detectar todos os drivers instalados no sistema
2. Criar um arquivo `drivers.json` na raiz do projeto
3. Preencher informações básicas (nome, versão, deviceId, OS)

### Especificar caminho de saída customizado

```bash
python detect-drivers.py --action scan --export meus-drivers.json
```

### Com logging detalhado

```bash
python detect-drivers.py --action scan --verbose
```

## O que o scan detecta automaticamente

O comando `--action scan` agora detecta e preenche automaticamente:

✅ **Fabricante** - Identifica o fabricante do hardware (Intel, AMD, Realtek, etc.)  
✅ **Site do fabricante** - Adiciona o link oficial para downloads  
✅ **Nome do arquivo** - Gera um nome sugerido baseado no driver e versão  
✅ **Tipo de dispositivo** - Classifica como Audio, Network, Graphics, etc.  
✅ **Filtragem inteligente** - Remove drivers genéricos do Windows automaticamente  
✅ **Argumentos silenciosos** - Adiciona argumentos comuns de instalação silenciosa  

### Exemplo de entrada gerada automaticamente:

```json
{
  "drivers": [
    {
      "name": "Intel(R) Ethernet Connection (14) I219-V",
      "manufacturer": "Intel Corporation",
      "deviceType": "Network",
      "version": "12.19.1.37",
      "deviceId": "PCI\\VEN_8086&DEV_15FA&SUBSYS_86721043&REV_11",
      "url": "https://www.intel.com/content/www/us/en/download-center/home.html",
      "fileName": "Intel_Ethernet_Connection_(14)_I219-V_v12_19_1_37.exe",
      "sha256": "",
      "type": "exe",
      "os": "windows",
      "silentArgs": "/S /v\"/qn\""
    },
    {
      "name": "AMD Radeon RX 6650 XT",
      "manufacturer": "AMD / ATI",
      "deviceType": "Graphics",
      "version": "32.0.12033.1030",
      "deviceId": "PCI\\VEN_1002&DEV_73EF&SUBSYS_50271462&REV_C1",
      "url": "https://www.amd.com/en/support",
      "fileName": "AMD_Radeon_RX_6650_XT_v32_0_12033_1030.exe",
      "sha256": "",
      "type": "exe",
      "os": "windows",
      "silentArgs": "/S /v\"/qn\""
    }
  ]
}
```

## Completando o drivers.json

Após o scan, você ainda precisa completar manualmente:

1. **URLs exatas de download**: Navegue no site do fabricante e encontre o link direto do arquivo
2. **Hashes SHA256**: Baixe os drivers e calcule os hashes para validação
3. **Verificar tipos de instalador**: Confirme se é exe, msi, zip, etc.
4. **Testar argumentos silenciosos**: Alguns drivers podem precisar de argumentos diferentes

## Outras Ações Disponíveis

### Listar drivers instalados

```bash
python detect-drivers.py --action installed
```

### Listar drivers disponíveis no manifesto

```bash
python detect-drivers.py --action available --manifest drivers.json
```

### Listar drivers não instalados

```bash
python detect-drivers.py --action not-installed --manifest drivers.json
```

### Listar drivers com versões diferentes

```bash
python detect-drivers.py --action different-versions --manifest drivers.json
```

### Listar drivers que precisam de atualização

```bash
python detect-drivers.py --action needing-update --manifest drivers.json
```

## Filtrar por Sistema Operacional

```bash
python detect-drivers.py --action available --manifest drivers.json --os-filter windows
python detect-drivers.py --action available --manifest drivers.json --os-filter linux
```

## Exportar Resultados

Qualquer ação pode exportar resultados para JSON:

```bash
python detect-drivers.py --action installed --export installed-drivers.json
python detect-drivers.py --action needing-update --manifest drivers.json --export updates-needed.json
```

## Fluxo de Trabalho Recomendado

1. **Varredura inicial**:
   ```bash
   python detect-drivers.py --action scan --verbose
   ```

2. **Editar drivers.json**: Complete URLs, hashes, etc.

3. **Testar em modo dry-run**:
   ```bash
   python setup-drivers.py --manifest drivers.json --dry-run
   ```

4. **Executar instalação real**:
   ```bash
   python setup-drivers.py --manifest drivers.json --auto-reboot
   ```

## Calcular SHA256 de Arquivos

### Windows (PowerShell):
```powershell
Get-FileHash -Algorithm SHA256 -Path "driver.exe"
```

### Linux:
```bash
sha256sum driver.exe
```

### Python:
```python
import hashlib

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

print(calculate_sha256("driver.exe"))
```

## Notas Importantes

- **Privilégios**: A detecção de drivers no Windows requer privilégios de administrador
- **Tempo**: A varredura pode levar alguns minutos dependendo do número de drivers
- **Completude**: O arquivo gerado é um template - URLs e hashes devem ser adicionados manualmente
- **Validação**: Sempre teste com `--dry-run` antes de executar instalações reais
