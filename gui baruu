"""
gui.py — KizunaGUI: all tkinter views and widgets.
Data / business logic lives in main.py (KizunaApp).
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import os
import subprocess
import sys


class KizunaGUI:

    PINK  = "#ffc0cb"
    DPINK = "#e57a8a"
    WHITE = "#ffffff"
    LIGHT = "#f9f9f9"
    GRAY  = "#888888"
    DGRAY = "#333333"

    # ─── INIT ─────────────────────────────────────────────────────────────────

    def __init__(self, app):
        self.app          = app          # KizunaApp instance (data / logic)
        self.login_attempts = 3
        self.current_user   = None

        self.root = tk.Tk()
        self.root.title("Kizuna")
        self.root.geometry("900x620")
        self.root.config(bg="#f2f2f2")

    def run(self):
        self.show_login()
        self.root.mainloop()

    # ─── SHARED HELPERS ───────────────────────────────────────────────────────

    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    def create_card(self, width=380, height=420):
        card = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=width, height=height)
        return card

    def make_scrollable(self, parent, bg="#f9f9f9"):
        canvas = tk.Canvas(parent, bg=bg, bd=0, highlightthickness=0)
        sb     = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg=bg)
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        return canvas, inner

    def add_placeholder(self, entry, placeholder, is_password=False):
        entry.placeholder            = placeholder
        entry.is_password            = is_password
        entry.is_showing_placeholder = True
        entry.config(fg="gray")
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.is_showing_placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")
                if is_password:
                    entry.config(show="*")
                entry.is_showing_placeholder = False

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="gray")
                if is_password:
                    entry.config(show="")
                entry.is_showing_placeholder = True

        entry.bind("<FocusIn>",  on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def get_entry_value(self, entry):
        return "" if entry.is_showing_placeholder else entry.get()

    def open_edit_dialog(self, title, current_text, on_save_fn, parent_win=None):
        parent = parent_win or self.root
        win = tk.Toplevel(parent)
        win.title(title)
        win.geometry("400x220")
        win.config(bg="white")
        win.grab_set()
        tk.Label(win, text=title, font=("Segoe UI", 12, "bold"), bg="white").pack(pady=10)
        txt = tk.Text(win, width=46, height=5, font=("Segoe UI", 10),
                      bd=1, relief="solid", wrap="word")
        txt.pack(padx=16, pady=(0, 8))
        txt.insert("1.0", current_text)
        txt.focus_set()

        def save():
            new_text = txt.get("1.0", tk.END).strip()
            if not new_text:
                messagebox.showerror("Error", "Teks tidak boleh kosong", parent=win)
                return
            on_save_fn(new_text)
            win.destroy()

        btn_row = tk.Frame(win, bg="white")
        btn_row.pack()
        tk.Button(btn_row, text="Simpan", bg=self.PINK,
                  font=("Segoe UI", 10, "bold"), bd=0, padx=12, pady=4,
                  command=save).pack(side="left", padx=4)
        tk.Button(btn_row, text="Batal", bg="#eee",
                  font=("Segoe UI", 10), bd=0, padx=12, pady=4,
                  command=win.destroy).pack(side="left", padx=4)

    # ─── SIDEBAR ──────────────────────────────────────────────────────────────

    def create_sidebar(self, title):
        sidebar = tk.Frame(self.root, bg=self.PINK, width=255)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text=title, font=("Segoe UI", 28, "bold"),
                 bg=self.PINK).pack(pady=(28, 10), anchor="w", padx=16)
        return sidebar

    def add_sidebar_btn(self, sidebar, label, cmd):
        tk.Frame(sidebar, bg="#e8a0b0", height=1).pack(fill="x")
        tk.Button(
            sidebar, text=label, width=22, anchor="w", padx=16,
            font=("Segoe UI", 11), bg="#f0d0d8", fg="#222222",
            bd=0, relief="flat", cursor="hand2", command=cmd,
            activebackground="#e8a0b0", activeforeground="#111111"
        ).pack(fill="x", ipady=10)
        tk.Frame(sidebar, bg="#e8a0b0", height=1).pack(fill="x")

    # ─── LOGIN ────────────────────────────────────────────────────────────────

    def show_login(self):
        self.clear_window()
        card = self.create_card()
        tk.Label(card, text="Kizuna", font=("Segoe UI", 24, "bold"), bg="white").pack(pady=30)

        self.login_user = tk.Entry(card, width=30, font=("Segoe UI", 11))
        self.login_user.pack(pady=5)
        self.add_placeholder(self.login_user, "Email / Username")

        self.login_pass = tk.Entry(card, width=30, font=("Segoe UI", 11))
        self.login_pass.pack(pady=5)
        self.add_placeholder(self.login_pass, "Password", is_password=True)

        self.login_user.bind("<Return>", lambda e: self.login_pass.focus())
        self.login_pass.bind("<Return>", lambda e: self._do_login())

        tk.Button(card, text="Login", width=15, bg=self.PINK,
                  font=("Segoe UI", 10, "bold"), command=self._do_login).pack(pady=15)
        tk.Button(card, text="New Here? Register", bd=0, bg="white",
                  fg="blue", cursor="hand2", command=self.show_register).pack()

        tk.Label(card,
                 text="Demo: rina / rina1234  |  admin / admin123  |  moderator / mod12345",
                 font=("Segoe UI", 8), bg="white", fg="gray").pack(pady=(8, 0))

    def _do_login(self):
        identifier = self.get_entry_value(self.login_user)
        password   = self.get_entry_value(self.login_pass)
        user = self.app.authenticate(identifier, password)
        if user:
            self.login_attempts = 3
            self.current_user   = user
            role = user["role"]
            if role == "Admin":
                self.show_admin_dashboard(user)
            elif role == "Moderator":
                self.show_moderator_dashboard(user)
            else:
                self.show_user_dashboard(user)
            return
        self.login_attempts -= 1
        if self.login_attempts > 0:
            messagebox.showerror("Login Gagal",
                f"Username atau Password salah\nSisa percobaan: {self.login_attempts}")
        else:
            messagebox.showerror("Login Gagal", "Akun terkunci sementara")
            self.login_attempts = 3

    # ─── REGISTER ─────────────────────────────────────────────────────────────

    def show_register(self):
        self.clear_window()
        card = self.create_card(420, 500)
        tk.Button(card, text="← Back", bd=0, bg="white",
                  command=self.show_login).pack(anchor="w", padx=10, pady=10)
        tk.Label(card, text="Kizuna", font=("Segoe UI", 24, "bold"), bg="white").pack(pady=10)

        self.reg_fullname = tk.Entry(card, width=35, font=("Segoe UI", 11))
        self.reg_fullname.pack(pady=5)
        self.add_placeholder(self.reg_fullname, "Nama Lengkap")

        self.reg_username = tk.Entry(card, width=35, font=("Segoe UI", 11))
        self.reg_username.pack(pady=5)
        self.add_placeholder(self.reg_username, "Username")

        self.reg_email = tk.Entry(card, width=35, font=("Segoe UI", 11))
        self.reg_email.pack(pady=5)
        self.add_placeholder(self.reg_email, "Email")

        self.reg_password = tk.Entry(card, width=35, font=("Segoe UI", 11))
        self.reg_password.pack(pady=5)
        self.add_placeholder(self.reg_password, "Password", is_password=True)

        self.reg_confirm = tk.Entry(card, width=35, font=("Segoe UI", 11))
        self.reg_confirm.pack(pady=5)
        self.add_placeholder(self.reg_confirm, "Konfirmasi Password", is_password=True)

        tk.Button(card, text="Register", width=15, bg=self.PINK,
                  font=("Segoe UI", 10, "bold"), command=self._do_register).pack(pady=15)
        tk.Button(card, text="Already Have Account? Login", bd=0, bg="white",
                  fg="blue", command=self.show_login).pack()

    def _do_register(self):
        fullname = self.get_entry_value(self.reg_fullname)
        username = self.get_entry_value(self.reg_username)
        email    = self.get_entry_value(self.reg_email)
        password = self.get_entry_value(self.reg_password)
        confirm  = self.get_entry_value(self.reg_confirm)

        if not fullname or not username or not email:
            messagebox.showerror("Error", "Semua field wajib diisi")
            return
        if password != confirm:
            messagebox.showerror("Error", "Konfirmasi password tidak cocok")
            return
        ok, err = self.app.register_user(fullname, username, email, password)
        if not ok:
            messagebox.showerror("Error", err)
            return
        messagebox.showinfo("Sukses", "Registrasi berhasil!")
        self.show_login()

    # ─── ADMIN DASHBOARD ──────────────────────────────────────────────────────

    def show_admin_dashboard(self, user):
        self.clear_window()
        sidebar = self.create_sidebar("Admin")
        content = tk.Frame(self.root, bg="white")
        content.pack(fill="both", expand=True)

        pages = {
            "home":      self._admin_page_home(content, user),
            "analytics": self._admin_page_analytics(content),
            "users":     self._admin_page_users(content),
            "posts":     self._admin_page_mod_list(content, "post"),
            "stories":   self._admin_page_mod_list(content, "story"),
            "hashtags":  self._admin_page_hashtags(content),
            "log":       self._admin_page_violation_log(content),
        }

        def show(name):
            for p in pages.values():
                p.pack_forget()
            pages[name].pack(fill="both", expand=True)

        self.add_sidebar_btn(sidebar, "🏠  Beranda",         lambda: show("home"))
        self.add_sidebar_btn(sidebar, "📊  Analitik",        lambda: show("analytics"))
        self.add_sidebar_btn(sidebar, "👥  Kelola User",      lambda: show("users"))
        self.add_sidebar_btn(sidebar, "📝  Moderasi Post",    lambda: show("posts"))
        self.add_sidebar_btn(sidebar, "📖  Moderasi Story",   lambda: show("stories"))
        self.add_sidebar_btn(sidebar, "      Kelola Hashtag", lambda: show("hashtags"))
        self.add_sidebar_btn(sidebar, "🚨  Log Pelanggaran",  lambda: show("log"))

        tk.Button(sidebar, text="Logout", bg="#f52a4c", fg="#333333",
                  font=("Segoe UI", 11, "bold"), bd=1, relief="solid", cursor="hand2",
                  command=self.show_login).pack(side="bottom", pady=20, padx=20, fill="x")
        show("home")

    # ─── ADMIN HOME ───────────────────────────────────────────────────────────

    def _admin_page_home(self, parent, user):
        P, D, W, L, G, DG = self.PINK, self.DPINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY
        page = tk.Frame(parent, bg=L)

        hdr = tk.Frame(page, bg=W, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"🏠  Selamat Datang, {user['fullname']} 👑",
                 font=("Segoe UI", 14, "bold"), bg=W, fg=DG).pack(side="left", padx=16)
        tk.Label(hdr, text=datetime.now().strftime("%A, %d %B %Y"),
                 font=("Segoe UI", 9), bg=W, fg=G).pack(side="right", padx=16)
        tk.Frame(page, bg="#eeeeee", height=1).pack(fill="x")

        outer = tk.Frame(page, bg=L)
        outer.pack(fill="both", expand=True)
        _, inner = self.make_scrollable(outer, L)

        # Stat cards
        stat_section = tk.Frame(inner, bg=L)
        stat_section.pack(fill="x", padx=16, pady=(14, 8))
        total_likes    = sum(len(p["likes"]) for p in self.app.posts)
        total_comments = sum(len(p.get("comments", [])) for p in self.app.posts)
        stat_items = [
            ("👥", "Total User",  len(self.app.users),    "#e3f2fd", "#1565c0"),
            ("📝", "Total Post",  len(self.app.posts),    "#fce4ec", "#c62828"),
            ("📖", "Total Story", len(self.app.stories),  "#f3e5f5", "#6a1b9a"),
            ("❤️",  "Total Like",  total_likes,            "#fff3e0", "#e65100"),
            ("💬", "Komentar",    total_comments,         "#e8f5e9", "#2e7d32"),
            ("🚨", "Pelanggaran", len(self.app.violation_log), "#ffebee", "#b71c1c"),
        ]
        cards_row = tk.Frame(stat_section, bg=L)
        cards_row.pack(anchor="w")
        for icon, label, val, bg_col, fg_col in stat_items:
            box = tk.Frame(cards_row, bg=bg_col, width=130, height=100,
                           highlightthickness=1, highlightbackground="#ddd")
            box.pack(side="left", padx=3)
            box.pack_propagate(False)
            tk.Label(box, text=icon, font=("Segoe UI", 13), bg=bg_col).pack(pady=(10, 2))
            tk.Label(box, text=str(val), font=("Segoe UI", 13, "bold"),
                     bg=bg_col, fg=fg_col).pack()
            tk.Label(box, text=label, font=("Segoe UI", 8), bg=bg_col, fg=G).pack(pady=(2, 10))

        tk.Frame(inner, bg="#eeeeee", height=1).pack(fill="x", padx=16, pady=(4, 0))

        # Two-column layout
        body = tk.Frame(inner, bg=L)
        body.pack(fill="both", expand=True, padx=16, pady=10)

        left_col = tk.Frame(body, bg=L)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Feed header
        feed_hdr = tk.Frame(left_col, bg=W, pady=8, padx=10,
                            highlightthickness=1, highlightbackground="#eee")
        feed_hdr.pack(fill="x", pady=(0, 6))
        tk.Label(feed_hdr, text="📰  Feed Semua Postingan",
                 font=("Segoe UI", 11, "bold"), bg=W, fg=DG).pack(side="left")

        feed_mode        = tk.StringVar(value="ranked")
        feed_user_filter = tk.StringVar(value="all")
        user_filter_lbl  = tk.StringVar(value="🌐 Semua")

        ctrl_row = tk.Frame(feed_hdr, bg=W)
        ctrl_row.pack(side="right")

        feed_scroll_frame = tk.Frame(left_col, bg=L)
        feed_scroll_frame.pack(fill="both", expand=True)
        feed_canvas = tk.Canvas(feed_scroll_frame, bg=L, bd=0, highlightthickness=0)
        feed_sb     = tk.Scrollbar(feed_scroll_frame, orient="vertical",
                                   command=feed_canvas.yview)
        feed_inner  = tk.Frame(feed_canvas, bg=L)
        feed_inner.bind("<Configure>",
            lambda e: feed_canvas.configure(scrollregion=feed_canvas.bbox("all")))
        feed_win = feed_canvas.create_window((0, 0), window=feed_inner, anchor="nw")
        feed_canvas.configure(yscrollcommand=feed_sb.set)
        feed_canvas.bind("<Configure>",
                         lambda e: feed_canvas.itemconfig(feed_win, width=e.width))
        feed_canvas.pack(side="left", fill="both", expand=True)
        feed_sb.pack(side="right", fill="y")

        def refresh_feed():
            for w in feed_inner.winfo_children():
                w.destroy()
            pool = list(self.app.posts)
            if feed_user_filter.get() != "all":
                pool = [p for p in pool if p["username"] == feed_user_filter.get()]
            if feed_mode.get() == "ranked":
                pool = sorted(pool, key=self.app.feed_score, reverse=True)
            else:
                pool = list(reversed(pool))
            if not pool:
                tk.Label(feed_inner, text="Tidak ada postingan.",
                         font=("Segoe UI", 10), bg=L, fg=G).pack(pady=30)
                return
            for p in pool:
                self._admin_post_card(p, feed_inner, refresh_feed)

        def cycle_user_filter():
            users_list = [u for u in self.app.users if u not in ("admin", "moderator")]
            current = feed_user_filter.get()
            if current == "all":
                if users_list:
                    feed_user_filter.set(users_list[0])
                    user_filter_lbl.set(f"@{users_list[0]}")
            else:
                idx = users_list.index(current) if current in users_list else -1
                if idx + 1 < len(users_list):
                    nxt = users_list[idx + 1]
                    feed_user_filter.set(nxt)
                    user_filter_lbl.set(f"@{nxt}")
                else:
                    feed_user_filter.set("all")
                    user_filter_lbl.set("🌐 Semua")
            refresh_feed()

        def toggle_mode():
            if feed_mode.get() == "ranked":
                feed_mode.set("recent")
                mode_btn.config(text="📅 Terbaru")
            else:
                feed_mode.set("ranked")
                mode_btn.config(text="🔥 Terpopuler")
            refresh_feed()

        tk.Button(ctrl_row, textvariable=user_filter_lbl, font=("Segoe UI", 8),
                  bg=L, fg=DG, bd=1, relief="solid", padx=6, pady=2,
                  cursor="hand2", command=cycle_user_filter).pack(side="left", padx=(0, 4))
        mode_btn = tk.Button(ctrl_row, text="🔥 Terpopuler", font=("Segoe UI", 8),
                             bg=L, fg=DG, bd=1, relief="solid", padx=6, pady=2,
                             cursor="hand2", command=toggle_mode)
        mode_btn.pack(side="left")
        refresh_feed()

        # Right sidebar
        right_col = tk.Frame(body, bg=L, width=200)
        right_col.pack(side="left", fill="y")
        right_col.pack_propagate(False)

        # User list widget
        au_box = tk.Frame(right_col, bg=W, highlightthickness=1, highlightbackground="#eee")
        au_box.pack(fill="x", pady=(0, 8))
        tk.Label(au_box, text="👥  Daftar User", font=("Segoe UI", 10, "bold"),
                 bg=W, fg=DG).pack(anchor="w", padx=10, pady=(8, 4))
        tk.Frame(au_box, bg="#eee", height=1).pack(fill="x")
        for uname, u in [(k, v) for k, v in self.app.users.items() if v.get("role") == "User"]:
            urow = tk.Frame(au_box, bg=W)
            urow.pack(fill="x", padx=8, pady=3)
            initials = "".join(w[0].upper() for w in u["fullname"].split()[:2])
            tk.Label(urow, text=initials, font=("Segoe UI", 8, "bold"),
                     bg=P, fg=DG, width=3).pack(side="left")
            info_f = tk.Frame(urow, bg=W)
            info_f.pack(side="left", padx=6)
            tk.Label(info_f, text=u["fullname"], font=("Segoe UI", 8, "bold"),
                     bg=W, fg=DG).pack(anchor="w")
            cnt = len([p for p in self.app.posts if p["username"] == uname])
            tk.Label(info_f, text=f"@{uname}  •  {cnt} post",
                     font=("Segoe UI", 7), bg=W, fg=G).pack(anchor="w")

        # Top hashtags widget
        ht_box = tk.Frame(right_col, bg=W, highlightthickness=1, highlightbackground="#eee")
        ht_box.pack(fill="x", pady=(0, 8))
        tk.Label(ht_box, text="#️⃣  Trending Hashtag", font=("Segoe UI", 10, "bold"),
                 bg=W, fg=DG).pack(anchor="w", padx=10, pady=(8, 4))
        tk.Frame(ht_box, bg="#eee", height=1).pack(fill="x")
        tag_colors = ["#e57a8a", "#f4a261", "#2ec4b6", "#a8dadc", "#457b9d"]
        for idx, tag in enumerate(sorted(self.app.communities,
                                         key=lambda t: len(self.app.communities[t]),
                                         reverse=True)[:5]):
            trow = tk.Frame(ht_box, bg=W)
            trow.pack(fill="x", padx=10, pady=3)
            tk.Label(trow, text=f"#{tag}", font=("Segoe UI", 9, "bold"),
                     bg=W, fg=tag_colors[idx % len(tag_colors)]).pack(side="left")
            tk.Label(trow, text=f"{len(self.app.communities[tag])} post",
                     font=("Segoe UI", 8), bg=W, fg=G).pack(side="right")

        # Recent violations widget
        viol_box = tk.Frame(right_col, bg=W, highlightthickness=1, highlightbackground="#eee")
        viol_box.pack(fill="x")
        tk.Label(viol_box, text="🚨  Pelanggaran Terbaru", font=("Segoe UI", 10, "bold"),
                 bg=W, fg=DG).pack(anchor="w", padx=10, pady=(8, 4))
        tk.Frame(viol_box, bg="#eee", height=1).pack(fill="x")
        recent_viols = list(reversed(self.app.violation_log))[:5]
        if not recent_viols:
            tk.Label(viol_box, text="Tidak ada pelanggaran.",
                     font=("Segoe UI", 8), bg=W, fg=G).pack(padx=10, pady=6, anchor="w")
        else:
            for log in recent_viols:
                vrow = tk.Frame(viol_box, bg=W)
                vrow.pack(fill="x", padx=10, pady=3)
                tk.Label(vrow, text=f"@{log['username']}",
                         font=("Segoe UI", 8, "bold"), bg=W, fg=DG).pack(side="left")
                tk.Label(vrow, text=log["kata"],
                         font=("Segoe UI", 7), bg="#fce4ec", fg="#c62828",
                         padx=3).pack(side="right")
        tk.Frame(viol_box, bg=L, height=8).pack()

        return page

    # ─── ADMIN POST CARD (home feed) ──────────────────────────────────────────

    def _admin_post_card(self, post, feed_inner, refresh_fn):
        P, W, L, G, DG = self.PINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY
        card = tk.Frame(feed_inner, bg=W, pady=10, padx=12,
                        highlightthickness=1, highlightbackground="#eeeeee")
        card.pack(fill="x", pady=(0, 6))

        header = tk.Frame(card, bg=W)
        header.pack(fill="x")
        u_data   = self.app.users.get(post["username"], {})
        fullname = u_data.get("fullname", post["username"])
        initials = "".join(x[0].upper() for x in fullname.split()[:2])
        tk.Label(header, text=initials, font=("Segoe UI", 10, "bold"),
                 bg=P, fg=DG, width=3).pack(side="left")
        tk.Label(header, text=f"  {fullname}",
                 font=("Segoe UI", 10, "bold"), bg=W, fg=DG).pack(side="left")
        tk.Label(header, text=f"  @{post['username']}",
                 font=("Segoe UI", 9), bg=W, fg=G).pack(side="left")
        ts_display = post["ts"] + ("  ✏️" if post.get("edited") else "")
        tk.Label(header, text=ts_display, font=("Segoe UI", 8),
                 bg=W, fg=G).pack(side="left", padx=6)

        stats_f = tk.Frame(header, bg=W)
        stats_f.pack(side="right")
        score = self.app.feed_score(post)
        tk.Label(stats_f, text=f"🔥 {score:.0f}", font=("Segoe UI", 8),
                 bg="#fff3e0", fg="#e65100", padx=4).pack(side="left", padx=2)
        tk.Label(stats_f, text=f"❤️ {len(post['likes'])}", font=("Segoe UI", 8),
                 bg="#fce4ec", fg="#c62828", padx=4).pack(side="left", padx=2)
        tk.Label(stats_f, text=f"💬 {len(post.get('comments', []))}", font=("Segoe UI", 8),
                 bg="#e8f5e9", fg="#2e7d32", padx=4).pack(side="left", padx=2)

        tk.Label(card, text=post["text"], font=("Segoe UI", 10),
                 bg=W, fg=DG, wraplength=380, justify="left").pack(anchor="w", pady=(6, 4))

        tags = self.app.extract_hashtags(post["text"])
        if tags:
            tag_row = tk.Frame(card, bg=W)
            tag_row.pack(anchor="w", pady=(0, 4))
            for tag in tags:
                tk.Label(tag_row, text=f"#{tag}", font=("Segoe UI", 7),
                         bg="#e3f2fd", fg="#1565c0", padx=3, pady=1).pack(side="left", padx=2)

        if post["likes"]:
            like_row = tk.Frame(card, bg=W)
            like_row.pack(anchor="w", pady=(0, 4))
            tk.Label(like_row, text="Disukai oleh:", font=("Segoe UI", 7),
                     bg=W, fg=G).pack(side="left")
            for liker in post["likes"][:4]:
                li = self.app.users.get(liker, {})
                li_init = "".join(x[0].upper() for x in li.get("fullname", liker).split()[:2])
                tk.Label(like_row, text=li_init, font=("Segoe UI", 7, "bold"),
                         bg="#fce4ec", fg="#c62828", padx=3).pack(side="left", padx=1)
            if len(post["likes"]) > 4:
                tk.Label(like_row, text=f"+{len(post['likes'])-4} lainnya",
                         font=("Segoe UI", 7), bg=W, fg=G).pack(side="left", padx=2)

        act_row = tk.Frame(card, bg=W)
        act_row.pack(anchor="e", fill="x")

        def open_comment_preview(p=post):
            win = tk.Toplevel(self.root)
            win.title(f"Komentar — Post @{p['username']}")
            win.geometry("400x300")
            win.config(bg=W)
            tk.Label(win, text=f"💬 Komentar ({len(p.get('comments',[]))})",
                     font=("Segoe UI", 11, "bold"), bg=W).pack(pady=8)
            lf = tk.Frame(win, bg=W)
            lf.pack(fill="both", expand=True, padx=12)
            _, ci = self.make_scrollable(lf, W)
            if not p.get("comments"):
                tk.Label(ci, text="Belum ada komentar.", font=("Segoe UI", 9),
                         bg=W, fg=G).pack(pady=12)
            else:
                for cm in p["comments"]:
                    row = tk.Frame(ci, bg=L, pady=5, padx=8,
                                   highlightthickness=1, highlightbackground="#eee")
                    row.pack(fill="x", pady=2)
                    tk.Label(row, text=f"@{cm['username']}  •  {cm['ts']}",
                             font=("Segoe UI", 7), bg=L, fg=G).pack(anchor="w")
                    tk.Label(row, text=cm["text"], font=("Segoe UI", 9),
                             bg=L, wraplength=340, justify="left").pack(anchor="w")

        def make_warn(pid=post["id"], uname=post["username"]):
            def do():
                messagebox.showwarning("Peringatan Dikirim",
                    f"Peringatan telah dikirim ke @{uname}.\nPost ID: {pid}")
                self.app.log_violation(uname, ["[admin-warning]"], "Post (Peringatan Admin)")
            return do

        def make_del(pid=post["id"]):
            def do():
                if messagebox.askyesno("Hapus Post", "Hapus postingan ini?"):
                    self.app.delete_post(pid)
                    refresh_fn()
            return do

        tk.Button(act_row, text="💬 Lihat Komentar", font=("Segoe UI", 8),
                  bg=L, fg=DG, bd=1, relief="solid", padx=6, pady=2,
                  cursor="hand2", command=open_comment_preview).pack(side="left", padx=(0, 4))
        tk.Button(act_row, text="⚠️ Peringatkan", font=("Segoe UI", 8),
                  bg="#fff3cd", fg="#856404", bd=1, relief="solid", padx=6, pady=2,
                  cursor="hand2", command=make_warn()).pack(side="left", padx=(0, 4))
        tk.Button(act_row, text="🗑 Hapus", font=("Segoe UI", 8, "bold"),
                  bg="tomato", fg="white", bd=0, padx=8, pady=2,
                  cursor="hand2", command=make_del()).pack(side="left")

    # ─── ADMIN ANALYTICS ──────────────────────────────────────────────────────

    def _admin_page_analytics(self, parent):
        P, W, L, G, DG = self.PINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY
        page = tk.Frame(parent, bg=L)

        hdr = tk.Frame(page, bg=W, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📊  Dashboard Analitik",
                 font=("Segoe UI", 16, "bold"), bg=W, fg=DG).pack(side="left", padx=16)

        btn_bar = tk.Frame(hdr, bg=W)
        btn_bar.pack(side="right", padx=12)

        def export_csv():
            try:
                path = self.app.export_analytics_csv()
                messagebox.showinfo("Export Berhasil", f"File berhasil disimpan:\n{path}")
            except Exception as e:
                messagebox.showerror("Export Gagal", str(e))

        def print_report():
            win = tk.Toplevel(self.root)
            win.title("📄 Print Preview")
            win.geometry("620x680")
            win.config(bg=W)
            toolbar = tk.Frame(win, bg="#f0f0f0", pady=6)
            toolbar.pack(fill="x")
            tk.Label(toolbar, text="Print Preview",
                     font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(side="left", padx=12)
            txt = tk.Text(win, font=("Courier New", 9), bg=W, bd=0, wrap="none")
            sb_x = tk.Scrollbar(win, orient="horizontal", command=txt.xview)
            sb_y = tk.Scrollbar(win, orient="vertical",   command=txt.yview)
            txt.configure(xscrollcommand=sb_x.set, yscrollcommand=sb_y.set)
            sb_y.pack(side="right", fill="y")
            sb_x.pack(side="bottom", fill="x")
            txt.pack(fill="both", expand=True, padx=8, pady=4)

            def do_print():
                path = os.path.join(os.path.expanduser("~"), "kizuna_report.txt")
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(txt.get("1.0", tk.END))
                    if sys.platform == "win32":
                        os.startfile(path, "print")
                    else:
                        subprocess.call(["lpr", path])
                    messagebox.showinfo("Print", f"Tersimpan di: {path}", parent=win)
                except Exception as e:
                    messagebox.showerror("Gagal", str(e), parent=win)

            tk.Button(toolbar, text="🖨  Cetak / Simpan TXT", bg=P,
                      font=("Segoe UI", 9, "bold"), bd=0, padx=10, pady=3,
                      command=do_print).pack(side="right", padx=12)

            SEP  = "=" * 64
            SEP2 = "-" * 64
            lines = [SEP, "          KIZUNA — LAPORAN ANALITIK PLATFORM",
                     f"          Dicetak: {datetime.now().strftime('%d %b %Y %H:%M')}", SEP, ""]
            total_likes    = sum(len(p["likes"]) for p in self.app.posts)
            total_comments = sum(len(p.get("comments",[])) for p in self.app.posts)
            lines += ["RINGKASAN PLATFORM", SEP2,
                      f"  Total User      : {len(self.app.users)}",
                      f"  Total Post      : {len(self.app.posts)}",
                      f"  Total Story     : {len(self.app.stories)}",
                      f"  Total Like      : {total_likes}",
                      f"  Total Komentar  : {total_comments}", ""]
            lines += ["ENGAGEMENT SCORE PER POST (TOP 10)", SEP2]
            for i, p in enumerate(sorted(self.app.posts, key=self.app.feed_score, reverse=True)[:10], 1):
                score   = self.app.feed_score(p)
                preview = p["text"][:30] + ("…" if len(p["text"]) > 30 else "")
                lines.append(f"  {i:<4} {p['username']:<12} {len(p['likes']):<7} "
                             f"{len(p.get('comments',[])):<10} {score:<8.1f}  {preview}")
            lines += ["", SEP, "          — Akhir Laporan —", SEP]
            txt.insert("1.0", "\n".join(lines))
            txt.config(state="disabled")

        tk.Button(btn_bar, text="📄  Print / Preview", font=("Segoe UI", 9),
                  bg=W, bd=1, relief="solid", padx=8, pady=3,
                  cursor="hand2", command=print_report).pack(side="left", padx=(0, 6))
        tk.Button(btn_bar, text="💾  Export CSV", font=("Segoe UI", 9),
                  bg=P, fg=DG, bd=0, padx=10, pady=3,
                  cursor="hand2", command=export_csv).pack(side="left")

        tk.Frame(page, bg="#eeeeee", height=1).pack(fill="x")
        outer = tk.Frame(page, bg=L)
        outer.pack(fill="both", expand=True)
        _, inner = self.make_scrollable(outer, L)

        # Summary cards
        sec1 = tk.Frame(inner, bg=L)
        sec1.pack(fill="x", padx=16, pady=(14, 6))
        tk.Label(sec1, text="Ringkasan Platform",
                 font=("Segoe UI", 11, "bold"), bg=L, fg=DG).pack(anchor="w", pady=(0, 8))
        cards_row = tk.Frame(sec1, bg=L)
        cards_row.pack(fill="x")
        total_likes    = sum(len(p["likes"]) for p in self.app.posts)
        total_comments = sum(len(p.get("comments",[])) for p in self.app.posts)
        avg_score      = (sum(self.app.feed_score(p) for p in self.app.posts) / len(self.app.posts)) if self.app.posts else 0
        for icon, label, val, bg_col, fg_col in [
            ("👥","User",len(self.app.users),"#e3f2fd","#1565c0"),
            ("📝","Post",len(self.app.posts),"#fce4ec","#c62828"),
            ("📖","Story",len(self.app.stories),"#f3e5f5","#6a1b9a"),
            ("❤️","Total Like",total_likes,"#fff3e0","#e65100"),
            ("💬","Komentar",total_comments,"#e8f5e9","#2e7d32"),
            ("🔥","Avg Score",f"{avg_score:.1f}","#fff8e1","#f57f17"),
        ]:
            box = tk.Frame(cards_row, bg=bg_col, width=130, height=100,
                           highlightthickness=1, highlightbackground="#ddd")
            box.pack(side="left", padx=3)
            box.pack_propagate(False)
            tk.Label(box, text=icon, font=("Segoe UI", 13), bg=bg_col).pack(pady=(10,2))
            tk.Label(box, text=str(val), font=("Segoe UI", 13, "bold"),
                     bg=bg_col, fg=fg_col).pack()
            tk.Label(box, text=label, font=("Segoe UI", 8), bg=bg_col, fg=G).pack(pady=(2,10))

        tk.Frame(inner, bg="#eeeeee", height=1).pack(fill="x", padx=16, pady=8)

        # Engagement bars
        sec2 = tk.Frame(inner, bg=L)
        sec2.pack(fill="x", padx=16, pady=(0, 6))
        hdr2 = tk.Frame(sec2, bg=L)
        hdr2.pack(fill="x", pady=(0,6))
        tk.Label(hdr2, text="🔥  Engagement Score per Post",
                 font=("Segoe UI", 11, "bold"), bg=L, fg=DG).pack(side="left")
        tk.Label(hdr2, text="(Skor = like×3 + komentar×5 + recency)",
                 font=("Segoe UI", 8), bg=L, fg=G).pack(side="left", padx=8)

        sorted_posts = sorted(self.app.posts, key=self.app.feed_score, reverse=True)
        max_score    = self.app.feed_score(sorted_posts[0]) if sorted_posts else 1
        for rank, p in enumerate(sorted_posts, 1):
            score   = self.app.feed_score(p)
            bar_pct = score / max_score if max_score > 0 else 0
            row = tk.Frame(sec2, bg=W, pady=6, padx=10,
                           highlightthickness=1, highlightbackground="#eee")
            row.pack(fill="x", pady=2)
            rank_clr = "#e57a8a" if rank==1 else ("#f4a261" if rank==2 else ("#2ec4b6" if rank==3 else G))
            tk.Label(row, text=f"#{rank}", font=("Segoe UI", 9, "bold"),
                     bg=rank_clr, fg="white", width=3).pack(side="left")
            info = tk.Frame(row, bg=W)
            info.pack(side="left", fill="x", expand=True, padx=8)
            top_line = tk.Frame(info, bg=W)
            top_line.pack(fill="x")
            tk.Label(top_line, text=f"@{p['username']}",
                     font=("Segoe UI", 9, "bold"), bg=W, fg=DG).pack(side="left")
            tk.Label(top_line,
                     text=f"  ❤️ {len(p['likes'])}   💬 {len(p.get('comments',[]))}   📅 {p['ts']}",
                     font=("Segoe UI", 8), bg=W, fg=G).pack(side="left")
            tk.Label(top_line, text=f"Score: {score:.1f}",
                     font=("Segoe UI", 9, "bold"), bg=W, fg="#e57a8a").pack(side="right")
            preview = p["text"][:70] + ("…" if len(p["text"])>70 else "")
            tk.Label(info, text=preview, font=("Segoe UI", 9),
                     bg=W, fg=DG, wraplength=420, justify="left").pack(anchor="w", pady=(2,4))
            bar_outer = tk.Frame(info, bg="#f0f0f0", height=6)
            bar_outer.pack(fill="x")
            bar_outer.pack_propagate(False)
            tk.Frame(bar_outer, bg="#e57a8a", height=6).place(relwidth=bar_pct, relheight=1.0)

        tk.Frame(inner, bg="#eeeeee", height=1).pack(fill="x", padx=16, pady=8)

        # Top hashtags
        sec3 = tk.Frame(inner, bg=L)
        sec3.pack(fill="x", padx=16, pady=(0,14))
        tk.Label(sec3, text="#️⃣  Top Trending Hashtag",
                 font=("Segoe UI", 11, "bold"), bg=L, fg=DG).pack(anchor="w", pady=(0,6))
        sorted_tags = sorted(self.app.communities, key=lambda t: len(self.app.communities[t]), reverse=True)
        max_count   = len(self.app.communities[sorted_tags[0]]) if sorted_tags else 1
        tag_colors  = ["#e57a8a","#f4a261","#2ec4b6","#a8dadc","#457b9d",
                        "#e9c46a","#264653","#e76f51","#6a4c93","#1982c4"]
        for idx, tag in enumerate(sorted_tags[:10]):
            count   = len(self.app.communities[tag])
            bar_pct = count / max_count if max_count > 0 else 0
            col     = tag_colors[idx % len(tag_colors)]
            row = tk.Frame(sec3, bg=W, pady=6, padx=10,
                           highlightthickness=1, highlightbackground="#eee")
            row.pack(fill="x", pady=2)
            lf = tk.Frame(row, bg=W, width=140)
            lf.pack(side="left"); lf.pack_propagate(False)
            tk.Label(lf, text=f"#{tag}", font=("Segoe UI", 10, "bold"), bg=W, fg=col).pack(anchor="w")
            tk.Label(lf, text=f"{count} post", font=("Segoe UI", 8), bg=W, fg=G).pack(anchor="w")
            rf = tk.Frame(row, bg=W)
            rf.pack(side="left", fill="x", expand=True, padx=(8,0))
            bar_bg = tk.Frame(rf, bg="#f0f0f0", height=18)
            bar_bg.pack(fill="x", pady=6); bar_bg.pack_propagate(False)
            tk.Frame(bar_bg, bg=col, height=18).place(relwidth=bar_pct, relheight=1.0)

        return page

    # ─── ADMIN USERS ──────────────────────────────────────────────────────────

    def _admin_page_users(self, parent):
        page = tk.Frame(parent, bg=self.LIGHT)
        tk.Label(page, text="Kelola User", font=("Segoe UI", 14, "bold"),
                 bg=self.LIGHT).pack(pady=10)

        top_bar = tk.Frame(page, bg=self.LIGHT)
        top_bar.pack(fill="x", padx=16, pady=(0, 6))

        lf = tk.Frame(page, bg=self.LIGHT)
        lf.pack(fill="both", expand=True, padx=16)
        _, inner = self.make_scrollable(lf)

        ROLE_OPTIONS = ["User", "Moderator", "Admin"]

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            for col, h in enumerate(["Nama Lengkap","Username","Email","Role","Aksi"]):
                tk.Label(inner, text=h, font=("Segoe UI", 9, "bold"),
                         bg=self.PINK, width=16, padx=4, pady=4).grid(
                             row=0, column=col, padx=1, pady=1)
            for ri, u in enumerate(list(self.app.users.values()), 1):
                for ci, val in enumerate([u["fullname"],u["username"],u["email"],u["role"]]):
                    tk.Label(inner, text=val, font=("Segoe UI", 9), bg="white",
                             width=16, padx=4, pady=4).grid(row=ri, column=ci, padx=1, pady=1)

                def make_edit(uname=u["username"]):
                    def do():
                        self._open_edit_user_dialog(uname, ROLE_OPTIONS, refresh)
                    return do

                def make_del(uname=u["username"]):
                    def do():
                        ok, err = self.app.delete_user(uname)
                        if not ok:
                            messagebox.showerror("Error", err)
                            return
                        refresh()
                    return do

                bf = tk.Frame(inner, bg="white")
                bf.grid(row=ri, column=4, padx=1, pady=1)
                tk.Button(bf, text="Edit", font=("Segoe UI", 8), bg="#ffe0a0",
                          bd=0, padx=4, command=make_edit()).pack(side="left", padx=2)
                tk.Button(bf, text="Hapus", font=("Segoe UI", 8), bg="tomato",
                          fg="white", bd=0, padx=4, command=make_del()).pack(side="left")

        tk.Button(top_bar, text="➕  Buat Akun Baru", font=("Segoe UI", 9, "bold"),
                  bg=self.PINK, bd=0, padx=10, pady=5, cursor="hand2",
                  command=lambda: self._open_create_user_dialog(ROLE_OPTIONS, refresh)
                  ).pack(side="left")
        refresh()
        return page

    def _open_edit_user_dialog(self, uname, role_options, refresh_fn):
        u = self.app.users[uname]
        win = tk.Toplevel(self.root)
        win.title(f"Edit User — @{uname}")
        win.geometry("360x380")
        win.config(bg="white")
        win.grab_set()
        tk.Label(win, text="Edit User", font=("Segoe UI", 13, "bold"), bg="white").pack(pady=12)

        tk.Label(win, text="Nama Lengkap", bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        fn_e = tk.Entry(win, width=36, font=("Segoe UI", 10))
        fn_e.insert(0, u["fullname"]); fn_e.pack(padx=20, pady=(2,8))

        tk.Label(win, text="Email", bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        em_e = tk.Entry(win, width=36, font=("Segoe UI", 10))
        em_e.insert(0, u["email"]); em_e.pack(padx=20, pady=(2,8))

        tk.Label(win, text="Role", bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        role_var = tk.StringVar(value=u.get("role","User"))
        role_row = tk.Frame(win, bg="white")
        role_row.pack(padx=20, pady=(2,8), anchor="w")
        for opt in role_options:
            tk.Radiobutton(role_row, text=opt, variable=role_var, value=opt,
                           bg="white", font=("Segoe UI", 9)).pack(side="left", padx=(0,10))

        tk.Label(win, text="Password Baru (kosongkan jika tidak diubah)",
                 bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        pwd_e = tk.Entry(win, width=36, show="*", font=("Segoe UI", 10))
        pwd_e.pack(padx=20, pady=(2,12))

        def save():
            new_fn    = fn_e.get().strip()
            new_email = em_e.get().strip()
            new_pwd   = pwd_e.get().strip() or None
            if not new_fn or not new_email:
                messagebox.showerror("Error", "Nama dan email tidak boleh kosong", parent=win)
                return
            ok, err = self.app.update_user(uname, fullname=new_fn, email=new_email,
                                           new_password=new_pwd, role=role_var.get())
            if not ok:
                messagebox.showerror("Error", err, parent=win)
                return
            win.destroy(); refresh_fn()
            messagebox.showinfo("Sukses", f"User @{uname} berhasil diperbarui.")

        tk.Button(win, text="Simpan", bg=self.PINK, font=("Segoe UI", 10, "bold"),
                  bd=0, padx=14, pady=6, command=save).pack(pady=4)

    def _open_create_user_dialog(self, role_options, refresh_fn):
        win = tk.Toplevel(self.root)
        win.title("Buat Akun Baru")
        win.geometry("360x460")
        win.config(bg="white")
        win.grab_set()
        tk.Label(win, text="Buat Akun Baru", font=("Segoe UI", 13, "bold"),
                 bg="white").pack(pady=12)

        fields = {}
        for label, key in [("Nama Lengkap","fullname"),("Username","username"),("Email","email")]:
            tk.Label(win, text=label, bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
            e = tk.Entry(win, width=36, font=("Segoe UI", 10))
            e.pack(padx=20, pady=(2,8)); fields[key] = e

        tk.Label(win, text="Password", bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        pwd_e = tk.Entry(win, width=36, show="*", font=("Segoe UI", 10))
        pwd_e.pack(padx=20, pady=(2,8))

        tk.Label(win, text="Role", bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        role_var = tk.StringVar(value="User")
        role_row = tk.Frame(win, bg="white")
        role_row.pack(padx=20, pady=(2,12), anchor="w")
        for opt in role_options:
            tk.Radiobutton(role_row, text=opt, variable=role_var, value=opt,
                           bg="white", font=("Segoe UI", 9)).pack(side="left", padx=(0,10))

        def save():
            fn = fields["fullname"].get().strip()
            un = fields["username"].get().strip()
            em = fields["email"].get().strip()
            pw = pwd_e.get().strip()
            if not fn or not un or not em:
                messagebox.showerror("Error", "Semua field wajib diisi", parent=win); return
            ok, err = self.app.register_user(fn, un, em, pw, role=role_var.get())
            if not ok:
                messagebox.showerror("Error", err, parent=win); return
            win.destroy(); refresh_fn()
            messagebox.showinfo("Sukses", f"Akun @{un} ({role_var.get()}) berhasil dibuat.")

        tk.Button(win, text="Buat Akun", bg=self.PINK, font=("Segoe UI", 10, "bold"),
                  bd=0, padx=14, pady=6, command=save).pack(pady=4)

    # ─── ADMIN MOD LIST ───────────────────────────────────────────────────────

    def _admin_page_mod_list(self, parent, kind):
        title = "Moderasi Postingan" if kind == "post" else "Moderasi Stories"
        page  = tk.Frame(parent, bg=self.LIGHT)
        tk.Label(page, text=title, font=("Segoe UI", 14, "bold"),
                 bg=self.LIGHT).pack(pady=10)
        lf = tk.Frame(page, bg=self.LIGHT)
        lf.pack(fill="both", expand=True, padx=16)
        _, inner = self.make_scrollable(lf)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            items = self.app.posts if kind == "post" else self.app.stories
            if not items:
                tk.Label(inner, text="Belum ada data.", bg=self.LIGHT,
                         fg="gray", font=("Segoe UI", 10)).pack(pady=20)
                return
            for item in items:
                row = tk.Frame(inner, bg="white", pady=6, padx=8,
                               highlightthickness=1, highlightbackground="#eee")
                row.pack(fill="x", pady=2)
                tk.Label(row, text=f"@{item['username']}  •  {item['ts']}",
                         font=("Segoe UI", 8), bg="white", fg="gray").pack(anchor="w")
                tk.Label(row, text=item["text"], font=("Segoe UI", 10),
                         bg="white", wraplength=480, justify="left").pack(anchor="w")

                def make_del(iid=item["id"]):
                    def do():
                        noun = "postingan" if kind == "post" else "story"
                        if messagebox.askyesno("Hapus", f"Hapus {noun} ini?"):
                            if kind == "post":
                                self.app.delete_post(iid)
                            else:
                                self.app.delete_story(iid)
                            refresh()
                    return do

                tk.Button(row, text="Hapus", bg="tomato", fg="white",
                          font=("Segoe UI", 8), bd=0, padx=6,
                          command=make_del()).pack(anchor="e")
        refresh()
        return page

    # ─── ADMIN HASHTAGS ───────────────────────────────────────────────────────

    def _admin_page_hashtags(self, parent):
        page = tk.Frame(parent, bg=self.LIGHT)
        tk.Label(page, text="Kelola Hashtag", font=("Segoe UI", 14, "bold"),
                 bg=self.LIGHT).pack(pady=10)
        top_bar = tk.Frame(page, bg=self.LIGHT)
        top_bar.pack(fill="x", padx=16, pady=(0,6))
        lf = tk.Frame(page, bg=self.LIGHT)
        lf.pack(fill="both", expand=True, padx=16, pady=(0,10))
        _, inner = self.make_scrollable(lf)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            for ci, (h, wd) in enumerate(zip(["No","Hashtag","Jumlah Post","Aksi"],[4,20,12,14])):
                tk.Label(inner, text=h, font=("Segoe UI", 9, "bold"),
                         bg=self.PINK, width=wd, padx=4, pady=5).grid(
                             row=0, column=ci, padx=1, pady=1, sticky="nsew")
            if not self.app.communities:
                tk.Label(inner, text="Belum ada hashtag.", bg=self.LIGHT,
                         fg="gray", font=("Segoe UI", 10)).grid(row=1, column=0, columnspan=4, pady=20)
                return
            sorted_tags = sorted(self.app.communities,
                                 key=lambda t: len(self.app.communities[t]), reverse=True)
            widths = [4, 20, 12, 14]
            for ri, tag in enumerate(sorted_tags, 1):
                count  = len(self.app.communities[tag])
                row_bg = "#fff5f5" if ri % 2 == 0 else "white"
                for ci, (val, wd) in enumerate(zip([str(ri), f"#{tag}", str(count)], widths[:3])):
                    tk.Label(inner, text=val, font=("Segoe UI", 9),
                             bg=row_bg, width=wd, padx=4, pady=4).grid(
                                 row=ri, column=ci, padx=1, pady=1, sticky="nsew")

                def make_edit_tag(old_tag=tag):
                    def do():
                        new_tag = simpledialog.askstring(
                            "Edit Hashtag", f"Ganti #{old_tag} menjadi:",
                            initialvalue=old_tag, parent=self.root)
                        if not new_tag:
                            return
                        new_tag = new_tag.lower().strip().lstrip("#")
                        if not new_tag or new_tag == old_tag:
                            return
                        if new_tag in self.app.communities:
                            messagebox.showerror("Error", "Hashtag sudah ada"); return
                        self.app.communities[new_tag] = self.app.communities.pop(old_tag)
                        import re
                        for p in self.app.posts:
                            p["text"] = re.sub(rf"#{re.escape(old_tag)}\b",
                                               f"#{new_tag}", p["text"], flags=re.IGNORECASE)
                        messagebox.showinfo("Sukses", f"#{old_tag} → #{new_tag}")
                        refresh()
                    return do

                def make_del_tag(t=tag):
                    def do():
                        if messagebox.askyesno("Hapus Hashtag",
                                               f"Hapus #{t} dan hapus tag dari semua post?"):
                            import re
                            post_ids = self.app.communities.pop(t, [])
                            for p in self.app.posts:
                                if p["id"] in post_ids:
                                    p["text"] = re.sub(rf"#{re.escape(t)}\b", "", p["text"],
                                                       flags=re.IGNORECASE).strip()
                            refresh()
                    return do

                bf = tk.Frame(inner, bg=row_bg)
                bf.grid(row=ri, column=3, padx=1, pady=1)
                tk.Button(bf, text="Edit", font=("Segoe UI", 8), bg="#ffe0a0",
                          bd=0, padx=4, command=make_edit_tag()).pack(side="left", padx=2)
                tk.Button(bf, text="Hapus", font=("Segoe UI", 8), bg="tomato",
                          fg="white", bd=0, padx=4, command=make_del_tag()).pack(side="left")

        def create_tag():
            new_tag = simpledialog.askstring("Buat Hashtag", "Nama hashtag baru (tanpa #):",
                                             parent=self.root)
            if not new_tag:
                return
            new_tag = new_tag.lower().strip().lstrip("#")
            if not new_tag:
                messagebox.showerror("Error", "Hashtag tidak boleh kosong"); return
            if new_tag in self.app.communities:
                messagebox.showerror("Error", "Hashtag sudah ada"); return
            self.app.communities[new_tag] = []
            messagebox.showinfo("Sukses", f"Hashtag #{new_tag} berhasil dibuat")
            refresh()

        tk.Button(top_bar, text="➕  Buat Hashtag Baru", font=("Segoe UI", 9),
                  bg=self.PINK, bd=0, padx=8, pady=4, cursor="hand2",
                  command=create_tag).pack(side="left")
        tk.Button(top_bar, text="↻  Refresh", font=("Segoe UI", 9),
                  bg=self.LIGHT, bd=1, relief="solid", padx=8, pady=4,
                  cursor="hand2", command=refresh).pack(side="left", padx=(6,0))
        refresh()
        return page

    # ─── ADMIN VIOLATION LOG ──────────────────────────────────────────────────

    def _admin_page_violation_log(self, parent):
        page = tk.Frame(parent, bg=self.LIGHT)
        tk.Label(page, text="Log Pelanggaran Filter", font=("Segoe UI", 14, "bold"),
                 bg=self.LIGHT).pack(pady=10)
        top_bar = tk.Frame(page, bg=self.LIGHT)
        top_bar.pack(fill="x", padx=16, pady=(0,6))
        lf = tk.Frame(page, bg=self.LIGHT)
        lf.pack(fill="both", expand=True, padx=16, pady=(0,10))
        _, inner = self.make_scrollable(lf)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            headers = ["No","Username","Kata Terlarang","Tipe Konten","Waktu"]
            widths  = [4, 14, 16, 12, 16]
            for ci, (h, wd) in enumerate(zip(headers, widths)):
                tk.Label(inner, text=h, font=("Segoe UI", 9, "bold"),
                         bg=self.PINK, width=wd, padx=4, pady=5).grid(
                             row=0, column=ci, padx=1, pady=1, sticky="nsew")
            if not self.app.violation_log:
                tk.Label(inner, text="Tidak ada pelanggaran tercatat.",
                         bg=self.LIGHT, fg="gray", font=("Segoe UI", 10)
                         ).grid(row=1, column=0, columnspan=5, pady=20)
                return
            for ri, log in enumerate(reversed(self.app.violation_log), 1):
                row_bg = "#fff5f5" if ri % 2 == 0 else "white"
                for ci, (val, wd) in enumerate(
                        zip([str(ri), log["username"], log["kata"], log["tipe"], log["ts"]],
                            widths)):
                    tk.Label(inner, text=val, font=("Segoe UI", 9),
                             bg=row_bg, width=wd, padx=4, pady=4).grid(
                                 row=ri, column=ci, padx=1, pady=1, sticky="nsew")

        def clear_log():
            if messagebox.askyesno("Hapus Log", "Hapus semua log pelanggaran?"):
                self.app.violation_log.clear()
                refresh()

        tk.Button(top_bar, text="🗑  Hapus Semua Log", font=("Segoe UI", 9),
                  bg="tomato", fg="white", bd=0, padx=8, pady=4,
                  cursor="hand2", command=clear_log).pack(side="right")
        tk.Button(top_bar, text="↻  Refresh", font=("Segoe UI", 9),
                  bg=self.PINK, bd=0, padx=8, pady=4,
                  cursor="hand2", command=refresh).pack(side="right", padx=(0,6))
        refresh()
        return page

    # ─── MODERATOR DASHBOARD ──────────────────────────────────────────────────

    def show_moderator_dashboard(self, user):
        self.clear_window()
        self.current_user = user
        P, D, W, L, G, DG = self.PINK, self.DPINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY

        topbar = tk.Frame(self.root, bg=W, height=52)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="Kizuna", font=("Segoe UI", 18, "bold"),
                 bg=W, fg=D).pack(side="left", padx=20)
        tk.Label(topbar, text="🔍 MODERATOR", font=("Segoe UI", 9, "bold"),
                 bg="#fff3cd", fg="#856404", padx=6, pady=2).pack(side="left", padx=4)
        tk.Button(topbar, text="Keluar", font=("Segoe UI", 9),
                  bg=P, fg=DG, bd=0, relief="flat", padx=10,
                  cursor="hand2", command=self.show_login).pack(side="right", padx=16, pady=10)
        tk.Label(topbar, text=f"👤  {user['fullname']}",
                 font=("Segoe UI", 10), bg=W, fg=G).pack(side="right", padx=4)
        tk.Frame(self.root, bg="#eeeeee", height=1).pack(fill="x")

        navbar = tk.Frame(self.root, bg=W, height=54)
        navbar.pack(fill="x", side="bottom")
        navbar.pack_propagate(False)
        tk.Frame(self.root, bg="#eeeeee", height=1).pack(fill="x", side="bottom")

        container = tk.Frame(self.root, bg=L)
        container.pack(fill="both", expand=True)
        pages    = []
        nav_btns = []

        for build_fn in [
            lambda c: self._build_mod_post_page(c, user, L, DG, G, P, W),
            lambda c: self._build_mod_story_page(c, user, L, DG, G, P, W),
            lambda c: self._build_community_page(c, user, L, DG, G, P, W),
            lambda c: self._build_mod_violation_page(c, L, DG, G, P, W),
            lambda c: self._build_mod_analytics_page(c, L, DG, G, P, W),
        ]:
            pg = tk.Frame(container, bg=L)
            pages.append(pg)
            build_fn(pg)

        def mod_nav_switch(index):
            for pg in pages:
                pg.pack_forget()
            pages[index].pack(fill="both", expand=True)
            for i, (frm, ico, lbl) in enumerate(nav_btns):
                if i == index:
                    frm.config(bg=P); ico.config(bg=P); lbl.config(bg=P, fg="#333")
                else:
                    frm.config(bg=W); ico.config(bg=W); lbl.config(bg=W, fg=G)

        for icon, label, idx in [("📝","Review Post",0),("📖","Review Story",1),
                                   ("#️⃣","Hashtag",2),("🚨","Pelanggaran",3),("📊","Analitik",4)]:
            bf = tk.Frame(navbar, bg=W, cursor="hand2")
            bf.pack(side="left", expand=True, fill="both")
            ico = tk.Label(bf, text=icon, font=("Segoe UI", 14), bg=W)
            ico.pack(pady=(6,0))
            lbl = tk.Label(bf, text=label, font=("Segoe UI", 8), bg=W, fg=G)
            lbl.pack()
            for w in (bf, ico, lbl):
                w.bind("<Button-1>", lambda e, i=idx: mod_nav_switch(i))
            nav_btns.append((bf, ico, lbl))

        mod_nav_switch(0)

    # ─── MOD PAGES ────────────────────────────────────────────────────────────

    def _build_mod_post_page(self, parent, user, L, DG, G, P, W):
        hdr = tk.Frame(parent, bg=W, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📝  Review Postingan",
                 font=("Segoe UI", 14, "bold"), bg=W, fg=DG).pack(side="left", padx=16)
        total_lbl = tk.Label(hdr, text="", font=("Segoe UI", 9), bg=W, fg=G)
        total_lbl.pack(side="left")
        tk.Frame(parent, bg="#eeeeee", height=1).pack(fill="x")
        lf = tk.Frame(parent, bg=L)
        lf.pack(fill="both", expand=True, padx=12, pady=8)
        _, inner = self.make_scrollable(lf, L)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            total_lbl.config(text=f"({len(self.app.posts)} postingan)")
            if not self.app.posts:
                tk.Label(inner, text="Tidak ada postingan.", bg=L, fg=G,
                         font=("Segoe UI", 10)).pack(pady=30)
                return
            for p in sorted(self.app.posts, key=lambda x: x.get("id",0), reverse=True):
                card = tk.Frame(inner, bg=W, pady=10, padx=12,
                                highlightthickness=1, highlightbackground="#eeeeee")
                card.pack(fill="x", pady=(0,6))
                top = tk.Frame(card, bg=W)
                top.pack(fill="x")
                u_data   = self.app.users.get(p["username"], {})
                fullname = u_data.get("fullname", p["username"])
                initials = "".join(ww[0].upper() for ww in fullname.split()[:2])
                tk.Label(top, text=initials, font=("Segoe UI", 10, "bold"),
                         bg=P, fg=DG, width=3).pack(side="left")
                tk.Label(top, text=f"  {fullname}  (@{p['username']})",
                         font=("Segoe UI", 10, "bold"), bg=W, fg=DG).pack(side="left")
                tk.Label(top, text=p["ts"] + (" ✏️" if p.get("edited") else ""),
                         font=("Segoe UI", 8), bg=W, fg=G).pack(side="left", padx=6)
                stats_f = tk.Frame(top, bg=W)
                stats_f.pack(side="right")
                score = self.app.feed_score(p)
                for txt_s, bg_s, fg_s in [
                    (f"❤️ {len(p['likes'])}", "#fce4ec", "#c62828"),
                    (f"💬 {len(p.get('comments',[]))}", "#e8f5e9", "#2e7d32"),
                    (f"🔥 {score:.0f}", "#fff3e0", "#e65100"),
                ]:
                    tk.Label(stats_f, text=txt_s, font=("Segoe UI", 8),
                             bg=bg_s, fg=fg_s, padx=4).pack(side="left", padx=2)
                tk.Label(card, text=p["text"], font=("Segoe UI", 10),
                         bg=W, fg=DG, wraplength=560, justify="left").pack(anchor="w", pady=(8,6))
                tags = self.app.extract_hashtags(p["text"])
                if tags:
                    tag_row = tk.Frame(card, bg=W)
                    tag_row.pack(anchor="w", pady=(0,4))
                    for tag in tags:
                        tk.Label(tag_row, text=f"#{tag}", font=("Segoe UI", 8),
                                 bg="#e3f2fd", fg="#1565c0", padx=4, pady=1).pack(side="left", padx=2)
                act = tk.Frame(card, bg=W)
                act.pack(anchor="e")

                def make_warn(pid=p["id"], uname=p["username"]):
                    def do():
                        messagebox.showwarning("Peringatan Dikirim",
                            f"Peringatan telah dikirim ke @{uname}.\nPost ID: {pid}")
                        self.app.log_violation(uname, ["[mod-warning]"], "Post (Peringatan Mod)")
                    return do

                def make_del(pid=p["id"]):
                    def do():
                        if messagebox.askyesno("Hapus Post", "Hapus postingan ini?"):
                            self.app.delete_post(pid)
                            refresh()
                    return do

                tk.Button(act, text="⚠️ Peringatkan", font=("Segoe UI", 8),
                          bg="#fff3cd", fg="#856404", bd=1, relief="solid", padx=6, pady=3,
                          cursor="hand2", command=make_warn()).pack(side="left", padx=4)
                tk.Button(act, text="🗑 Hapus Post", font=("Segoe UI", 8, "bold"),
                          bg="tomato", fg="white", bd=0, padx=8, pady=3,
                          cursor="hand2", command=make_del()).pack(side="left")
        refresh()

    def _build_mod_story_page(self, parent, user, L, DG, G, P, W):
        hdr = tk.Frame(parent, bg=W, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📖  Review Story",
                 font=("Segoe UI", 14, "bold"), bg=W, fg=DG).pack(side="left", padx=16)
        total_lbl = tk.Label(hdr, text="", font=("Segoe UI", 9), bg=W, fg=G)
        total_lbl.pack(side="left")
        tk.Frame(parent, bg="#eeeeee", height=1).pack(fill="x")
        lf = tk.Frame(parent, bg=L)
        lf.pack(fill="both", expand=True, padx=12, pady=8)
        _, inner = self.make_scrollable(lf, L)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            total_lbl.config(text=f"({len(self.app.stories)} story)")
            if not self.app.stories:
                tk.Label(inner, text="Tidak ada story.", bg=L, fg=G,
                         font=("Segoe UI", 10)).pack(pady=30)
                return
            for s in sorted(self.app.stories, key=lambda x: x.get("id",0), reverse=True):
                card = tk.Frame(inner, bg=W, pady=10, padx=12,
                                highlightthickness=1, highlightbackground="#eeeeee")
                card.pack(fill="x", pady=(0,6))
                top = tk.Frame(card, bg=W)
                top.pack(fill="x")
                u_data   = self.app.users.get(s["username"], {})
                fullname = u_data.get("fullname", s["username"])
                initials = "".join(ww[0].upper() for ww in fullname.split()[:2])
                tk.Label(top, text=initials, font=("Segoe UI", 10, "bold"),
                         bg=P, fg=DG, width=3).pack(side="left")
                tk.Label(top, text=f"  {fullname}  (@{s['username']})",
                         font=("Segoe UI", 10, "bold"), bg=W, fg=DG).pack(side="left")
                tk.Label(top, text=s["ts"], font=("Segoe UI", 8),
                         bg=W, fg=G).pack(side="left", padx=6)
                tk.Label(card, text=s["text"], font=("Segoe UI", 10),
                         bg=W, fg=DG, wraplength=560, justify="left").pack(anchor="w", pady=(8,6))
                act = tk.Frame(card, bg=W)
                act.pack(anchor="e")

                def make_warn_s(sid=s["id"], uname=s["username"]):
                    def do():
                        messagebox.showwarning("Peringatan Dikirim",
                            f"Peringatan telah dikirim ke @{uname}.\nStory ID: {sid}")
                        self.app.log_violation(uname, ["[mod-warning]"], "Story (Peringatan Mod)")
                    return do

                def make_del_s(sid=s["id"]):
                    def do():
                        if messagebox.askyesno("Hapus Story", "Hapus story ini?"):
                            self.app.delete_story(sid)
                            refresh()
                    return do

                tk.Button(act, text="⚠️ Peringatkan", font=("Segoe UI", 8),
                          bg="#fff3cd", fg="#856404", bd=1, relief="solid", padx=6, pady=3,
                          cursor="hand2", command=make_warn_s()).pack(side="left", padx=4)
                tk.Button(act, text="🗑 Hapus Story", font=("Segoe UI", 8, "bold"),
                          bg="tomato", fg="white", bd=0, padx=8, pady=3,
                          cursor="hand2", command=make_del_s()).pack(side="left")
        refresh()

    def _build_mod_violation_page(self, parent, L, DG, G, P, W):
        hdr = tk.Frame(parent, bg=W, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🚨  Log Pelanggaran",
                 font=("Segoe UI", 14, "bold"), bg=W, fg=DG).pack(side="left", padx=16)
        btn_bar = tk.Frame(hdr, bg=W)
        btn_bar.pack(side="right", padx=12)
        tk.Frame(parent, bg="#eeeeee", height=1).pack(fill="x")
        lf = tk.Frame(parent, bg=L)
        lf.pack(fill="both", expand=True, padx=12, pady=8)
        _, inner = self.make_scrollable(lf, L)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            if not self.app.violation_log:
                tk.Label(inner, text="Tidak ada pelanggaran tercatat.",
                         bg=L, fg=G, font=("Segoe UI", 10)).pack(pady=30)
                return
            for ri, log in enumerate(reversed(self.app.violation_log), 1):
                row_bg = "#fff5f5" if ri % 2 == 0 else W
                card = tk.Frame(inner, bg=row_bg, pady=8, padx=12,
                                highlightthickness=1, highlightbackground="#eee")
                card.pack(fill="x", pady=2)
                top = tk.Frame(card, bg=row_bg)
                top.pack(fill="x")
                tk.Label(top, text=f"#{ri}", font=("Segoe UI", 8, "bold"),
                         bg="#e57a8a", fg="white", padx=4).pack(side="left")
                tk.Label(top, text=f"  @{log['username']}",
                         font=("Segoe UI", 10, "bold"), bg=row_bg, fg=DG).pack(side="left")
                tk.Label(top, text=log["ts"], font=("Segoe UI", 8),
                         bg=row_bg, fg=G).pack(side="right")
                detail = tk.Frame(card, bg=row_bg)
                detail.pack(fill="x", pady=(4,0))
                tk.Label(detail, text="Kata: ", font=("Segoe UI", 9),
                         bg=row_bg, fg=G).pack(side="left")
                tk.Label(detail, text=log["kata"], font=("Segoe UI", 9, "bold"),
                         bg="#fce4ec", fg="#c62828", padx=4).pack(side="left")
                tk.Label(detail, text=f"  Tipe: {log['tipe']}", font=("Segoe UI", 9),
                         bg=row_bg, fg=G).pack(side="left", padx=8)

        def clear_log():
            if messagebox.askyesno("Hapus Log", "Hapus semua log pelanggaran?"):
                self.app.violation_log.clear()
                refresh()

        tk.Button(btn_bar, text="↻ Refresh", font=("Segoe UI", 9),
                  bg=P, bd=0, padx=8, pady=3, cursor="hand2",
                  command=refresh).pack(side="left", padx=(0,6))
        tk.Button(btn_bar, text="🗑 Hapus Semua", font=("Segoe UI", 9),
                  bg="tomato", fg="white", bd=0, padx=8, pady=3,
                  cursor="hand2", command=clear_log).pack(side="left")
        refresh()

    def _build_mod_analytics_page(self, parent, L, DG, G, P, W):
        hdr = tk.Frame(parent, bg=W, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📊  Analitik Platform",
                 font=("Segoe UI", 14, "bold"), bg=W, fg=DG).pack(side="left", padx=16)
        tk.Frame(parent, bg="#eeeeee", height=1).pack(fill="x")
        outer = tk.Frame(parent, bg=L)
        outer.pack(fill="both", expand=True)
        _, inner = self.make_scrollable(outer, L)

        cards_wrap = tk.Frame(inner, bg=L)
        cards_wrap.pack(fill="x", padx=16, pady=14)
        tk.Label(cards_wrap, text="Ringkasan Platform",
                 font=("Segoe UI", 11, "bold"), bg=L, fg=DG).pack(anchor="w", pady=(0,8))
        cards_row = tk.Frame(cards_wrap, bg=L)
        cards_row.pack(anchor="w")
        total_likes    = sum(len(p["likes"]) for p in self.app.posts)
        total_comments = sum(len(p.get("comments",[])) for p in self.app.posts)
        for icon, label, val, bg_col, fg_col in [
            ("👥","User",len(self.app.users),"#e3f2fd","#1565c0"),
            ("📝","Post",len(self.app.posts),"#fce4ec","#c62828"),
            ("📖","Story",len(self.app.stories),"#f3e5f5","#6a1b9a"),
            ("❤️","Like",total_likes,"#fff3e0","#e65100"),
            ("💬","Komentar",total_comments,"#e8f5e9","#2e7d32"),
            ("🚨","Pelanggaran",len(self.app.violation_log),"#ffebee","#b71c1c"),
        ]:
            box = tk.Frame(cards_row, bg=bg_col, width=130, height=100,
                           highlightthickness=1, highlightbackground="#ddd")
            box.pack(side="left", padx=3); box.pack_propagate(False)
            tk.Label(box, text=icon, font=("Segoe UI", 13), bg=bg_col).pack(pady=(10,2))
            tk.Label(box, text=str(val), font=("Segoe UI", 13, "bold"),
                     bg=bg_col, fg=fg_col).pack()
            tk.Label(box, text=label, font=("Segoe UI", 8), bg=bg_col, fg=G).pack(pady=(2,10))

        tk.Frame(inner, bg="#eeeeee", height=1).pack(fill="x", padx=16, pady=8)

        sec = tk.Frame(inner, bg=L)
        sec.pack(fill="x", padx=16, pady=(0,8))
        tk.Label(sec, text="🔥  Top Post Engagement",
                 font=("Segoe UI", 11, "bold"), bg=L, fg=DG).pack(anchor="w", pady=(0,6))
        sorted_posts = sorted(self.app.posts, key=self.app.feed_score, reverse=True)
        max_score    = self.app.feed_score(sorted_posts[0]) if sorted_posts else 1
        for rank, p in enumerate(sorted_posts[:8], 1):
            score   = self.app.feed_score(p)
            bar_pct = score / max_score if max_score > 0 else 0
            row = tk.Frame(sec, bg=W, pady=6, padx=10,
                           highlightthickness=1, highlightbackground="#eee")
            row.pack(fill="x", pady=2)
            rank_clr = "#e57a8a" if rank==1 else ("#f4a261" if rank==2 else ("#2ec4b6" if rank==3 else G))
            tk.Label(row, text=f"#{rank}", font=("Segoe UI", 9, "bold"),
                     bg=rank_clr, fg="white", width=3).pack(side="left")
            info = tk.Frame(row, bg=W)
            info.pack(side="left", fill="x", expand=True, padx=8)
            top_line = tk.Frame(info, bg=W)
            top_line.pack(fill="x")
            tk.Label(top_line, text=f"@{p['username']}",
                     font=("Segoe UI", 9, "bold"), bg=W, fg=DG).pack(side="left")
            tk.Label(top_line,
                     text=f"  ❤️ {len(p['likes'])}   💬 {len(p.get('comments',[]))}",
                     font=("Segoe UI", 8), bg=W, fg=G).pack(side="left")
            tk.Label(top_line, text=f"Score: {score:.1f}",
                     font=("Segoe UI", 9, "bold"), bg=W, fg="#e57a8a").pack(side="right")
            preview = p["text"][:65] + ("…" if len(p["text"])>65 else "")
            tk.Label(info, text=preview, font=("Segoe UI", 9),
                     bg=W, fg=DG, wraplength=460, justify="left").pack(anchor="w", pady=(2,4))
            bar_outer = tk.Frame(info, bg="#f0f0f0", height=5)
            bar_outer.pack(fill="x"); bar_outer.pack_propagate(False)
            tk.Frame(bar_outer, bg="#e57a8a", height=5).place(relwidth=bar_pct, relheight=1.0)

    # ─── USER DASHBOARD ───────────────────────────────────────────────────────

    def show_user_dashboard(self, user):
        self.clear_window()
        self.current_user = user
        P, D, W, L, G, DG = self.PINK, self.DPINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY

        topbar = tk.Frame(self.root, bg=W, height=52)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="Kizuna", font=("Segoe UI", 18, "bold"),
                 bg=W, fg=D).pack(side="left", padx=20)
        tk.Button(topbar, text="Keluar", font=("Segoe UI", 9),
                  bg=P, fg=DG, bd=0, relief="flat", padx=10,
                  cursor="hand2", command=self.show_login).pack(side="right", padx=16, pady=10)
        tk.Label(topbar, text=f"👤  {user['fullname']}",
                 font=("Segoe UI", 10), bg=W, fg=G).pack(side="right", padx=4)
        tk.Frame(self.root, bg="#eeeeee", height=1).pack(fill="x")

        navbar = tk.Frame(self.root, bg=W, height=54)
        navbar.pack(fill="x", side="bottom")
        navbar.pack_propagate(False)
        tk.Frame(self.root, bg="#eeeeee", height=1).pack(fill="x", side="bottom")

        container = tk.Frame(self.root, bg=L)
        container.pack(fill="both", expand=True)
        pages    = []
        nav_btns = []

        # ── PAGE 0: Beranda ───────────────────────────────────────────────────
        page0 = tk.Frame(container, bg=L)
        pages.append(page0)

        story_outer = tk.Frame(page0, bg=W)
        story_outer.pack(fill="x", padx=16, pady=(10,4))
        tk.Label(story_outer, text="Stories", font=("Segoe UI", 9, "bold"),
                 bg=W, fg=DG).pack(anchor="w", padx=8, pady=(6,2))
        s_canvas = tk.Canvas(story_outer, bg=W, height=70, bd=0, highlightthickness=0)
        s_scroll = tk.Scrollbar(story_outer, orient="horizontal", command=s_canvas.xview)
        s_inner  = tk.Frame(s_canvas, bg=W)
        s_inner.bind("<Configure>",
                     lambda e: s_canvas.configure(scrollregion=s_canvas.bbox("all")))
        s_canvas.create_window((0,0), window=s_inner, anchor="nw")
        s_canvas.configure(xscrollcommand=s_scroll.set)
        s_canvas.pack(fill="x", padx=8)
        s_scroll.pack(fill="x", padx=8)

        def refresh_stories():
            for w in s_inner.winfo_children():
                w.destroy()
            add_box = tk.Frame(s_inner, bg=L, width=54, height=60, cursor="hand2")
            add_box.pack(side="left", padx=4)
            add_box.pack_propagate(False)
            tk.Label(add_box, text="＋", font=("Segoe UI", 18), bg=P, width=3).pack(expand=True)
            tk.Label(add_box, text="Tambah", font=("Segoe UI", 7), bg=L).pack()
            for w in [add_box] + list(add_box.winfo_children()):
                w.bind("<Button-1>", lambda e: self._open_add_story(refresh_stories))
            for s in self.app.stories:
                sbox = tk.Frame(s_inner, bg=W, width=54, height=60, cursor="hand2",
                                highlightthickness=1, highlightbackground=P)
                sbox.pack(side="left", padx=4)
                sbox.pack_propagate(False)
                tk.Label(sbox, text=s["username"][:2].upper(), font=("Segoe UI", 13, "bold"),
                         bg=P, fg=DG).pack(expand=True)
                tk.Label(sbox, text=f"@{s['username'][:6]}", font=("Segoe UI", 7),
                         bg=W, fg=G).pack()
                def make_view(story=s):
                    def do(e=None):
                        messagebox.showinfo(f"Story @{story['username']}",
                                            f"{story['text']}\n\n🕐 {story['ts']}")
                    return do
                for w in [sbox] + list(sbox.winfo_children()):
                    w.bind("<Button-1>", make_view(s))

        refresh_stories()

        input_frame = tk.Frame(page0, bg=W, pady=10)
        input_frame.pack(fill="x", padx=16, pady=(4,6))
        tk.Label(input_frame, text="Apa yang kamu pikirkan? Gunakan #hashtag",
                 font=("Segoe UI", 9), bg=W, fg=G).pack(anchor="w", padx=10)
        self.post_entry = tk.Entry(input_frame, font=("Segoe UI", 11),
                                   bd=0, bg=L, fg=DG, insertbackground=DG)
        self.post_entry.pack(fill="x", padx=10, pady=6, ipady=4)
        tk.Frame(input_frame, bg="#eeeeee", height=1).pack(fill="x", padx=10)

        post_btn_row = tk.Frame(input_frame, bg=W)
        post_btn_row.pack(fill="x", padx=10, pady=8)

        feed_mode   = tk.StringVar(value="ranked")
        feed_filter = tk.StringVar(value="all")

        def toggle_feed_mode():
            if feed_mode.get() == "ranked":
                feed_mode.set("recent"); mode_btn.config(text="📅 Terbaru")
            else:
                feed_mode.set("ranked"); mode_btn.config(text="🔥 Terpopuler")
            refresh_feed()

        def toggle_feed_filter():
            if feed_filter.get() == "all":
                feed_filter.set("following"); filter_btn.config(text="👥 Following")
            else:
                feed_filter.set("all"); filter_btn.config(text="🌐 Semua")
            refresh_feed()

        tk.Button(input_frame, text="  Posting  ", font=("Segoe UI", 9, "bold"),
                  bg=P, fg=DG, bd=0, relief="flat", padx=8, pady=4, cursor="hand2",
                  command=lambda: self._do_create_post(user, refresh_feed)
                  ).pack(in_=post_btn_row, side="right")
        filter_btn = tk.Button(post_btn_row, text="🌐 Semua", font=("Segoe UI", 8),
                               bg=L, fg=DG, bd=1, relief="solid", padx=6, pady=3,
                               cursor="hand2", command=toggle_feed_filter)
        filter_btn.pack(side="left", padx=(0,4))
        mode_btn = tk.Button(post_btn_row, text="🔥 Terpopuler", font=("Segoe UI", 8),
                             bg=L, fg=DG, bd=1, relief="solid", padx=6, pady=3,
                             cursor="hand2", command=toggle_feed_mode)
        mode_btn.pack(side="left")

        list_frame  = tk.Frame(page0, bg=L)
        list_frame.pack(fill="both", expand=True, padx=16, pady=(0,8))
        feed_canvas = tk.Canvas(list_frame, bg=L, bd=0, highlightthickness=0)
        feed_sb     = tk.Scrollbar(list_frame, orient="vertical", command=feed_canvas.yview)
        self.feed_inner = tk.Frame(feed_canvas, bg=L)
        self.feed_inner.bind("<Configure>",
            lambda e: feed_canvas.configure(scrollregion=feed_canvas.bbox("all")))
        feed_win_id = feed_canvas.create_window((0,0), window=self.feed_inner, anchor="nw")
        feed_canvas.configure(yscrollcommand=feed_sb.set)
        feed_canvas.bind("<Configure>",
                         lambda e: feed_canvas.itemconfig(feed_win_id, width=e.width))
        feed_canvas.pack(side="left", fill="both", expand=True)
        feed_sb.pack(side="right", fill="y")
        self.canvas_ref = feed_canvas

        # ── PAGE 1: Tagar ─────────────────────────────────────────────────────
        page1 = tk.Frame(container, bg=L)
        pages.append(page1)
        self._build_community_page(page1, user, L, DG, G, P, W)

        # ── PAGE 2: Chat ──────────────────────────────────────────────────────
        page2 = tk.Frame(container, bg=L)
        pages.append(page2)
        self._build_chat_page(page2, user, L, DG, G, P, W)

        # ── PAGE 3: Aktivitas ─────────────────────────────────────────────────
        page3 = tk.Frame(container, bg=L)
        pages.append(page3)
        tk.Label(page3, text="Aktivitas", font=("Segoe UI", 14, "bold"),
                 bg=L, fg=DG).pack(pady=14)
        act_lf = tk.Frame(page3, bg=L)
        act_lf.pack(fill="both", expand=True, padx=16)
        _, act_inner = self.make_scrollable(act_lf, L)

        def refresh_activity():
            for w in act_inner.winfo_children():
                w.destroy()
            found = False
            for p in reversed(self.app.posts):
                if p["username"] == user["username"]:
                    for liker in p["likes"]:
                        found = True
                        row = tk.Frame(act_inner, bg=W, pady=6, padx=10,
                                       highlightthickness=1, highlightbackground="#eee")
                        row.pack(fill="x", pady=2)
                        tk.Label(row, text=f"❤️  @{liker} menyukai postinganmu",
                                 font=("Segoe UI", 10), bg=W, fg=DG).pack(anchor="w")
                        tk.Label(row, text=f"\"{p['text'][:50]}...\"",
                                 font=("Segoe UI", 9), bg=W, fg=G).pack(anchor="w")
                    for c in p.get("comments", []):
                        if c["username"] != user["username"]:
                            found = True
                            row = tk.Frame(act_inner, bg=W, pady=6, padx=10,
                                           highlightthickness=1, highlightbackground="#eee")
                            row.pack(fill="x", pady=2)
                            tk.Label(row, text=f"💬  @{c['username']} mengomentari postinganmu",
                                     font=("Segoe UI", 10), bg=W, fg=DG).pack(anchor="w")
                            tk.Label(row, text=f"\"{c['text']}\"",
                                     font=("Segoe UI", 9), bg=W, fg=G).pack(anchor="w")
            if not found:
                tk.Label(act_inner, text="Belum ada aktivitas.",
                         font=("Segoe UI", 10), bg=L, fg=G).pack(pady=30)

        refresh_activity()

        def refresh_feed():
            for w in self.feed_inner.winfo_children():
                w.destroy()
            pool = list(self.app.posts)
            if feed_filter.get() == "following":
                following = self.app.follows.get(user["username"], set())
                pool = [p for p in pool
                        if p["username"] in following or p["username"] == user["username"]]
            if feed_mode.get() == "ranked":
                pool = sorted(pool, key=self.app.feed_score, reverse=True)
            else:
                pool = list(reversed(pool))
            if not pool:
                tk.Label(self.feed_inner,
                         text="Belum ada postingan." if feed_filter.get() == "all"
                              else "Belum ada postingan dari orang yang kamu ikuti.",
                         font=("Segoe UI", 10), bg=L, fg=G).pack(pady=30)
                return
            for p in pool:
                self._add_post_card(p, user, refresh_feed, refresh_activity)

        refresh_feed()

        # ── PAGE 4: Profil ────────────────────────────────────────────────────
        page4 = tk.Frame(container, bg=L)
        pages.append(page4)
        self._render_profile(page4, user, refresh_feed)

        # ── Nav ───────────────────────────────────────────────────────────────
        for icon, label, idx in [("🏠","Beranda",0),("#️⃣","Tagar",1),
                                   ("💬","Chat",2),("❤️","Aktivitas",3),("👤","Profil",4)]:
            bf = tk.Frame(navbar, bg=W, cursor="hand2")
            bf.pack(side="left", expand=True, fill="both")
            ico = tk.Label(bf, text=icon, font=("Segoe UI", 14), bg=W)
            ico.pack(pady=(6,0))
            lbl = tk.Label(bf, text=label, font=("Segoe UI", 8), bg=W, fg=G)
            lbl.pack()
            for w in (bf, ico, lbl):
                w.bind("<Button-1>",
                       lambda e, i=idx: self._nav_switch(
                           pages, i, nav_btns, page4, user, refresh_feed, refresh_activity))
            nav_btns.append((bf, ico, lbl))

        self._nav_switch(pages, 0, nav_btns, page4, user, refresh_feed, refresh_activity)

    def _nav_switch(self, pages, index, nav_btns, page4, user, rf, ra):
        P, W, G = self.PINK, self.WHITE, self.GRAY
        for pg in pages:
            pg.pack_forget()
        pages[index].pack(fill="both", expand=True)
        if index == 3:
            ra()
        if index == 4:
            self._render_profile(page4, user, rf)
        for i, (frm, ico, lbl) in enumerate(nav_btns):
            if i == index:
                frm.config(bg=P); ico.config(bg=P); lbl.config(bg=P, fg="#333")
            else:
                frm.config(bg=W); ico.config(bg=W); lbl.config(bg=W, fg=G)

    # ─── STORY DIALOG ─────────────────────────────────────────────────────────

    def _open_add_story(self, refresh_fn):
        win = tk.Toplevel(self.root)
        win.title("Tambah Story")
        win.geometry("360x200")
        win.config(bg="white")
        tk.Label(win, text="Isi Story kamu:", font=("Segoe UI", 10), bg="white").pack(pady=10)
        entry = tk.Text(win, width=40, height=4, font=("Segoe UI", 10))
        entry.pack(padx=16)

        def submit():
            text = entry.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Error", "Story tidak boleh kosong", parent=win); return
            self.app.add_story(self.current_user["username"], text)
            win.destroy()
            refresh_fn()

        tk.Button(win, text="Posting Story", bg=self.PINK,
                  font=("Segoe UI", 10, "bold"), command=submit).pack(pady=10)

    # ─── CREATE POST ──────────────────────────────────────────────────────────

    def _do_create_post(self, user, refresh_fn):
        text = self.post_entry.get().strip()
        if not text:
            return
        self.app.add_post(user["username"], text)
        self.post_entry.delete(0, tk.END)
        refresh_fn()
        self.canvas_ref.update_idletasks()
        self.canvas_ref.yview_moveto(0.0)

    # ─── POST CARD (user feed) ────────────────────────────────────────────────

    def _add_post_card(self, post, viewer, refresh_feed_fn, refresh_activity_fn):
        P, W, L, G, DG = self.PINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY
        card = tk.Frame(self.feed_inner, bg=W, pady=10, padx=12,
                        highlightthickness=1, highlightbackground="#eeeeee")
        card.pack(fill="x", pady=(0,8))

        header = tk.Frame(card, bg=W)
        header.pack(fill="x")
        u_data   = self.app.users.get(post["username"], {})
        fullname = u_data.get("fullname", post["username"])
        initials = "".join(x[0].upper() for x in fullname.split()[:2])
        tk.Label(header, text=initials, font=("Segoe UI", 10, "bold"),
                 bg=P, fg=DG, width=3).pack(side="left")
        tk.Label(header, text=f"  {post['username']}",
                 font=("Segoe UI", 10, "bold"), bg=W, fg=DG).pack(side="left")
        ts_display = post["ts"] + ("  ✏️ diedit" if post.get("edited") else "")
        tk.Label(header, text=f"  {ts_display}",
                 font=("Segoe UI", 8), bg=W, fg=G).pack(side="left")

        if post["username"] == viewer["username"]:
            def make_delete(pid=post["id"]):
                def do():
                    if messagebox.askyesno("Hapus Post",
                                           "Apakah kamu yakin ingin menghapus postingan ini?"):
                        self.app.delete_post(pid)
                        refresh_feed_fn()
                return do

            def make_edit_post(p=post):
                def do():
                    def on_save(new_text):
                        self.app.edit_post(p, new_text, viewer["username"])
                        refresh_feed_fn()
                    self.open_edit_dialog("Edit Postingan", p["text"], on_save)
                return do

            act_btns = tk.Frame(header, bg=W)
            act_btns.pack(side="right")
            tk.Button(act_btns, text="✏️", font=("Segoe UI", 9), bg=W,
                      bd=0, fg=DG, cursor="hand2", command=make_edit_post()).pack(side="left")
            tk.Button(act_btns, text="🗑", font=("Segoe UI", 9), bg=W,
                      bd=0, fg="tomato", cursor="hand2", command=make_delete()).pack(side="left")

        post_text_var = tk.StringVar(value=post["text"])
        tk.Label(card, textvariable=post_text_var, font=("Segoe UI", 11),
                 bg=W, fg=DG, wraplength=500, justify="left").pack(anchor="w", pady=(8,4))

        action_row = tk.Frame(card, bg=W)
        action_row.pack(anchor="w", fill="x")

        liked    = viewer["username"] in post["likes"]
        like_var = tk.StringVar(value=f"{'❤️' if liked else '♡'} {len(post['likes'])}")
        like_btn = tk.Button(action_row, textvariable=like_var, font=("Segoe UI", 10),
                             bg=W, bd=0, fg="#e57a8a" if liked else G, cursor="hand2")
        like_btn.pack(side="left", padx=(0,8))

        def toggle_like(p=post, var=like_var, btn=like_btn):
            liked_now = self.app.toggle_like(p, viewer["username"])
            var.set(f"{'❤️' if liked_now else '♡'} {len(p['likes'])}")
            btn.config(fg="#e57a8a" if liked_now else G)
            refresh_activity_fn()

        like_btn.config(command=toggle_like)

        cmt_btn = tk.Button(action_row, text=f"💬 {len(post.get('comments',[]))}",
                            font=("Segoe UI", 10), bg=W, bd=0, fg=G, cursor="hand2")
        cmt_btn.pack(side="left")
        cmt_btn.config(command=lambda p=post, btn=cmt_btn: self._open_comments(
            p, btn, viewer, refresh_activity_fn))

    # ─── COMMENTS ─────────────────────────────────────────────────────────────

    def _open_comments(self, post, cmt_btn, viewer, refresh_activity_fn):
        P, W, L, G, DG = self.PINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY
        win = tk.Toplevel(self.root)
        win.title("Komentar")
        win.geometry("420x480")
        win.config(bg=W)
        tk.Label(win, text="Komentar", font=("Segoe UI", 13, "bold"), bg=W).pack(pady=10)
        lf = tk.Frame(win, bg=W)
        lf.pack(fill="both", expand=True, padx=16)
        _, c_inner = self.make_scrollable(lf, W)

        def render_comments():
            for w in c_inner.winfo_children():
                w.destroy()
            if not post.get("comments"):
                tk.Label(c_inner, text="Belum ada komentar.",
                         bg=W, fg=G, font=("Segoe UI", 9)).pack(pady=10)
                return
            for cm in post["comments"]:
                row = tk.Frame(c_inner, bg=L, pady=6, padx=8,
                               highlightthickness=1, highlightbackground="#eee")
                row.pack(fill="x", pady=2)
                meta_row = tk.Frame(row, bg=L)
                meta_row.pack(fill="x")
                cmt_ts_disp = cm["ts"] + ("  ✏️" if cm.get("edited") else "")
                tk.Label(meta_row, text=f"@{cm['username']}  •  {cmt_ts_disp}",
                         font=("Segoe UI", 8), bg=L, fg=G).pack(side="left", anchor="w")

                if cm["username"] == viewer["username"]:
                    def make_edit_cmt(comment=cm):
                        def do():
                            def on_save(new_text):
                                self.app.edit_comment(comment, new_text, viewer["username"])
                                render_comments()
                                cmt_btn.config(text=f"💬 {len(post.get('comments',[]))}")
                                refresh_activity_fn()
                            self.open_edit_dialog("Edit Komentar", comment["text"], on_save, win)
                        return do

                    def make_del_cmt(cid=cm["id"]):
                        def do():
                            self.app.delete_comment(post, cid)
                            render_comments()
                            cmt_btn.config(text=f"💬 {len(post.get('comments',[]))}")
                            refresh_activity_fn()
                        return do

                    action_f = tk.Frame(meta_row, bg=L)
                    action_f.pack(side="right")
                    tk.Button(action_f, text="✏️ Edit", bg=L, fg=DG,
                              font=("Segoe UI", 7), bd=0, padx=3,
                              command=make_edit_cmt()).pack(side="left")
                    tk.Button(action_f, text="Hapus", bg="tomato", fg="white",
                              font=("Segoe UI", 7), bd=0, padx=4,
                              command=make_del_cmt()).pack(side="left", padx=(2,0))

                tk.Label(row, text=cm["text"], font=("Segoe UI", 10),
                         bg=L, wraplength=340, justify="left").pack(anchor="w")

        render_comments()

        bottom = tk.Frame(win, bg=W)
        bottom.pack(fill="x", padx=16, pady=8)
        cmt_input = tk.Entry(bottom, font=("Segoe UI", 10), bd=1, relief="solid")
        cmt_input.pack(side="left", fill="x", expand=True, ipady=4)
        self.add_placeholder(cmt_input, "Tulis komentar...")

        def post_comment():
            text = self.get_entry_value(cmt_input)
            if not text:
                return
            self.app.add_comment(post, viewer["username"], text)
            cmt_input.delete(0, tk.END)
            cmt_input.is_showing_placeholder = False
            render_comments()
            cmt_btn.config(text=f"💬 {len(post.get('comments',[]))}")
            refresh_activity_fn()

        tk.Button(bottom, text="Kirim", bg=P, font=("Segoe UI", 9, "bold"),
                  bd=0, padx=10, command=post_comment).pack(side="left", padx=(6,0))
        cmt_input.bind("<Return>", lambda e: post_comment())

    # ─── CHAT ─────────────────────────────────────────────────────────────────

    def _build_chat_page(self, parent, user, L, DG, G, P, W):
        self._chat_store  = {}
        self._chat_target = [None]
        tk.Label(parent, text="Chat", font=("Segoe UI", 14, "bold"),
                 bg=L, fg=DG).pack(pady=14)
        main = tk.Frame(parent, bg=L)
        main.pack(fill="both", expand=True, padx=16)
        left = tk.Frame(main, bg=W, width=200)
        left.pack(side="left", fill="y", padx=(0,8))
        left.pack_propagate(False)
        tk.Label(left, text="Pengguna", font=("Segoe UI", 10, "bold"), bg=W).pack(pady=8)
        right = tk.Frame(main, bg=W)
        right.pack(side="left", fill="both", expand=True)
        chat_display = tk.Text(right, state="disabled", font=("Segoe UI", 10),
                               bg="#f0f0f0", bd=0, wrap="word", height=16)
        chat_display.pack(fill="both", expand=True, padx=8, pady=8)
        bottom = tk.Frame(right, bg=W)
        bottom.pack(fill="x", padx=8, pady=(0,8))
        chat_entry = tk.Entry(bottom, font=("Segoe UI", 10), bd=1, relief="solid")
        chat_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.add_placeholder(chat_entry, "Ketik pesan...")

        def select_user(uname):
            self._chat_target[0] = uname
            chat_display.config(state="normal")
            chat_display.delete("1.0", tk.END)
            for msg in self._chat_store.get(uname, []):
                prefix = "Kamu" if msg["from"] == user["username"] else f"@{msg['from']}"
                chat_display.insert(tk.END, f"{prefix}: {msg['text']}\n")
            chat_display.config(state="disabled")

        def send_msg():
            target = self._chat_target[0]
            if not target:
                messagebox.showinfo("Info", "Pilih pengguna dulu"); return
            text = self.get_entry_value(chat_entry)
            if not text:
                return
            self._chat_store.setdefault(target, []).append(
                {"from": user["username"], "text": text})
            chat_entry.delete(0, tk.END)
            chat_entry.is_showing_placeholder = False
            select_user(target)

        tk.Button(bottom, text="Kirim", bg=P, fg=DG,
                  font=("Segoe UI", 9, "bold"), bd=0, padx=10,
                  command=send_msg).pack(side="left", padx=(6,0))
        chat_entry.bind("<Return>", lambda e: send_msg())

        for uname in self.app.users:
            if uname == user["username"]:
                continue
            tk.Button(left, text=f"@{uname}", font=("Segoe UI", 9),
                      bg=W, bd=0, anchor="w", padx=8, pady=4, cursor="hand2",
                      command=lambda u=uname: select_user(u)).pack(fill="x")

    # ─── COMMUNITY / HASHTAG ──────────────────────────────────────────────────

    def _build_community_page(self, parent, user, L, DG, G, P, W):
        tk.Label(parent, text="Hashtag", font=("Segoe UI", 14, "bold"),
                 bg=L, fg=DG).pack(pady=14)
        top = tk.Frame(parent, bg=L)
        top.pack(fill="x", padx=16, pady=(0,8))
        search_var   = tk.StringVar()
        search_entry = tk.Entry(top, textvariable=search_var, font=("Segoe UI", 10),
                                bd=1, relief="solid", width=20)
        search_entry.pack(side="left", ipady=3)
        self.add_placeholder(search_entry, "Cari #hashtag...")

        right_panel = tk.Frame(parent, bg=L)
        right_panel.pack(fill="both", expand=True, padx=16)
        tag_list_frame = tk.Frame(right_panel, bg=W, width=160)
        tag_list_frame.pack(side="left", fill="y", padx=(0,8))
        tag_list_frame.pack_propagate(False)
        tk.Label(tag_list_frame, text="Trending #", font=("Segoe UI", 10, "bold"),
                 bg=W, fg=DG).pack(pady=8, padx=8, anchor="w")
        post_panel = tk.Frame(right_panel, bg=L)
        post_panel.pack(side="left", fill="both", expand=True)
        post_lf = tk.Frame(post_panel, bg=L)
        post_lf.pack(fill="both", expand=True)
        _, post_inner = self.make_scrollable(post_lf, L)

        def show_tag_posts(tag):
            for w in post_inner.winfo_children():
                w.destroy()
            tag_posts = sorted(
                [p for p in self.app.posts if p["id"] in self.app.communities.get(tag,[])],
                key=self.app.feed_score, reverse=True)
            tk.Label(post_inner, text=f"#{tag}  —  {len(tag_posts)} postingan",
                     font=("Segoe UI", 11, "bold"), bg=L, fg=DG).pack(anchor="w", pady=(4,8))
            if not tag_posts:
                tk.Label(post_inner, text="Belum ada postingan dengan hashtag ini.",
                         font=("Segoe UI", 10), bg=L, fg=G).pack(pady=20)
                return
            for p in tag_posts:
                row = tk.Frame(post_inner, bg=W, pady=8, padx=10,
                               highlightthickness=1, highlightbackground="#eee")
                row.pack(fill="x", pady=3)
                u_data   = self.app.users.get(p["username"], {})
                fullname = u_data.get("fullname", p["username"])
                initials = "".join(ww[0].upper() for ww in fullname.split()[:2])
                h = tk.Frame(row, bg=W)
                h.pack(fill="x")
                tk.Label(h, text=initials, font=("Segoe UI", 9, "bold"),
                         bg=P, fg=DG, width=3).pack(side="left")
                tk.Label(h, text=f"  @{p['username']}", font=("Segoe UI", 9, "bold"),
                         bg=W, fg=DG).pack(side="left")
                score = self.app.feed_score(p)
                tk.Label(h, text=f"  🔥{score:.0f}", font=("Segoe UI", 8),
                         bg=W, fg="#e57a8a").pack(side="left")
                tk.Label(h, text=p["ts"] + (" ✏️" if p.get("edited") else ""),
                         font=("Segoe UI", 8), bg=W, fg=G).pack(side="right")
                tk.Label(row, text=p["text"], font=("Segoe UI", 10),
                         bg=W, fg=DG, wraplength=360, justify="left").pack(anchor="w", pady=(4,2))
                stat = tk.Frame(row, bg=W)
                stat.pack(anchor="w")
                tk.Label(stat, text=f"❤️ {len(p['likes'])}  💬 {len(p.get('comments',[]))}",
                         font=("Segoe UI", 8), bg=W, fg=G).pack(side="left")

        def refresh_tag_list(filter_text=""):
            for w in tag_list_frame.winfo_children():
                if isinstance(w, tk.Label) and w.cget("text") == "Trending #":
                    continue
                if not isinstance(w, tk.Label):
                    w.destroy()
                elif w.cget("text") != "Trending #":
                    w.destroy()
            sorted_tags = sorted(self.app.communities,
                                 key=lambda t: len(self.app.communities[t]), reverse=True)
            if filter_text:
                sorted_tags = [t for t in sorted_tags if filter_text.lower() in t]
            for tag in sorted_tags[:20]:
                tk.Button(tag_list_frame,
                          text=f"#{tag}  ({len(self.app.communities[tag])})",
                          font=("Segoe UI", 9), bg=W, bd=0,
                          anchor="w", padx=8, pady=3, cursor="hand2",
                          command=lambda t=tag: show_tag_posts(t)).pack(fill="x")
            if not sorted_tags:
                tk.Label(tag_list_frame, text="Belum ada #hashtag",
                         font=("Segoe UI", 8), bg=W, fg=G).pack(pady=8, padx=8)

        def on_search(*args):
            q = search_var.get().lstrip("#").strip()
            if search_entry.is_showing_placeholder:
                q = ""
            refresh_tag_list(q)

        search_var.trace_add("write", on_search)

        def do_search(event=None):
            q = self.get_entry_value(search_entry).lstrip("#").strip()
            if q:
                refresh_tag_list(q)
                if q in self.app.communities:
                    show_tag_posts(q)

        search_entry.bind("<Return>", do_search)
        tk.Button(top, text="Cari", font=("Segoe UI", 9), bg=P, fg=DG,
                  bd=0, padx=8, pady=3, command=do_search).pack(side="left", padx=(6,0))

        refresh_tag_list()
        if self.app.communities:
            first_tag = sorted(self.app.communities,
                               key=lambda t: len(self.app.communities[t]), reverse=True)[0]
            show_tag_posts(first_tag)
        else:
            tk.Label(post_inner, text="Post dengan #hashtag akan muncul di sini.",
                     font=("Segoe UI", 10), bg=L, fg=G).pack(pady=30)

    # ─── PROFILE ──────────────────────────────────────────────────────────────

    def _render_profile(self, parent, user, refresh_feed_fn=None):
        P, W, L, G, DG = self.PINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY
        for w in parent.winfo_children():
            w.destroy()

        top_bar = tk.Frame(parent, bg=L)
        top_bar.pack(fill="x", padx=16, pady=(10,0))
        tk.Label(top_bar, text="Profil Saya", font=("Segoe UI", 14, "bold"),
                 bg=L, fg=DG).pack(side="left")
        tk.Button(top_bar, text="↻  Refresh", font=("Segoe UI", 9),
                  bg=P, fg=DG, bd=0, padx=10, pady=3, cursor="hand2",
                  command=lambda: self._render_profile(parent, user, refresh_feed_fn)
                  ).pack(side="right")
        tk.Frame(parent, bg="#eeeeee", height=1).pack(fill="x", padx=16, pady=(6,0))

        body_frame = tk.Frame(parent, bg=L)
        body_frame.pack(fill="both", expand=True)
        _, body_inner = self.make_scrollable(body_frame, L)

        av = tk.Frame(body_inner, bg=L)
        av.pack(pady=16)
        initials = "".join(x[0].upper() for x in user["fullname"].split()[:2])
        tk.Label(av, text=initials, font=("Segoe UI", 22, "bold"),
                 bg=P, fg=DG, width=3, height=1).pack()

        tk.Label(body_inner, text=user["fullname"], font=("Segoe UI", 14, "bold"),
                 bg=L, fg=DG).pack()
        tk.Label(body_inner, text=f"@{user['username']}", font=("Segoe UI", 10),
                 bg=L, fg=G).pack(pady=2)
        tk.Label(body_inner, text=user["email"], font=("Segoe UI", 10),
                 bg=L, fg=G).pack()
        bio = user.get("bio", "") or "Belum ada bio"
        tk.Label(body_inner, text=bio, font=("Segoe UI", 9, "italic"),
                 bg=L, fg=G).pack(pady=4)

        # Stats
        stats_wrapper = tk.Frame(body_inner, bg=L)
        stats_wrapper.pack(pady=6)
        stats_frame = tk.Frame(stats_wrapper, bg=L)
        stats_frame.pack(anchor="center")

        user_posts      = [p for p in self.app.posts   if p["username"] == user["username"]]
        user_stories    = [s for s in self.app.stories if s["username"] == user["username"]]
        following_count = len(self.app.follows.get(user["username"], set()))
        followers_count = sum(1 for f in self.app.follows.values() if user["username"] in f)
        total_likes_rcv = sum(len(p["likes"]) for p in user_posts)
        eng_score       = sum(self.app.feed_score(p) for p in user_posts)

        for label, val in [("Post",len(user_posts)),("Story",len(user_stories)),
                            ("Following",following_count),("Followers",followers_count),
                            ("❤️ Likes",total_likes_rcv),("🔥 Score",f"{eng_score:.0f}")]:
            box = tk.Frame(stats_frame, bg=W, width=75, height=52,
                           highlightthickness=1, highlightbackground="#ddd")
            box.pack(side="left", padx=4)
            box.pack_propagate(False)
            tk.Label(box, text=str(val), font=("Segoe UI", 13, "bold"),
                     bg=W, fg="#e57a8a").pack(expand=True)
            tk.Label(box, text=label, font=("Segoe UI", 7), bg=W, fg=G).pack()

        tk.Label(body_inner, text=f"⏱ Diperbarui: {datetime.now().strftime('%H:%M:%S')}",
                 font=("Segoe UI", 7), bg=L, fg=G).pack(pady=(2,0))
        tk.Frame(body_inner, bg="#eeeeee", height=1).pack(fill="x", padx=40, pady=8)

        btn_row = tk.Frame(body_inner, bg=L)
        btn_row.pack()
        tk.Button(btn_row, text="  ✏️ Edit Profil  ", font=("Segoe UI", 10),
                  bg=P, fg=DG, bd=0, padx=12, pady=6, cursor="hand2",
                  command=lambda: self._open_edit_profile(
                      user, parent, refresh_feed_fn)).pack(side="left", padx=4)
        tk.Button(btn_row, text="  👥 Connect  ", font=("Segoe UI", 10),
                  bg=L, fg=DG, bd=1, relief="solid", padx=12, pady=6, cursor="hand2",
                  command=lambda: self._open_social_connect(user)).pack(side="left", padx=4)

        tk.Frame(body_inner, bg="#eeeeee", height=1).pack(fill="x", padx=40, pady=(8,4))

        tab_frame = tk.Frame(body_inner, bg=L)
        tab_frame.pack(fill="x", padx=40)
        content_frame = tk.Frame(body_inner, bg=L)
        content_frame.pack(fill="both", expand=True, padx=16, pady=(4,8))
        _, content_inner = self.make_scrollable(content_frame, L)
        active_tab = [0]

        def render_tab():
            for w in content_inner.winfo_children():
                w.destroy()
            if active_tab[0] == 0:
                items = sorted([p for p in self.app.posts if p["username"] == user["username"]],
                               key=lambda x: x["id"], reverse=True)
                if not items:
                    tk.Label(content_inner, text="Belum ada postingan.",
                             font=("Segoe UI", 10), bg=L, fg=G).pack(pady=20)
                for p in items:
                    row = tk.Frame(content_inner, bg=W, pady=8, padx=10,
                                   highlightthickness=1, highlightbackground="#eee")
                    row.pack(fill="x", pady=3)
                    top_r = tk.Frame(row, bg=W)
                    top_r.pack(fill="x")
                    tk.Label(top_r, text=p["ts"] + (" ✏️ diedit" if p.get("edited") else ""),
                             font=("Segoe UI", 8), bg=W, fg=G).pack(side="left")
                    tk.Label(top_r, text=f"❤️{len(p['likes'])} 💬{len(p.get('comments',[]))}",
                             font=("Segoe UI", 8), bg=W, fg=G).pack(side="right")
                    tk.Label(row, text=p["text"], font=("Segoe UI", 10),
                             bg=W, fg=DG, wraplength=380, justify="left").pack(anchor="w", pady=(4,2))

                    def make_edit_p(pp=p):
                        def do():
                            def on_save(new_text):
                                self.app.edit_post(pp, new_text, user["username"])
                                if refresh_feed_fn:
                                    refresh_feed_fn()
                                render_tab()
                            self.open_edit_dialog("Edit Postingan", pp["text"], on_save)
                        return do

                    def make_del_p(pp=p):
                        def do():
                            if messagebox.askyesno("Hapus Post", "Hapus postingan ini?"):
                                self.app.delete_post(pp["id"])
                                if refresh_feed_fn:
                                    refresh_feed_fn()
                                render_tab()
                        return do

                    act_r = tk.Frame(row, bg=W)
                    act_r.pack(anchor="e")
                    tk.Button(act_r, text="✏️ Edit", bg=L, fg=DG, font=("Segoe UI", 8),
                              bd=0, padx=4, command=make_edit_p()).pack(side="left")
                    tk.Button(act_r, text="🗑 Hapus", bg="tomato", fg="white",
                              font=("Segoe UI", 8), bd=0, padx=4,
                              command=make_del_p()).pack(side="left", padx=(4,0))
            else:
                items = sorted([s for s in self.app.stories if s["username"] == user["username"]],
                               key=lambda x: x["id"], reverse=True)
                if not items:
                    tk.Label(content_inner, text="Belum ada story.",
                             font=("Segoe UI", 10), bg=L, fg=G).pack(pady=20)
                for s in items:
                    row = tk.Frame(content_inner, bg=W, pady=8, padx=10,
                                   highlightthickness=1, highlightbackground="#eee")
                    row.pack(fill="x", pady=3)
                    tk.Label(row, text=s["ts"], font=("Segoe UI", 8), bg=W, fg=G).pack(anchor="w")
                    tk.Label(row, text=s["text"], font=("Segoe UI", 10),
                             bg=W, fg=DG, wraplength=380, justify="left").pack(anchor="w", pady=(4,2))

                    def make_del_s(ss=s):
                        def do():
                            if messagebox.askyesno("Hapus Story", "Hapus story ini?"):
                                self.app.delete_story(ss["id"])
                                render_tab()
                        return do

                    tk.Button(row, text="🗑 Hapus", bg="tomato", fg="white",
                              font=("Segoe UI", 8), bd=0, padx=4,
                              command=make_del_s()).pack(anchor="e")

        def switch_tab(idx, btn_post, btn_story):
            active_tab[0] = idx
            btn_post.config(bg=P if idx==0 else W, relief="flat" if idx==0 else "groove")
            btn_story.config(bg=P if idx==1 else W, relief="flat" if idx==1 else "groove")
            render_tab()

        btn_post  = tk.Button(tab_frame, text="📝 Postingan", font=("Segoe UI", 9),
                              bg=P, bd=0, relief="flat", padx=10, pady=4, cursor="hand2")
        btn_story = tk.Button(tab_frame, text="📖 Story", font=("Segoe UI", 9),
                              bg=W, bd=1, relief="groove", padx=10, pady=4, cursor="hand2")
        btn_post.pack(side="left", padx=(0,4))
        btn_story.pack(side="left")
        btn_post.config( command=lambda: switch_tab(0, btn_post, btn_story))
        btn_story.config(command=lambda: switch_tab(1, btn_post, btn_story))
        render_tab()

    def _open_edit_profile(self, user, profile_page, refresh_feed_fn=None):
        P, W = self.PINK, self.WHITE
        win = tk.Toplevel(self.root)
        win.title("Edit Profil")
        win.geometry("360x420")
        win.config(bg=W)
        tk.Label(win, text="Edit Profil", font=("Segoe UI", 14, "bold"), bg=W).pack(pady=14)

        fields = {}
        for label, key in [("Nama Lengkap","fullname"),("Username","username"),
                            ("Email","email"),("Bio","bio")]:
            tk.Label(win, text=label, bg=W, font=("Segoe UI", 9)).pack(anchor="w", padx=20)
            e = tk.Entry(win, width=38, font=("Segoe UI", 10))
            e.insert(0, user.get(key, ""))
            e.pack(padx=20, pady=(2,8))
            fields[key] = e

        tk.Label(win, text="Password Baru (kosongkan jika tidak diubah)",
                 bg=W, font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        pwd_entry = tk.Entry(win, width=38, show="*", font=("Segoe UI", 10))
        pwd_entry.pack(padx=20, pady=(2,12))

        def save():
            new_username = fields["username"].get().strip()
            old_username = user["username"]
            new_pwd = pwd_entry.get().strip() or None
            ok, err = self.app.update_user(
                old_username,
                fullname=fields["fullname"].get().strip(),
                email=fields["email"].get().strip(),
                bio=fields["bio"].get().strip(),
                new_username=new_username if new_username != old_username else None,
                new_password=new_pwd,
            )
            if not ok:
                messagebox.showerror("Error", err, parent=win); return
            # Update local reference
            user["fullname"] = fields["fullname"].get().strip()
            user["email"]    = fields["email"].get().strip()
            user["bio"]      = fields["bio"].get().strip()
            if new_username != old_username:
                user["username"] = new_username
            win.destroy()
            self._render_profile(profile_page, user, refresh_feed_fn)
            messagebox.showinfo("Sukses", "Profil berhasil diperbarui!")

        tk.Button(win, text="Simpan", bg=P, font=("Segoe UI", 10, "bold"),
                  bd=0, padx=14, pady=6, command=save).pack()

    def _open_social_connect(self, viewer):
        P, W, L, G, DG = self.PINK, self.WHITE, self.LIGHT, self.GRAY, self.DGRAY
        win = tk.Toplevel(self.root)
        win.title("Social Connect")
        win.geometry("480x460")
        win.config(bg=L)
        tk.Label(win, text="Social Connect", font=("Segoe UI", 13, "bold"),
                 bg=L, fg=DG).pack(pady=12)
        lf = tk.Frame(win, bg=L)
        lf.pack(fill="both", expand=True, padx=16)
        _, inner = self.make_scrollable(lf, L)

        def refresh():
            for w in inner.winfo_children():
                w.destroy()
            other_users = [u for uname, u in self.app.users.items()
                           if uname != viewer["username"]]
            if not other_users:
                tk.Label(inner, text="Belum ada pengguna lain.",
                         font=("Segoe UI", 10), bg=L, fg=G).pack(pady=20)
                return
            for u in other_users:
                row = tk.Frame(inner, bg=W, pady=8, padx=10,
                               highlightthickness=1, highlightbackground="#eee")
                row.pack(fill="x", pady=3)
                initials = "".join(x[0].upper() for x in u["fullname"].split()[:2])
                left = tk.Frame(row, bg=W)
                left.pack(side="left", fill="x", expand=True)
                tk.Label(left, text=initials, font=("Segoe UI", 10, "bold"),
                         bg=P, fg=DG, width=3).pack(side="left")
                info = tk.Frame(left, bg=W)
                info.pack(side="left", padx=8)
                tk.Label(info, text=u["fullname"], font=("Segoe UI", 10, "bold"),
                         bg=W, fg=DG).pack(anchor="w")
                tk.Label(info, text=f"@{u['username']}  •  {u.get('role','User')}",
                         font=("Segoe UI", 8), bg=W, fg=G).pack(anchor="w")
                u_posts = len([p for p in self.app.posts if p["username"] == u["username"]])
                u_flwrs = sum(1 for f in self.app.follows.values() if u["username"] in f)
                tk.Label(info, text=f"📝 {u_posts} post  •  👥 {u_flwrs} followers",
                         font=("Segoe UI", 8), bg=W, fg=G).pack(anchor="w")
                is_flw   = self.app.is_following(viewer["username"], u["username"])
                btn_text = "✓ Following" if is_flw else "+ Follow"
                btn_bg   = "#d0f0d0" if is_flw else P

                def make_follow_toggle(target_uname=u["username"]):
                    def do():
                        self.app.toggle_follow(viewer["username"], target_uname)
                        refresh()
                    return do

                tk.Button(row, text=btn_text, font=("Segoe UI", 8, "bold"),
                          bg=btn_bg, fg=DG, bd=0, padx=8, pady=4,
                          cursor="hand2", command=make_follow_toggle()).pack(side="right")
        refresh()
