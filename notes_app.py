import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

class ZenNotes(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ZenNotes - Modern Writing")
        self.geometry("1100x700")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_note_id = None

        # Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="ZEN NOTES", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=(20, 10), padx=20)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_search)
        self.search_bar = ctk.CTkEntry(self.sidebar, placeholder_text="🔍 Search notes...", 
                                       textvariable=self.search_var)
        self.search_bar.pack(pady=10, padx=20, fill="x")

        self.new_btn = ctk.CTkButton(self.sidebar, text="+ New Note", command=self.clear_editor, 
                                     fg_color="#2ecc71", hover_color="#27ae60")
        self.new_btn.pack(pady=10, padx=20, fill="x")

        self.scrollable_notes_frame = ctk.CTkScrollableFrame(self.sidebar, label_text="My Notes")
        self.scrollable_notes_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Editor Area ---
        self.editor_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)

        self.title_entry = ctk.CTkEntry(self.editor_frame, placeholder_text="Note Title", 
                                        font=ctk.CTkFont(size=28, weight="bold"), 
                                        border_width=0, fg_color="transparent")
        self.title_entry.pack(fill="x", pady=(0, 10))

        self.textbox = ctk.CTkTextbox(self.editor_frame, font=("Inter", 16), undo=True, wrap="word")
        self.textbox.pack(fill="both", expand=True)

        # --- Bottom Buttons ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=1, sticky="ew", padx=30, pady=20)

        self.delete_btn = ctk.CTkButton(self.button_frame, text="Delete Current", fg_color="#e74c3c", 
                                        hover_color="#c0392b", command=self.delete_note)
        self.delete_btn.pack(side="left")

        self.save_btn = ctk.CTkButton(self.button_frame, text="Save Changes", command=self.save_note, width=150)
        self.save_btn.pack(side="right")

        self.refresh_note_list()

    # --- Feature Logic ---

    def rename_note_dialog(self, note_id, old_title):
        """Opens a modern dialog to rename the note."""
        dialog = ctk.CTkInputDialog(text=f"Rename '{old_title}' to:", title="Rename Note")
        new_name = dialog.get_input()
        
        if new_name and new_name.strip():
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET title = ? WHERE id = ?", (new_name, note_id))
            conn.commit()
            conn.close()
            
            # If the renamed note is currently open, update the editor title
            if self.current_note_id == note_id:
                self.title_entry.delete(0, 'end')
                self.title_entry.insert(0, new_name)
                
            self.refresh_note_list()

    def update_search(self, *args):
        self.refresh_note_list(self.search_var.get())

    def refresh_note_list(self, filter_text=""):
        for widget in self.scrollable_notes_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        if filter_text:
            cursor.execute("SELECT id, title FROM notes WHERE title LIKE ? ORDER BY id DESC", ('%' + filter_text + '%',))
        else:
            cursor.execute("SELECT id, title FROM notes ORDER BY id DESC")
        notes = cursor.fetchall()
        conn.close()

        for note_id, title in notes:
            display_title = title if title.strip() else "Untitled Note"
            
            # Container frame for the button and rename option
            item_frame = ctk.CTkFrame(self.scrollable_notes_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)

            btn = ctk.CTkButton(item_frame, text=f"📄 {display_title}", 
                                anchor="w", fg_color="transparent", text_color=("gray10", "gray90"),
                                hover_color=("gray70", "gray30"),
                                command=lambda n_id=note_id: self.load_note(n_id))
            btn.pack(side="left", fill="x", expand=True)

            # Modern 'Rename' icon-button inside the list
            rename_btn = ctk.CTkButton(item_frame, text="✏️", width=30, fg_color="transparent",
                                       hover_color=("gray70", "gray30"),
                                       command=lambda n_id=note_id, t=display_title: self.rename_note_dialog(n_id, t))
            rename_btn.pack(side="right", padx=5)

    def save_note(self):
        title = self.title_entry.get()
        content = self.textbox.get("1.0", "end-1c")
        if not title.strip() and not content.strip(): return

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        if self.current_note_id:
            cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, self.current_note_id))
        else:
            cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            self.current_note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        self.refresh_note_list()

    def load_note(self, note_id):
        self.current_note_id = note_id
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        conn.close()
        if note:
            self.title_entry.delete(0, 'end')
            self.title_entry.insert(0, note[0])
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", note[1])

    def delete_note(self):
        if not self.current_note_id: return
        if messagebox.askyesno("Confirm", "Delete this note?"):
            conn = sqlite3.connect("notes.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (self.current_note_id,))
            conn.commit()
            conn.close()
            self.clear_editor()
            self.refresh_note_list()

    def clear_editor(self):
        self.current_note_id = None
        self.title_entry.delete(0, 'end')
        self.textbox.delete("1.0", "end")

if __name__ == "__main__":
    init_db()
    app = ZenNotes()
    app.mainloop()