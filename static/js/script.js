document.addEventListener("DOMContentLoaded", () => {
  // 1. Inisialisasi Tooltips Bootstrap
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  )
  tooltipTriggerList.map(
    (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
  )

  // 2. Logic Pencarian Gejala (Filter)
  const searchInput = document.getElementById("symptom-search")
  const symptomItems = document.querySelectorAll(".symptom-item")

  if (searchInput) {
    searchInput.addEventListener("keyup", (e) => {
      const term = e.target.value.toLowerCase()

      symptomItems.forEach((item) => {
        const text = item.innerText.toLowerCase()
        if (text.includes(term)) {
          item.style.display = "" // Tampilkan
        } else {
          item.style.display = "none" // Sembunyikan
        }
      })
    })
  }

  // 3. Logic Progress Bar & Highlight Card
  const checkboxes = document.querySelectorAll(
    'input[type="checkbox"][name="gejala"]'
  )
  const progressBar = document.getElementById("progress-bar")
  const progressText = document.getElementById("progress-text")

  function updateUI() {
    // Hitung Progress
    const total = checkboxes.length
    const checkedCount = document.querySelectorAll(
      'input[type="checkbox"][name="gejala"]:checked'
    ).length

    if (progressBar && progressText) {
      const percent = Math.round((checkedCount / total) * 100)
      progressBar.style.width = `${percent}%`
      progressText.innerText = `${percent}%`

      // Ubah warna jika sudah banyak dipilih
      if (percent > 0) {
        progressBar.classList.remove("bg-secondary")
      }
    }

    // Update Style Kartu (Highlight)
    checkboxes.forEach((cb) => {
      const card = cb.closest(".symptom-card")
      if (card) {
        if (cb.checked) {
          card.classList.add("selected")
        } else {
          card.classList.remove("selected")
        }
      }
    })
  }

  // Event Listener untuk setiap Checkbox
  checkboxes.forEach((cb) => {
    cb.addEventListener("change", updateUI)

    // Fitur: Klik di mana saja pada kartu untuk mencentang
    const card = cb.closest(".symptom-card")
    if (card) {
      card.addEventListener("click", (e) => {
        // Mencegah double event jika yang diklik langsung checkbox/labelnya
        if (e.target !== cb && e.target.tagName !== "LABEL") {
          cb.checked = !cb.checked
          updateUI() // Panggil update manual karena mengubah .checked via JS tidak memicu event 'change'
        }
      })
    }
  })

  // Jalankan sekali saat load (untuk handle kondisi back button browser / re-render)
  updateUI()

  // 4. Auto Scroll ke Hasil (Jika ada hasil)
  const hasilSection = document.getElementById("hasil-section")
  if (hasilSection) {
    setTimeout(() => {
      hasilSection.scrollIntoView({ behavior: "smooth", block: "start" })
    }, 500) // Delay sedikit agar animasi render selesai
  }

  // 5. Animasi Loading saat Submit
  const form = document.getElementById("diagnosisForm")
  if (form) {
    form.addEventListener("submit", function () {
      const btn = this.querySelector('button[type="submit"]')
      if (btn) {
        const originalText = btn.innerHTML
        btn.disabled = true
        btn.innerHTML =
          '<span class="spinner-border spinner-border-sm me-2"></span>Menganalisa...'

        // Restore jika user menekan back (opsional, browser modern menghandle bfcache)
        setTimeout(() => {
          btn.disabled = false
          btn.innerHTML = originalText
        }, 5000)
      }
    })
  }
})
