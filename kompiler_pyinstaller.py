from subprocess import run, CalledProcessError
from platform import system
from colorama import Fore, Back
from os import environ
from modul import bersihkan_layar
from tkinter.filedialog import askopenfilename as pilih_file, askdirectory as pilih_folder
from tkinter.messagebox import askyesno

if system() in ("Windows", "Darwin"):
    error : bool = False
    bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi pyinstaller{Fore.RESET}")
    try:
        run("pyinstaller --version", shell = False, check = True)
    except CalledProcessError:
        error = True
        print(f"{Fore.LIGHTRED_EX}Perintah pyinstaller tidak ditemukan!{Fore.RESET}")
        if system() == "Windows":
            PERINTAH_INSTALASI = "pip install pyinstaller"
            print(f"{Fore.YELLOW}Menjalankan perintah instalasi pyinstaller {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH_INSTALASI}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(PERINTAH_INSTALASI, shell = False, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Instalasi pyinstaller gagal!{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Instalasi pyinstaller dihentikan!{Fore.RESET}")
            else:
                error = False
                print(F"{Fore.LIGHTGREEN_EX}Instalasi pyinstaller selesai{Fore.RESET}")
    if not error:
        print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
        try:
            file_python = pilih_file(title = "*Pilih file Python untuk dikompilasi", defaultextension = ".py", filetypes = [("Kode sumber Python", "*.py")])
            if file_python:
                direktori_dist_dan_spec = pilih_folder(title = "*Pilih lokasi folder dist dan spec")
                if direktori_dist_dan_spec:
                    if system() == "Windows":
                        for kategori in environ:
                            match kategori:
                                case "TEMP" | "TMP":
                                    direktori_sementara = environ[kategori]
                                    break
                        else:
                            direktori_sementara = pilih_folder(title = "*Pilih file sementara (temporary)").replace("/", "\\")
                    else:
                        direktori_sementara = pilih_folder(title = "*Pilih file sementara (temporary)")
                    if direktori_sementara:
                        if system() == "Windows":
                            file_python = file_python.replace("/", "\\")
                            direktori_dist_dan_spec = direktori_dist_dan_spec.replace("/", "\\")
                            direktori_sementara = direktori_sementara.replace("/", "\\")
                        perintah = f"pyinstaller --distpath \"{direktori_dist_dan_spec}\" --specpath \"{direktori_dist_dan_spec}\" --workpath \"{direktori_sementara}\" --clean "
                        if askyesno("Konfirmasi", "Buat dalam satu file?"):
                            perintah += "--onefile "
                        else:
                            perintah += "--onedir "
                        while True:
                            print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                            direktori_import = pilih_folder(title = "Pilih direktori import Python [Opsional]")
                            if direktori_import:
                                if system() == "Windows":
                                    direktori_import = direktori_import.replace("/", "\\")
                                print(f"{Fore.LIGHTGREEN_EX}{direktori_import}{Fore.RESET}")
                                perintah += f"--paths \"{direktori_import} "
                            else:
                                break
                        if system() in ["Windows", "Darwin"]:
                            if askyesno(title = "Pilih Mode Jendela atau Konsol", message = "Ya untuk mode jendela\nTidak untuk mode konsol"):
                                perintah += "--windowed "
                            else:
                                perintah += "--console "
                            while True:
                                print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                                file_ikon = pilih_file(title = "Pilih file ikon [Opsional]", filetypes = [("File Ikon", "*.ico *.icns"), ("File Executable Windows", "*.exe"), ("Semua File", "*.*")])
                                if file_ikon:
                                    if system() == "Windows":
                                        file_ikon = file_ikon.replace("/", "\\")
                                    print(f"{Fore.LIGHTGREEN_EX}{file_ikon}{Fore.RESET}")
                                    perintah += f"--icon \"{file_ikon}\" "
                                else:
                                    break
                            if askyesno(title = "disable windowed traceback", message = "Nonaktifkan traceback dump dari error yang tidak ditangani dalam mode jendela"):
                                perintah += "--disable-windowed-traceback "
                            if system() == "Windows":
                                print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                                FILE_VERSI = pilih_file(title = "Pilih file versi untuk disertakan ke executable [Opsional]", filetypes = [("Semua File", "*.*")]).replace("/", "\\")
                                if FILE_VERSI:
                                    perintah += f"--version-file \"{FILE_VERSI}\" "
                                FILE_MANIFEST = pilih_file(title = "Pilih file manifest untuk disertakan ke executable [Opsional]", filetypes = [("Extensible Markup Language", "*.xml"), ("Semua File", "*.*")]).replace("/", "\\")
                                if FILE_MANIFEST:
                                    perintah += f"--manifest \"{FILE_MANIFEST}\""
                                while True:
                                    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                                    FILE_SUMBER_DAYA = pilih_file(title = "Pilih file sumber daya DLL atau exe untuk disertakan ke executable [Opsional]", filetypes = [("Dynamic Link Library", "*.dll"), ("File Executable Windows", "*.exe")]).replace("/", "\\")
                                    if FILE_SUMBER_DAYA:
                                        print(f"{Fore.LIGHTGREEN_EX}{FILE_SUMBER_DAYA}{Fore.RESET}")
                                        perintah += f"--resource \"{FILE_SUMBER_DAYA}\" * * * "
                                    else:
                                        break
                                if askyesno(title = "Mode Administratif", message = "Output executable memerlukan hak akses administrator?"):
                                    perintah += "--uac-admin "
                                if askyesno(title = "Mode Administratif", message = "Output executable memerlukan hak akses administrator yang berfungsi untuk Remote Desktop?"):
                                    perintah += "--uac-uiaccess "
                            elif system() == "Darwin":
                                if askyesno(title = "Aktifkan emulasi argv?", message = "Jika diaktifkan, peristiwa dokumen/URL awal yang terbuka diproses oleh bootloader dan jalur file atau URL yang diteruskan ditambahkan ke sys.argv."):
                                    perintah += "--argv-emulation "
                        perintah += f"\"{file_python}\""
                        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                        try:
                            run(perintah, shell = False, check = True)
                        except CalledProcessError:
                            print(f"{Fore.LIGHTRED_EX}Kompilasi Gagal!{Fore.RESET}")
                        except KeyboardInterrupt:
                            print(f"{Fore.LIGHTRED_EX}Kompilasi Dihentikan!{Fore.RESET}")
                        else:
                            print(f"{Fore.LIGHTGREEN_EX}Kompilasi Berhasil!{Fore.RESET}")
                    else:
                        print(f"{Fore.LIGHTRED_EX}Direktori file sementara tidak dipilih!{Fore.RESET}")
        except KeyboardInterrupt:
            print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C\nProgram ditutup!{Fore.RESET}")