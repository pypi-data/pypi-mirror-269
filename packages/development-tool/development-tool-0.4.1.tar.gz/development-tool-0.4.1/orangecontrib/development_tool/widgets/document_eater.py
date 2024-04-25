import os
import sys
import Orange.data
import numpy as np
import pandas as pd
from Orange.data.pandas_compat import table_from_frame, table_to_frame
from PyQt5 import uic, QtWidgets
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
from AnyQt.QtCore import Qt, QObject, pyqtSignal

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from sentence_transformers import SentenceTransformer
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton
from PyQt5 import QtCore

class DocumentEater(widget.OWWidget):
    name = "DocumentEater"
    description = "Documents ingestion to generate embeddings and store it in db and add it to input file"
    icon = "icons/data-integration.png"
    want_control_area = False

    dossier_du_script = os.path.dirname(os.path.abspath(__file__))
    input_data = None
    working_dir = os.path.dirname(os.path.abspath(__file__) + '/tests/')
    model_dir = os.path.join(working_dir, "Models")
    data_dir = os.path.join(working_dir, "Data")
    db_dir = os.path.join(data_dir, "db")

    auto_send = False  # Variable de classe pour suivre l'état de la case à cocher

    dataChanged = pyqtSignal()

    class Inputs:
        input_data = Input("Data", Orange.data.Table)

    class Outputs:
        data_out = Output("Data", Orange.data.Table)

    @Inputs.input_data
    def set_data(self, input_data):
        self.input_data = input_data
        print("new input data")
        if self.auto_send:  # Si auto_send est activé
            self.generate_embeddings()  # Appeler generate_embeddings automatiquement

    def __init__(self):
        super().__init__()

        self.setFixedWidth(470)
        self.setFixedHeight(300)
        # QT Management
        uic.loadUi(self.dossier_du_script + '/widget_designer/document_eater.ui', self)

        self.selectFolderButton = self.findChild(QPushButton, 'push')
        # Connexion du clic du bouton à la méthode pour ouvrir le sélecteur de fichier
        self.selectFolderButton.clicked.connect(self.select_folder)

        self.generate = self.findChild(QPushButton, 'generate')
        self.generate.clicked.connect(self.generate_embeddings)

        self.modelPathLabel = self.findChild(QtWidgets.QLabel,
                                             'label')  # Récupérer le QLabel à partir du fichier .ui
        self.modelPathLabel.setText("Model Folder Path: Not selected")  # Définir le texte initial

        self.generateCheckBox = self.findChild(QtWidgets.QCheckBox,
                                               'checkBox')  # Récupérer le QCheckBox à partir du fichier .ui
        self.generateCheckBox.stateChanged.connect(self.toggle_auto_send)  # Connecter le signal stateChanged
        self.generate.setEnabled(not self.generateCheckBox.isChecked())  # Désactiver le bouton de génération

    def toggle_auto_send(self, state):
        self.auto_send = state == QtCore.Qt.Checked
        if self.auto_send and self.input_data is not None:
            self.generate_embeddings()

    def select_folder(self):
        # Ouvrir la boîte de dialogue pour sélectionner un dossier
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        # Si un dossier a été sélectionné
        if folder_path:
            # Récupérer la liste des fichiers dans le dossier
            files = os.listdir(folder_path)
            # Vérifier s'il y a des fichiers dans le dossier
            if files:
                # Sélectionner le premier fichier dans la liste (peu importe lequel)
                file_name = files[0]
                # Construire le chemin complet du fichier en utilisant le chemin du dossier et le nom du fichier
                model_name = os.path.join(folder_path, file_name)
                # Mettre à jour self.model_name avec le chemin complet du fichier
                self.model_name = folder_path
                self.label.setText(f"Model Folder Path: {folder_path}")
                # Imprimer le chemin complet du dossier et le nom du fichier
                print("Chemin du dossier sélectionné:", folder_path)
                print("Nom du fichier dans le dossier:", file_name)
                print("Chemin complet du fichier:", self.model_name)
            else:
                print("Le dossier sélectionné est vide.")
        else:
            print("Aucun dossier sélectionné.")

    def generate_embeddings(self):
        try:
            if self.input_data is None:
                self.Outputs.data_out.send(None)  # Envoyer None si input_data est None
                return

            data = self.input_data

            df = table_to_frame(data)

            # Initialisation du modèle Sentence Transformers
            # Ajout repertoire pour aller chercher
            model_name = getattr(self, 'model_name', None)  # Obtient self.model_name s'il est défini, sinon None
            if model_name is None:  # or model_name not in SentenceTransformer.available_models():
                # Utilise "all-mini-lm-6-v2" comme valeur par défaut si self.model_name n'est pas défini ou inconnu
                model_name = "all-MiniLM-L6-v2"
                print("Using default model:", model_name)

            model = SentenceTransformer(model_name)

            # Génération des embeddings pour chaque contenu dans la colonne "content"
            embeddings = []

            # Copie de la table d'entrée + génération des colonnes d'embeddings
            # Création d'un DataFrame à partir de la datatable
            data_dict = {}
            for col in data.domain.variables + data.domain.metas:
                data_dict[col.name] = []

            for row in data:
                for col in data.domain.variables + data.domain.metas:
                    data_dict[col.name].append(row[col].value)

            df = pd.DataFrame(data_dict)

            # Génération des embeddings pour chaque contenu dans la colonne "content"
            embeddings = []
            for content in df["content"]:
                embedding = model.encode(content)
                embeddings.append(embedding)

            # Création d'un DataFrame pour stocker les embeddings
            df_embeddings = pd.DataFrame(embeddings, columns=[f'embedding_{i}' for i in range(len(embeddings[0]))])

            # Concaténation du DataFrame des embeddings avec le DataFrame original
            df_concat = pd.concat([df, df_embeddings], axis=1)

            # Convertir les embeddings en un tableau numpy
            embeddings = np.array(df[[col for col in df.columns if col.startswith("embedding_")]].values.tolist())

            out_data = table_from_frame(df_concat)
            print('df_concat', df_concat.columns)
            self.Outputs.data_out.send(out_data)
        except Exception as e:
            print("An error occurred during embeddings processing:", str(e))

    def load_input_data(self):
        print("self.data", self.input_data.domain)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.refresh_all()

        return super().eventFilter(source, event)

    def show_warning_box(self, title: str, text: str):
        # Afficher une boîte de dialogue indiquant que les colonnes nécessaires sont manquantes
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

    def refresh_all(self):
        self.load_input_data()
        print("is it called ?")


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mon_objet = DocumentEater()
    mon_objet.show()

    app.exec_()
