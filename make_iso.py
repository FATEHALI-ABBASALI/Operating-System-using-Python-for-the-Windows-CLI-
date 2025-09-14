import os
import subprocess
import shutil

FWOS_FILE = "fwos.py"
ISO_NAME = "fwos.iso"
WORK_DIR = "fwos_build"

def run(cmd):
    print(f"[*] {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    # Clean old build
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR, exist_ok=True)

    # 1. Download Alpine Linux minirootfs
    if not os.path.exists("alpine-minirootfs.tar.gz"):
        run("wget -O alpine-minirootfs.tar.gz "
            "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-latest-x86_64.tar.gz")

    # 2. Extract rootfs
    run(f"mkdir -p {WORK_DIR}/rootfs")
    run(f"sudo tar -xzf alpine-minirootfs.tar.gz -C {WORK_DIR}/rootfs")

    # 3. Copy FWOS script
    run(f"cp {FWOS_FILE} {WORK_DIR}/rootfs/root/fwos.py")

    # 4. Install python3 and autostart fwos
    run(f"sudo chroot {WORK_DIR}/rootfs /bin/sh -c \"apk add --no-cache python3 && "
        f"echo 'python3 /root/fwos.py' >> /etc/profile\"")

    # 5. Prepare ISO directory
    iso_dir = f"{WORK_DIR}/iso"
    os.makedirs(f"{iso_dir}/boot/grub", exist_ok=True)

    # Copy kernel & initrd
    run(f"cp {WORK_DIR}/rootfs/boot/vmlinuz-* {iso_dir}/boot/vmlinuz")
    run(f"cp {WORK_DIR}/rootfs/boot/initramfs-* {iso_dir}/boot/initrd")

    # 6. Write GRUB config
    grub_cfg = f"""\
set default=0
set timeout=3

menuentry "Fam Word OS (FWOS)" {{
    linux /boot/vmlinuz
    initrd /boot/initrd
}}
"""
    with open(f"{iso_dir}/boot/grub/grub.cfg", "w") as f:
        f.write(grub_cfg)

    # 7. Build ISO with grub-mkrescue
    run(f"grub-mkrescue -o {ISO_NAME} {iso_dir}")

    print(f"\n✅ Done! ISO created: {ISO_NAME}\n")
    print("👉 You can now run it in VirtualBox.")

if __name__ == "__main__":
    main()
