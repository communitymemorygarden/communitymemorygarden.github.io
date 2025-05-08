import os
from github import Github
from datetime import datetime
import platform
import subprocess  # Für Druckbefehle auf Unix/macOS/Linux

# GitHub Setup
token = os.getenv("GITHUB_TOKEN")
repo_name = "communitymemorygarden/communitymemorygarden.github.io"  # Dein GitHub-Repository
g = Github(token)
repo = g.get_repo(repo_name)

# Feste Überschrift und Bild
DEFAULT_TITLE = "Community Memory Garden"
DEFAULT_IMAGE_PATH = "IMG_0831.jpeg"

def format_for_58mm(text):
    # Maximale Zeichen pro Zeile (58mm Drucker, ca. 32 Zeichen je nach Schriftart)
    max_chars = 32
    lines = []
    for line in text.splitlines():
        while len(line) > max_chars:
            lines.append(line[:max_chars])
            line = line[max_chars:]
        lines.append(line)
    return "\n".join(lines)

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
    formatted_text = format_for_58mm(formatted_text)

    if platform.system() in ["Linux", "Darwin"]:  # Für Raspberry Pi (Linux/macOS)
        try:
            # Verwende `lpr`, das auf dem Raspberry Pi verfügbar ist
            process = subprocess.run(
                ["lpr"], input=formatted_text.encode(), text=False, check=True
            )
            print("\u2713 Post wurde gedruckt!")
        except Exception as e:
            print(f"Fehler beim Drucken: {e}")
    else:
        print("Druckfunktion ist nur unter Linux/macOS verfügbar.")

def main():
    print("Post-Eingabe (Strg+C zum Beenden)")
    while True:
        try:
            # Eingabe des Textinhalts
            text = input("\nInhalt des Posts: ").strip()

            # Validierung der Eingabe
            if text:
                add_post(text)
                print("\u2713 Post wurde gesendet!")
            else:
                print("Der Inhalt des Posts darf nicht leer sein!")
        except KeyboardInterrupt:
            print("\nProgramm beendet.")
            break
        except Exception as e:
            print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
