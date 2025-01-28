import os
from github import Github
from datetime import datetime
import platform
import subprocess  # Für Druckbefehle auf Unix/macOS

# GitHub Setup
token = os.getenv("GITHUB_TOKEN")
repo_name = "lulugrosche/post"  # Dein GitHub-Repository
g = Github(token)
repo = g.get_repo(repo_name)

# Feste Überschrift und Bild
DEFAULT_TITLE = "Community Memory Garden"
DEFAULT_IMAGE_PATH = "computer.jpeg"

def add_post(text):
    # Aktuelle Datei holen
    file = repo.get_contents("index.html")
    content = file.decoded_content.decode()
    
    # Neuen Post erstellen
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    new_post = f'''
    <div class="post">
        <h2>{DEFAULT_TITLE}</h2>
        <div class="image-container">
            <img src="{DEFAULT_IMAGE_PATH}" alt="Beispielbild">
        </div>
        <hr>
        <div class="timestamp">{timestamp}</div>
        <hr>
        <div class="content">{text}</div>
    </div>'''
    
    # Post einfügen (nach der posts div)
    new_content = content.replace('<div id="posts">', '<div id="posts">\n        ' + new_post)
    
    # Datei aktualisieren
    repo.update_file(
        file.path,
        f"Neuer Post: {timestamp}",
        new_content,
        file.sha
    )
    
    # Den Post-Inhalt drucken
    print_post(text, timestamp)

def print_post(text, timestamp):
    # Inhalt für den Druck formatieren
    formatted_text = f"Post erstellt am: {timestamp}\n\nTitel: {DEFAULT_TITLE}\n\n{text}"
    
    if platform.system() == "Windows":
        # Drucken unter Windows
        import win32print
        import win32ui
        printer = win32print.GetDefaultPrinter()
        hprinter = win32ui.CreateDC()
        hprinter.CreatePrinterDC(printer)
        hprinter.StartDoc("Neuer Post")
        hprinter.StartPage()
        hprinter.TextOut(100, 100, formatted_text)  # Position und Text
        hprinter.EndPage()
        hprinter.EndDoc()
        hprinter.DeleteDC()
        print("✓ Post wurde gedruckt!")
    else:
        # Drucken unter macOS/Linux (verwende lpr oder lp)
        try:
            process = subprocess.run(
                ["lpr"], input=formatted_text.encode(), text=False, check=True
            )
            print("✓ Post wurde gedruckt!")
        except Exception as e:
            print(f"Fehler beim Drucken: {e}")

def main():
    print("Post-Eingabe (Strg+C zum Beenden)")
    while True:
        try:
            # Eingabe des Textinhalts
            text = input("\nInhalt des Posts: ").strip()
            
            # Validierung der Eingabe
            if text:
                add_post(text)
                print("✓ Post wurde gesendet!")
            else:
                print("Der Inhalt des Posts darf nicht leer sein!")
        except KeyboardInterrupt:
            print("\nProgramm beendet.")
            break
        except Exception as e:
            print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
