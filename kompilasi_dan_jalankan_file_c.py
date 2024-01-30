from subprocess import run, CalledProcessError
from platform import system
from colorama import Fore, Back
from tkinter.filedialog import askopenfilename as pilih_file, askdirectory as pilih_folder
from os.path import exists
from os import remove
from modul import bersihkan_layar

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi GCC ...{Fore.RESET}")
try:
    run("gcc --version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah GCC tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    file_input = pilih_file(title = "Pilih file .c", defaultextension = ".c", filetypes = [("Kode Sumber C", "*.c")])
    if file_input:
        tambahan_perintah_include = ""
        while True:
            folder_include = pilih_folder(title = "Tambahkan folder include")
            if folder_include:
                if system() == "Windows":
                    folder_include = folder_include.replace("/", "\\")
                tambahan_perintah_include += f"-I \"{folder_include}\" "
            else:
                break
        if system() == "Windows":
            EKSTENSI_OUTPUT = ".exe"
        else:
            EKSTENSI_OUTPUT = ".bin"
        DIREKTORI_FOLDER = "/".join(file_input.split("/")[:-1])
        NAMA_FILE_OUTPUT = ".".join(file_input.split("/")[-1].split(".")[:-1]) + EKSTENSI_OUTPUT
        file_output = f"{DIREKTORI_FOLDER}/{NAMA_FILE_OUTPUT}"
        if system() == "Windows":
            file_input = file_input.replace("/", "\\")
            file_output = file_output.replace("/", "\\")
        if tambahan_perintah_include != "":
            PERINTAH_KOMPILASI = f"gcc -fdiagnostics-color=always {tambahan_perintah_include.strip()} -o \"{file_output}\" \"{file_input}\""
        else:
            PERINTAH_KOMPILASI = f"gcc -fdiagnostics-color=always -o \"{file_output}\" \"{file_input}\""
        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH_KOMPILASI}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
        try:
            run(PERINTAH_KOMPILASI, shell = True, check = True)
        except CalledProcessError:
            print(f"{Fore.LIGHTRED_EX}Kompilasi Gagal!{Fore.RESET}")
            if exists(file_output):
                remove(file_output)
        else:
            print(f"{Fore.LIGHTGREEN_EX}Kompilasi Berhasil!{Fore.RESET}")
            if system() == "Windows":
                print(f"{Fore.YELLOW}Menjalankan {Fore.LIGHTYELLOW_EX}{Back.BLUE}\"{file_output}\"{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                run(f"\"{file_output}\"", shell = True, check = True)
    else:
        print(f"{Fore.LIGHTRED_EX}File .c tidak dipilih!{Fore.RESET}")