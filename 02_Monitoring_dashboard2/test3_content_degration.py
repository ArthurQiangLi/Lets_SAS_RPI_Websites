import shutil
import logging

CURRENT_HTML = "/var/www/html/index.html"
HIGH_LOAD_HTML = "/var/www/html/high_load.html"
NORMAL_CONTENT_HTML = "/var/www/html/normal_content.html"

def switch_content(degrade=False):
    try:
        # Determine the target content
        # print(degrade)
        target_content_path = HIGH_LOAD_HTML if degrade else NORMAL_CONTENT_HTML

        # Read the contents of CURRENT_HTML
        with open(CURRENT_HTML, 'r') as current_file:
            current_content = current_file.read()

        # Read the contents of the target content
        with open(target_content_path, 'r') as target_file:
            target_content = target_file.read()

        # Check if the contents are the same
        if current_content == target_content:
            logging.info("Content already matches the target. No changes made.")
            print("[INFO] Content already matches the target. No changes made.")
            return

        # Switch the content by copying the target file to CURRENT_HTML
        shutil.copyfile(target_content_path, CURRENT_HTML)
        # os.utime(CURRENT_HTML, None)
        # subprocess.run(["curl", "http://localhost"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info(f"Content switched to {'high_load.html' if degrade else 'normal_content.html'}")
        print(f"[INFO] Content switched to {'high_load.html' if degrade else 'normal_content.html'}")
    except Exception as e:
        logging.error(f"Error switching content: {e}")
        print(f"[ERROR] Error switching content: {e}")