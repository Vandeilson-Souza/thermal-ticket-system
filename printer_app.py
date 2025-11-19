from datetime import datetime
import qrcode
from waitress import serve
from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont
import os
import win32print
import win32ui
from PIL import ImageWin
import logging
import urllib.parse
import unicodedata

# Configurações específicas para EPSON M-T532
PRINTER_NAME = win32print.GetDefaultPrinter()  # Usa a impressora padrão do Windows
PAPER_WIDTH_MM = 80
DOTS_PER_MM = 8
PAPER_WIDTH = PAPER_WIDTH_MM * DOTS_PER_MM

logging.basicConfig(level=logging.INFO)

def remove_accents(text):
    """Remove acentos de um texto para compatibilidade com impressoras térmicas"""
    if not text:
        return text
    try:
        # Normaliza o texto para NFD (decompõe caracteres acentuados)
        nfd = unicodedata.normalize('NFD', text)
        # Remove marcas diacríticas (acentos)
        without_accents = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
        return without_accents
    except:
        return text

# Criar pasta ticket se não existir
if not os.path.exists("ticket"):
    os.makedirs("ticket")
    print("✅ Pasta 'ticket' criada")

class EpsonPrinter:
    def __init__(self):
        self.printer_name = PRINTER_NAME
        print(f"🖨️  Usando impressora: {self.printer_name}")
        
    def send_escpos_commands(self, commands):
        """Envia comandos ESC/POS diretamente para a impressora"""
        try:
            hprinter = win32print.OpenPrinter(self.printer_name)
            try:
                win32print.StartDocPrinter(hprinter, 1, ("ESCPOS Print", None, "RAW"))
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, commands)
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)
                print("✅ Comandos ESC/POS enviados com sucesso")
                return True
            except Exception as e:
                print(f"❌ Erro ao enviar comandos ESC/POS: {e}")
                return False
            finally:
                win32print.ClosePrinter(hprinter)
        except Exception as e:
            print(f"❌ Erro ao acessar impressora: {e}")
            return False

    def print_text_ticket(self, created_date, code, services, header, footer):
        """Imprime ticket usando comandos ESC/POS nativos"""
        try:
            commands = b''
            
            # Inicializar impressora
            commands += b'\x1B\x40'  # Initialize printer
            
            # CÓDIGO EM DESTAQUE (tamanho triplo, negrito) - PRIMEIRO
            commands += b'\x1B\x21\x30'  # Select double height and width
            commands += b'\x1B\x45\x01'  # Turn emphasized mode on
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += f"COD: {remove_accents(code)}\r\n".encode('cp860', errors='ignore')
            commands += b'\x1B\x21\x00'  # Cancel double height and width
            commands += b'\x1B\x45\x00'  # Turn emphasized mode off
            
            # Linha separadora
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += ('=' * 42 + '\r\n').encode('cp860', errors='ignore')
            
            # Header (centralizado, negrito, tamanho duplo) - DEPOIS
            if header:
                commands += b'\x1B\x21\x30'  # Select double height and width
                commands += b'\x1B\x45\x01'  # Turn emphasized mode on
                commands += b'\x1B\x61\x01'  # Center alignment
                commands += (remove_accents(header) + '\r\n').encode('cp860', errors='ignore')
                commands += b'\x1B\x21\x00'  # Cancel double height and width
                commands += b'\x1B\x45\x00'  # Turn emphasized mode off
            
            # Linha separadora
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += ('-' * 42 + '\r\n').encode('cp860', errors='ignore')
            
            # Data
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += f"Data: {created_date}\r\n\r\n".encode('cp860', errors='ignore')
            
            # Serviços
            commands += b'\x1B\x61\x00'  # Left alignment
            commands += b'\x1B\x45\x01'  # Turn emphasized mode on
            commands += "SERVICOS:\r\n".encode('cp860', errors='ignore')
            commands += b'\x1B\x45\x00'  # Turn emphasized mode off
            
            # Quebrar texto dos serviços em linhas
            services_text = remove_accents(services)
            words = services_text.split()
            line = ""
            for word in words:
                if len(line + " " + word) <= 40:  # 40 caracteres por linha
                    line += " " + word
                else:
                    commands += (" " + line.strip() + "\r\n").encode('cp860', errors='ignore')
                    line = word
            if line:
                commands += (" " + line.strip() + "\r\n").encode('cp860', errors='ignore')
            
            commands += b'\r\n'
            
            # Footer
            if footer:
                commands += b'\x1B\x61\x01'  # Center alignment
                commands += b'\x1B\x34'  # Italic on
                commands += (remove_accents(footer) + '\r\n').encode('cp860', errors='ignore')
                commands += b'\x1B\x35'  # Italic off
            
            # Avançar papel SUFICIENTE antes de cortar
            commands += b'\r\n\r\n\r\n\r\n\r\n'  # Mais linhas de avanço (5 linhas)
            commands += b'\x1D\x56\x01'  # Partial cut
            
            return self.send_escpos_commands(commands)
        except Exception as e:
            print(f"❌ Erro no formato ESC/POS: {e}")
            return False

    def print_qrcode_ticket(self, created_date, code, services, header, footer, qrcode_data):
        """Imprime ticket com QR code usando ESC/POS"""
        try:
            commands = b''
            
            # Inicializar impressora
            commands += b'\x1B\x40'  # Initialize printer
            
            # CÓDIGO EM DESTAQUE (tamanho triplo, negrito) - PRIMEIRO
            commands += b'\x1B\x21\x30'  # Select double height and width
            commands += b'\x1B\x45\x01'  # Turn emphasized mode on
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += f"COD: {remove_accents(code)}\r\n".encode('cp860', errors='ignore')
            commands += b'\x1B\x21\x00'  # Cancel double height and width
            commands += b'\x1B\x45\x00'  # Turn emphasized mode off
            
            # Linha separadora
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += ('=' * 42 + '\r\n').encode('cp860', errors='ignore')
            
            # Header (centralizado, negrito, tamanho duplo) - DEPOIS
            if header:
                commands += b'\x1B\x21\x30'  # Select double height and width
                commands += b'\x1B\x45\x01'  # Turn emphasized mode on
                commands += b'\x1B\x61\x01'  # Center alignment
                commands += (remove_accents(header) + '\r\n').encode('cp860', errors='ignore')
                commands += b'\x1B\x21\x00'  # Cancel double height and width
                commands += b'\x1B\x45\x00'  # Turn emphasized mode off
            
            # Linha separadora
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += ('-' * 42 + '\r\n').encode('cp860', errors='ignore')
            
            # Data
            commands += b'\x1B\x61\x01'  # Center alignment
            commands += f"Data: {created_date}\r\n\r\n".encode('cp860', errors='ignore')
            
            # Serviços
            commands += b'\x1B\x61\x00'  # Left alignment
            commands += b'\x1B\x45\x01'  # Turn emphasized mode on
            commands += "SERVICOS:\r\n".encode('cp860', errors='ignore')
            commands += b'\x1B\x45\x00'  # Turn emphasized mode off
            
            # Quebrar texto dos serviços em linhas
            services_text = remove_accents(services)
            words = services_text.split()
            line = ""
            for word in words:
                if len(line + " " + word) <= 40:  # 40 caracteres por linha
                    line += " " + word
                else:
                    commands += (" " + line.strip() + "\r\n").encode('cp860', errors='ignore')
                    line = word
            if line:
                commands += (" " + line.strip() + "\r\n").encode('cp860', errors='ignore')
            
            commands += b'\r\n'
            
            # QR Code - Versão melhorada
            commands += self._generate_qrcode_escpos(qrcode_data)
            
            # Footer
            if footer:
                commands += b'\r\n\r\n'  # Espaço extra antes do footer
                commands += b'\x1B\x61\x01'  # Center alignment
                commands += b'\x1B\x34'  # Italic on
                commands += (remove_accents(footer) + '\r\n').encode('cp860', errors='ignore')
                commands += b'\x1B\x35'  # Italic off
            
            # Avançar papel MUITO antes de cortar (especialmente após QR code)
            commands += b'\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n'  # 8 linhas de avanço para QR code
            commands += b'\x1D\x56\x01'  # Partial cut
            
            return self.send_escpos_commands(commands)
        except Exception as e:
            print(f"❌ Erro no QR code ESC/POS: {e}")
            return False

    def _generate_qrcode_escpos(self, data):
        """Gera QR code usando comandos ESC/POS nativos - versão melhorada"""
        commands = b''
        
        # Centralizar QR code
        commands += b'\x1B\x61\x01'  # Center alignment
        
        # Configuração do QR code para melhor legibilidade
        commands += b'\x1D\x28\x6B\x03\x00\x31\x43\x06'  # Size 6
        commands += b'\x1D\x28\x6B\x03\x00\x31\x45\x31'  # Error correction L
        
        # Armazenar dados do QR code - remover acentos para compatibilidade
        data_clean = remove_accents(data)
        data_encoded = data_clean.encode('cp860', errors='ignore')
        
        pL = len(data_encoded) + 3
        pH = 0x00
        
        commands += b'\x1D\x28\x6B' + bytes([pL & 0xFF, pH, 49, 80, 48]) + data_encoded
        
        # Imprimir QR code
        commands += b'\x1D\x28\x6B\x03\x00\x31\x51\x30'
        
        return commands

    def print_image_ticket(self, created_date, code, services, header, footer, qrcode_data=None):
        """Método usando imagem bitmap"""
        try:
            print("🖼️  Gerando imagem do ticket...")
            
            # Configurações para 80mm
            width = 576  # Largura para 80mm
            padding = 20
            
            # Calcular altura dinâmica com margem extra
            base_height = 280
            services_lines = len(services) // 35 + 2
            dynamic_height = base_height + (services_lines * 20)
            
            if qrcode_data:
                dynamic_height += 400  # Aumentado para 400 - MUITO mais espaço para QR code completo
            else:
                dynamic_height += 100  # Espaço para footer
                
            height = min(dynamic_height, 1500)  # Limite máximo aumentado para 1500
            
            # Criar imagem
            img = Image.new('1', (width, height), 1)  # 1-bit bitmap, fundo branco
            draw = ImageDraw.Draw(img)
            
            # Carregar fontes
            try:
                title_font = ImageFont.truetype("arial.ttf", 24)
                large_bold_font = ImageFont.truetype("arialbd.ttf", 28)  # Fonte maior para código
                bold_font = ImageFont.truetype("arialbd.ttf", 20)
                normal_font = ImageFont.truetype("arial.ttf", 16)
                small_font = ImageFont.truetype("arial.ttf", 14)
            except:
                print("⚠️  Usando fontes padrão")
                title_font = ImageFont.load_default()
                large_bold_font = ImageFont.load_default()
                bold_font = ImageFont.load_default()
                normal_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            y = padding
            
            # CÓDIGO EM DESTAQUE (fonte maior) - PRIMEIRO
            code_text = f"COD: {code}"
            try:
                bbox = draw.textbbox((0, 0), code_text, font=large_bold_font)
                w = bbox[2] - bbox[0]
                x = (width - w) // 2
                draw.text((x, y), code_text, font=large_bold_font, fill=0)
                y += bbox[3] - bbox[1] + 15
            except:
                w = draw.textlength(code_text, font=large_bold_font)
                x = (width - w) // 2
                draw.text((x, y), code_text, font=large_bold_font, fill=0)
                y += 35
            
            # Linha separadora
            draw.line([(50, y), (width-50, y)], fill=0, width=2)
            y += 15
            
            # Header - DEPOIS
            if header:
                try:
                    bbox = draw.textbbox((0, 0), header, font=bold_font)
                    w = bbox[2] - bbox[0]
                    x = (width - w) // 2
                    draw.text((x, y), header, font=bold_font, fill=0)
                    y += bbox[3] - bbox[1] + 10
                except:
                    w = draw.textlength(header, font=bold_font)
                    x = (width - w) // 2
                    draw.text((x, y), header, font=bold_font, fill=0)
                    y += 30
            
            # Linha separadora
            draw.line([(50, y), (width-50, y)], fill=0, width=1)
            y += 15
            
            # Data
            date_text = f"Data: {created_date}"
            try:
                bbox = draw.textbbox((0, 0), date_text, font=normal_font)
                w = bbox[2] - bbox[0]
                x = (width - w) // 2
                draw.text((x, y), date_text, font=normal_font, fill=0)
                y += bbox[3] - bbox[1] + 15
            except:
                w = draw.textlength(date_text, font=normal_font)
                x = (width - w) // 2
                draw.text((x, y), date_text, font=normal_font, fill=0)
                y += 20
            
            # Serviços
            serv_label = "SERVICOS:"
            try:
                bbox = draw.textbbox((0, 0), serv_label, font=normal_font)
                draw.text((padding, y), serv_label, font=normal_font, fill=0)
                y += bbox[3] - bbox[1] + 8
            except:
                draw.text((padding, y), serv_label, font=normal_font, fill=0)
                y += 20
            
            # Texto dos serviços com quebra de linha
            services_text = services
            words = services_text.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                try:
                    line_width = draw.textbbox((0, 0), test_line, font=normal_font)[2]
                except:
                    line_width = draw.textlength(test_line, font=normal_font)
                
                if line_width <= width - (padding * 2):
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            for line in lines:
                try:
                    bbox = draw.textbbox((0, 0), line, font=normal_font)
                    draw.text((padding + 10, y), line, font=normal_font, fill=0)
                    y += bbox[3] - bbox[1] + 4
                except:
                    draw.text((padding + 10, y), line, font=normal_font, fill=0)
                    y += 18
            
            y += 10  # Reduzido de 15 para 10 - menos espaço antes do QR code
            
            # QR Code
            if qrcode_data:
                try:
                    # Gerar QR code
                    qr = qrcode.QRCode(
                        version=5,
                        error_correction=qrcode.constants.ERROR_CORRECT_M,
                        box_size=4,
                        border=2
                    )
                    qr.add_data(qrcode_data)
                    qr_img = qr.make_image(fill_color="black", back_color="white")
                    
                    # Redimensionar
                    qr_size = 200
                    qr_img = qr_img.resize((qr_size, qr_size))
                    
                    # Centralizar e posicionar
                    qr_x = (width - qr_size) // 2
                    qr_y = y
                    
                    # Converter para 1-bit e colar
                    qr_bw = qr_img.convert('1')
                    img.paste(qr_bw, (qr_x, qr_y))
                    
                    y += qr_size + 40  # Aumentado para 40 - MUITO mais espaço após QR code
                    print(f"✅ QR code gerado: {qr_size}x{qr_size}")
                except Exception as e:
                    print(f"❌ Erro ao gerar QR code: {e}")
            
            y += 20  # Aumentado para 20 - mais espaço antes do footer
            
            # Footer - SEMPRE NO FINAL
            if footer:
                try:
                    bbox = draw.textbbox((0, 0), footer, font=small_font)
                    w = bbox[2] - bbox[0]
                    x = (width - w) // 2
                    draw.text((x, y), footer, font=small_font, fill=0)
                except:
                    w = draw.textlength(footer, font=small_font)
                    x = (width - w) // 2
                    draw.text((x, y), footer, font=small_font, fill=0)
            
            # Salvar imagem para debug
            debug_path = os.path.join("ticket", f"debug_{datetime.now().strftime('%H%M%S')}.png")
            img.save(debug_path)
            print(f"💾 Imagem salva em: {debug_path}")
            
            # Imprimir
            return self._print_image_win32(img)
            
        except Exception as e:
            print(f"❌ Erro na geração de imagem: {e}")
            return False

    def _print_image_win32(self, img):
        """Imprime imagem via Win32"""
        try:
            print("🖨️  Enviando para impressora...")
            
            # Salvar imagem temporária
            temp_path = os.path.join("ticket", f"print_{datetime.now().strftime('%H%M%S')}.bmp")
            img.save(temp_path)
            
            hprinter = win32print.OpenPrinter(self.printer_name)
            
            try:
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(self.printer_name)
                
                # Calcular escala
                target_width = 576
                scale = target_width / img.size[0]
                target_height = int(img.size[1] * scale)
                
                # Redimensionar
                bmp = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                # Imprimir
                hdc.StartDoc("Ticket")
                hdc.StartPage()
                
                dib = ImageWin.Dib(bmp)
                dib.draw(hdc.GetHandleOutput(), (0, 0, target_width, target_height))
                
                hdc.EndPage()
                hdc.EndDoc()
                
                print("✅ Impressão enviada com sucesso!")
                
                # Avançar papel e cortar
                try:
                    # Avançar MUITO papel antes de cortar para garantir que todo conteúdo seja visível
                    feed_and_cut = b'\x1B\x64\x0A'  # Feed 10 lines (aumentado de 6 para 10)
                    feed_and_cut += b'\x1D\x56\x01'  # Partial cut
                    
                    win32print.StartDocPrinter(hprinter, 1, ("Cut", None, "RAW"))
                    win32print.StartPagePrinter(hprinter)
                    win32print.WritePrinter(hprinter, feed_and_cut)
                    win32print.EndPagePrinter(hprinter)
                    win32print.EndDocPrinter(hprinter)
                    print("✅ Comando de avanço e corte enviado (10 linhas)")
                except Exception as e:
                    print(f"⚠️  Corte não suportado: {e}")
                
                return True
                
            except Exception as e:
                print(f"❌ Erro na impressão: {e}")
                return False
            finally:
                win32print.ClosePrinter(hprinter)
                
        except Exception as e:
            print(f"❌ Erro no sistema de impressão: {e}")
            return False

app = Flask(__name__)

def decode_url_parameter(param):
    """Decodifica parâmetros URL que podem conter acentos"""
    if param:
        try:
            # Tenta decodificar como URL encoded
            decoded = urllib.parse.unquote(param)
            # Garante que está em UTF-8
            if isinstance(decoded, str):
                return decoded
            else:
                return decoded.encode('utf-8').decode('utf-8')
        except Exception as e:
            print(f"⚠️  Erro ao decodificar: {e}")
            return param
    return param

@app.route("/imprimir")
def imprimir_texto():
    try:
        printer = EpsonPrinter()
        
        # Decodificar parâmetros para lidar com acentos
        created_date = decode_url_parameter(request.args.get('created_date', datetime.now().strftime("%d/%m/%Y %H:%M")))
        code = decode_url_parameter(request.args.get('code', 'TEST001'))
        services = decode_url_parameter(request.args.get('services', 'Servico de Teste'))
        header = decode_url_parameter(request.args.get('header', 'TICKET TESTE'))
        footer = decode_url_parameter(request.args.get('footer', 'Obrigado pela preferencia!'))
        
        print(f"🎫 Imprimindo ticket: {code}")
        print(f"📋 Serviços: {services}")
        print(f"📝 Header: {header}")
        print(f"📝 Footer: {footer}")
        
        # Primeiro tenta ESC/POS
        success = printer.print_text_ticket(created_date, code, services, header, footer)
        if not success:
            print("🔄 Fallback para imagem...")
            success = printer.print_image_ticket(created_date, code, services, header, footer)
        
        if success:
            return "✅ Ticket impresso com sucesso!"
        else:
            return "❌ Falha na impressão - verifique o log"
                
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return f"❌ Erro: {str(e)}"

@app.route("/imprimir/qrcode")
def imprimir_qrcode():
    try:
        printer = EpsonPrinter()
        
        # Decodificar parâmetros para lidar com acentos
        created_date = decode_url_parameter(request.args.get('created_date', datetime.now().strftime("%d/%m/%Y %H:%M")))
        code = decode_url_parameter(request.args.get('code', 'QRCODE001'))
        services = decode_url_parameter(request.args.get('services', 'Servico com QR Code'))
        header = decode_url_parameter(request.args.get('header', 'TICKET QR CODE'))
        footer = decode_url_parameter(request.args.get('footer', 'Scan o QR Code!'))
        qrcode_data = decode_url_parameter(request.args.get('qrcode', f'COD:{code}'))
        
        print(f"🎫 Imprimindo QR code: {code}")
        print(f"📋 Serviços: {services}")
        print(f"📝 Header: {header}")
        print(f"📝 Footer: {footer}")
        print(f"🔗 QR Data: {qrcode_data}")
        
        # Primeiro tenta ESC/POS
        success = printer.print_qrcode_ticket(created_date, code, services, header, footer, qrcode_data)
        if not success:
            print("🔄 Fallback para imagem...")
            success = printer.print_image_ticket(created_date, code, services, header, footer, qrcode_data)
        
        if success:
            return "✅ QR Code impresso com sucesso!"
        else:
            return "❌ Falha na impressão - verifique o log"
                
    except Exception as e:
        print(f"❌ Erro QR: {e}")
        return f"❌ Erro QR: {str(e)}"

@app.route("/")
def index():
    current_time = datetime.now().strftime("%H%M")
    return f"""
    <html>
        <head>
            <title>EPSON M-T532 - Sistema de Impressão</title>
            <style>
                body {{ font-family: Arial; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .test-link {{ display: inline-block; margin: 10px; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; transition: background 0.3s; }}
                .test-link:hover {{ background: #218838; }}
                .info {{ background: #e8f4ff; padding: 15px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #007bff; }}
                .feature {{ background: #d4edda; padding: 10px; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🖨️ EPSON M-T532 - Sistema de Impressão</h1>
                
                <div class="feature">
                    <strong>✨ Novas Melhorias:</strong>
                    <ul>
                        <li>✅ <strong>Código em DESTAQUE</strong> - Tamanho maior e negrito</li>
                        <li>✅ <strong>Suporte a acentos</strong> - Via URLs externas</li>
                        <li>✅ Layout profissional otimizado</li>
                    </ul>
                </div>
                
                <div class="info">
                    <strong>📝 Status:</strong> Sistema em execução<br>
                    <strong>🖨️ Impressora:</strong> {PRINTER_NAME}<br>
                    <strong>📁 Pasta:</strong> ticket/ criada<br>
                    <strong>🕒 Hora:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M")}
                </div>
                
                <h3>🧪 Testes com Acentos:</h3>
                <a class="test-link" href="/imprimir?code=SNEHA{current_time}&services=Serviço%%20com%%20acentuação%%20para%%20teste%%20Sneha&header=Loja%%20Sneha%%20Especial&footer=Volte%%20sempre%%20à%%20Sneha!">
                    Teste com Acentos
                </a>
                <a class="test-link" href="/imprimir/qrcode?code=QR{current_time}&services=Serviço%%20Sneha%%20com%%20QR%%20Code%%20e%%20acentos&header=Sneha%%20QR%%20Code&footer=Scan%%20o%%20código%%20Sneha!&qrcode=https://sneha.com/ticket/{current_time}">
                    QR Code com Acentos
                </a>
                
                <div style="margin-top: 30px; padding: 15px; background: #fff3cd; border-radius: 5px;">
                    <strong>💡 Dica:</strong> Agora o sistema suporta acentos via URL e o código aparece em <strong>DESTAQUE</strong>!
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🖨️  EPSON M-T532 - Sistema de Impressão")
    print("="*60)
    print(f"📍 Impressora: {PRINTER_NAME}")
    print("✨ Melhorias aplicadas:")
    print("   ✅ Código em DESTAQUE (tamanho maior)")
    print("   ✅ Suporte a acentos via URL")
    print("   ✅ Layout profissional")
    print("📍 URLs:")
    print("   http://localhost:5000/ - Página de teste")
    print("   http://localhost:5000/imprimir - Teste texto") 
    print("   http://localhost:5000/imprimir/qrcode - Teste QR code")
    print("="*60)
    
    # Verificar se a impressora existe
    try:
        hprinter = win32print.OpenPrinter(PRINTER_NAME)
        win32print.ClosePrinter(hprinter)
        print("✅ Impressora encontrada e acessível")
    except:
        print("❌ Impressora não encontrada ou inacessível")
        print("💡 Configure a impressora padrão no Windows")
    
    serve(app, host='0.0.0.0', port=5000, threads=1)