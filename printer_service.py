import os
import cups

class ThermalPrinter:
    def __init__(self, printer_name=None):
        self.conn = cups.Connection()
        self.printers = self.conn.getPrinters()
        
        if printer_name and printer_name in self.printers:
            self.printer = printer_name
        else:
            self.printer = list(self.printers.keys())[0] if self.printers else None
    
    def print_text(self, text):
        if not self.printer:
            raise Exception("Nenhuma impressora configurada")
        
        # Criar arquivo temporário
        temp_file = "/tmp/cupom.txt"
        with open(temp_file, 'w') as f:
            f.write(text)
        
        # Configurar opções de impressão
        options = {
            'raw': 'True',
            'page-height': '297mm',  # Tamanho do rolo
            'page-width': '80mm',    # Largura comum para impressoras térmicas
            'scaling': '100'         # Sem escalonamento
        }
        
        # Enviar para impressão
        job_id = self.conn.printFile(self.printer, temp_file, "Cupom Fiscal", options)
        
        # Remover arquivo temporário
        os.remove(temp_file)
        
        return job_id

# Exemplo de uso
if __name__ == "__main__":
    printer = ThermalPrinter()
    cupom = """LOJA XYZ
    CUPOM FISCAL
    --------------------------------
    2x CAMISETA BRANCA - R$ 59.80
    1x CALÇA JEANS - R$ 89.90
    --------------------------------
    TOTAL: R$ 149.70
    """
    printer.print_text(cupom)
