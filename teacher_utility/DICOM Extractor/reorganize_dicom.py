import os
import shutil
import pydicom

def organize_dicom_by_patient_flat(input_root, output_root):
    """
    Traverse the input_root directory, read each DICOM file, extract the PatientID (or PatientName),
    and copy the file into a new directory structure organized by patient only.
    
    Parameters:
    - input_root: Path to the root of the current DICOM folder (e.g., "Root/DICOM").
    - output_root: Path to the root of the organized DICOM folder where files will be copied.
    """
    # Walk through all files under the input_root directory
    for dirpath, _, filenames in os.walk(input_root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Read the DICOM file (force=True to handle files without extension)
                ds = pydicom.dcmread(file_path, force=True)
            except Exception as e:
                print(f"Skipping non-DICOM or unreadable file: {file_path}. Error: {e}")
                continue

            # Extract PatientID or PatientName
            patient_id = getattr(ds, "PatientID", None) or str(getattr(ds, "PatientName", "UnknownPatient"))

            # Build the destination directory path - only by patient_id
            dest_dir = os.path.join(output_root, patient_id)
            os.makedirs(dest_dir, exist_ok=True)

            # Copy the file to the new location
            # If filenames collide, append an index to the new filename
            dest_path = os.path.join(dest_dir, filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                counter += 1
            
            shutil.copy2(file_path, dest_path)

    print("DICOM files have been organized by patient ID successfully.")


if __name__ == "__main__":
    # Modify these paths as needed
    input_root = r"C:/MS Course Mat/Comfort Data/Root Modified/DICOM"
    output_root = r"C:/MS Course Mat/Comfort Data/Root Modified/Organized DICOM"

    organize_dicom_by_patient(input_root, output_root)
