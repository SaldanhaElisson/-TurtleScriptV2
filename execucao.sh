#!/bin/bash

if [ -z "$1" ]; then
  echo "Erro: Você deve fornecer o caminho para o arquivo de entrada."
  echo "Uso: ./run_program.sh <caminho/para/arquivo_de_entrada.txt>"
  exit 1
fi

# Ativa o ambiente virtual
source .venv/bin/activate
if [ $? -ne 0 ]; then
  echo "Erro: Não foi possível ativar o ambiente virtual. Verifique o caminho ou permissões."
  exit 1
fi

echo "Instalando dependências a partir do requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "Erro: Falha ao instalar as dependências."
  exit 1
fi

echo "Executando o programa com o arquivo de entrada: $1"
python3 -m src.main "$1"
EXEC_STATUS=$?

if [ $EXEC_STATUS -ne 0 ]; then
  echo "Execução falhou com o código de saída $EXEC_STATUS. Abortando."
  exit $EXEC_STATUS
fi

echo "Execução finalizada com sucesso."
echo ""

echo "Escolha uma opção:"
echo "1 - Executar arquivo gerado (examples/saida1.py)"
echo "2 - Sair"
read -p "Opção: " user_choice

case "$user_choice" in
  1)
    echo "Executando examples/saida1.py..."
    python3 examples/saida1.py
    ;;
  2)
    echo "Saindo."
    ;;
  *)
    echo "Opção inválida. Saindo."
    ;;
esac
