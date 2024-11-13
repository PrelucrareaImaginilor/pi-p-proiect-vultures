# diagnosis.py
import cv2
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime


class RetinalDiagnosisSystem:
    """
    Sistem de diagnostic pentru evaluarea riscului de diabet bazat pe analiza leziunilor retiniene.
    """

    def __init__(self):
        self.risk_thresholds = {
            'low': {'dark_lesion_area': 0.001, 'bright_lesion_area': 0.001},
            'medium': {'dark_lesion_area': 0.005, 'bright_lesion_area': 0.005},
            'high': {'dark_lesion_area': 0.01, 'bright_lesion_area': 0.01}
        }

        # Ponderi pentru diferite tipuri de leziuni în calculul riscului
        self.weights = {
            'dark_lesions': 0.6,  # Microanevrisme și hemoragii au impact mai mare
            'bright_lesions': 0.4  # Exudate
        }

    def calculate_lesion_features(self, dark_mask, bright_mask):
        """
        Calculează caracteristicile leziunilor pentru diagnostic.

        Args:
            dark_mask (numpy.ndarray): Masca leziunilor întunecate
            bright_mask (numpy.ndarray): Masca leziunilor luminoase

        Returns:
            dict: Caracteristicile calculate ale leziunilor
        """
        total_pixels = dark_mask.size

        # Calculează ariile relative ale leziunilor
        dark_area = np.sum(dark_mask > 0) / total_pixels
        bright_area = np.sum(bright_mask > 0) / total_pixels

        # Analiza distribuției leziunilor
        dark_components = self._analyze_components(dark_mask)
        bright_components = self._analyze_components(bright_mask)

        return {
            'dark_lesions': {
                'relative_area': dark_area,
                'count': dark_components['count'],
                'avg_size': dark_components['avg_size'],
                'density': dark_components['density']
            },
            'bright_lesions': {
                'relative_area': bright_area,
                'count': bright_components['count'],
                'avg_size': bright_components['avg_size'],
                'density': bright_components['density']
            }
        }

    def _analyze_components(self, mask):
        """
        Analizează componentele conectate din mască.

        Args:
            mask (numpy.ndarray): Masca binară a leziunilor

        Returns:
            dict: Statistici despre componente
        """
        if not mask.any():
            return {'count': 0, 'avg_size': 0, 'density': 0}

        # Găsește componentele conectate
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            mask.astype(np.uint8), connectivity=8
        )

        # Exclude background (label 0)
        if num_labels > 1:
            areas = stats[1:, cv2.CC_STAT_AREA]
            avg_size = np.mean(areas)
            density = len(areas) / mask.size
        else:
            avg_size = 0
            density = 0

        return {
            'count': num_labels - 1,  # Exclude background
            'avg_size': avg_size,
            'density': density
        }

    def calculate_risk_score(self, features):
        """
        Calculează scorul de risc bazat pe caracteristicile leziunilor.

        Args:
            features (dict): Caracteristicile leziunilor

        Returns:
            float: Scor de risc între 0 și 1
        """
        # Calculează subscoruri pentru fiecare tip de leziune
        dark_score = self._calculate_lesion_type_score(
            features['dark_lesions'],
            self.risk_thresholds['high']['dark_lesion_area']
        )

        bright_score = self._calculate_lesion_type_score(
            features['bright_lesions'],
            self.risk_thresholds['high']['bright_lesion_area']
        )

        # Combină scorurile folosind ponderile definite
        total_score = (
                dark_score * self.weights['dark_lesions'] +
                bright_score * self.weights['bright_lesions']
        )

        return min(1.0, total_score)

    def _calculate_lesion_type_score(self, lesion_features, max_threshold):
        """
        Calculează scorul pentru un tip specific de leziune.
        """
        area_score = min(1.0, lesion_features['relative_area'] / max_threshold)
        density_score = min(1.0, lesion_features['density'] * 1000)  # Scalare pentru densitate

        # Combină scorurile (putem ajusta formula în funcție de necesități)
        return (area_score * 0.7 + density_score * 0.3)

    def get_risk_level(self, risk_score):
        """
        Determină nivelul de risc bazat pe scorul calculat.

        Args:
            risk_score (float): Scorul de risc calculat

        Returns:
            tuple: (nivel_risc, descriere, recomandări)
        """
        if risk_score < 0.3:
            return ('Scăzut',
                    'Risc scăzut de dezvoltare a diabetului',
                    ['Monitorizare anuală de rutină',
                     'Menținerea unui stil de viață sănătos'])
        elif risk_score < 0.6:
            return ('Mediu',
                    'Risc moderat de dezvoltare a diabetului',
                    ['Consultație oftalmologică în următoarele 6 luni',
                     'Teste glicemice regulate',
                     'Evaluarea factorilor de risc pentru diabet'])
        else:
            return ('Ridicat',
                    'Risc ridicat de dezvoltare a diabetului',
                    ['Consultație medicală urgentă',
                     'Teste complete pentru diabet',
                     'Monitorizare oftalmologică frecventă'])

    def generate_diagnosis_report(self, image_path, features, risk_score):
        """
        Generează un raport detaliat de diagnostic.

        Args:
            image_path (str): Calea către imaginea analizată
            features (dict): Caracteristicile leziunilor
            risk_score (float): Scorul de risc calculat

        Returns:
            dict: Raportul complet de diagnostic
        """
        risk_level, risk_description, recommendations = self.get_risk_level(risk_score)

        report = {
            'image_name': Path(image_path).name,
            'analysis_date': datetime.now().isoformat(),
            'risk_assessment': {
                'score': float(risk_score),
                'level': risk_level,
                'description': risk_description
            },
            'lesion_analysis': {
                'dark_lesions': {
                    'relative_area': float(features['dark_lesions']['relative_area']),
                    'count': int(features['dark_lesions']['count']),
                    'average_size': float(features['dark_lesions']['avg_size'])
                },
                'bright_lesions': {
                    'relative_area': float(features['bright_lesions']['relative_area']),
                    'count': int(features['bright_lesions']['count']),
                    'average_size': float(features['bright_lesions']['avg_size'])
                }
            },
            'recommendations': recommendations
        }

        return report

    def save_diagnosis_report(self, report, output_dir):
        """
        Salvează raportul de diagnostic în format JSON.

        Args:
            report (dict): Raportul de diagnostic
            output_dir (str): Directorul pentru salvarea raportului
        """
        output_path = Path(output_dir) / f"diagnosis_{report['image_name']}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)