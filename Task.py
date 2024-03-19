from tkinter import Tk, Label, Button, Entry, messagebox, Listbox, Scrollbar
from datetime import datetime

icon_path = r"C:\Users\leocuttaia\Desktop\Visual Studio Code\App1 test\TaskManager\cache\TaskManager.ico"

def log_action(action, task=None, modified_task=None):
    """Enregistre l'action de l'utilisateur dans le fichier log.txt avec un horodatage."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("log.txt", "a") as log_file:
        if task:
            if action == "Création":
                log_file.write(f"{timestamp} - Tâche créée: {task}\n")
            elif action == "Suppression":
                log_file.write(f"{timestamp} - Tâche supprimée: {task}\n")
            elif action == "Modification":
                log_file.write(f"{timestamp} - Tâche modifiée: Avant: {task}, Après: {modified_task}\n")
        else:
            log_file.write(f"{timestamp} - {action}\n")

class MainApplication:
    def __init__(self, root):
        log_action("L'utilisateur a ouvert l'application.")
        self.root = root
        self.tasks = []
        self.load_tasks()  # Charge les tâches depuis le fichier
        self.root.title("Gestionnaire de tâches")
        self.root.geometry("800x600")
        self.root.iconbitmap(icon_path)
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")
        self.header()
        self.home()

    def load_tasks(self):
        """Charge les tâches depuis le fichier tasks.txt."""
        with open("tasks.txt", "r") as file:
            self.tasks = file.readlines()

    def header(self):
        """Affiche l'en-tête de l'application."""
        header_label = Label(self.root, text="Gestionnaire de Tâches", font=("Helvetica", 25), bg="#2C3E50", fg="white")
        header_label.pack()

    def home(self):
        """Affiche l'interface principale de l'application."""
        self.clear_window()
        home_label = Label(self.root, text="Liste des Tâches:", font=("Helvetica", 20), bg="#2C3E50", fg="white")
        home_label.pack()

        scrollbar = Scrollbar(self.root, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.tasks_listbox = Listbox(self.root, yscrollcommand=scrollbar.set, bg="#34495E", fg="white", font=("Helvetica", 14))
        self.tasks_listbox.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.tasks_listbox.yview)

        self.update_tasks_listbox()

        add_task_btn = Button(self.root, text="Ajouter une Tâche", command=self.add_task, bg="#3498DB", fg="white")
        add_task_btn.pack()

        edit_task_btn = Button(self.root, text="Modifier la Tâche Sélectionnée", command=self.edit_selected_task, bg="#3498DB", fg="white")
        edit_task_btn.pack()

        remove_task_btn = Button(self.root, text="Supprimer la Tâche Sélectionnée", command=self.confirm_remove_selected_task, bg="#E74C3C", fg="white")
        remove_task_btn.pack()

    def add_task(self):
        """Affiche la fenêtre pour ajouter une nouvelle tâche."""
        task_window = Tk()
        task_window.title("Ajouter une Tâche")
        task_window.geometry("400x200")
        task_window.configure(bg="#2C3E50")

        task_label = Label(task_window, text="Entrez la Tâche:", font=("Helvetica", 16), bg="#2C3E50", fg="white")
        task_label.pack()

        task_entry = Entry(task_window, font=("Helvetica", 14))
        task_entry.pack()

        confirm_btn = Button(task_window, text="Confirmer", command=lambda: self.confirm_task(task_window, task_entry.get()), bg="#3498DB", fg="white")
        confirm_btn.pack()

        # Lier la touche "Entrée" pour confirmer la tâche
        task_entry.bind("<Return>", lambda event: self.confirm_task(task_window, task_entry.get()))

        task_window.mainloop()

    def confirm_task(self, task_window, task_text):
        log_action("Création", task_text)
        """Valide l'ajout d'une tâche et l'ajoute à la liste des tâches."""
        if task_text:
            task_with_timestamp = f"{task_text} - Créé le {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            self.tasks.append(task_with_timestamp)
            self.update_tasks_listbox()
            with open("tasks.txt", "a") as file:
                file.write(task_with_timestamp + "\n")
            task_window.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez entrer une tâche.")

    def confirm_remove_selected_task(self):
        """Demande confirmation avant de supprimer une tâche sélectionnée."""
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            confirm = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette tâche?")
            if confirm:
                removed_task = self.tasks[selected_index[0]]
                log_action("Suppression", removed_task)
                self.remove_selected_task(selected_index)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une tâche à supprimer.")

    def remove_selected_task(self, selected_index):
        log_action("Suppression", self.tasks[selected_index[0]])
        """Supprime la tâche sélectionnée."""
        self.tasks.pop(selected_index[0])
        self.update_tasks_listbox()
        with open("tasks.txt", "w") as file:
            file.write("\n".join(self.tasks))

    def edit_selected_task(self):
        """Affiche la fenêtre pour modifier une tâche sélectionnée."""
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            task_window = Tk()
            task_window.title("Modifier une Tâche")
            task_window.geometry("400x200")
            task_window.configure(bg="#2C3E50")

            task_label = Label(task_window, text="Modifier la Tâche:", font=("Helvetica", 16), bg="#2C3E50", fg="white")
            task_label.pack()

            task_entry = Entry(task_window, font=("Helvetica", 14))
            task_entry.pack()

            confirm_btn = Button(task_window, text="Confirmer", command=lambda: self.confirm_edit_task(task_window, task_entry.get(), selected_index[0]), bg="#3498DB", fg="white")
            confirm_btn.pack()
            task_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une tâche à modifier.")

    def confirm_edit_task(self, task_window, new_task_text, index):
        """Valide la modification d'une tâche et met à jour la liste des tâches."""
        if new_task_text:
            modified_task = self.tasks[index]
            task_with_timestamp = f"{new_task_text} - Modifié le {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            self.tasks[index] = task_with_timestamp

            log_action("Modification", modified_task, task_with_timestamp)
            self.update_tasks_listbox()
            with open("tasks.txt", "w") as file:
                file.write("\n".join(self.tasks))
            task_window.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez entrer une nouvelle tâche.")

    def update_tasks_listbox(self):
        """Met à jour la liste des tâches affichées."""
        self.tasks_listbox.delete(0, "end")
        for task in self.tasks:
            self.tasks_listbox.insert("end", task)

    def clear_window(self):
        """Efface tous les widgets de la fenêtre principale."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = MainApplication(root)
    root.mainloop()
else:
    log_action("L'utilisateur a quitté l'application.")