import os
import colorama
from colorama import Fore, Style
import subprocess

# Renk tanımlamaları
success_color = Fore.GREEN
error_color = Fore.RED
info_color = Fore.YELLOW
reset_color = Style.RESET_ALL

bash_script = "./bash.sh"

# Bash betiği yüklü mü kontrol et
if not os.path.exists(bash_script):
    try:
        install_command = f"chmod +x {bash_script} && ./{bash_script}"
        result = subprocess.run(install_command, shell=True, check=True, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        print("Çıkış kodu:", result.returncode)
        print("Çıkış:")
        print(result.stdout)
        print("Hata:")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("Hata oluştu:", e)
else:
    print("bash.sh dosyası zaten mevcut. İşlem devam ediyor.")

# Taranacak adreslerin listesini giriniz
print(info_color + "Taranacak adreslerin listesini giriniz" + reset_color)
dosya_yolu = input("Dosya yolunu girin (örn: /root/Desktop/Serenity/sy-ub.txt): ")

if not os.path.exists(dosya_yolu):
    print(error_color + f"{dosya_yolu} bulunamadı!" + reset_color)
    exit()

with open(dosya_yolu, 'r') as f:
    domainler = [line.strip() for line in f if line.strip()]

for domain in domainler:
    print(info_color + f"\n==> {domain} için işlemler başlatılıyor..." + reset_color)

    klasor = f"/root/Desktop/Serenity/{domain}"
    os.makedirs(klasor, exist_ok=True)

    subfinder_output = f"{klasor}/subdomain.txt"
    httpx_output = f"{klasor}/httpx.txt"
    nuclei_output = f"{klasor}/nuclei.txt"

    # Subfinder
    komut1 = f"cd /root/go/bin && ./subfinder -d {domain} >> {subfinder_output}"
    if os.system(komut1) == 0:
        print(success_color + f"Subfinder başarılı: {subfinder_output}" + reset_color)
    else:
        print(error_color + f"Subfinder hata verdi." + reset_color)

    # httpx
    komut2 = f"cd /root/go/bin && cat '{subfinder_output}' | ./httpx >> {httpx_output}"
    if os.system(komut2) == 0:
        print(success_color + f"httpx başarılı: {httpx_output}" + reset_color)
    else:
        print(error_color + f"httpx hata verdi." + reset_color)

    # nuclei
    komut3 = f"cd /root/go/bin && ./nuclei -l '{httpx_output}' -o '{nuclei_output}'"
    if os.system(komut3) == 0:
        print(success_color + f"nuclei başarılı: {nuclei_output}" + reset_color)
    else:
        print(error_color + f"nuclei hata verdi." + reset_color)

    # CVE ve Seviyeler
    print("------ CVE BULGULARI ------")
    os.system(f"awk '/CVE-[0-9]{{4}}-[0-9]{{4,8}}/' {nuclei_output}")

    print("------ LOW BULGULARI ------")
    os.system(rf"awk '/\[low\]/' {nuclei_output}")

    print("------ MEDIUM BULGULARI ------")
    os.system(rf"awk '/\[medium\]/' {nuclei_output}")

    print("------ HIGH BULGULARI ------")
    os.system(rf"awk '/\[high\]/' {nuclei_output}")

    print("------ CRITICAL BULGULARI ------")
    os.system(rf"awk '/\[critical\]/' {nuclei_output}")

    print("------ UNKNOWN BULGULARI ------")
    os.system(rf"awk '/\[unknown\]/' {nuclei_output}")

# Ses dosyasını çalmak için kullanılacak fonksiyon
def play_audio():
    subprocess.run(["mpv", "--loop", "fbı.mp3"])

try:
    play_audio()
except KeyboardInterrupt:
    print("Ctrl+C tuş kombinasyonu algılandı. Çıkılıyor...")
