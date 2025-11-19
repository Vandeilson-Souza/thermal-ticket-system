"""
Script para gerar o executável (.exe) do sistema de impressão
Usa PyInstaller para criar um arquivo executável único
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    print("📦 Verificando PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller já instalado")
        return True
    except ImportError:
        print("⚠️  PyInstaller não encontrado. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller instalado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao instalar PyInstaller: {e}")
            return False

def build_exe():
    """Gera o executável usando PyInstaller"""
    print("\n" + "="*60)
    print("🔨 GERANDO EXECUTÁVEL DO SISTEMA DE IMPRESSÃO")
    print("="*60)
    
    # Comando PyInstaller com todas as opções necessárias
    command = [
        "pyinstaller",
        "--onefile",                    # Gera um único arquivo .exe
        "--name=TicketPrinter",         # Nome do executável
        "--icon=NONE",                  # Sem ícone personalizado
        "--clean",                      # Limpa arquivos temporários
        "--noconfirm",                  # Não pede confirmação
        "--add-data=ticket;ticket",     # Inclui pasta ticket
        "--hidden-import=win32print",   # Importações ocultas
        "--hidden-import=win32ui",
        "--hidden-import=PIL",
        "--hidden-import=qrcode",
        "--hidden-import=waitress",
        "--hidden-import=flask",
        "--hidden-import=unicodedata",
        "--collect-all=qrcode",         # Coleta todos os módulos do qrcode
        "--collect-all=PIL",            # Coleta todos os módulos do PIL
        "printer_app.py"                # Arquivo principal
    ]
    
    print("\n🔧 Configuração:")
    print(f"   Nome: TicketPrinter.exe")
    print(f"   Tipo: Executável único (--onefile)")
    print(f"   Arquivo: printer_app.py")
    print(f"   Pasta: ticket/ (incluída)")
    
    print("\n⏳ Iniciando build... (isso pode levar alguns minutos)")
    print("-" * 60)
    
    try:
        # Executar PyInstaller
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ BUILD CONCLUÍDO COM SUCESSO!")
            print("="*60)
            print("\n📁 Arquivos gerados:")
            print(f"   Executável: dist\\TicketPrinter.exe")
            print(f"   Especificação: TicketPrinter.spec")
            print(f"   Build: build\\")
            
            # Verificar se o executável foi criado
            exe_path = os.path.join("dist", "TicketPrinter.exe")
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"\n✅ Executável criado: {exe_path}")
                print(f"📏 Tamanho: {size_mb:.2f} MB")
                
                print("\n" + "="*60)
                print("🚀 COMO USAR:")
                print("="*60)
                print("1. Vá para a pasta: dist\\")
                print("2. Execute: TicketPrinter.exe")
                print("3. Acesse: http://localhost:5000")
                print("4. Configure a impressora padrão no Windows")
                print("\n💡 Dica: Copie o arquivo .exe para onde quiser usar")
                print("="*60)
            else:
                print("⚠️  Executável não encontrado em dist\\")
        else:
            print("❌ ERRO NO BUILD!")
            print("="*60)
            print("\nSaída do erro:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Erro ao executar PyInstaller: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🖨️  TICKET PRINTER - GERADOR DE EXECUTÁVEL")
    print("="*60)
    
    # Verificar se estamos na pasta correta
    if not os.path.exists("printer_app.py"):
        print("❌ Erro: printer_app.py não encontrado!")
        print("💡 Execute este script na mesma pasta do printer_app.py")
        sys.exit(1)
    
    # Instalar PyInstaller se necessário
    if not install_pyinstaller():
        print("❌ Não foi possível instalar o PyInstaller")
        sys.exit(1)
    
    # Gerar executável
    if build_exe():
        print("\n✅ Processo concluído!")
    else:
        print("\n❌ Processo falhou!")
        sys.exit(1)
