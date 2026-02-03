import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    # App Page Settings
    page.title = "Universal Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # UI Components
    url_input = ft.TextField(
        label="Video URL",
        hint_text="Paste link from YouTube, TikTok, IG, etc.",
        border_radius=15,
        prefix_icon=ft.icons.LINK,
        expand=True
    )
    
    status_label = ft.Text("Ready", color="grey", text_align="center")
    progress_bar = ft.ProgressBar(width=400, color="blue", visible=False)
    
    # Function to grab text from clipboard automatically
    def paste_link(e):
        # On Android, this grabs whatever you just copied
        url_input.value = page.get_clipboard()
        page.update()

    def download_video(e):
        if not url_input.value:
            status_label.value = "❌ Error: Please paste a link!"
            status_label.color = "red"
            page.update()
            return

        # Start UI feedback
        status_label.value = "⏳ Analyzing video... please wait"
        status_label.color = "blue"
        progress_bar.visible = True
        page.update()

        # Android Download Path (Universal Downloads Folder)
        save_path = "/storage/emulated/0/Download/%(title)s.%(ext)s"

        # Universal Downloader Engine Settings
        ydl_opts = {
            'format': 'best', # Best quality single file (prevents crash on slow phones)
            'outtmpl': save_path,
            'noplaylist': True,
            'ignoreerrors': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])
            
            status_label.value = "✅ Success! Saved to 'Downloads' folder."
            status_label.color = "green"
            url_input.value = "" 
        except Exception as ex:
            status_label.value = f"❌ Error: {str(ex)}"
            status_label.color = "red"
        
        progress_bar.visible = False
        page.update()

    # Layout
    page.add(
        ft.Icon(name=ft.icons.DOWNLOAD_FOR_OFFLINE, size=100, color="blue"),
        ft.Text("Universal Downloader", size=32, weight="bold"),
        ft.Text("Supports 1000+ Sites", color="grey700"),
        
        # Row with Input and Paste Button
        ft.Row([
            url_input,
            ft.IconButton(
                icon=ft.icons.CONTENT_PASTE, 
                on_click=paste_link, 
                tooltip="Paste from clipboard"
            )
        ]),
        
        # Download Button
        ft.ElevatedButton(
            "Download Now",
            icon=ft.icons.GET_APP,
            on_click=download_video,
            style=ft.ButtonStyle(
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=250
        ),
        
        progress_bar,
        status_label,
        
        ft.Divider(height=20, color="transparent"),
        ft.Text("Tip: Make sure you have a stable internet connection.", size=12, color="grey")
    )

# Run the app
ft.app(target=main)