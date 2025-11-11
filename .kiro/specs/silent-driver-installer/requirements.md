# Requirements Document

## Introdução

Este documento especifica os requisitos para um sistema automatizado de instalação silenciosa de drivers multiplataforma (Windows e Linux), focado na placa-mãe Asus Prime Z590M-PLUS. O sistema, implementado em Python para portabilidade universal, deve baixar, validar e instalar drivers de forma completamente automática, com reinicialização única ao final do processo, minimizando a intervenção do usuário.

## Glossary

- **Sistema**: O pacote Python `driver_installer` e seus módulos (cli, installer, utils)
- **CLI**: Interface de linha de comando (`driver-installer` ou `python -m driver_installer.cli`)
- **Manifesto**: Arquivo JSON (`drivers.json`) contendo lista de drivers com URLs, hashes SHA256 e parâmetros de instalação
- **Driver**: Pacote de software (exe, msi, zip, deb, rpm) que adiciona suporte a componentes de hardware
- **Instalação Silenciosa**: Instalação sem interface gráfica ou prompts ao usuário
- **Hash SHA256**: Checksum criptográfico de 256 bits usado para validar integridade de arquivos
- **Reinicialização Pendente**: Estado do sistema que requer reboot para completar instalações
- **Privilégios Elevados**: Administrador no Windows ou root/sudo no Linux necessários para instalar drivers
- **Multiplataforma**: Suporte para Windows e Linux no mesmo código
- **Pacote Python**: Estrutura modular instalável via pip (`pip install driver-installer`)
- **Bootstrap**: Scripts que instalam Python automaticamente se necessário (com permissão do usuário)

## Requirements

### Requirement 1

**User Story:** Como administrador de sistema, quero baixar automaticamente todos os drivers necessários de URLs oficiais, para que eu não precise fazer downloads manuais de múltiplos sites.

#### Acceptance Criteria

1. WHEN o Sistema inicia, THE Sistema SHALL ler o Manifesto e extrair todas as URLs de download
2. WHEN o Sistema processa uma entrada do Manifesto, THE Sistema SHALL baixar o arquivo da URL especificada para a pasta `downloads_work`
3. IF um arquivo já existe na pasta `downloads_work` e o parâmetro Force não está ativado, THEN THE Sistema SHALL pular o download e usar o arquivo existente
4. WHEN um download falha, THE Sistema SHALL registrar o erro no log e continuar com o próximo driver
5. THE Sistema SHALL usar timeout de 600 segundos para cada operação de download

### Requirement 2

**User Story:** Como administrador de sistema, quero que todos os arquivos baixados sejam validados com SHA256, para garantir que não foram corrompidos ou adulterados.

#### Acceptance Criteria

1. WHEN o Sistema completa um download, THE Sistema SHALL calcular o hash SHA256 do arquivo baixado
2. WHEN o Manifesto contém um hash SHA256 para um driver, THE Sistema SHALL comparar o hash calculado com o hash esperado
3. IF o hash calculado não corresponde ao hash esperado, THEN THE Sistema SHALL registrar erro no log e pular a instalação daquele driver
4. IF o Manifesto não contém hash SHA256 para um driver, THEN THE Sistema SHALL registrar aviso no log e prosseguir com a instalação
5. WHEN a validação de hash é bem-sucedida, THE Sistema SHALL registrar confirmação no log

### Requirement 3

**User Story:** Como administrador de sistema, quero que os drivers sejam instalados silenciosamente sem interação do usuário, para que o processo seja completamente automatizado.

#### Acceptance Criteria

1. WHEN o Sistema instala um driver tipo exe no Windows, THE Sistema SHALL tentar argumentos silenciosos na seguinte ordem: argumentos do Manifesto, depois `/S`, `/silent`, `/quiet`, `/verysilent`, `/s`, `/s /v"/qn"`, `/S /v"/qn"`
2. WHEN o Sistema instala um driver tipo msi no Windows, THE Sistema SHALL executar `msiexec.exe /i "<arquivo>" /qn /norestart`
3. WHEN o Sistema instala um driver tipo deb no Linux, THE Sistema SHALL executar `dpkg -i <arquivo>` ou `apt install <arquivo>`
4. WHEN o Sistema instala um driver tipo rpm no Linux, THE Sistema SHALL executar `rpm -i <arquivo>` ou `dnf install <arquivo>`
5. WHEN o Sistema instala um driver tipo zip, THE Sistema SHALL extrair o arquivo para pasta temporária, localizar instalador interno e executar instalação silenciosa apropriada para o sistema operacional
6. IF nenhuma tentativa de instalação silenciosa for bem-sucedida, THEN THE Sistema SHALL executar o instalador sem argumentos permitindo interação do usuário
7. WHEN o Sistema processa entrada tipo manual no Manifesto, THE Sistema SHALL criar arquivo de texto com instruções e URL na pasta `downloads_work`

### Requirement 4

**User Story:** Como administrador de sistema, quero que o sistema reinicie apenas uma vez ao final de todas as instalações, para minimizar tempo de inatividade.

#### Acceptance Criteria

1. WHEN o Sistema completa instalação de um driver, THE Sistema SHALL marcar que reinicialização é necessária
2. WHEN o Sistema completa processamento de todos os drivers do Manifesto, THE Sistema SHALL verificar se reinicialização é necessária
3. IF o parâmetro AutoReboot está ativado e reinicialização é necessária no Windows, THEN THE Sistema SHALL executar `shutdown /r /t 0`
4. IF o parâmetro AutoReboot está ativado e reinicialização é necessária no Linux, THEN THE Sistema SHALL executar `reboot`
5. IF o parâmetro AutoReboot não está ativado e reinicialização é necessária, THEN THE Sistema SHALL exibir mensagem instruindo usuário a reiniciar manualmente
6. THE Sistema SHALL registrar no log se reinicialização automática foi executada ou se é necessária reinicialização manual

### Requirement 5

**User Story:** Como administrador de sistema, quero que todas as operações sejam registradas em log detalhado, para que eu possa auditar e diagnosticar problemas.

#### Acceptance Criteria

1. WHEN o Sistema executa qualquer operação, THE Sistema SHALL registrar timestamp e descrição da operação no arquivo `setup-drivers.log`
2. WHEN o Sistema registra uma entrada de log, THE Sistema SHALL exibir a mesma mensagem no console PowerShell
3. WHEN o Sistema encontra um erro, THE Sistema SHALL registrar mensagem de erro com detalhes no log
4. THE Sistema SHALL incluir no log: início de execução, downloads, validações de hash, tentativas de instalação, códigos de retorno e conclusão
5. THE Sistema SHALL usar formato de timestamp ISO 8601 (YYYY-MM-DDTHH:MM:SS) para todas as entradas de log

### Requirement 6

**User Story:** Como administrador de sistema, quero que o script valide privilégios elevados antes de iniciar, para evitar falhas durante a instalação.

#### Acceptance Criteria

1. WHEN o Sistema inicia, THE Sistema SHALL verificar se está sendo executado com privilégios elevados (Administrador no Windows ou root/sudo no Linux)
2. IF o Sistema não está sendo executado com privilégios elevados, THEN THE Sistema SHALL exibir mensagem de erro e terminar com código de saída 1
3. WHEN a verificação de privilégios é bem-sucedida, THE Sistema SHALL prosseguir com o processamento do Manifesto
4. THE Sistema SHALL registrar no log se a verificação de privilégios foi bem-sucedida
5. THE Sistema SHALL exibir mensagem clara instruindo o usuário a executar com sudo (Linux) ou como Administrador (Windows) se a verificação falhar

### Requirement 7

**User Story:** Como administrador de sistema, quero que o script suporte manifesto externo e manifesto embutido, para flexibilidade em diferentes cenários de uso.

#### Acceptance Criteria

1. WHEN o Sistema inicia, THE Sistema SHALL verificar se o arquivo de Manifesto especificado no parâmetro existe
2. IF o arquivo de Manifesto existe, THEN THE Sistema SHALL carregar e parsear o JSON do arquivo
3. IF o arquivo de Manifesto não existe, THEN THE Sistema SHALL usar manifesto embutido com driver Intel Chipset como exemplo
4. WHEN o Sistema falha ao parsear o JSON do Manifesto, THE Sistema SHALL registrar erro e terminar com código de saída 4
5. THE Sistema SHALL registrar no log qual manifesto está sendo usado (externo ou embutido)

### Requirement 8

**User Story:** Como administrador de sistema, quero que o script processe drivers na ordem definida no manifesto, para garantir que dependências sejam respeitadas.

#### Acceptance Criteria

1. WHEN o Sistema carrega o Manifesto, THE Sistema SHALL preservar a ordem das entradas conforme definido no JSON
2. WHEN o Sistema processa drivers, THE Sistema SHALL executar download, validação e instalação na ordem sequencial do Manifesto
3. WHEN um driver falha em qualquer etapa, THE Sistema SHALL registrar o erro e continuar com o próximo driver na sequência
4. THE Sistema SHALL processar todos os drivers do Manifesto antes de verificar necessidade de reinicialização
5. THE Sistema SHALL registrar no log o progresso através da lista de drivers

### Requirement 9

**User Story:** Como administrador de sistema, quero que o script suporte parâmetro Force para forçar re-download de arquivos, para casos onde arquivos existentes possam estar corrompidos.

#### Acceptance Criteria

1. WHEN o parâmetro Force está ativado, THE Sistema SHALL baixar todos os arquivos mesmo se já existirem na pasta `downloads_work`
2. WHEN o parâmetro Force não está ativado e um arquivo existe, THE Sistema SHALL pular o download e usar o arquivo existente
3. WHEN o Sistema pula um download devido a arquivo existente, THE Sistema SHALL registrar no log que o arquivo já existe
4. THE Sistema SHALL validar hash SHA256 de arquivos existentes mesmo quando download é pulado
5. IF validação de hash falha para arquivo existente, THEN THE Sistema SHALL registrar erro e pular instalação daquele driver

### Requirement 10

**User Story:** Como administrador de sistema, quero que o script crie automaticamente a pasta de trabalho se não existir, para simplificar a configuração inicial.

#### Acceptance Criteria

1. WHEN o Sistema inicia processamento de drivers, THE Sistema SHALL verificar se a pasta `downloads_work` existe
2. IF a pasta `downloads_work` não existe, THEN THE Sistema SHALL criar a pasta
3. WHEN o Sistema cria a pasta `downloads_work`, THE Sistema SHALL usar caminho relativo ao diretório do script
4. THE Sistema SHALL registrar no log se a pasta foi criada ou já existia
5. THE Sistema SHALL continuar execução normalmente após criar a pasta

### Requirement 11

**User Story:** Como administrador de sistema, quero que o script valide a presença do Python e suas dependências antes de executar, para garantir que o ambiente está configurado corretamente.

#### Acceptance Criteria

1. WHEN o Sistema inicia, THE Sistema SHALL verificar se Python 3.7 ou superior está instalado
2. IF Python não está instalado ou versão é inferior a 3.7, THEN THE Sistema SHALL exibir mensagem de erro e terminar com código de saída 2
3. WHEN o Sistema detecta Python válido, THE Sistema SHALL verificar se arquivo `requirements.txt` existe no diretório do script
4. IF arquivo `requirements.txt` existe, THEN THE Sistema SHALL verificar se todas as dependências listadas estão instaladas
5. IF alguma dependência está ausente, THEN THE Sistema SHALL exibir mensagem instruindo instalação via `pip install -r requirements.txt` e terminar com código de saída 3
6. WHEN todas as dependências estão instaladas, THE Sistema SHALL registrar versão do Python e dependências no log
7. THE Sistema SHALL detectar automaticamente o sistema operacional (Windows ou Linux) e registrar no log
