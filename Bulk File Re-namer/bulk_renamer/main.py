import os
import json

UNDO_LOG_FILE = "undo_log.json"


def save_undo_log(log):
    with open(UNDO_LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)


def load_undo_log():
    if not os.path.exists(UNDO_LOG_FILE):
        return None
    with open(UNDO_LOG_FILE, "r") as f:
        return json.load(f)


def delete_undo_log():
    if os.path.exists(UNDO_LOG_FILE):
        os.remove(UNDO_LOG_FILE)


def bulk_rename(folder_path, new_name, extension_filter=None):
    try:
        files = os.listdir(folder_path)
        files = [
            f for f in files if os.path.isfile(os.path.join(folder_path, f))
        ]  # Only files

        if extension_filter:
            files = [f for f in files if f.lower().endswith(extension_filter.lower())]

        files.sort()  # Sort for consistency

        if not files:
            print("\n⚠️ No files to rename with the given filter.")
            return

        count = 1
        undo_log = []

        for filename in files:
            old_path = os.path.join(folder_path, filename)
            _, ext = os.path.splitext(filename)

            if len(files) == 1:
                new_filename = f"{new_name}{ext}"
            else:
                new_filename = f"{new_name}_{count}{ext}"

            new_path = os.path.join(folder_path, new_filename)

            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                undo_log.append({"old": filename, "new": new_filename})
                count += 1

        save_undo_log({"folder": folder_path, "changes": undo_log})
        print("\n✅ Renaming completed. You can undo this operation.")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def undo_last_rename():
    undo_data = load_undo_log()
    if not undo_data:
        print("\n⚠️ No undo log found.")
        return

    folder_path = undo_data["folder"]
    for change in undo_data["changes"]:
        new_path = os.path.join(folder_path, change["new"])
        old_path = os.path.join(folder_path, change["old"])

        if os.path.exists(new_path):
            os.rename(new_path, old_path)
            print(f"Reverted: {change['new']} -> {change['old']}")
        else:
            print(f"⚠️ File not found for undo: {change['new']}")

    delete_undo_log()
    print("\n✅ Undo completed.")


if __name__ == "__main__":
    print("=== Bulk File Renamer ===\n")
    choice = (
        input("Do you want to (R)ename files or (U)ndo last rename? ").strip().lower()
    )

    if choice == "r":
        folder = input("Enter folder path: ").strip()
        name = input("Enter new base name: ").strip()
        ext_filter = input(
            "Enter extension to filter (e.g., .jpg), or leave blank: "
        ).strip()

        if not os.path.isdir(folder):
            print("\n❌ Invalid folder path. Please try again.")
        else:
            ext_filter = ext_filter if ext_filter else None
            bulk_rename(folder, name, ext_filter)

    elif choice == "u":
        undo_last_rename()

    else:
        print("\n❌ Invalid choice. Please enter 'R' or 'U'.")
