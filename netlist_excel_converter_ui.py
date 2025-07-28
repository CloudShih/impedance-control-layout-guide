import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import pandas as pd
import re

class NetlistExcelConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Netlist to Excel Converter")
        self.setGeometry(100, 100, 800, 400)
        self.initUI()

    # Descriptions from layout_guide.md
    spi_description = "SPI 總線的所有走線應在同一層中由附近的接地走線良好屏蔽。這些走線還應該被 n-1 和 n+1 層中的接地走線包圍，並且彼此靠近。SPI 總線的所有走線應遠離噪聲源，例如 Buck 開關節點等。對於 PMIC SPI 總線，也適用類似的屏蔽要求。PMIC SPI 走線應遠離 VBUS（插入式尖峰）和 Buck 開關節點等噪聲源。SOC 和 PMIC 之間的 SPI 總線的最大長度應短於 6 英寸（考慮 6 英寸約等於 1 納秒的延遲）。"
    i2c_description = "I2C/I3C 應用: AP-I2C 和 SCP-I2C 來自不同的 IP，因此請勿將 AP/SCP 設備連接到同一個 I2C 總線。I2C0~I2C9 具有內部上拉電阻（軟體預設 1KΩ，硬體預設 10KΩ，也支援 3KΩ），因此不需要外部上拉電阻。對於 I2C 標準模式、快速模式和快速模式增強版，建議將 I/O 類型配置為開漏（內部上拉 1KΩ）。對於高速模式，建議使用推挽式 (Push-pull) 類型。為提高訊號品質，在 SDA 線路中串聯一個電阻將有助於改善過衝或下衝。當 I2C I/O 類型配置為開漏時，最大 I2C 總線時脈為 400KHz（快速模式）。同一 I2C 總線上的設備其 I2C 地址必須是唯一的。建議為攝影機應用使用專用的 I2C 總線，以防止因攝影機關閉時的 I/O 漏電流導致總線死鎖問題。當支援 PIP/VIV (畫中畫/多畫面)、雙/三攝影機功能時，請為後置和前置攝影機分配不同的 I2C 總線。對於磁力計、氣壓計、光感應器、距離感應器、濕度感應器等感測器，應使用 SCP_I2C。請勿與其他非 SCP 設備共用 I2C 總線。"
    rf_description = "Being surrounded by ground in each trace."
    other_description = "General purpose signal, 50 Ohm impedance control."

    def is_excluded_word(self, word):
        # 1. Starts with an English letter, followed by all digits (e.g., R123, C45)
        if re.fullmatch(r'[a-zA-Z][0-9]+', word):
            return True
        # 2. All digits (e.g., 12345)
        if re.fullmatch(r'[0-9]+', word):
            return True
        # 3. Starts with a digit, and ends with "ohm", "f", or "h" (case-insensitive)
        if re.fullmatch(r'[0-9]+(ohm|f|h)', word, re.IGNORECASE):
            return True
        return False

    def initUI(self):
        main_layout = QVBoxLayout()

        # Netlist File Input
        netlist_layout = QHBoxLayout()
        self.netlist_path_input = QLineEdit()
        self.netlist_path_input.setPlaceholderText("Select .net file...")
        self.netlist_button = QPushButton("Browse .net")
        self.netlist_button.clicked.connect(self.browse_netlist_file)
        netlist_layout.addWidget(QLabel("Netlist File:"))
        netlist_layout.addWidget(self.netlist_path_input)
        netlist_layout.addWidget(self.netlist_button)
        main_layout.addLayout(netlist_layout)

        # Layout Template File Input
        template_layout = QHBoxLayout()
        self.template_path_input = QLineEdit()
        self.template_path_input.setPlaceholderText("Select layout template (Excel) file...")
        self.template_button = QPushButton("Browse Template")
        self.template_button.clicked.connect(self.browse_template_file)
        template_layout.addWidget(QLabel("Layout Template:"))
        template_layout.addWidget(self.template_path_input)
        template_layout.addWidget(self.template_button)
        main_layout.addLayout(template_layout)

        # Output Excel File Path
        output_layout = QHBoxLayout()
        self.output_path_input = QLineEdit()
        self.output_path_input.setPlaceholderText("Select output Excel file path...")
        self.output_button = QPushButton("Save As")
        self.output_button.clicked.connect(self.save_output_file)
        output_layout.addWidget(QLabel("Output Excel:"))
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(self.output_button)
        main_layout.addLayout(output_layout)

        # Generate Button
        self.generate_button = QPushButton("Generate Excel")
        self.generate_button.clicked.connect(self.generate_excel)
        main_layout.addWidget(self.generate_button)

        # Status/Message Area
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        main_layout.addWidget(QLabel("Status:"))
        main_layout.addWidget(self.status_display)

        self.setLayout(main_layout)

        # Apply dark theme stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #3c3c3c;
                color: #f0f0f0;
                border: 1px solid #555555;
                padding: 5px;
            }
            QPushButton {
                background-color: #555555;
                color: #f0f0f0;
                border: 1px solid #666666;
                padding: 8px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QLabel {
                color: #f0f0f0;
            }
        """)

    def browse_netlist_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select .net File", "", "Netlist Files (*.net);;All Files (*)")
        if file_path:
            self.netlist_path_input.setText(file_path)

    def browse_template_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Layout Template (Excel) File", "", "Excel Files (*.xlsx *.xls);;All Files (*)")
        if file_path:
            self.template_path_input.setText(file_path)

    def save_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Output Excel File", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            if not file_path.endswith(".xlsx"):
                file_path += ".xlsx"
            self.output_path_input.setText(file_path)

    def generate_excel(self):
        netlist_file = self.netlist_path_input.text()
        template_file = self.template_path_input.text()
        output_file = self.output_path_input.text()

        if not all([netlist_file, template_file, output_file]):
            self.status_display.setText("Error: All file paths must be selected.")
            return

        self.status_display.setText(f"Generating Excel from {netlist_file} using {template_file}...")
        
        try:
            # Read .net file and extract net names
            with open(netlist_file, 'r') as f:
                netlist_content = f.read()
            
            net_names = []
            for line in netlist_content.splitlines():
                line = line.strip()
                # Check if the line starts with a number (indicating a netlist entry)
                if line and line[0].isdigit():
                    parts = line.split()
                    if len(parts) > 1: # Ensure there's a second part for the net name
                        potential_net_name = parts[1]
                        if not self.is_excluded_word(potential_net_name):
                            net_names.append(potential_net_name) # Net name is the second word
            
            self.status_display.append(f"\nExtracted {len(net_names)} net names.")
            self.status_display.append(f"Net names: {', '.join(net_names)}")

            # Read template Excel file
            template_df = pd.read_excel(template_file)
            self.status_display.append(f"\nSuccessfully loaded template: {template_file}")

            # Prepare data for new Excel
            output_data = []
            for net_name in net_names:
                category = "Other"
                signal_type = "Single-End"
                description = self.other_description
                impedance = "50 Ohm"

                # Determine category and apply rules
                if "I2C" in net_name or "SCL" in net_name or "SDA" in net_name or "ADR" in net_name:
                    category = "Communication Interface"
                    signal_type = "I2C"
                    description = self.i2c_description
                elif "SPI" in net_name or "CSB" in net_name or "MI" in net_name or "MO" in net_name:
                    category = "Communication Interface"
                    signal_type = "SPI"
                    description = self.spi_description
                elif "RF" in net_name or "ANT" in net_name or "RX" in net_name or "TX" in net_name:
                    category = "RF"
                    description = self.rf_description
                
                output_data.append({
                    "Category": category,
                    "Net Name": net_name,
                    "Pin (MT7921)": "NaN",
                    "Description": description,
                    "Impedance": impedance,
                    "Type": signal_type,
                    "Width": "NaN",
                    "Length Limit (mil)": "NaN"
                })
            
            output_df = pd.DataFrame(output_data)

            # Save to Excel
            output_df.to_excel(output_file, index=False)
            self.status_display.append(f"\nExcel file saved to: {output_file}")
            self.status_display.append("\nExcel generation complete.")

        except Exception as e:
            self.status_display.setText(f"Error during generation: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NetlistExcelConverterApp()
    ex.show()
    sys.exit(app.exec_())