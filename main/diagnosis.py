# diagnosis.py
import numpy as np
from datetime import datetime


def analyze_severity(analysis):
    # Initialize scoring system
    severity_score = 0
    max_score = 10

    # Score based on dark lesions (microaneurysms and hemorrhages)
    if analysis['dark_lesion_density'] > 0.5:
        severity_score += 3
    elif analysis['dark_lesion_density'] > 0.2:
        severity_score += 2
    elif analysis['dark_lesion_density'] > 0.1:
        severity_score += 1

    # Score based on bright lesions (exudates)
    if analysis['bright_lesion_density'] > 0.3:
        severity_score += 4
    elif analysis['bright_lesion_density'] > 0.1:
        severity_score += 2
    elif analysis['bright_lesion_density'] > 0.05:
        severity_score += 1

    # Score based on lesion counts
    if analysis['dark_lesion_count'] > 50 or analysis['bright_lesion_count'] > 30:
        severity_score += 3
    elif analysis['dark_lesion_count'] > 20 or analysis['bright_lesion_count'] > 15:
        severity_score += 2

    # Calculate confidence score (0-1)
    confidence = min(severity_score / max_score * 100, 100)

    # Determine severity level
    if severity_score >= 8:
        return "SEVER", confidence
    elif severity_score >= 5:
        return "MODERAT", confidence
    elif severity_score >= 3:
        return "UȘOR", confidence
    else:
        return "NORMAL", confidence


def generate_diagnosis(lesion_data, filename, analysis):
    severity_level, confidence = analyze_severity(analysis)

    # Define recommendations based on severity
    recommendations = {
        "SEVER": {
            "diagnostic": "Retinopatie diabetică severă",
            "tratament": [
                "Consultație oftalmologică de urgență",
                "Terapie laser panretinală",
                "Monitorizare glicemică strictă",
                "Posibilă intervenție chirurgicală",
                "Control la 1-2 luni"
            ]
        },
        "MODERAT": {
            "diagnostic": "Retinopatie diabetică moderată",
            "tratament": [
                "Terapie laser focală",
                "Monitorizare glicemică regulată",
                "Consultație oftalmologică la 3-4 luni",
                "Control dietetic strict",
                "Posibile injecții anti-VEGF"
            ]
        },
        "UȘOR": {
            "diagnostic": "Retinopatie diabetică ușoară",
            "tratament": [
                "Monitorizare periodică",
                "Optimizarea controlului glicemic",
                "Consultație oftalmologică la 6 luni",
                "Menținerea unui stil de viață sănătos"
            ]
        },
        "NORMAL": {
            "diagnostic": "Aspect normal al retinei",
            "tratament": [
                "Screening anual",
                "Menținerea controlului glicemic",
                "Stil de viață sănătos"
            ]
        }
    }

    # Generate detailed report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_filename = f"diagnosis/{filename}_diagnosis.txt"

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"RAPORT ANALIZA RETINIANA\n")
        f.write(f"Data: {timestamp}\n")
        f.write(f"Cod pacient: {filename}\n")
        f.write("\n=== REZULTATE ANALIZA ===\n")
        f.write(f"Diagnostic: {recommendations[severity_level]['diagnostic']}\n")
        f.write(f"Nivel de severitate: {severity_level}\n")
        f.write(f"Grad de încredere: {confidence:.1f}%\n")
        f.write("\n=== DETALII ANALIZA ===\n")
        f.write(f"Leziuni întunecate detectate: {analysis['dark_lesion_count']}\n")
        f.write(f"Leziuni luminoase detectate: {analysis['bright_lesion_count']}\n")
        f.write(f"Densitate leziuni întunecate: {analysis['dark_lesion_density']:.3f}/1000px\n")
        f.write(f"Densitate leziuni luminoase: {analysis['bright_lesion_density']:.3f}/1000px\n")
        f.write("\n=== RECOMANDARI TRATAMENT ===\n")
        for idx, rec in enumerate(recommendations[severity_level]['tratament'], 1):
            f.write(f"{idx}. {rec}\n")

        f.write("\nNOTA: Acest raport este generat automat și ar trebui interpretat de un specialist.")

    print(f"Diagnostic detaliat salvat în {output_filename}")
