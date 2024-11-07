import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import psycopg2

class ThreatViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyber Threat Data Viewer")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        # Set up layout and table
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.load_data()

        # Set up central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        # Connect to PostgreSQL and fetch threat data
        conn = psycopg2.connect(
            dbname="cyber_threats",
            user="postgres",
            password="yourpassword",
            host="localhost"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, source_ip, threat_type, severity, description FROM threats ORDER BY timestamp DESC LIMIT 20")
        rows = cursor.fetchall()

        # Set table dimensions
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Source IP", "Threat Type", "Severity", "Description"])

        # Populate table
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        conn.close()

app = QApplication(sys.argv)
viewer = ThreatViewer()
viewer.show()
sys.exit(app.exec_())
