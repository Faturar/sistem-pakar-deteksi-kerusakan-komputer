from flask import Flask, render_template, request, jsonify
from knowledge_base import kerusakan, gejala, rules_cf, solusi
import re

app = Flask(__name__)

def hitung_cf_backward(selected_hypothesis, confirmed_symptoms):
    """
    Menghitung Certainty Factor untuk metode Backward Chaining
    """
    aturan = rules_cf.get(selected_hypothesis, [])
    if not aturan:
        return 0, []
    
    total_cf_rule = 0
    matched_cf = 0
    matched_symptoms = []
    critical_matched = 0
    total_critical = 0
    
    # Hitung total CF dan hitung gejala kritis
    for kode_g, cf_pakar, weight in aturan:
        total_cf_rule += cf_pakar
        if weight == "critical":
            total_critical += 1
    
    # Hitung CF untuk gejala yang dikonfirmasi
    for kode_g, cf_pakar, weight in aturan:
        if kode_g in confirmed_symptoms:
            matched_cf += cf_pakar
            matched_symptoms.append(gejala[kode_g])
            
            if weight == "critical":
                critical_matched += 1
    
    # Berikan bobot ekstra untuk gejala kritis
    if total_critical > 0:
        critical_bonus = (critical_matched / total_critical) * 0.2
        matched_cf = matched_cf * (1 + critical_bonus)
    
    # Normalisasi CF
    if total_cf_rule > 0:
        persen = min(100, (matched_cf / total_cf_rule) * 100)
    else:
        persen = 0
    
    return persen, matched_symptoms

def get_differential_diagnosis(selected_hypothesis, confirmed_symptoms):
    """
    Mendapatkan diagnosis alternatif (differential diagnosis)
    """
    alternatives = []
    
    for kode_k, aturan in rules_cf.items():
        if kode_k != selected_hypothesis:
            matched_symptoms = 0
            total_symptoms = len(aturan)
            
            for kode_g, cf_pakar, _ in aturan:
                if kode_g in confirmed_symptoms:
                    matched_symptoms += 1
            
            if matched_symptoms > 0:
                confidence = (matched_symptoms / total_symptoms) * 100
                if confidence > 30:  # Threshold untuk alternatif
                    alternatives.append({
                        'kode': kode_k,
                        'nama': kerusakan[kode_k],
                        'confidence': confidence,
                        'matched_symptoms': matched_symptoms
                    })
    
    return sorted(alternatives, key=lambda x: x['confidence'], reverse=True)[:3]

@app.route('/')
def index():
    return render_template('index.html', kerusakan=kerusakan)

@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    selected_hypothesis = None
    hasil_analisis = None
    differential = None
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        if 'hypothesis' in data:
            selected_hypothesis = data['hypothesis']
            
            # Validasi input
            if not re.match(r'^K\d{2}$', selected_hypothesis):
                return jsonify({'error': 'Hipotesis tidak valid'}), 400
            
            confirmed_symptoms = data.get('symptoms', [])
            if isinstance(confirmed_symptoms, str):
                confirmed_symptoms = [confirmed_symptoms]
            
            # Validasi setiap gejala
            for symptom in confirmed_symptoms:
                if not re.match(r'^G\d{2}$', symptom):
                    return jsonify({'error': f'Gejala {symptom} tidak valid'}), 400
            
            # Hitung CF
            persen, matched_symptoms = hitung_cf_backward(selected_hypothesis, confirmed_symptoms)
            
            # Tentukan status dan CSS class
            if persen >= 80:
                status = "Sangat Mungkin"
                css_class = "danger"
                recommendation = "Sangat disarankan untuk segera diperbaiki"
            elif persen >= 60:
                status = "Mungkin"
                css_class = "warning"
                recommendation = "Disarankan untuk diperiksa lebih lanjut"
            elif persen >= 40:
                status = "Kemungkinan Sedang"
                css_class = "info"
                recommendation = "Perlu dipantau perkembangannya"
            else:
                status = "Kecil Kemungkinan"
                css_class = "secondary"
                recommendation = "Kemungkinan bukan penyebab utama"
            
            # Dapatkan solusi jika confidence cukup tinggi
            solusi_list = solusi.get(selected_hypothesis, []) if persen >= 40 else []
            
            # Dapatkan diagnosis alternatif
            differential = get_differential_diagnosis(selected_hypothesis, confirmed_symptoms)
            
            hasil_analisis = {
                'nama': kerusakan[selected_hypothesis],
                'kode': selected_hypothesis,
                'persen': round(persen, 1),
                'status': status,
                'css': css_class,
                'recommendation': recommendation,
                'gejala_cocok': matched_symptoms,
                'solusi': solusi_list,
                'total_gejala': len(rules_cf.get(selected_hypothesis, [])),
                'gejala_terkonfirmasi': len(confirmed_symptoms)
            }
            
            if request.is_json:
                return jsonify({
                    'hasil': hasil_analisis,
                    'differential': differential
                })
    
    return render_template(
        'backward.html',
        kerusakan=kerusakan,
        gejala=gejala,
        rules_cf=rules_cf,
        selected=selected_hypothesis,
        hasil=hasil_analisis,
        differential=differential
    )

@app.route('/api/hypothesis/<hypothesis_id>')
def get_hypothesis_details(hypothesis_id):
    """API untuk mendapatkan detail hipotesis"""
    if not re.match(r'^K\d{2}$', hypothesis_id):
        return jsonify({'error': 'Hipotesis tidak valid'}), 400
    
    aturan = rules_cf.get(hypothesis_id, [])
    if not aturan:
        return jsonify({'error': 'Hipotesis tidak ditemukan'}), 404
    
    symptoms = []
    for kode_g, cf_pakar, weight in aturan:
        symptoms.append({
            'kode': kode_g,
            'deskripsi': gejala[kode_g],
            'cf': cf_pakar,
            'weight': weight,
            'pertanyaan': f"Apakah komputer mengalami: {gejala[kode_g]}?"
        })
    
    return jsonify({
        'kode': hypothesis_id,
        'nama': kerusakan[hypothesis_id],
        'gejala': symptoms
    })

if __name__ == '__main__':
    app.run(debug=True)