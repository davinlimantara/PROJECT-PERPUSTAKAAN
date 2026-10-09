import tkinter as tk
from PIL import Image, ImageTk  # Library untuk mengolah gambar
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_NAV,
    FONT_CARD_TITLE, FONT_CARD_BODY, ARTIKEL_PERPUSTAKAAN, HoverButton,
)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # ==========================================================
        # 1. NAVBAR
        # ==========================================================
        navbar = tk.Frame(self, bg=COLOR_PRIMARY, height=70)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        # Frame pembungkus Logo & Teks agar rapi
        logo_frame = tk.Frame(navbar, bg=COLOR_PRIMARY)
        logo_frame.pack(side="left", padx=30)

        # [GAMBAR 1] Logo di Navbar
        try:
            logo_raw = Image.open("image.png").resize((32, 32), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo_raw)
            
            logo_icon = tk.Label(logo_frame, image=self.logo_img, bg=COLOR_PRIMARY)
            logo_icon.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Gambar logo tidak ditemukan atau gagal dimuat: {e}")

        logo_label = tk.Label(
            logo_frame, text="Perpustakaan Digital",
            bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 16, "bold")
        )
        logo_label.pack(side="left")

        self.nav_right = tk.Frame(navbar, bg=COLOR_PRIMARY)
        self.nav_right.pack(side="right", padx=30)

        # ==========================================================
        # 2. HERO / BANNER
        # ==========================================================
        hero = tk.Frame(self, bg=COLOR_ACCENT, height=180)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        # [GAMBAR 2] Banner Background Hero (Opsional)
        try:
            hero_bg_raw = Image.open("assets/hero_banner.png").resize((1200, 180), Image.Resampling.LANCZOS)
            self.hero_bg_img = ImageTk.PhotoImage(hero_bg_raw)
            
            hero_bg_label = tk.Label(hero, image=self.hero_bg_img, bg=COLOR_ACCENT)
            hero_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Gambar hero banner tidak ditemukan/opsional: {e}")

        hero_inner = tk.Frame(hero, bg=COLOR_ACCENT)
        hero_inner.pack(expand=True)

        tk.Label(
            hero_inner, text="MONO DIGITAL LIBRARY",
            bg=COLOR_ACCENT, fg="white", font=FONT_TITLE
        ).pack(pady=(30, 5))

        tk.Label(
            hero_inner,
            text="Jelajahi koleksi buku, baca artikel terbaru, dan kelola peminjamanmu di sini.",
            bg=COLOR_ACCENT, fg="#eaf2f8", font=FONT_SUBTITLE
        ).pack()

        # ==========================================================
        # 3. CONTENT AREA (ARTIKEL DIBATASI 2 BARAIS KEBAWAH)
        # ==========================================================
        content_area = tk.Frame(self, bg=COLOR_BG)
        content_area.pack(fill="both", expand=True, padx=40, pady=25)

        tk.Label(
            content_area, text="Newest article and information",
            bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(0, 15))

        cards_frame = tk.Frame(content_area, bg=COLOR_BG)
        cards_frame.pack(fill="both", expand=True)

        # Mengatur agar kolom tunggal (kolom 0) memenuhi lebar area secara responsif
        cards_frame.grid_columnconfigure(0, weight=1)

        # Menggunakan slicing [:2] agar hanya mengambil maksimal 2 artikel pertama
        for idx, artikel in enumerate(ARTIKEL_PERPUSTAKAAN[:2]):
            self._build_article_card(cards_frame, artikel, row=idx, col=0)

        # ==========================================================
        # 4. FOOTER
        # ==========================================================
        footer = tk.Frame(self, bg=COLOR_PRIMARY, height=36)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(
            footer, text="© 2026 Perpustakaan Digital — Semua hak cipta dilindungi.",
            bg=COLOR_PRIMARY, fg="#bdc3c7", font=("Segoe UI", 9)
        ).pack(pady=8)

    # ==========================================================
    # BUILD CARD (ARTIKEL)
    # ==========================================================
    def _build_article_card(self, parent, artikel, row, col):
        card = tk.Frame(
            parent, bg=COLOR_CARD, bd=0, highlightthickness=1,
            highlightbackground="#dfe6e9"
        )
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        # [GAMBAR 3] Gambar Sampul Artikel pada Kartu
        if "gambar" in artikel and artikel["gambar"]:
            try:
                img_raw = Image.open(artikel["gambar"]).resize((960, 200), Image.Resampling.LANCZOS)
                card.image_ref = ImageTk.PhotoImage(img_raw)

                img_label = tk.Label(card, image=card.image_ref, bg=COLOR_CARD)
                img_label.pack(fill="x", side="top")
            except Exception as e:
                print(f"Gagal memuat gambar artikel '{artikel.get('judul')}': {e}")

        badge = tk.Label(
            card, text=artikel["kategori"], bg="#eaf2f8", fg=COLOR_ACCENT,
            font=("Segoe UI", 9, "bold"), padx=10, pady=3
        )
        badge.pack(anchor="w", padx=18, pady=(12, 8))

        tk.Label(
            card, text=artikel["judul"], bg=COLOR_CARD, fg=COLOR_TEXT,
            font=FONT_CARD_TITLE, wraplength=900, justify="left"
        ).pack(anchor="w", padx=18)

        tk.Label(
            card, text=artikel["ringkasan"], bg=COLOR_CARD, fg=COLOR_MUTED,
            font=FONT_CARD_BODY, wraplength=900, justify="left"
        ).pack(anchor="w", padx=18, pady=(6, 18))

    # ==========================================================
    # ON SHOW
    # ==========================================================
    def on_show(self):
        for widget in self.nav_right.winfo_children():
            widget.destroy()

        if self.controller.current_user:
            tk.Label(
                self.nav_right, text=f"👤 {self.controller.current_user}",
                bg=COLOR_PRIMARY, fg="white", font=FONT_NAV
            ).pack(side="left", padx=(0, 15))

            HoverButton(
                self.nav_right, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
                text="⫶☰", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2",
                command=lambda: self.controller.show_frame("BookManagementPage")
            ).pack(side="left", padx=(0, 10))

            HoverButton(
                self.nav_right, bg_normal="#c0392b", bg_hover="#a93226",
                text="➜]", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2", command=self.controller.logout
            ).pack(side="left")
        else:
            HoverButton(
                self.nav_right, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
                text="Login", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2",
                command=lambda: self.controller.show_frame("SignInPage")
            ).pack(side="left", padx=(0, 10))

            HoverButton(
                self.nav_right, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
                text="Sign Up", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2",
                command=lambda: self.controller.show_frame("SignUpPage")
            ).pack(side="left")