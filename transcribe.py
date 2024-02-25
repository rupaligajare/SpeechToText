import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
from docx import Document
from fpdf import FPDF

def transcribe_audio():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showerror("Error", "Please select an audio file")
        return

    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data)
            result_text.config(state='normal')  # Make text editable
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, transcript)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def convert_to_word():
    text = result_text.get("1.0", tk.END)
    if not text.strip():
        messagebox.showerror("Error", "No text to convert")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
    if file_path:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)
        messagebox.showinfo("Success", "File converted to Word successfully")

def convert_to_pdf():
    text = result_text.get("1.0", tk.END)
    if not text.strip():
        messagebox.showerror("Error", "No text to convert")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Document", "*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=text)
        pdf.output(file_path)
        messagebox.showinfo("Success", "File converted to PDF successfully")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav;*.flac;*.ogg;*.mp3")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# Create tkinter window
window = tk.Tk()
window.title("Audio Transcription")
window.geometry("500x520")  # Increased height to accommodate additional buttons

# Set window background color
window.configure(bg="#f0f0f0")

# File Selection
file_frame = tk.Frame(window, bg="#f0f0f0")
file_frame.pack(pady=10)

file_label = tk.Label(file_frame, text="Select Audio File:", bg="#f0f0f0", font=("Helvetica", 12))
file_label.pack(side=tk.LEFT, padx=(10,5))

file_entry = tk.Entry(file_frame, width=40)
file_entry.pack(side=tk.LEFT, padx=(0,10))

browse_button = tk.Button(file_frame, text="Browse", command=browse_file, bg="#008CBA", fg="white")
browse_button.pack(side=tk.LEFT)

# Transcribe Button
transcribe_button = tk.Button(window, text="Transcribe", command=transcribe_audio, bg="#4CAF50", fg="white")
transcribe_button.pack(pady=(10,0))

# Result Text
result_frame = tk.Frame(window, bg="#f0f0f0")
result_frame.pack(pady=(10,0))

result_label = tk.Label(result_frame, text="Transcription Result:", bg="#f0f0f0", font=("Helvetica", 12))
result_label.pack()

result_text = tk.Text(result_frame, height=10, width=60)
result_text.pack()

# Convert to Word Button
word_button = tk.Button(window, text="Convert to Word", command=convert_to_word, bg="#FF5733", fg="white")
word_button.pack(side=tk.LEFT, padx=5, pady=5)

# Convert to PDF Button
pdf_button = tk.Button(window, text="Convert to PDF", command=convert_to_pdf, bg="#FF5733", fg="white")
pdf_button.pack(side=tk.LEFT, padx=5, pady=5)

window.mainloop()
