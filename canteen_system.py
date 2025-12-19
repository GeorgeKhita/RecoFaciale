import cv2
import numpy as np
import pickle
import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import threading


class CantineSystemGUI:
    def __init__(self):
        # Initialise le système de reconnaissance
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.known_names = []
        self.accounts = {}
        self.trained = False
        self.load_data()

        # Variables pour la caméra
        self.video = None
        self.current_frame = None
        self.camera_running = False
        self.current_mode = "recognition"  # "recognition" ou "capture"
        self.capture_samples = []
        self.capture_name = ""
        self.last_recognized = None
        self.meal_price = 3.50
        self.auto_debit = True  # Débit automatique
        self.debited_users = {}  # Pour éviter les doubles débits
        self.debit_cooldown = 10  # Secondes avant de pouvoir débiter à nouveau

        # Crée l'interface
        self.setup_gui()

        # Démarre la caméra
        self.start_camera()

    def setup_gui(self):
        """Crée l'interface graphique"""
        self.root = tk.Tk()
        self.root.title("Système de Cantine - Reconnaissance Faciale")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')

        # Frame principale divisée en 2
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # GAUCHE - Flux vidéo
        left_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Titre caméra
        cam_title = tk.Label(left_frame, text="📹 Caméra en Direct",
                             font=('Arial', 16, 'bold'), bg='#34495e', fg='white')
        cam_title.pack(pady=10)

        # Label pour la vidéo
        self.video_label = tk.Label(left_frame, bg='black')
        self.video_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Info reconnaissance
        self.info_label = tk.Label(left_frame, text="En attente...",
                                   font=('Arial', 14), bg='#34495e', fg='#ecf0f1',
                                   wraplength=600)
        self.info_label.pack(pady=10)

        # DROITE - Panneau de contrôle
        right_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.config(width=350)

        # Titre
        title = tk.Label(right_frame, text="🍽️ Panneau de Contrôle",
                         font=('Arial', 16, 'bold'), bg='#34495e', fg='white')
        title.pack(pady=15)

        # Prix du repas
        price_frame = tk.Frame(right_frame, bg='#34495e')
        price_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(price_frame, text="Prix du repas (€):",
                 font=('Arial', 11), bg='#34495e', fg='white').pack(side=tk.LEFT)

        self.price_entry = tk.Entry(price_frame, font=('Arial', 11), width=8)
        self.price_entry.insert(0, "3.50")
        self.price_entry.pack(side=tk.RIGHT)

        # Bouton TOGGLE AUTO/MANUEL
        self.toggle_btn = tk.Button(right_frame, text="🔄 MODE: AUTO",
                                    font=('Arial', 12, 'bold'),
                                    bg='#3498db', fg='white',
                                    activebackground='#2980b9',
                                    command=self.toggle_auto_debit,
                                    cursor='hand2')
        self.toggle_btn.pack(pady=(20, 5), padx=20, fill=tk.X)

        # Bouton DÉBITER (pour mode manuel)
        self.debit_btn = tk.Button(right_frame, text="💳 DÉBITER MAINTENANT",
                                   font=('Arial', 14, 'bold'),
                                   bg='#27ae60', fg='white',
                                   activebackground='#229954',
                                   command=self.debit_current_user,
                                   height=2, cursor='hand2')
        self.debit_btn.pack(pady=5, padx=20, fill=tk.X)

        # Séparateur
        tk.Frame(right_frame, height=2, bg='#7f8c8d').pack(fill=tk.X, padx=20, pady=10)

        # Boutons d'action
        btn_frame = tk.Frame(right_frame, bg='#34495e')
        btn_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Button(btn_frame, text="➕ Nouvel Utilisateur",
                  font=('Arial', 11), bg='#3498db', fg='white',
                  command=self.add_user_dialog, cursor='hand2').pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="💰 Ajouter Crédit",
                  font=('Arial', 11), bg='#f39c12', fg='white',
                  command=self.add_credit_dialog, cursor='hand2').pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="📊 Voir Comptes",
                  font=('Arial', 11), bg='#9b59b6', fg='white',
                  command=self.show_accounts_window, cursor='hand2').pack(fill=tk.X, pady=5)

        # Liste des comptes (aperçu)
        tk.Label(right_frame, text="Comptes:",
                 font=('Arial', 12, 'bold'), bg='#34495e', fg='white').pack(pady=(20, 5))

        accounts_frame = tk.Frame(right_frame, bg='#2c3e50', relief=tk.SUNKEN, bd=1)
        accounts_frame.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        self.accounts_text = tk.Text(accounts_frame, height=12, width=30,
                                     font=('Courier', 10), bg='#2c3e50',
                                     fg='#ecf0f1', relief=tk.FLAT)
        self.accounts_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.update_accounts_display()

        # Bouton quitter
        tk.Button(right_frame, text="❌ Quitter",
                  font=('Arial', 11), bg='#e74c3c', fg='white',
                  command=self.quit_app, cursor='hand2').pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        tk.Button(btn_frame, text="🗑️ Supprimer un utilisateur",
                  font=('Arial', 11), bg='#e74c3c', fg='white',
                  command=self.delete_user_dialog, cursor='hand2').pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="♻️ Réinitialiser limites",
                  font=('Arial', 11), bg='#16a085', fg='white',
                  command=self.reset_daily_limits, cursor='hand2').pack(fill=tk.X, pady=5)

    def start_camera(self):
        """Démarre la caméra"""
        self.video = cv2.VideoCapture(0)
        self.camera_running = True
        self.update_camera()

    def update_camera(self):
        """Met à jour le flux vidéo"""
        if not self.camera_running:
            return

        ret, frame = self.video.read()
        if ret:
            self.current_frame = frame.copy()

            # Traite selon le mode
            if self.current_mode == "recognition":
                frame = self.process_recognition(frame)
            elif self.current_mode == "capture":
                frame = self.process_capture(frame)

            # Convertit pour affichage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.root.after(10, self.update_camera)

    def process_recognition(self, frame):
        """Traite la reconnaissance faciale"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        self.last_recognized = None

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (200, 200))
            color = (255, 255, 0)
            text = "Visage"
            info = ""

            if self.trained and len(self.known_names) > 0:
                label, confidence = self.face_recognizer.predict(face_roi)

                if confidence < 70:
                    name = self.known_names[label]
                    balance = self.accounts[name]['balance']
                    self.last_recognized = name

                    # Débit automatique une fois par jour
                    if self.auto_debit:
                        today = datetime.now().date()
                        last_debit = self.accounts[name].get('last_debit_date', None)

                        if last_debit != str(today):
                            try:
                                amount = float(self.price_entry.get())
                                if self.debit_account(name, amount):
                                    self.accounts[name]['last_debit_date'] = str(today)
                                    self.update_accounts_display()
                                    self.save_data()
                                    color = (0, 255, 0)
                                    text = f"{name} - DÉBITÉ!"
                                    info = f"-{amount:.2f}€ | Solde: {self.accounts[name]['balance']:.2f}€"
                                    self.info_label.config(
                                        text=f"✅ {name} débité!\n-{amount:.2f}€\n"
                                             f"Nouveau solde: {self.accounts[name]['balance']:.2f}€",
                                        fg='#2ecc71'
                                    )
                            except:
                                color = (255, 165, 0)
                                text = f"{name}"
                                info = f"{balance:.2f}€"
                                self.info_label.config(
                                    text=f"⚠️ Erreur de prix\n{name}: {balance:.2f}€",
                                    fg='#f39c12'
                                )
                        else:
                            # Déjà débité aujourd'hui
                            color = (255, 165, 0)
                            text = f"{name} - DÉJÀ DÉBITÉ"
                            info = "A dejà ete debite aujourd'hui"
                            self.info_label.config(
                                text=f"⏳ {name} a déjà été débité aujourd'hui",
                                fg='#f39c12'
                            )
                    else:
                        # Mode manuel
                        color = (0, 255, 0)
                        text = f"{name}"
                        info = f"{balance:.2f}€"
                        self.info_label.config(
                            text=f"✅ {name} reconnu\nSolde: {balance:.2f}€\n(Mode manuel)",
                            fg='#2ecc71'
                        )
                else:
                    color = (0, 0, 255)
                    text = "Inconnu"
                    info = ""
                    self.info_label.config(text="❌ Personne non reconnue", fg='#e74c3c')
            else:
                color = (255, 255, 0)
                text = "Pas d'utilisateurs"
                info = ""
                self.info_label.config(text="⚠️ Aucun utilisateur enregistré", fg='#f39c12')

            # Dessine le rectangle et le texte
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
            cv2.rectangle(frame, (x, y - 35), (x + w, y), color, -1)
            cv2.putText(frame, text, (x + 6, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            if info:
                cv2.putText(frame, info, (x + 6, y + h + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if len(faces) == 0:
            self.info_label.config(text="👤 Aucun visage détecté", fg='#95a5a6')

        return frame

    def process_capture(self, frame):
        """Traite la capture d'échantillons"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_sample = gray[y:y + h, x:x + w]
            face_sample = cv2.resize(face_sample, (200, 200))
            self.capture_samples.append(face_sample)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            text = f"{len(self.capture_samples)}/30"
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame

    def toggle_auto_debit(self):
        """Active/désactive le débit automatique"""
        self.auto_debit = not self.auto_debit
        if self.auto_debit:
            self.toggle_btn.config(text="🔄 MODE: AUTO", bg='#3498db')
            self.debit_btn.config(state='disabled', bg='#95a5a6')
            messagebox.showinfo("Mode Automatique",
                                "✅ Débit automatique ACTIVÉ\n"
                                "Les élèves seront débités dès leur reconnaissance")
        else:
            self.toggle_btn.config(text="🔄 MODE: MANUEL", bg='#e67e22')
            self.debit_btn.config(state='normal', bg='#27ae60')
            messagebox.showinfo("Mode Manuel",
                                "⚠️ Débit automatique DÉSACTIVÉ\n"
                                "Cliquez sur 'DÉBITER MAINTENANT' pour débiter")

    def debit_current_user(self):
        """Débite l'utilisateur reconnu (mode manuel)"""
        if not self.last_recognized:
            messagebox.showwarning("Attention", "Aucune personne reconnue!")
            return

        try:
            amount = float(self.price_entry.get())
        except:
            messagebox.showerror("Erreur", "Prix invalide!")
            return

        if self.debit_account(self.last_recognized, amount):
            messagebox.showinfo("Succès",
                                f"✅ {amount:.2f}€ débités de {self.last_recognized}\n"
                                f"Nouveau solde: {self.accounts[self.last_recognized]['balance']:.2f}€")
            self.update_accounts_display()
        else:
            messagebox.showerror("Erreur",
                                 f"❌ Solde insuffisant pour {self.last_recognized}!")

    def add_user_dialog(self):
        """Dialogue pour ajouter un utilisateur"""
        name = simpledialog.askstring("Nouvel Utilisateur", "Nom de l'utilisateur:")
        if not name:
            return

        if name in self.known_names:
            messagebox.showerror("Erreur", f"{name} existe déjà!")
            return

        balance = simpledialog.askfloat("Solde Initial",
                                        "Solde initial (€):", initialvalue=50.0)
        if balance is None:
            return

        # Lance la capture
        self.capture_name = name
        self.capture_samples = []
        self.current_mode = "capture"
        self.info_label.config(text=f"📸 Capture de {name} en cours...\n"
                                    "Bougez légèrement la tête", fg='#3498db')

        # Thread pour surveiller la capture
        threading.Thread(target=self.monitor_capture, args=(name, balance), daemon=True).start()

    def delete_user(self, name):
        if name not in self.known_names:
            messagebox.showerror("Erreur", f"{name} n'existe pas.")
            return

        # 1. Supprimer le dossier d'images
        sample_dir = f"face_samples/{name}"
        if os.path.exists(sample_dir):
            import shutil
            shutil.rmtree(sample_dir)

        # 2. Supprimer le nom de la liste
        self.known_names.remove(name)

        # 3. Supprimer le compte
        if name in self.accounts:
            del self.accounts[name]

        # 4. Réentraîner le recognizer
        self.train_recognizer()

        # 5. Sauvegarder les données
        self.save_data()

        # 6. Mettre à jour l'affichage
        self.update_accounts_display()

        messagebox.showinfo("Suppression", f"{name} a été supprimé avec succès.")

    def monitor_capture(self, name, balance):
        """Surveille la capture des échantillons"""
        while len(self.capture_samples) < 30 and self.current_mode == "capture":
            self.root.after(100, lambda: None)

        if len(self.capture_samples) >= 30:
            self.finalize_user_capture(name, balance)

    def finalize_user_capture(self, name, balance):
        """Finalise l'ajout d'un utilisateur"""
        user_id = len(self.known_names)
        self.known_names.append(name)

        # Sauvegarde les échantillons
        self.save_face_samples(name, self.capture_samples[:30])

        # Crée le compte
        self.accounts[name] = {
            'balance': balance,
            'transactions': [],
            'last_debit_date': None
        }

        # Réentraîne
        self.train_recognizer()
        self.save_data()

        self.current_mode = "recognition"
        messagebox.showinfo("Succès", f"✅ {name} ajouté avec succès!\nSolde: {balance:.2f}€")
        self.update_accounts_display()

    def add_credit_dialog(self):
        """Dialogue pour ajouter du crédit"""
        if not self.accounts:
            messagebox.showwarning("Attention", "Aucun compte enregistré!")
            return

        # Fenêtre de sélection
        win = tk.Toplevel(self.root)
        win.title("Ajouter du Crédit")
        win.geometry("300x200")
        win.configure(bg='#34495e')

        tk.Label(win, text="Sélectionner un utilisateur:",
                 font=('Arial', 11), bg='#34495e', fg='white').pack(pady=10)

        user_var = tk.StringVar()
        combo = ttk.Combobox(win, textvariable=user_var,
                             values=list(self.accounts.keys()), state='readonly')
        combo.pack(pady=5)

        tk.Label(win, text="Montant (€):",
                 font=('Arial', 11), bg='#34495e', fg='white').pack(pady=5)

        amount_entry = tk.Entry(win, font=('Arial', 11))
        amount_entry.pack(pady=5)

        def add():
            name = user_var.get()
            try:
                amount = float(amount_entry.get())
                if self.add_credit(name, amount):
                    messagebox.showinfo("Succès",
                                        f"✅ {amount:.2f}€ ajoutés à {name}")
                    self.update_accounts_display()
                    win.destroy()
            except:
                messagebox.showerror("Erreur", "Montant invalide!")

        tk.Button(win, text="Ajouter", command=add,
                  bg='#27ae60', fg='white', font=('Arial', 11)).pack(pady=10)

    def show_accounts_window(self):
        """Affiche une fenêtre avec tous les comptes"""
        win = tk.Toplevel(self.root)
        win.title("Tous les Comptes")
        win.geometry("500x400")
        win.configure(bg='#34495e')

        tk.Label(win, text="📊 Comptes et Soldes",
                 font=('Arial', 14, 'bold'), bg='#34495e', fg='white').pack(pady=10)

        frame = tk.Frame(win, bg='#2c3e50', relief=tk.SUNKEN, bd=2)
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        text = tk.Text(frame, font=('Courier', 11), bg='#2c3e50',
                       fg='#ecf0f1', relief=tk.FLAT)
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        if not self.accounts:
            text.insert('1.0', "Aucun compte enregistré")
        else:
            for name, account in self.accounts.items():
                text.insert('end', f"{name:<20} {account['balance']:>8.2f}€\n")
                text.insert('end', "-" * 35 + "\n")

        text.config(state='disabled')

    def update_accounts_display(self):
        """Met à jour l'affichage des comptes"""
        self.accounts_text.config(state='normal')
        self.accounts_text.delete('1.0', 'end')

        if not self.accounts:
            self.accounts_text.insert('1.0', "Aucun compte")
        else:
            for name, account in self.accounts.items():
                self.accounts_text.insert('end',
                                          f"{name:<12} {account['balance']:>6.2f}€\n")

        self.accounts_text.config(state='disabled')

    def reset_daily_limits(self):
        """Réinitialise les limites de débit pour tous les utilisateurs (tests uniquement)"""
        for name in self.accounts:
            self.accounts[name]['last_debit_date'] = None
        self.save_data()
        self.update_accounts_display()
        messagebox.showinfo("Réinitialisation",
                            "✅ Les limites quotidiennes ont été réinitialisées pour tous les utilisateurs.")

    def quit_app(self):
        """Ferme l'application"""
        self.camera_running = False
        if self.video:
            self.video.release()
        self.root.quit()
        self.root.destroy()

    def delete_user_dialog(self):
        name = simpledialog.askstring("Supprimer utilisateur", "Nom de l'utilisateur à supprimer :")
        if name:
            confirm = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer {name} ?")
            if confirm:
                self.delete_user(name)

    # Méthodes de données (identiques à avant)
    def load_data(self):
        if os.path.exists('face_recognizer.yml'):
            self.face_recognizer.read('face_recognizer.yml')
            self.trained = True
        if os.path.exists('names.pkl'):
            with open('names.pkl', 'rb') as f:
                self.known_names = pickle.load(f)
        if os.path.exists('accounts.json'):
            with open('accounts.json', 'r', encoding='utf-8') as f:

                self.accounts = json.load(f)

    def save_data(self):
        if self.trained:
            self.face_recognizer.write('face_recognizer.yml')
        with open('names.pkl', 'wb') as f:
            pickle.dump(self.known_names, f)
        with open('accounts.json', 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, indent=2, ensure_ascii=False)

    def save_face_samples(self, name, samples):
        sample_dir = f'face_samples/{name}'
        if not os.path.exists(sample_dir):
            os.makedirs(sample_dir)
        for i, sample in enumerate(samples):
            cv2.imwrite(f'{sample_dir}/sample_{i}.jpg', sample)

    def train_recognizer(self):
        if not os.path.exists('face_samples'):
            os.makedirs('face_samples')
        faces = []
        labels = []
        for user_id, name in enumerate(self.known_names):
            sample_dir = f'face_samples/{name}'
            if os.path.exists(sample_dir):
                for filename in os.listdir(sample_dir):
                    if filename.endswith('.jpg'):
                        img_path = os.path.join(sample_dir, filename)
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        faces.append(img)
                        labels.append(user_id)
        if len(faces) > 0:
            self.face_recognizer.train(faces, np.array(labels))
            self.trained = True

    def debit_account(self, name, amount):
        if name in self.accounts:
            if self.accounts[name]['balance'] >= amount:
                self.accounts[name]['balance'] -= amount
                self.accounts[name]['transactions'].append({
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'amount': -amount,
                    'type': 'debit'
                })
                self.save_data()
                return True
        return False

    def add_credit(self, name, amount):
        if name in self.accounts:
            self.accounts[name]['balance'] += amount
            self.accounts[name]['transactions'].append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'amount': amount,
                'type': 'credit'
            })
            self.save_data()
            return True
        return False



    def run(self):
        """Lance l'application"""
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.root.mainloop()


if __name__ == "__main__":
    app = CantineSystemGUI()
    app.run()