import numpy as np


# Metoda pentru generarea diagnosticului în funcție de procentajul de leziuni
def generate_diagnosis(lesion_data, filename):
    # Calculăm procentajul de leziuni cu mai multă precizie
    lesion_count = np.sum(lesion_data == 0)
    total_pixels = lesion_data.size
    lesion_percentage = (lesion_count / total_pixels) * 100

    # Diagnoză mai nuanțată
    if lesion_percentage > 7:  # Prag ușor modificat
        risk_level = "RIDICAT" if lesion_percentage > 15 else "MODERAT"
        diagnosis = f"Diabet retinopatic identificat - Nivel de risc: {risk_level}"
        treatment = (
            "Terapie laser, monitorizare constantă a glucozei, "
            "injecții anti-VEGF, evaluare oftalmologică periodică."
        )
    else:
        diagnosis = "Pacientul este sănătos."
        treatment = (
            "Menținerea unui stil de viață sănătos, control periodic, "
            "monitorizarea nivelului de zahăr din sânge."
        )

    # Salvăm diagnostic cu mai multe detalii
    output_filename = f"diagnosis/{filename}_diagnosis.txt"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"Diagnostic: {diagnosis}\n")
        f.write(f"Procentaj leziuni: {lesion_percentage:.2f}%\n")
        f.write(f"Tratament recomandat: {treatment}\n")

    print(f"Diagnostic detaliat salvat în {output_filename}!")