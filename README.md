# Segmentation of Diabetic Retinopathy Lesions 
 by VULTURES: Panaite Alexandru, Danalache Sebastian

# Ce este retinopatia diabetică?
Retinopatia diabetică (DR) este o afecțiune a ochiului cauzată de răni la nivelul vaselor sanguine ale retinei. Având în vedere că relativ asimptomatic până în punctul în care pacientul începe să-și piardă vederea, specialiștii recomandă consultări dese ale pacienților cu diabet. Analiza imaginilor la rezoluție înaltă obținute în urma consultărilor necesită un efort considerabil pe o durată costisitoare de timp din partea personalului specializat, întrucât leziunile pot fi dificil de detectat. Deși diagnosticul afecțiunii necesită în cele din urmă un doctor, detectarea automatizată a leziunilor DR poate îmbunătăți semnificativ starea pacientului și rezultatele obținute. Dezvoltările recente (în ceea ce privește machine learning și computer vision) permit clasificarea și localizarea într-o imagine, astfel devenind soluția optimă pentru detectarea retinopatiei diabetice. Ceea ce ne interesează este detectarea cu acuratețe a leziunilor la nivelul pixelilor, ceea ce ușurează drastic munca doctorilor și reduc incertitudinea în privința diagnosticului pacienților.


# Cum o detectăm?

Pentru a detecta leziunile specifice DR, trebuie analizat în amănunt globul ocular pentru a se identifica:
➢ Microanevrisme: puncte mici și negre care apar de obicei în apropierea vaselor de sânge 
➢ Hemoragii: se manifestă ca pete mari, roșii și mai difuze în comparație cu microanevrismele 
➢ Exsudate dure: depuneri galbene, strălucitoare, găsite în principal în zonele centrale ➢ Exsudate moi: sub forma unor pete albe, pufoase, situate de obicei de-a lungul vaselor de sânge 
➢ Neovascularizare: vase de sânge noi, anormale, care pot fi dificil de segmentat din cauza formei neregulate și a dimensiunilor mici
![enter image description here](https://imgur.com/a/jKzCYwa)

Pentru a detecta leziunile mai eficient, se recomandă ca imaginile să aibă luminozitatea și contrastul crescut, iar cantitatea de roșu din culoare să fie redusă.

Înainte:
![enter image description here](https://imgur.com/a/n7Utue3)

După:
![enter image description here](https://imgur.com/a/iWkyC3k)

Apoi, se vor folosi algoritmii necesari pentru a identifica, separa și extrage defectele cauzate de DR pentru a stabili diagnosticul pacientului.

# Articole / documentații studiate:
![enter image description here](https://imgur.com/a/GNdPlBA)

# Proiectarea soluției

![enter image description here](https://imgur.com/a/xXGYCDR)


# Bibliografie 

 ➢ [Improving Lesion Segmentation For Diabetic Retinopathy Using Adversarial Learning](https://arxiv.org/pdf/2007.13854v1)
➢ [A Novel Attention-Based U-Net For Diabetic Retinopathy Lesion Segmentation](https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2023.1309795/full)
➢ [Unsupervised Domain Adaptation For Diabetic Retinopathy Lesion Segmentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC11130363/)
➢ [3D Convolutional Neural Networks For Diabetic Retinopathy Lesion Segmentation](https://www.mdpi.com/2075-4426/12/9/1454)
➢ [Multi-scale Feature Fusion For Diabetic Retinopathy Lesion Segmentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC9777401/)

