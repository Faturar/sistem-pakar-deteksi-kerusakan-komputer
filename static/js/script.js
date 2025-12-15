document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  )
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  // Initialize backward chaining system
  window.backwardChaining = new BackwardChaining()
})

class BackwardChaining {
  constructor() {
    this.selectedHypothesis = null
    this.currentStep = 0
    this.confirmedSymptoms = []
    this.symptoms = []
    this.mode = "selection" // selection, quick, guided, result
    this.init()
  }

  init() {
    this.setupEventListeners()
    this.showSelectionScreen()
  }

  setupEventListeners() {
    // Hypothesis selection
    document.querySelectorAll(".hypothesis-card").forEach((card) => {
      card.addEventListener("click", () => {
        const hypothesis = card.dataset.hypothesis
        this.selectHypothesis(hypothesis)
      })
    })

    // Search functionality
    const searchInput = document.getElementById("hypothesisSearch")
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.filterHypotheses(e.target.value)
      })
    }

    // Mode toggle buttons
    const quickModeBtn = document.getElementById("quickModeBtn")
    const guidedModeBtn = document.getElementById("guidedModeBtn")

    if (quickModeBtn) {
      quickModeBtn.addEventListener("click", () => {
        this.showQuickMode()
      })
    }

    if (guidedModeBtn) {
      guidedModeBtn.addEventListener("click", () => {
        this.showGuidedMode()
      })
    }

    // Back to top button
    const backToTopButton = document.querySelector(".fab")
    if (backToTopButton) {
      window.addEventListener("scroll", () => {
        if (window.pageYOffset > 300) {
          backToTopButton.style.display = "flex"
        } else {
          backToTopButton.style.display = "none"
        }
      })

      backToTopButton.addEventListener("click", () => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        })
      })
    }
  }

  filterHypotheses(searchTerm) {
    const cards = document.querySelectorAll(".hypothesis-card")
    const term = searchTerm.toLowerCase()

    cards.forEach((card) => {
      const text = card.textContent.toLowerCase()
      if (text.includes(term)) {
        card.style.display = "block"
      } else {
        card.style.display = "none"
      }
    })
  }

  selectHypothesis(hypothesis) {
    this.selectedHypothesis = hypothesis

    // Update UI
    document.querySelectorAll(".hypothesis-card").forEach((card) => {
      card.classList.remove("selected")
    })

    const selectedCard = document.querySelector(
      `[data-hypothesis="${hypothesis}"]`
    )
    if (selectedCard) {
      selectedCard.classList.add("selected")
    }

    // Load symptoms for selected hypothesis
    this.loadSymptoms(hypothesis)
  }

  async loadSymptoms(hypothesis) {
    try {
      const response = await fetch(`/api/hypothesis/${hypothesis}`)
      const data = await response.json()

      if (data.error) {
        console.error(data.error)
        return
      }

      this.symptoms = data.gejala
      this.showModeSelection()
    } catch (error) {
      console.error("Error loading symptoms:", error)
    }
  }

  showModeSelection() {
    const modeSelection = document.getElementById("modeSelection")
    if (modeSelection) {
      modeSelection.style.display = "block"
      modeSelection.scrollIntoView({ behavior: "smooth" })
    }
  }

  showQuickMode() {
    this.mode = "quick"
    this.showQuickModeScreen()
  }

  showGuidedMode() {
    this.mode = "guided"
    this.startGuidedMode()
  }

  showQuickModeScreen() {
    const modeSelection = document.getElementById("modeSelection")
    const quickModeScreen = document.getElementById("quickModeScreen")

    if (modeSelection) modeSelection.style.display = "none"
    if (quickModeScreen) {
      quickModeScreen.style.display = "block"
      quickModeScreen.scrollIntoView({ behavior: "smooth" })
    }

    // Generate symptom checkboxes
    this.generateSymptomCheckboxes()
  }

  generateSymptomCheckboxes() {
    const container = document.getElementById("symptomCheckboxes")
    if (!container) return

    container.innerHTML = this.symptoms
      .map(
        (symptom, index) => `
      <div class="symptom-card animate-up" style="animation-delay: ${
        index * 0.1
      }s">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" 
                 id="symptom-${symptom.kode}" 
                 value="${symptom.kode}"
                 data-weight="${symptom.weight}">
          <label class="form-check-label w-100" for="symptom-${symptom.kode}">
            <div class="d-flex justify-content-between align-items-center">
              <span>
                <span class="badge bg-primary me-2">${symptom.kode}</span>
                ${symptom.deskripsi}
              </span>
              <span class="badge bg-${this.getWeightColor(symptom.weight)}">
                ${this.getWeightLabel(symptom.weight)}
              </span>
            </div>
          </label>
        </div>
      </div>
    `
      )
      .join("")

    // Add event listeners
    container.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        this.updateProgress()
      })
    })
  }

  startGuidedMode() {
    const modeSelection = document.getElementById("modeSelection")
    const guidedModeScreen = document.getElementById("guidedModeScreen")

    if (modeSelection) modeSelection.style.display = "none"
    if (guidedModeScreen) {
      guidedModeScreen.style.display = "block"
      guidedModeScreen.scrollIntoView({ behavior: "smooth" })
    }

    this.currentStep = 0
    this.confirmedSymptoms = []
    this.showNextQuestion()
  }

  showNextQuestion() {
    if (this.currentStep >= this.symptoms.length) {
      this.showResults()
      return
    }

    const symptom = this.symptoms[this.currentStep]
    const questionContainer = document.getElementById("questionContainer")

    if (questionContainer) {
      questionContainer.innerHTML = `
        <div class="question-card animate-up">
          <div class="d-flex align-items-center mb-3">
            <div class="question-number">${this.currentStep + 1}</div>
            <div class="ms-3">
              <h5 class="mb-1">Pertanyaan ${this.currentStep + 1} dari ${
        this.symptoms.length
      }</h5>
              <div class="progress" style="height: 8px; width: 200px;">
                <div class="progress-bar" style="width: ${
                  ((this.currentStep + 1) / this.symptoms.length) * 100
                }%"></div>
              </div>
            </div>
          </div>
          <div class="question-text">${symptom.pertanyaan}</div>
          <div class="answer-buttons">
            <button class="answer-btn yes" onclick="backwardChaining.answerQuestion(true)">
              <i class="bi bi-check-circle-fill text-success me-2"></i>
              Ya
            </button>
            <button class="answer-btn no" onclick="backwardChaining.answerQuestion(false)">
              <i class="bi bi-x-circle-fill text-danger me-2"></i>
              Tidak
            </button>
            <button class="answer-btn skip" onclick="backwardChaining.answerQuestion('skip')">
              <i class="bi bi-skip-forward-fill text-secondary me-2"></i>
              Tidak Tahu
            </button>
          </div>
        </div>
      `
    }
  }

  answerQuestion(answer) {
    const symptom = this.symptoms[this.currentStep]

    if (answer !== "skip") {
      this.confirmedSymptoms.push({
        kode: symptom.kode,
        answer: answer,
        cf: symptom.cf,
        weight: symptom.weight,
      })
    }

    this.currentStep++

    if (this.currentStep < this.symptoms.length) {
      this.showNextQuestion()
    } else {
      this.showResults()
    }
  }

  updateProgress() {
    const checkboxes = document.querySelectorAll(
      '#symptomCheckboxes input[type="checkbox"]:checked'
    )
    const total = document.querySelectorAll(
      '#symptomCheckboxes input[type="checkbox"]'
    ).length
    const progress = (checkboxes.length / total) * 100

    const progressBar = document.getElementById("quickModeProgress")
    const progressText = document.getElementById("quickModeProgressText")

    if (progressBar) {
      progressBar.style.width = `${progress}%`
    }

    if (progressText) {
      progressText.textContent = `${Math.round(progress)}%`
    }
  }

  async showResults() {
    // Get confirmed symptoms
    let confirmedSymptoms = []
    if (this.mode === "quick") {
      const checkboxes = document.querySelectorAll(
        '#symptomCheckboxes input[type="checkbox"]:checked'
      )
      confirmedSymptoms = Array.from(checkboxes).map((cb) => cb.value)
    } else {
      confirmedSymptoms = this.confirmedSymptoms
        .filter((s) => s.answer === true)
        .map((s) => s.kode)
    }

    // Send to server
    try {
      const response = await fetch("/diagnosis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          hypothesis: this.selectedHypothesis,
          symptoms: confirmedSymptoms,
        }),
      })

      const data = await response.json()

      if (data.error) {
        console.error(data.error)
        return
      }

      this.displayResults(data.hasil, data.differential)
    } catch (error) {
      console.error("Error:", error)
    }
  }

  displayResults(hasil, differential) {
    const resultsContainer = document.getElementById("resultsContainer")
    if (!resultsContainer) return

    resultsContainer.innerHTML = `
      <div class="result-card ${hasil.css} animate-up">
        <div class="card-body">
          <div class="text-center mb-4">
            <h3 class="fw-bold">${hasil.nama}</h3>
            <p class="text-muted">Hasil Analisa Hipotesis</p>
            
            <div class="confidence-score text-${hasil.css}">${
      hasil.persen
    }%</div>
            <div class="confidence-meter mb-3">
              <div class="confidence-fill bg-${hasil.css}" style="width: ${
      hasil.persen
    }%"></div>
            </div>
            <div class="confidence-labels">
              <span>0%</span>
              <span>25%</span>
              <span>50%</span>
              <span>75%</span>
              <span>100%</span>
            </div>
            
            <div class="mt-3">
              <span class="badge bg-${hasil.css} fs-6">${hasil.status}</span>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <small class="text-muted">Gejala Terkonfirmasi</small>
              <div class="fw-bold">${hasil.gejala_terkonfirmasi} dari ${
      hasil.total_gejala
    }</div>
            </div>
            <div class="col-md-6">
              <small class="text-muted">Tingkat Keyakinan</small>
              <div class="fw-bold">${hasil.recommendation}</div>
            </div>
          </div>

          ${
            hasil.solusi.length > 0
              ? `
            <div class="alert alert-light border">
              <h6 class="fw-bold text-primary mb-3">
                <i class="bi bi-lightbulb me-2"></i>Rekomendasi Perbaikan:
              </h6>
              <ol class="mb-0 ps-3">
                ${hasil.solusi
                  .map((sol) => `<li class="mb-2">${sol}</li>`)
                  .join("")}
              </ol>
            </div>
          `
              : ""
          }

          <div class="d-grid gap-2 mt-4 d-print-none">
            <button onclick="location.reload()" class="btn btn-outline-secondary">
              <i class="bi bi-arrow-clockwise me-2"></i>Diagnosis Ulang
            </button>
          </div>
        </div>
      </div>

      ${
        differential && differential.length > 0
          ? `
        <div class="card mt-4 animate-up">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">
              <i class="bi bi-compass me-2"></i>Diagnosis Alternatif
            </h5>
          </div>
          <div class="card-body">
            <p class="text-muted mb-3">Kemungkinan lain berdasarkan gejala yang sama:</p>
            ${differential
              .map(
                (alt) => `
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div>
                  <strong>${alt.nama}</strong>
                  <small class="text-muted d-block">${alt.kode}</small>
                </div>
                <div class="text-end">
                  <div class="fw-bold">${alt.confidence.toFixed(1)}%</div>
                  <small class="text-muted">${
                    alt.matched_symptoms
                  } gejala cocok</small>
                </div>
              </div>
            `
              )
              .join("")}
          </div>
        </div>
      `
          : ""
      }
    `

    resultsContainer.scrollIntoView({ behavior: "smooth" })
  }

  getWeightColor(weight) {
    switch (weight) {
      case "critical":
        return "danger"
      case "high":
        return "warning"
      case "medium":
        return "info"
      default:
        return "secondary"
    }
  }

  getWeightLabel(weight) {
    switch (weight) {
      case "critical":
        return "Kritis"
      case "high":
        return "Penting"
      case "medium":
        return "Sedang"
      default:
        return "Rendah"
    }
  }

  showSelectionScreen() {
    // Initial setup already done in HTML
    console.log("Selection screen ready")
  }
}
