# Segmentation of Diabetic Retinopathy Lesions 
 by VULTURES: Panaite Alexandru, Danalache Sebastian

# Ce este retinopatia diabetică?
Retinopatia diabetică (DR) este o afecțiune a ochiului cauzată de răni la nivelul vaselor sanguine ale retinei. Având în vedere că relativ asimptomatic până în punctul în care pacientul începe să-și piardă vederea, specialiștii recomandă consultări dese ale pacienților cu diabet. Analiza imaginilor la rezoluție înaltă obținute în urma consultărilor necesită un efort considerabil pe o durată costisitoare de timp din partea personalului specializat, întrucât leziunile pot fi dificil de detectat. Deși diagnosticul afecțiunii necesită în cele din urmă un doctor, detectarea automatizată a leziunilor DR poate îmbunătăți semnificativ starea pacientului și rezultatele obținute. Dezvoltările recente (în ceea ce privește machine learning și computer vision) permit clasificarea și localizarea într-o imagine, astfel devenind soluția optimă pentru detectarea retinopatiei diabetice. Ceea ce ne interesează este detectarea cu acuratețe a leziunilor la nivelul pixelilor, ceea ce ușurează drastic munca doctorilor și reduc incertitudinea în privința diagnosticului pacienților.


# Cum o detectăm?

Pentru a detecta leziunile specifice DR, trebuie analizat în amănunt globul ocular pentru a se identifica:

➢ Microanevrisme: puncte mici și negre care apar de obicei în apropierea vaselor de sânge 

➢ Hemoragii: se manifestă ca pete mari, roșii și mai difuze în comparație cu microanevrismele 

➢ Exsudate dure: depuneri galbene, strălucitoare, găsite în principal în zonele centrale 

➢ Exsudate moi: sub forma unor pete albe, pufoase, situate de obicei de-a lungul vaselor de sânge 

➢ Neovascularizare: vase de sânge noi, anormale, care pot fi dificil de segmentat din cauza formei neregulate și a dimensiunilor mici.

![Aspose Words d742e223-56c4-4149-a4fe-f237e7aed767 001](https://github.com/user-attachments/assets/82bae987-8a91-457a-82e5-a7ee8b350e58)

Pentru a detecta leziunile mai eficient, se recomandă ca imaginile să aibă luminozitatea și contrastul crescut, iar cantitatea de roșu din culoare să fie redusă.

Înainte:

![Aspose Words d742e223-56c4-4149-a4fe-f237e7aed767 002](https://github.com/user-attachments/assets/2429763d-c379-4b9f-8882-3ab8a0c204ec)

După:

![Aspose Words d742e223-56c4-4149-a4fe-f237e7aed767 003](https://github.com/user-attachments/assets/9c11e156-d09f-49b7-8d0f-eda83e2b5d85)

Apoi, se vor folosi algoritmii necesari pentru a identifica, separa și extrage defectele cauzate de DR pentru a stabili diagnosticul pacientului.

# Articole / documentații studiate:

![c2RfWP8](https://github.com/user-attachments/assets/ed9ea5fc-58a8-4692-ac68-9784ccc73993)

# Proiectarea soluției

![3veLdQN - Imgur](https://github.com/user-attachments/assets/911afdf6-9308-4568-82e8-06edd8746ae9)

# Bibliografie 

 ➢ [Improving Lesion Segmentation For Diabetic Retinopathy Using Adversarial Learning](https://arxiv.org/pdf/2007.13854v1)
➢ [A Novel Attention-Based U-Net For Diabetic Retinopathy Lesion Segmentation](https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2023.1309795/full)
➢ [Unsupervised Domain Adaptation For Diabetic Retinopathy Lesion Segmentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC11130363/)
➢ [3D Convolutional Neural Networks For Diabetic Retinopathy Lesion Segmentation](https://www.mdpi.com/2075-4426/12/9/1454)
➢ [Multi-scale Feature Fusion For Diabetic Retinopathy Lesion Segmentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC9777401/)

