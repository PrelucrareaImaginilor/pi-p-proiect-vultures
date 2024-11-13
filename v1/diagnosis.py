import numpy as np


# Metoda pentru generarea diagnosticului în funcție de procentajul de leziuni
def generate_diagnosis(lesion_data, filename):
    lesion_count = np.sum(lesion_data == 0)
    total_pixels = lesion_data.size
    lesion_percentage = (lesion_count / total_pixels) * 100
    if lesion_percentage > 5:
        diagnosis, treatment = (
            "Diabet retinopatic identificat",
            "Terapie laser, monitorizarea constantă a glucozei, injecții anti-VEGF."
        )
    else:
        diagnosis, treatment = (
            "Pacientul este sănătos.",
            "Menținerea unui stil de viață sănătos și monitorizarea periodică a nivelului de zahăr din sânge."
        )
    output_filename = f"diagnosis/{filename}_diagnosis.txt"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"Diagnostic: {diagnosis}\nTratament: {treatment}\n")
    print(f"Diagnostic salvat în fișierul {output_filename}!")
