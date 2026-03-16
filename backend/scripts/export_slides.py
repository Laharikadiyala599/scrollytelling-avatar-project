from pathlib import Path
import win32com.client

BASE_DIR = Path(__file__).resolve().parent.parent
PPTX_PATH = BASE_DIR / "input" / "sample_report.pptx"
OUTPUT_DIR = BASE_DIR / "output" / "slides"

def main():
    if not PPTX_PATH.exists():
        print(f"PowerPoint file not found: {PPTX_PATH}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1

    presentation = None

    try:
        presentation = powerpoint.Presentations.Open(str(PPTX_PATH))
        presentation.Export(str(OUTPUT_DIR), "PNG")
        print(f"Slides exported successfully to: {OUTPUT_DIR}")
    except Exception as e:
        print("Error exporting slides:")
        print(e)
    finally:
        if presentation is not None:
            presentation.Close()
        powerpoint.Quit()

if __name__ == "__main__":
    main()