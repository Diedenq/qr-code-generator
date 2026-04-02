import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime

class ModernQRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Generator")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        
        self.bg_primary = "#0F172A"
        self.bg_secondary = "#1E293B"
        self.bg_card = "#334155"
        self.accent = "#3B82F6"
        self.accent_hover = "#2563EB"
        self.text_primary = "#F1F5F9"
        self.text_secondary = "#94A3B8"
        self.success = "#10B981"
        
        self.root.configure(bg=self.bg_primary)
        
        
        main_container = tk.Frame(root, bg=self.bg_primary)
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        
        header = tk.Frame(main_container, bg=self.bg_primary)
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text="QR Code Generator", 
                        font=("Segoe UI", 28, "bold"),
                        bg=self.bg_primary, fg=self.text_primary)
        title.pack(side=tk.LEFT)
        
        subtitle = tk.Label(header, text="✨", 
                           font=("Segoe UI", 24),
                           bg=self.bg_primary)
        subtitle.pack(side=tk.LEFT, padx=(10, 0))
        
        
        input_card = tk.Frame(main_container, bg=self.bg_secondary, 
                             relief=tk.FLAT, bd=0)
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        input_inner = tk.Frame(input_card, bg=self.bg_secondary)
        input_inner.pack(fill=tk.BOTH, padx=25, pady=25)
        
        
        url_label = tk.Label(input_inner, text="Enter URL or Text", 
                            font=("Segoe UI", 11),
                            bg=self.bg_secondary, fg=self.text_secondary)
        url_label.pack(anchor=tk.W, pady=(0, 8))
        
       
        entry_frame = tk.Frame(input_inner, bg=self.bg_card, 
                              highlightthickness=2, 
                              highlightbackground=self.bg_card,
                              highlightcolor=self.accent)
        entry_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.url_entry = tk.Entry(entry_frame, 
                                  font=("Segoe UI", 12),
                                  bg=self.bg_card, 
                                  fg=self.text_primary,
                                  relief=tk.FLAT,
                                  insertbackground=self.accent,
                                  bd=0)
        self.url_entry.pack(fill=tk.X, padx=15, pady=12)
        self.url_entry.focus()
        
       
        settings_label = tk.Label(input_inner, text="Settings", 
                                 font=("Segoe UI", 11),
                                 bg=self.bg_secondary, fg=self.text_secondary)
        settings_label.pack(anchor=tk.W, pady=(0, 8))
        
       
        size_frame = tk.Frame(input_inner, bg=self.bg_secondary)
        size_frame.pack(fill=tk.X, pady=(0, 15))
        
        size_label = tk.Label(size_frame, text="QR Size:", 
                             font=("Segoe UI", 10),
                             bg=self.bg_secondary, fg=self.text_primary)
        size_label.pack(side=tk.LEFT)
        
        self.size_var = tk.IntVar(value=10)
        size_slider = tk.Scale(size_frame, from_=5, to=20,
                              orient=tk.HORIZONTAL,
                              variable=self.size_var,
                              bg=self.bg_secondary,
                              fg=self.text_primary,
                              highlightthickness=0,
                              troughcolor=self.bg_card,
                              activebackground=self.accent,
                              bd=0,
                              width=15,
                              length=200)
        size_slider.pack(side=tk.LEFT, padx=(15, 0))
        
        # Цвет QR-кода
        color_frame = tk.Frame(input_inner, bg=self.bg_secondary)
        color_frame.pack(fill=tk.X, pady=(0, 15))
        
        color_label = tk.Label(color_frame, text="QR Color:", 
                              font=("Segoe UI", 10),
                              bg=self.bg_secondary, fg=self.text_primary)
        color_label.pack(side=tk.LEFT)
        
        self.color_var = tk.StringVar(value="black")
        colors = [("Black", "black"), ("Blue", "#3B82F6"), 
                 ("Purple", "#8B5CF6"), ("Red", "#EF4444")]
        
        for text, color in colors:
            rb = tk.Radiobutton(color_frame, text=text, 
                               variable=self.color_var, value=color,
                               bg=self.bg_secondary, fg=self.text_primary,
                               selectcolor=self.bg_card,
                               activebackground=self.bg_secondary,
                               activeforeground=self.text_primary,
                               font=("Segoe UI", 9))
            rb.pack(side=tk.LEFT, padx=(15, 0))
        
        # Логотип
        logo_frame = tk.Frame(input_inner, bg=self.bg_secondary)
        logo_frame.pack(fill=tk.X)
        
        logo_label = tk.Label(logo_frame, text="Logo (optional):", 
                             font=("Segoe UI", 10),
                             bg=self.bg_secondary, fg=self.text_primary)
        logo_label.pack(side=tk.LEFT)
        
        self.logo_path = None
        self.logo_btn = tk.Button(logo_frame, text="Choose Logo",
                                 command=self.choose_logo,
                                 font=("Segoe UI", 9),
                                 bg=self.bg_card,
                                 fg=self.text_primary,
                                 relief=tk.FLAT,
                                 bd=0,
                                 padx=15,
                                 pady=5,
                                 cursor="hand2")
        self.logo_btn.pack(side=tk.LEFT, padx=(15, 0))
        
        self.logo_status = tk.Label(logo_frame, text="No logo selected", 
                                   font=("Segoe UI", 9),
                                   bg=self.bg_secondary, fg=self.text_secondary)
        self.logo_status.pack(side=tk.LEFT, padx=(10, 0))
        
        self.clear_logo_btn = tk.Button(logo_frame, text="✕",
                                       command=self.clear_logo,
                                       font=("Segoe UI", 9),
                                       bg=self.bg_card,
                                       fg=self.text_secondary,
                                       relief=tk.FLAT,
                                       bd=0,
                                       padx=8,
                                       pady=5,
                                       cursor="hand2")
        self.clear_logo_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Кнопка генерации
        btn_frame = tk.Frame(main_container, bg=self.bg_primary)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.generate_btn = tk.Button(btn_frame, text="Generate QR Code",
                                     command=self.generate_qr,
                                     font=("Segoe UI", 12, "bold"),
                                     bg=self.accent,
                                     fg="white",
                                     relief=tk.FLAT,
                                     bd=0,
                                     padx=30,
                                     pady=12,
                                     cursor="hand2",
                                     activebackground=self.accent_hover,
                                     activeforeground="white")
        self.generate_btn.pack(fill=tk.X)
        
        
        self.generate_btn.bind("<Enter>", lambda e: self.generate_btn.config(bg=self.accent_hover))
        self.generate_btn.bind("<Leave>", lambda e: self.generate_btn.config(bg=self.accent))
        
        # Превью QR-кода
        preview_card = tk.Frame(main_container, bg=self.bg_secondary, 
                               relief=tk.FLAT, bd=0)
        preview_card.pack(fill=tk.BOTH, expand=True)
        
        preview_inner = tk.Frame(preview_card, bg=self.bg_secondary)
        preview_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        preview_label = tk.Label(preview_inner, text="Preview", 
                                font=("Segoe UI", 11),
                                bg=self.bg_secondary, fg=self.text_secondary)
        preview_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Канвас для превью
        self.preview_frame = tk.Frame(preview_inner, bg=self.bg_card,
                                      width=300, height=300)
        self.preview_frame.pack(expand=True)
        self.preview_frame.pack_propagate(False)
        
        self.preview_label = tk.Label(self.preview_frame, 
                                      text="Your QR code will appear here",
                                      font=("Segoe UI", 10),
                                      bg=self.bg_card, 
                                      fg=self.text_secondary)
        self.preview_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Создание папки для сохранения
        self.output_dir = "qr_codes"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def choose_logo(self):
        filename = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.logo_path = filename
            # Показываем только имя файла
            logo_name = os.path.basename(filename)
            if len(logo_name) > 20:
                logo_name = logo_name[:17] + "..."
            self.logo_status.config(text=f"✓ {logo_name}", fg=self.success)
    
    def clear_logo(self):
        self.logo_path = None
        self.logo_status.config(text="No logo selected", fg=self.text_secondary)
    
    def generate_qr(self):
        url = self.url_entry.get().strip()
        
        if not url:
            self.show_notification("⚠️ Please enter URL or text", error=True)
            return
        
        try:
            # Создание QR-кода
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.size_var.get(),
                border=4,
            )
            
            qr.add_data(url)
            qr.make(fit=True)
            
            # Создание изображения с выбранным цветом
            img = qr.make_image(fill_color=self.color_var.get(), 
                               back_color="white").convert('RGB')
            
            
            if self.logo_path:
                img = self.add_logo_to_qr(img)
            
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath)
            
            # Показ превью
            self.show_preview(img)
            
            
            self.show_notification(f"✅ Saved to {filename}")
            
        except Exception as e:
            self.show_notification(f"❌ Error: {str(e)}", error=True)
    
    def add_logo_to_qr(self, qr_img):
        """Добавляет логотип в центр QR-кода"""
        try:
            logo = Image.open(self.logo_path)
            
            
            qr_width, qr_height = qr_img.size
            
            
            logo_size = int(qr_width * 0.25)
            
            
            logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            
            logo_bg_size = int(logo_size * 1.1)
            logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')
            
            
            logo_pos = ((logo_bg_size - logo.width) // 2, 
                       (logo_bg_size - logo.height) // 2)
            
            #
            if logo.mode == 'RGBA':
                logo_bg.paste(logo, logo_pos, logo)
            else:
                logo_bg.paste(logo, logo_pos)
            
            
            qr_pos = ((qr_width - logo_bg_size) // 2, 
                     (qr_height - logo_bg_size) // 2)
            
            
            qr_img.paste(logo_bg, qr_pos)
            
            return qr_img
            
        except Exception as e:
            self.show_notification(f"⚠️ Logo error: {str(e)}", error=True)
            return qr_img
    
    def show_preview(self, img):
        # Изменение размера для превью
        img_resized = img.resize((280, 280), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        
        self.preview_label.config(image=photo, text="")
        self.preview_label.image = photo
    
    def show_notification(self, message, error=False):
        color = "#EF4444" if error else self.success
        
        notification = tk.Label(self.root, text=message,
                               font=("Segoe UI", 10),
                               bg=color,
                               fg="white",
                               padx=20, pady=10)
        notification.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        
        self.root.after(3000, notification.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernQRGenerator(root)
    root.mainloop()