from flask import Flask, render_template, request
from knowledge_base import gejala, kerusakan, rules_cf, solusi
from functools import lru_cache
import re

app = Flask(__name__)

def hitung_cf_kombinasi(gejala_user):
    """
    Menghitung kombinasi Certainty Factor untuk setiap kerusakan berdasarkan gejala yang dipilih
    """
    hasil_diagnosa = []

    for kode_k, aturan in rules_cf.items():
        cf_combine = 0
        rule_triggered = False
        gejala_cocok = []
        matched_symptoms = 0
        critical_symptoms_matched = 0
        total_critical_symptoms = 0
        
        # Hitung total gejala kritis
        for _, _, weight in aturan:
            if weight == "critical":
                total_critical_symptoms += 1
        
        for kode_g, cf_pakar, weight in aturan:
            if kode_g in gejala_user:
                rule_triggered = True
                matched_symptoms += 1
                gejala_cocok.append(gejala[kode_g])
                
                # Tambahkan bobot untuk gejala kritis
                weight_multiplier = 1.0
                if weight == "critical":
                    weight_multiplier = 1.3
                    critical_symptoms_matched += 1
                elif weight == "high":
                    weight_multiplier = 1.2
                elif weight == "medium":
                    weight_multiplier = 1.1
                    
                # Skala keyakinan user berdasarkan jumlah gejala yang dipilih
                cf_user = min(1.0, len(gejala_user) / 15)
                cf_current = cf_user * cf_pakar * weight_multiplier
                
                if cf_combine == 0:
                    cf_combine = cf_current
                else:
                    cf_combine = cf_combine + cf_current * (1 - cf_combine)
        
        # Berikan penalti jika gejala kritis tidak cocok
        if rule_triggered and total_critical_symptoms > 0:
            critical_ratio = critical_symptoms_matched / total_critical_symptoms
            cf_combine = cf_combine * critical_ratio
        
        # Berikan penalti untuk gejala yang hilang
        if rule_triggered:
            total_symptoms = len(aturan)
            coverage = matched_symptoms / total_symptoms
            cf_combine = cf_combine * coverage  # Kurangi CF jika tidak semua gejala ada
            
            # Hanya sertakan hasil dengan CF yang berarti
            if cf_combine > 0.1:
                persentase = round(cf_combine * 100, 2)
                hasil_diagnosa.append({
                    'kode': kode_k,
                    'nama': kerusakan[kode_k],
                    'cf': persentase,
                    'gejala_cocok': gejala_cocok,
                    'solusi': solusi.get(kode_k, [])
                })
    
    # Urutkan berdasarkan CF tertinggi
    return sorted(hasil_diagnosa, key=lambda x: x['cf'], reverse=True)

# Cache untuk hasil diagnosa
@lru_cache(maxsize=32)
def get_cached_diagnosis(symptoms_tuple):
    """
    Mendapatkan hasil diagnosa dari cache atau hitung baru
    """
    symptoms = list(symptoms_tuple)
    return hitung_cf_kombinasi(symptoms)

def validate_input(input_string, pattern):
    """
    Validasi input untuk mencegah injection
    """
    if not re.match(pattern, input_string):
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html', gejala=gejala, kerusakan=kerusakan)

@app.route('/forward', methods=['GET', 'POST'])
def forward():
    hasil = []
    gejala_terpilih = []
    
    if request.method == 'POST':
        gejala_terpilih = request.form.getlist('gejala')
        
        # Validasi setiap kode gejala
        for symptom in gejala_terpilih:
            if not validate_input(symptom, r'^G\d{2}$'):
                return render_template('forward.html', 
                                       gejala=gejala, 
                                       error="Input tidak valid")
        
        # Gunakan versi cache jika tersedia
        symptoms_tuple = tuple(sorted(gejala_terpilih))
        hasil = get_cached_diagnosis(symptoms_tuple)

    return render_template('forward.html', 
                           gejala=gejala, 
                           hasil=hasil, 
                           terpilih=gejala_terpilih)

@app.route('/backward', methods=['GET', 'POST'])
def backward():
    selected_kerusakan = None
    analisa_hasil = None

    if request.method == 'POST':
        selected_kerusakan = request.form.get('kerusakan_id')
        
        if selected_kerusakan:
            # Validasi input
            if not validate_input(selected_kerusakan, r'^K\d{2}$'):
                return render_template('backward.html',
                                       kerusakan=kerusakan,
                                       gejala=gejala,
                                       rules_cf=rules_cf,
                                       error="Input tidak valid")
            
            aturan = rules_cf.get(selected_kerusakan, [])
            total_cf_rule = sum(cf for _, cf, _ in aturan)
            
            matched_cf = 0
            gejala_input = request.form.getlist('gejala_check')
            
            # Validasi gejala input
            for g in gejala_input:
                if not validate_input(g, r'^G\d{2}$'):
                    return render_template('backward.html',
                                           kerusakan=kerusakan,
                                           gejala=gejala,
                                           rules_cf=rules_cf,
                                           selected=selected_kerusakan,
                                           error="Input tidak valid")
            
            # Hitung CF untuk gejala yang cocok
            for g, cf, weight in aturan:
                if g in gejala_input:
                    # Berikan bobot ekstra untuk gejala kritis
                    if weight == "critical":
                        matched_cf += cf * 1.3
                    elif weight == "high":
                        matched_cf += cf * 1.2
                    else:
                        matched_cf += cf

            # Normalisasi CF
            if total_cf_rule > 0:
                persen = min(100, (matched_cf / total_cf_rule) * 100)
            else:
                persen = 0
            
            # Tentukan status dan CSS class
            if persen >= 80:
                status = "Sangat Mungkin"
                css_class = "danger"
            elif persen >= 50:
                status = "Mungkin"
                css_class = "warning"
            else:
                status = "Kecil Kemungkinan"
                css_class = "info"

            analisa_hasil = {
                'nama': kerusakan[selected_kerusakan],
                'persen': round(persen, 2),
                'status': status,
                'css': css_class,
                'solusi': solusi.get(selected_kerusakan, []) if persen >= 50 else []
            }
    
    return render_template(
        'backward.html',
        kerusakan=kerusakan,
        gejala=gejala,
        rules_cf=rules_cf,
        selected=selected_kerusakan,
        hasil=analisa_hasil
    )

if __name__ == '__main__':
    app.run(debug=True)