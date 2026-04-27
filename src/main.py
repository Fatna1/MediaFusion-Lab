"""
Multimedia Technology Application - Main UI
Integrates all 8 algorithms for Text, Image, Audio, and Video processing
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading

# Import algorithm modules
import image
import video
import audio
import text_algo

class MultimediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediaFusion Lab")
        self.root.geometry("900x700")
        
        # ========== BLACK BACKGROUND THEME ==========
        self.bg_color = "#000000"      # Pure black background
        self.bg_secondary = "#1a1a1a"  # Dark gray for secondary elements
        self.fg_color = "#ffffff"      # White text
        self.accent_color = "#4ED362"  # Green accent
        self.button_bg = "#333333"     # Dark gray buttons
        self.button_fg = "#ffffff"     # White button text
        self.button_active = "#C6EFC8" # Light green when hovering
        self.output_bg = "#0a0a0a"     # Very dark for output area
        self.output_fg = "#d0d7d0"     # Light gray text for output
        
        # Apply black background to root window
        self.root.configure(bg=self.bg_color)
        
        # Current file paths
        self.current_image_path = None
        self.current_video_path = None
        self.current_audio_path = None
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Title with black background
        title_label = tk.Label(self.root, text="MediaFusion Lab", 
                               font=('Arial', 18, 'bold'), 
                               bg=self.bg_color, 
                               fg=self.accent_color)
        title_label.pack(pady=10)
        
        # Configure ttk style for tabs (dark theme)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab', 
                       background=self.button_bg,
                       foreground=self.fg_color,
                       padding=[10, 5])
        style.map('TNotebook.Tab',
                 background=[('selected', self.accent_color),
                           ('active', self.button_active)])
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_image_tab()
        self.create_video_tab()
        self.create_audio_tab()
        self.create_text_tab()
        self.create_ai_bonus_tab()
        
        # Output display area with dark theme
        output_frame = tk.LabelFrame(self.root, text="Output / Results", 
                                     bg=self.bg_secondary, 
                                     fg=self.fg_color,
                                     font=('Arial', 10, 'bold'))
        output_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, 
                                                      wrap=tk.WORD, 
                                                      font=('Courier', 10),
                                                      bg=self.output_bg,
                                                      fg=self.output_fg,
                                                      insertbackground=self.fg_color)
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def create_image_tab(self):
        tab = tk.Frame(self.notebook, bg=self.bg_secondary)
        self.notebook.add(tab, text="Image Processing")
        
        # File selection
        tk.Button(tab, text="Select Image", command=self.select_image,
                 bg=self.button_bg, fg=self.button_fg, 
                 font=('Arial', 10, 'bold'),
                 activebackground=self.button_active,
                 activeforeground=self.button_fg,
                 padx=20, pady=5).pack(pady=10)
        
        # Algorithm buttons
        btn_frame = tk.Frame(tab, bg=self.bg_secondary)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="1. Grayscale Conversion", 
                 command=self.run_grayscale, width=25, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
        tk.Button(btn_frame, text="2. Edge Detection (Canny)", 
                 command=self.run_edge_detection, width=25, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
    def create_video_tab(self):
        tab = tk.Frame(self.notebook, bg=self.bg_secondary)
        self.notebook.add(tab, text="Video Processing")
        
        tk.Button(tab, text="Select Video", command=self.select_video,
                 bg=self.button_bg, fg=self.button_fg, 
                 font=('Arial', 10, 'bold'),
                 activebackground=self.button_active,
                 activeforeground=self.button_fg,
                 padx=20, pady=5).pack(pady=10)
        
        btn_frame = tk.Frame(tab, bg=self.bg_secondary)
        btn_frame.pack(pady=10)
        
        # Frame interval entry
        interval_frame = tk.Frame(btn_frame, bg=self.bg_secondary)
        interval_frame.pack(pady=5)
        tk.Label(interval_frame, text="Frame interval (every N frames):", 
                bg=self.bg_secondary, fg=self.fg_color).pack(side=tk.LEFT)
        self.frame_interval = tk.Entry(interval_frame, width=10,
                                       bg=self.output_bg,
                                       fg=self.fg_color,
                                       insertbackground=self.fg_color)
        self.frame_interval.insert(0, "30")
        self.frame_interval.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="3. Extract Frames", 
                 command=self.run_extract_frames, width=25, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
        tk.Button(btn_frame, text="4. Motion Detection", 
                 command=self.run_motion_detection, width=25, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
    def create_audio_tab(self):
        tab = tk.Frame(self.notebook, bg=self.bg_secondary)
        self.notebook.add(tab, text="Audio Processing")
        
        tk.Button(tab, text="Select Audio (WAV)", command=self.select_audio,
                 bg=self.button_bg, fg=self.button_fg, 
                 font=('Arial', 10, 'bold'),
                 activebackground=self.button_active,
                 activeforeground=self.button_fg,
                 padx=20, pady=5).pack(pady=10)
        
        btn_frame = tk.Frame(tab, bg=self.bg_secondary)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="5. Fourier Transform (FFT) Analysis", 
                 command=self.run_fft_analysis, width=30, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
        # Cutoff frequency for noise reduction
        cutoff_frame = tk.Frame(btn_frame, bg=self.bg_secondary)
        cutoff_frame.pack(pady=5)
        tk.Label(cutoff_frame, text="Cutoff frequency (Hz):", 
                bg=self.bg_secondary, fg=self.fg_color).pack(side=tk.LEFT)
        self.cutoff_freq = tk.Entry(cutoff_frame, width=10,
                                    bg=self.output_bg,
                                    fg=self.fg_color,
                                    insertbackground=self.fg_color)
        self.cutoff_freq.insert(0, "1000")
        self.cutoff_freq.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="6. Noise Reduction (Low-Pass Filter)", 
                 command=self.run_noise_reduction, width=30, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
    def create_text_tab(self):
        tab = tk.Frame(self.notebook, bg=self.bg_secondary)
        self.notebook.add(tab, text="Text Processing")
        
        # Text input area
        tk.Label(tab, text="Enter or paste text:", 
                bg=self.bg_secondary, fg=self.fg_color).pack(pady=5)
        self.text_input = scrolledtext.ScrolledText(tab, height=10, width=80,
                                                     bg=self.output_bg,
                                                     fg=self.fg_color,
                                                     insertbackground=self.fg_color)
        self.text_input.pack(pady=5, padx=10)
        
        # Example text button
        tk.Button(tab, text="Load Example", command=self.load_example_text,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
        btn_frame = tk.Frame(tab, bg=self.bg_secondary)
        btn_frame.pack(pady=10)
        
        # Shift for Caesar cipher
        shift_frame = tk.Frame(btn_frame, bg=self.bg_secondary)
        shift_frame.pack(pady=5)
        tk.Label(shift_frame, text="Caesar shift (1-25):", 
                bg=self.bg_secondary, fg=self.fg_color).pack(side=tk.LEFT)
        self.caesar_shift = tk.Entry(shift_frame, width=10,
                                     bg=self.output_bg,
                                     fg=self.fg_color,
                                     insertbackground=self.fg_color)
        self.caesar_shift.insert(0, "3")
        self.caesar_shift.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="7. Word Frequency Counter", 
                 command=self.run_word_frequency, width=25, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)
        
        tk.Button(btn_frame, text="8. Caesar Cipher Encryption", 
                 command=self.run_caesar_encrypt, width=25, height=2,
                 bg=self.button_bg, fg=self.button_fg,
                 activebackground=self.button_active,
                 activeforeground=self.button_fg).pack(pady=5)

    # ========== AI BONUS TAB ==========
    def create_ai_bonus_tab(self):
        tab = tk.Frame(self.notebook, bg=self.bg_secondary)
        self.notebook.add(tab, text="AI Bonus")
    
        # Title
        title = tk.Label(tab, text="AI Content Generator", 
                    font=('Arial', 16, 'bold'),
                    bg=self.bg_secondary, fg='#00ff00')
        title.pack(pady=20)
    
        # Prompt input
        tk.Label(tab, text="Enter your prompt:", 
            bg=self.bg_secondary, fg='white').pack()
        self.ai_prompt = tk.Text(tab, height=4, width=70,
                             bg='#0a0a0a', fg='white',
                             insertbackground='white')
        self.ai_prompt.pack(pady=10, padx=20)
    
        # Example prompt button
        tk.Button(tab, text="Example", command=self.set_example_prompt,
             bg='#333', fg='white').pack(pady=5)
    
        # Buttons frame
        btn_frame = tk.Frame(tab, bg=self.bg_secondary)
        btn_frame.pack(pady=20)
    
        # Three generation buttons
        tk.Button(btn_frame, text="Generate Image", 
             command=self.ai_text_to_image,
             bg='#4CAF50', fg='white', width=20, height=2,
             font=('Arial', 10, 'bold')).pack(pady=5)
    
        tk.Button(btn_frame, text="Generate Video", 
             command=self.ai_text_to_video,
             bg='#FF9800', fg='white', width=20, height=2,
             font=('Arial', 10, 'bold')).pack(pady=5)
    
        # Status label
        self.ai_status = tk.Label(tab, text="Ready", 
                              bg=self.bg_secondary, fg='#00ff00')
        self.ai_status.pack(pady=10)

    def set_example_prompt(self):
        """Set example prompt"""
        example = "A beautiful sunset over mountains"
        self.ai_prompt.delete(1.0, tk.END)
        self.ai_prompt.insert(1.0, example)

    def ai_text_to_image(self):
        """Generate image from text"""
        prompt = self.ai_prompt.get(1.0, tk.END).strip()
        if not prompt:
            messagebox.showwarning("No prompt", "Please enter a prompt")
            return
        
        self.ai_status.config(text="Generating image...")
        self.update_output(f"\n[IMAGE] Generating image for: {prompt}\n")
        
        def generate():
            try:
                from ai_bonus import AIGenerator
                ai = AIGenerator()
                result, msg = ai.text_to_image(prompt)
                self.root.after(0, lambda: self.update_output(f"{msg}\n"))
                self.root.after(0, lambda: self.ai_status.config(text="Image generated"))
            except Exception as e:
                self.root.after(0, lambda: self.update_output(f"Error: {e}\n"))
                self.root.after(0, lambda: self.ai_status.config(text="Error"))
        
        threading.Thread(target=generate, daemon=True).start()


    def ai_text_to_video(self):
        """Generate video from text"""
        prompt = self.ai_prompt.get(1.0, tk.END).strip()
        if not prompt:
            messagebox.showwarning("No prompt", "Please enter a prompt")
            return
        
        self.ai_status.config(text="Generating video...")
        self.update_output(f"\n[VIDEO] Generating video for: {prompt}\n")
        
        def generate():
            try:
                from ai_bonus import AIGenerator
                ai = AIGenerator()
                result, msg = ai.text_to_video(prompt)
                self.root.after(0, lambda: self.update_output(f"{msg}\n"))
                self.root.after(0, lambda: self.ai_status.config(text="Video generated"))
            except Exception as e:
                self.root.after(0, lambda: self.update_output(f"Error: {e}\n"))
                self.root.after(0, lambda: self.ai_status.config(text="Error"))
        
        threading.Thread(target=generate, daemon=True).start()

    # ========== IMAGE METHODS ==========
    def select_image(self):
        self.current_image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if self.current_image_path:
            self.update_output(f"Selected image: {self.current_image_path}\n")
    
    def run_grayscale(self):
        if not self.current_image_path:
            messagebox.showwarning("No file", "Please select an image first")
            return
        
        self.run_in_thread(image.grayscale_conversion, self.current_image_path)
    
    def run_edge_detection(self):
        if not self.current_image_path:
            messagebox.showwarning("No file", "Please select an image first")
            return
        
        self.run_in_thread(image.edge_detection, self.current_image_path)
    
    # ========== VIDEO METHODS ==========
    def select_video(self):
        self.current_video_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if self.current_video_path:
            self.update_output(f"Selected video: {self.current_video_path}\n")
    
    def run_extract_frames(self):
        if not self.current_video_path:
            messagebox.showwarning("No file", "Please select a video first")
            return
        
        try:
            interval = int(self.frame_interval.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid frame interval")
            return
        
        self.run_in_thread(video.extract_frames, 
                          self.current_video_path, interval)
    
    def run_motion_detection(self):
        if not self.current_video_path:
            messagebox.showwarning("No file", "Please select a video first")
            return
        
        self.run_in_thread(video.motion_detection, self.current_video_path)
    
    # ========== AUDIO METHODS ==========
    def select_audio(self):
        self.current_audio_path = filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav")]
        )
        if self.current_audio_path:
            self.update_output(f"Selected audio: {self.current_audio_path}\n")
    
    def run_fft_analysis(self):
        if not self.current_audio_path:
            messagebox.showwarning("No file", "Please select an audio file first")
            return
        
        self.run_in_thread(audio.fourier_transform_analysis, 
                          self.current_audio_path)
    
    def run_noise_reduction(self):
        if not self.current_audio_path:
            messagebox.showwarning("No file", "Please select an audio file first")
            return
        
        try:
            cutoff = int(self.cutoff_freq.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid cutoff frequency")
            return
        
        self.run_in_thread(audio.noise_reduction, 
                          self.current_audio_path, cutoff)
    
    # ========== TEXT METHODS ==========
    def load_example_text(self):
        example = """This is a Multimedia technology course final Project, it handles various types of Data, including Video, text, images, and audio. 
This is an example text for word frequency analysis. The system will count how many times each word appears.
Multimedia applications are used in education, entertainment, and business. Understanding word frequencies can help 
in text analysis and natural language processing. This example includes repeated words to demonstrate the frequency counter."""
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, example)
    
    def run_word_frequency(self):
        text = self.text_input.get(1.0, tk.END)
        if not text.strip():
            messagebox.showwarning("No text", "Please enter some text first")
            return
        
        result, explanation = text_algo.word_frequency_counter(text)
        self.update_output(f"\n{result}\n\n{explanation}\n")
    
    def run_caesar_encrypt(self):
        text = self.text_input.get(1.0, tk.END)
        if not text.strip():
            messagebox.showwarning("No text", "Please enter some text first")
            return
        
        try:
            shift = int(self.caesar_shift.get())
            if shift < 1 or shift > 25:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Shift must be between 1 and 25")
            return
        
        encrypted, explanation = text_algo.caesar_cipher_encrypt(text, shift)
        self.update_output(f"\nOriginal text:\n{text}\n")
        self.update_output(f"\nEncrypted (shift={shift}):\n{encrypted}\n")
        self.update_output(f"\n{explanation}\n")
    
    # ========== UTILITY METHODS ==========
    def update_output(self, message):
        """Add message to output area"""
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def run_in_thread(self, func, *args):
        """Run algorithm in separate thread to prevent UI freezing"""
        def task():
            try:
                result, message = func(*args)
                self.root.after(0, lambda: self.update_output(f"\n{message}\n"))
                if result is not None:
                    self.root.after(0, lambda: self.update_output(f"Operation completed\n"))
            except Exception as e:
                self.root.after(0, lambda: self.update_output(f"\nError: {str(e)}\n"))
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        self.update_output("Processing...\n")

def main():
    root = tk.Tk()
    app = MultimediaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()




