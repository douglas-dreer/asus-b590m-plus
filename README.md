## Drivers — Asus Prime B560-PLUS

Última atualização: 2025-11-10

Este README reúne orientações práticas e links úteis para baixar e instalar os drivers necessários para a placa mãe Asus Prime B560-PLUS.

> Observação: o modelo indicado nas referências fornecidas é a Prime B560-PLUS (ASUS). Se o modelo da sua placa for diferente, confirme o modelo impresso na própria placa ou na caixa antes de instalar drivers específicos.

## Links oficiais

- Página do produto (ASUS — Brasil): https://www.asus.com/br/motherboards-components/motherboards/prime/prime-b560-plus/
- Página de drivers e downloads (ASUS): acesse a seção "Support / Drivers & Tools" na página acima e selecione o sistema operacional desejado.
- Fenvi (adaptadores Wi‑Fi / Bluetooth, drivers): https://fenvi.com/drive.html?page=7
- Fenvi (página de produto China, exemplo): https://cn.fenvi.com/product_detail_29.html

Use sempre as páginas do fabricante (ASUS, Intel, Realtek, Fenvi) como fonte primária para downloads — isso reduz o risco de obter drivers adulterados.

## Resumo dos drivers recomendados

Baixe e instale, na ordem recomendada (ver seção abaixo):

- Intel Chipset Driver (INF) — fornece informação ao Windows sobre rotas do barramento e topologia do chipset.
- Intel Management Engine / MEI (se disponível para o modelo) — necessária para recursos de gerenciamento e algumas funcionalidades de power/firmware.
- Intel Rapid Storage Technology (RST) / drivers SATA — para desempenho/compatibilidade de portas SATA e arrays (se usar RAID)
- Intel/ASMedia USB 3.x drivers — para portas USB 3.0/3.2 quando aplicável.
- LAN (Ethernet) — normalmente Realtek Gigabit LAN para essa família de placas; baixar o driver Realtek correspondente.
- Áudio — driver Realtek High Definition Audio (HD Audio codec) fornecido pela ASUS/Realtek.
- Gráficos integrados — se usar a GPU integrada do processador (Intel UHD Graphics), baixe o driver Intel Graphics apropriado (ou use Windows Update).
- Wi‑Fi / Bluetooth — se usar um adaptador Fenvi (ou outro adaptador M.2/PCIe), baixe os drivers do site da Fenvi; se for adaptador baseado em Intel/Qualcomm/Broadcom, use os drivers do fabricante.
- BIOS / Firmware — atualizações no site da ASUS (use somente se a atualização corrige um problema que você tem).
- Utilitários opcionais: Armoury Crate / AI Suite / ASUS EZ Update — ferramentas de monitoramento e atualização da Asus.

Observação: o Windows 10/11 instala automaticamente muitos drivers via Windows Update, mas para estabilidade e recursos completos é recomendado baixar os pacotes do fabricante.

## Ordem recomendada de instalação (Windows)

1. Atualize o Windows pelo Windows Update e reinicie.
2. Instale o driver Intel Chipset (INF).
3. Instale o Intel Management Engine (MEI), se disponível para seu modelo.
4. Instale o driver Intel RST (caso use NVMe em modos especiais ou RAID) e drivers SATA/Storage.
5. Instale drivers USB 3.x (Intel/ASMedia) se houverem problemas com portas USB.
6. Instale o driver da placa de rede (LAN).
7. Instale o driver de áudio Realtek.
8. Instale drivers de gráficos (Intel iGPU) ou drivers da GPU dedicada (NVIDIA/AMD) diretamente do fabricante da placa de vídeo.
9. Instale drivers Wi‑Fi/BT (por exemplo, drivers Fenvi) e reinicie.
10. Instale utilitários ASUS e faça um último reinício.

Instalar drivers na ordem acima reduz conflitos e garante que o sistema reconheça corretamente os controladores base antes dos componentes dependentes.

## Passos rápidos de instalação (Windows — exemplos práticos)

1. Baixe o pacote de drivers no site da ASUS (escolha a versão do Windows correta — ex: Windows 10 64-bit ou Windows 11 64-bit).
2. Extraia o arquivo zip (se aplicável) em uma pasta temporária.
3. Clique com o botão direito em cada instalador (setup.exe) e selecione "Executar como administrador".
4. Siga as instruções do instalador e reinicie quando solicitado.

Comandos úteis no PowerShell para identificar o Windows e dispositivos (copiar/colar no PowerShell):

```powershell
# Ver nome e versão do Windows
(Get-CimInstance Win32_OperatingSystem) | Select-Object Caption, Version

# Listar adaptadores de rede (resumo)
Get-NetAdapter | Format-Table -AutoSize

# Para ver hardware PCI/USB no Windows use o utilitário de terceiros ou Device Manager
```

## Drivers Fenvi (Wi‑Fi / Bluetooth)

As páginas fornecidas da Fenvi contêm drivers para adaptadores Wi‑Fi/BT que a empresa vende (M.2/PCIe). Recomendações:

- Identifique o modelo exato do adaptador Fenvi (ex.: FN-*). Consulte a etiqueta na placa ou a caixa.
- Baixe o driver correspondente na página da Fenvi (links fornecidos no topo deste README).
- Se for um adaptador baseado em chipset Intel, prefira drivers Intel quando listados.
- Para Windows 10/11: usar o instalador oficial; para Linux: verifique suporte do kernel e firmware (veja seção Linux abaixo).

## Notas para Linux

- O kernel moderno (5.x/6.x) já inclui suporte para a maior parte do chipset B560 — drivers de rede e áudio geralmente funcionam sem intervenção.
- Para identificar hardware:

```bash
# Mostrar dispositivos PCI (Wi‑Fi/BT, LAN, etc.)
sudo lspci -nnk

# Mostrar dispositivos USB
lsusb
```

- Se o adaptador Wi‑Fi for um módulo Broadcom/Qualcomm, pode ser necessário instalar firmwares específicos (pacotes firmware-brcm, broadcom-sta, ath10k-firmware, etc.).
- Para adaptadores Fenvi baseados em chips que necessitem de firmware, a página do produto costuma indicar a compatibilidade e fornecer instruções.

## Solução de problemas (Windows)

- Se após instalar um driver um dispositivo não funcionar, tente:
	- Reiniciar o sistema.
	- No Device Manager (`devmgmt.msc`), localizar o dispositivo com problema, clic direito → Driver → Roll Back Driver (se disponível) ou Update Driver → Browse my computer → Let me pick.
	- Desinstalar o driver e marcar a opção para remover o software do driver, depois reinstalar.
	- Para drivers de vídeo, use DDU (Display Driver Uninstaller) em modo de segurança antes de reinstalar drivers NVIDIA/AMD.
- Para problemas de rede Wi‑Fi/BT, verifique interferência, antennae conectadas, slots M.2 corretamente inseridos e, se necessário, atualize o driver Bluetooth separadamente.

## Verificação pós‑instalação

- Abra o Device Manager (`devmgmt.msc`) e confirme que não há dispositivos com "!" amarelo.
- Verifique o funcionamento de: som (reproduzir áudio), rede (ping gateway), portas USB, e aceleração gráfica (se aplicável).

## Segurança e boas práticas

- Prefira sempre drivers da página oficial do fabricante (ASUS, Intel, Realtek, Fenvi). Evite sites de fontes duvidosas.
- Antes de atualizar a BIOS, faça backup de dados importantes e leia o changelog da BIOS no site da ASUS.

## Referências e créditos

- ASUS Prime B560-PLUS — https://www.asus.com/br/motherboards-components/motherboards/prime/prime-b560-plus/
- Fenvi drivers e páginas fornecidas — https://fenvi.com/drive.html?page=7  e https://cn.fenvi.com/product_detail_29.html

## Links de download — URLs diretas de referência (verificar versão)

Esses links levam às páginas oficiais onde os pacotes mais recentes costumam ser publicados. Sempre confirme a versão e a data de publicação na própria página/arquivo antes de instalar.

- ASUS — Página de suporte / downloads da Prime B560-PLUS (Drivers & Tools):
	- https://www.asus.com/br/Motherboards-Components/Motherboards/PRIME/PRIME-B560-PLUS/HelpDesk_Download/

- Fenvi — Driver / Support (lista de produtos e drivers):
	- https://fenvi.com/drive.html
	- Página de produto (exemplo FV-946CD): https://cn.fenvi.com/product_detail_29.html

- Intel — Centro de Downloads (Chipset / Graphics / RST / MEI):
	- Intel Download Center (busque "Chipset Device Software", "Intel Graphics", "Intel RST", "Intel Management Engine"): https://www.intel.com/content/www/us/en/download-center/home.html

- Realtek — Áudio / LAN (busque o modelo listado no site ASUS ou no Device Manager):
	- Realtek Downloads: https://www.realtek.com/en/downloads

- NVIDIA / AMD — Drivers para placas de vídeo dedicadas (se aplicável):
	- NVIDIA: https://www.nvidia.com/Download/index.aspx
	- AMD: https://www.amd.com/en/support

Observação: muitos instaladores são disponibilizados pela ASUS já empacotados; se preferir, baixe o pacote ASUS (em "Support / Drivers") e use os instaladores ali contidos — eles normalmente incluem versões compatíveis ajustadas para a placa.

### Como validar a "última versão" antes de baixar/instalar

1. Na página de download, verifique a coluna/version e a data de lançamento (Release Date) do arquivo.
2. Abra o arquivo Readme/ChangeLog (quando disponível) para confirmar correções/compatibilidade.
3. Compare a versão com a instalada (Windows: Device Manager → driver properties → Driver Version / Driver Date).
4. Prefira pacotes assinados e scripts oficiais (ex.: setup.exe da ASUS). Evite builds de terceiros sem histórico confiável.
5. Quando em dúvida, baixe o pacote e verifique o hash (se o fornecedor disponibilizar checksum) antes de executar.

Se quiser, eu posso:

- Fazer o mapeamento e retornar os links diretos (arquivos .exe, .zip) encontrados hoje para Windows 10/11 64-bit; para isso confirme qual versão do Windows você usa.
- Ou gerar uma checklist imprimível (CSV/Markdown) com os links e campos para a versão atual e a versão recomendada.

## Script PowerShell para Identificar Dispositivos

Este repositório inclui um script `get-devices-info.ps1` que lista automaticamente todos os dispositivos de hardware (GPU, LAN, Áudio, Armazenamento, etc.) instalados no seu sistema.

**Como usar:**

1. Abra o PowerShell como Administrador.
2. Navegue até `D:\drivers`.
3. Execute o script:

```powershell
.\get-devices-info.ps1
```

4. (Opcional) Para salvar a saída em um arquivo:

```powershell
.\get-devices-info.ps1 | Out-File dispositivos-relatorio.txt
```

**O script fornece:**
- Informações do SO (Windows 10/11), processador, placa-mãe
- Modelo e Vendor ID (VID_PID) de GPU, LAN, Wi-Fi, Áudio
- Identificação de controladores Intel Management Engine (MEI)
- Lista de dispositivos PCI (Intel, AMD, Realtek)

Consulte o arquivo `dispositivos-identificados.txt` para um exemplo de hardware já mapeado.

## Configuração por Sistema Operacional

### Windows

**Pasta:** `windows/`

1. Execute o PowerShell como **Administrador**
2. Navegue para `windows/`
3. Execute o script de setup:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   .\setup-drivers-windows.ps1
   ```

**Arquivos Windows:**
- `get-devices-info.ps1` — Identifica dispositivos
- `setup-drivers-windows.ps1` — (futuro) Script de instalação automática

### Linux

**Pasta:** `linux/`

1. Faça download/clone do repositório no seu PC com Linux
2. Abra o terminal
3. Navegue para `linux/`
4. Execute o script de identificação (opcional):
   ```bash
   chmod +x get-devices-info.sh
   sudo ./get-devices-info.sh
   ```

5. Execute o script de setup automático:
   ```bash
   chmod +x setup-drivers-linux.sh
   sudo ./setup-drivers-linux.sh
   ```

6. Reinicie o sistema:
   ```bash
   sudo reboot
   ```

**Arquivos Linux:**
- `get-devices-info.sh` — Identifica dispositivos (lspci, lsusb)
- `setup-drivers-linux.sh` — Instala drivers/firmware automaticamente
- `README-LINUX.md` — Guia completo de setup para Linux

**Distribuições suportadas automaticamente:**
- Debian / Ubuntu (18.04+)
- Fedora (32+)
- Arch Linux / Manjaro
- openSUSE (Leap / Tumbleweed)
- RHEL / CentOS (8+)

## Workflow Recomendado (Windows → Linux)

## Workflow Recomendado (Windows → Linux)

1. **Instale Windows** na sua máquina com Asus Prime B560-PLUS
2. **Clone ou baixe este repositório:**
   ```bash
   git clone https://github.com/douglas-dreer/asus-z590m-plus.git
   cd asus-z590m-plus
   ```
   
3. **Setup Windows (opcional — muitos drivers já vêm com Windows Update):**
   - (Futuro) Será adicionado script PowerShell de setup automático
   - Ou siga manualmente: veja `windows/` e `links-checklist.md`

4. **Instale Linux** (Ubuntu, Fedora, Arch, etc.) como dual-boot ou VM

5. **Clone novamente o repositório em Linux:**
   ```bash
   git clone https://github.com/douglas-dreer/asus-z590m-plus.git
   cd asus-z590m-plus/linux
   ```

6. **Execute o setup automático:**
   ```bash
   chmod +x setup-drivers-linux.sh
   sudo ./setup-drivers-linux.sh
   ```

7. **Reinicie:**
   ```bash
   sudo reboot
   ```

Pronto! Seu sistema Linux estará com todos os drivers atualizados.

## Troubleshooting — Dispositivos com erro no Device Manager

Se após instalar os drivers ver mensagens de erro "!" ou status "Error" em alguns dispositivos, veja **`DRIVERS-FALTANTES.md`**.

**Problema mais comum:** Controlador SMBus (SM Bus Controller) com erro
- **Causa:** Driver Intel Chipset não instalado
- **Solução rápida:**
  1. Baixe: https://downloadcenter.intel.com/download/19347/chipset-inf-utility.html
  2. Execute `SetupChipset.exe` como Administrador
  3. Reinicie o Windows
  4. Verifique Device Manager → Controladores → "Controlador de barramento SM" (deve desaparecer o erro)

Para investigar dispositivos específicos:
1. Device Manager → `View` → `Devices by connection`
2. Procure por `PCI\VEN_8086` (Intel)
3. Se vir "Unknown Device", anote o DEV_XXXX (ex: DEV_43A3)
4. Veja `DRIVERS-FALTANTES.md` para identificação

Dispositivos Intel desconhecidos comuns:
- `DEV_43A3` → SM Bus Controller (resolver com Intel Chipset INF)
- `DEV_43E9`, `DEV_43E8` → Trace Hub ou Power Controllers (resolver com Intel Chipset INF)
- `INT34C6` → ACPI Device genérico (pode ser sensor ou Power Button) (resolver com Intel Chipset INF + Windows Update)
- Se persistir após Chipset INF, pode ser ignorado (não afeta funcionalidade)

---

## Changelog

- 2025-11-10 (v3): Adicionado suporte completo a **Linux** com:
  - Script bash `get-devices-info.sh` (lspci, lsusb, dmidecode) para identificar dispositivos
  - Script bash `setup-drivers-linux.sh` com suporte automático a Debian/Ubuntu, Fedora, Arch, openSUSE
  - README-LINUX.md com guia detalhado de instalação e troubleshooting
  - Script universal `auto-setup.sh` que detecta Windows/Linux e executa o setup correto

- 2025-11-10 (v2): Adicionado script PowerShell `get-devices-info.ps1` para identificar dispositivos do sistema. Incluído arquivo `dispositivos-identificados.txt` com exemplo de hardware mapeado (Intel i5-10400F, AMD RX 6650 XT, Intel LAN I219-V, Realtek Audio). Atualizado `links-checklist.md` com URLs de download dos fornecedores (Intel, Realtek, Fenvi, NVIDIA, AMD).

- 2025-11-10 (v1): README inicial criado com instruções de download e instalação de drivers para Asus Prime B560-PLUS e notas sobre adaptadores Fenvi.

---

**Próximos passos:**
1. **Windows:** Execute `Get-ExecutionPolicy -List` depois `.\windows\get-devices-info.ps1`
2. **Linux:** Execute `chmod +x linux/setup-drivers-linux.sh && sudo linux/setup-drivers-linux.sh`
3. Para mais detalhes, leia `windows/` (futuro) ou `linux/README-LINUX.md`

