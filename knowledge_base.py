# knowledge_base.py

# Data Gejala yang Diperluas
gejala = {
    "G01": "Layar tidak menyala",
    "G02": "Komputer tidak bisa booting",
    "G03": "Kipas tidak berputar",
    "G04": "Muncul suara beep",
    "G05": "Harddisk tidak terdeteksi",
    "G06": "Lampu indikator mati",
    "G07": "Suara kipas berisik",
    "G08": "Layar berkedip atau bergaris",
    "G09": "Sistem sering hang",
    "G10": "Komputer restart sendiri",
    "G11": "Port USB tidak berfungsi",
    "G12": "Mouse dan keyboard tidak merespon",
    "G13": "Sistem lambat saat booting",
    "G14": "Tidak ada suara dari speaker",
    "G15": "Baterai laptop cepat habis",
    "G16": "Overheating (panas berlebihan)",
    "G17": "WiFi tidak terdeteksi",
    "G18": "Port charger tidak mengisi daya",
    "G19": "Blue screen muncul saat startup",
    "G20": "Tombol power tidak berfungsi",
    "G21": "Layar menampilkan 'No Signal'",
    "G22": "Komputer mati tiba-tiba",
    "G23": "DVD/CD ROM tidak terbaca",
    "G24": "Aplikasi sering not responding",
    "G25": "Jam bios reset ke default",
    "G26": "Kursor mouse bergerak sendiri",
    "G27": "Tidak bisa connect internet",
    "G28": "File corrupt tidak bisa dibuka",
    "G29": "Komputer lambat membuka program",
    "G30": "Muncul pesan error saat startup",
    "G31": "Monitor berwarna tidak normal",
    "G32": "Touchpad tidak berfungsi",
    "G33": "Bluetooth tidak bisa aktif",
    "G34": "Kamera laptop tidak aktif",
    "G35": "Komputer tidak bisa sleep/hibernate"
}

# Data Kerusakan yang Diperluas
kerusakan = {
    "K01": "Kerusakan Power Supply",
    "K02": "Kerusakan RAM",
    "K03": "Kerusakan Harddisk/SSD",
    "K04": "Kerusakan Motherboard",
    "K05": "Kerusakan VGA Card",
    "K06": "Kerusakan Sistem Operasi",
    "K07": "Kerusakan Baterai Laptop",
    "K08": "Kerusakan Keyboard/Mouse",
    "K09": "Kerusakan Pendingin/Kipas",
    "K10": "Kerusakan Charger/Port Charging",
    "K11": "Kerusakan Monitor/LCD",
    "K12": "Kerusakan Processor",
    "K13": "Kerusakan BIOS/CMOS",
    "K14": "Kerusakan Optical Drive",
    "K15": "Kerusakan Network Card",
    "K16": "Kerusakan Sound Card",
    "K17": "Kerusakan USB Port",
    "K18": "Kerusakan Software/Driver",
    "K19": "Kerusakan Touchpad",
    "K20": "Kerusakan Webcam"
}

# Rules dengan Certainty Factor dan Bobot
rules_cf = {
    "K01": [
        ("G01", 0.9, "critical"), 
        ("G06", 0.95, "critical"), 
        ("G20", 0.85, "high"),
        ("G22", 0.8, "high")
    ],
    "K02": [
        ("G02", 0.9, "critical"), 
        ("G04", 0.8, "high"), 
        ("G19", 0.85, "critical"), 
        ("G10", 0.7, "medium"),
        ("G25", 0.6, "medium")
    ],
    "K03": [
        ("G05", 0.95, "critical"), 
        ("G09", 0.8, "high"), 
        ("G13", 0.85, "high"),
        ("G28", 0.7, "medium"),
        ("G29", 0.6, "medium")
    ],
    "K04": [
        ("G03", 0.9, "critical"), 
        ("G07", 0.8, "high"), 
        ("G08", 0.85, "high"), 
        ("G16", 0.75, "medium"),
        ("G25", 0.7, "medium")
    ],
    "K05": [
        ("G08", 0.95, "critical"), 
        ("G14", 0.9, "high"), 
        ("G19", 0.85, "critical"),
        ("G31", 0.8, "high")
    ],
    "K06": [
        ("G09", 0.85, "high"), 
        ("G19", 0.9, "critical"), 
        ("G13", 0.8, "high"), 
        ("G10", 0.75, "medium"),
        ("G24", 0.7, "medium"),
        ("G30", 0.8, "high")
    ],
    "K07": [
        ("G15", 0.95, "critical"), 
        ("G18", 0.9, "critical"), 
        ("G20", 0.5, "low")
    ],
    "K08": [
        ("G11", 0.85, "high"), 
        ("G12", 0.9, "critical"),
        ("G26", 0.7, "medium"),
        ("G32", 0.8, "high")
    ],
    "K09": [
        ("G07", 0.95, "critical"), 
        ("G03", 0.85, "high"), 
        ("G16", 0.9, "critical"),
        ("G22", 0.8, "high")
    ],
    "K10": [
        ("G18", 0.95, "critical"), 
        ("G20", 0.6, "medium"),
        ("G15", 0.5, "low")
    ],
    "K11": [
        ("G01", 0.9, "critical"), 
        ("G21", 0.95, "critical"),
        ("G31", 0.85, "high")
    ],
    "K12": [
        ("G16", 0.95, "critical"), 
        ("G22", 0.9, "critical"),
        ("G02", 0.85, "high")
    ],
    "K13": [
        ("G25", 0.95, "critical"), 
        ("G02", 0.8, "high"),
        ("G30", 0.7, "medium")
    ],
    "K14": [
        ("G23", 0.95, "critical"), 
        ("G05", 0.6, "medium")
    ],
    "K15": [
        ("G17", 0.9, "critical"), 
        ("G27", 0.85, "high"),
        ("G11", 0.5, "low")
    ],
    "K16": [
        ("G14", 0.95, "critical"), 
        ("G24", 0.6, "medium")
    ],
    "K17": [
        ("G11", 0.9, "critical"), 
        ("G12", 0.7, "medium"),
        ("G33", 0.6, "medium")
    ],
    "K18": [
        ("G24", 0.85, "high"), 
        ("G30", 0.8, "high"),
        ("G28", 0.7, "medium"),
        ("G34", 0.6, "medium")
    ],
    "K19": [
        ("G32", 0.95, "critical"), 
        ("G12", 0.7, "medium")
    ],
    "K20": [
        ("G34", 0.95, "critical"), 
        ("G24", 0.5, "low")
    ]
}

# Data Solusi Perbaikan yang Diperluas
solusi = {
    "K01": [
        "Periksa kabel power apakah sudah terpasang dengan benar.",
        "Cek tegangan listrik rumah menggunakan stabilizer/UPS.",
        "Ganti Power Supply Unit (PSU) dengan yang baru jika kipas PSU tidak berputar.",
        "Bersihkan debu dari PSU untuk mencegah overheating."
    ],
    "K02": [
        "Lepas RAM, bersihkan pin kuningan dengan penghapus pensil, lalu pasang kembali.",
        "Coba pindahkan RAM ke slot yang berbeda.",
        "Jika menggunakan 2 keping RAM, coba pasang satu per satu untuk cek mana yang rusak.",
        "Update BIOS ke versi terbaru.",
        "Ganti RAM dengan yang baru jika masalah tetap ada."
    ],
    "K03": [
        "Cek kabel SATA/Power Harddisk apakah longgar.",
        "Lakukan Defrag atau Check Disk (chkdsk) melalui CMD.",
        "Segera backup data penting dan ganti Harddisk/SSD jika bunyi kasar terdengar.",
        "Cek health Harddisk menggunakan software CrystalDiskInfo.",
        "Update driver storage controller."
    ],
    "K04": [
        "Cek fisik motherboard apakah ada kapasitor yang kembung/pecah.",
        "Reset BIOS dengan cara melepas baterai CMOS selama 5 menit.",
        "Bersihkan motherboard dari debu secara berkala.",
        "Periksa apakah ada komponen yang kepanasan.",
        "Disarankan dibawa ke teknisi ahli untuk pengecekan jalur komponen."
    ],
    "K05": [
        "Update driver VGA ke versi terbaru.",
        "Bersihkan debu pada kipas VGA Card.",
        "Cek suhu VGA, pastikan sirkulasi udara casing lancar.",
        "Ganti thermal paste pada GPU jika overheating.",
        "Coba gunakan slot PCIe yang berbeda."
    ],
    "K06": [
        "Scan virus/malware menggunakan antivirus terupdate.",
        "Lakukan System Restore ke tanggal sebelum masalah muncul.",
        "Install ulang Windows jika kerusakan sistem terlalu parah.",
        "Update Windows ke versi terbaru.",
        "Lakukan cleanup disk untuk menghapus file temporary."
    ],
    "K07": [
        "Lakukan kalibrasi baterai (cas penuh, pakai sampai habis, cas lagi).",
        "Kurangi kecerahan layar dan matikan fitur yang tidak dipakai.",
        "Ganti baterai laptop dengan yang original.",
        "Periksa pengaturan power management.",
        "Update driver battery management."
    ],
    "K08": [
        "Cek port USB dengan mencolokkan device lain.",
        "Update driver USB/IO Controller.",
        "Bersihkan debu di sela-sela keyboard/mouse.",
        "Coba gunakan keyboard/mouse eksternal untuk testing.",
        "Ganti keyboard/mouse jika kerusakan fisik."
    ],
    "K09": [
        "Bersihkan debu pada heatsink dan kipas prosesor.",
        "Ganti thermal paste pada prosesor.",
        "Pastikan putaran kipas lancar, ganti jika macet.",
        "Tambahkan kipas casing tambahan jika perlu.",
        "Pastikan ventilasi udara tidak terblokir."
    ],
    "K10": [
        "Cek kabel charger apakah ada yang terkelupas.",
        "Coba gunakan charger lain yang kompatibel.",
        "Periksa port charging di laptop apakah goyang/longgar.",
        "Bersihkan port charging dari debu.",
        "Ganti port charging jika perlu."
    ],
    "K11": [
        "Periksa kabel VGA/HDMI apakah terpasang baik.",
        "Coba monitor dengan komputer lain untuk testing.",
        "Ganti kabel monitor jika ada kerusakan.",
        "Reset setting monitor ke factory default.",
        "Service monitor jika ada garis atau bayangan."
    ],
    "K12": [
        "Pastikan thermal paste processor masih baik.",
        "Cek suhu processor menggunakan monitoring software.",
        "Downclock processor jika overheating.",
        "Ganti processor jika sudah sangat tua.",
        "Pastikan clock speed sesuai spesifikasi."
    ],
    "K13": [
        "Reset BIOS ke setting default.",
        "Ganti baterai CMOS jika sudah habis.",
        "Update BIOS ke versi terbaru.",
        "Periksa jumper BIOS pada motherboard.",
        "Hindari update BIOS jika tidak perlu."
    ],
    "K14": [
        "Bersihkan lensa optical drive dengan cleaning kit.",
        "Coba DVD/CD yang berbeda untuk testing.",
        "Update driver optical drive.",
        "Ganti optical drive jika sudah tidak bisa membaca.",
        "Pertimbangkan upgrade ke external drive."
    ],
    "K15": [
        "Restart router/modem WiFi.",
        "Update driver network card.",
        "Cek apakah WiFi terdeteksi di device manager.",
        "Reset network settings di Windows.",
        "Ganti network card jika rusak."
    ],
    "K16": [
        "Cek volume mixer apakah tidak mute.",
        "Update driver sound card.",
        "Cek speaker/headphone dengan device lain.",
        "Test sound card dengan diagnostic tool.",
        "Ganti sound card jika integrated."
    ],
    "K17": [
        "Cek driver USB controller di device manager.",
        "Uninstall dan reinstall USB root hub.",
        "Disable power saving untuk USB.",
        "Update chipset driver.",
        "Gunakan USB port yang berbeda."
    ],
    "K18": [
        "Uninstall dan reinstall software bermasalah.",
        "Update semua driver ke versi terbaru.",
        "Lakukan clean boot untuk troubleshooting.",
        "Install ulang software jika corrupt.",
        "Cek compatibility dengan OS."
    ],
    "K19": [
        "Update driver touchpad ke versi terbaru.",
        "Cek setting touchpad di control panel.",
        "Disable dan enable touchpad di device manager.",
        "Bersihkan permukaan touchpad.",
        "Ganti touchpad jika rusak fisik."
    ],
    "K20": [
        "Cek apakah webcam terdeteksi di device manager.",
        "Update driver webcam.",
        "Test webcam dengan aplikasi lain.",
        "Cek privacy setting apakah webcam di-block.",
        "Ganti webcam jika integrated dan rusak."
    ]
}