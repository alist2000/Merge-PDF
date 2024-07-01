import os
import io
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox, \
    QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def get_sorted_pdf_files(directory):
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    pdf_files.sort()
    return pdf_files


def merge_pdfs(directory, output_filename):
    merger = PdfMerger()
    pdf_files = get_sorted_pdf_files(directory)

    for pdf in pdf_files:
        merger.append(os.path.join(directory, pdf))

    merger.write(output_filename)
    merger.close()


def add_page_numbers(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for i in range(len(reader.pages)):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        page_width = letter[0]
        page_number = str(i + 1)
        text_width = can.stringWidth(page_number, "Helvetica", 12)
        x_position = (page_width - text_width) / 2

        can.drawString(x_position, 10, page_number)
        can.save()

        packet.seek(0)

        number_pdf = PdfReader(packet)
        number_page = number_pdf.pages[0]

        page = reader.pages[i]
        page.merge_page(number_page)
        writer.add_page(page)

    with open(output_pdf, 'wb') as output:
        writer.write(output)


class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Merger')

        layout = QVBoxLayout()

        self.select_dir_button = QPushButton('Select Directory', self)
        self.select_dir_button.clicked.connect(self.select_directory)
        layout.addWidget(self.select_dir_button)

        self.page_number_checkbox = QCheckBox('Add Page Numbers', self)
        layout.addWidget(self.page_number_checkbox)

        self.generate_button = QPushButton('Generate', self)
        self.generate_button.clicked.connect(self.generate_pdf)
        layout.addWidget(self.generate_button)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Center the window on the screen
        self.setGeometry(100, 100, 400, 200)
        self.center()

        # Apply a minimal style
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QCheckBox {
                padding: 10px;
            }
        """)

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            directory = directory.replace("/", "\\")
            self.directory = directory

            self.status_label.setText(f'Selected Directory: {directory}')

    def generate_pdf(self):
        if not hasattr(self, 'directory'):
            self.status_label.setText('Please select a directory first.')
            return

        cwd = os.getcwd()
        merged_pdf = os.path.join(cwd, 'merged_output.pdf')
        final_pdf_with_numbers = os.path.join(cwd, 'final_output_with_page_numbers.pdf')

        self.status_label.setText('Merging PDFs...')
        merge_pdfs(self.directory, merged_pdf)

        if self.page_number_checkbox.isChecked():
            self.status_label.setText('Adding page numbers...')
            add_page_numbers(merged_pdf, final_pdf_with_numbers)
            os.remove(merged_pdf)
            self.status_label.setText(f'PDF generated: {final_pdf_with_numbers}')
        else:
            self.status_label.setText(f'PDF generated: {merged_pdf}')


if __name__ == '__main__':
    app = QApplication([])
    window = PDFMergerApp()
    window.show()
    app.exec()
