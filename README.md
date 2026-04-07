# Drug synergy prediction 💊🧬

End-to-end ml project on prediction of drug interaction effects. The aim is to practice project structure, modularization and deployment.

I pick a dataset on my own and follow the contents from the course 'End-to-end ML project' from krishnaik06 on [youtube](https://www.youtube.com/playlist?list=PLZoTAELRMXVPS-dOaVbAux22vzqdgoGhG), with an appropriate, custom analysis for the data

---

## Overview

* Understanding combinatorial effects of drug application is essential in pharmaceutical research for drug development and therapeutics. Experimentation at large scales is impractical and presents several challenges, so computational approaches for hypothesis generation are popular choices.
* Given a dataset with over 3.4k drug combination experiments with different targets and over several cell lines, we aim to predict a given pair's Synergy Score, a measure on whether the interaction has additive or antagonistic effects
* We load, integrate and preprocess the data, perform exploratory data analysis and train-validate a few toy models for prediction. As our main goal is to gather experience in project structure and modularization, rather than prediction, we don't prioritize model efficiency.
---

## Data

* We use the data and pre-procesing steps from [this paper](https://doi.org/10.1093/biomethods/bpaf033), which in turns takes over from the [Drug combination prediction DREAM challenge](https://doi.org/10.1038/s41467-019-09799-2) 
- Description: the final dataset contains 8 categorical and 13 numerical features:
    - Cell line name: 85 unique cancer cell lines (categorical)
    - Compound A/B: 69 unique drugs (categorical)
    - Max. conc. A/B: highest dose tested in the experiment (numerical)
    - IC50 A/B: concentration required to reach half inhibition; a measure of drug's potency (numerical)
    - Einf A/B: maximal effect (lowest viability) achieved at infinite concentration; a measure of drug efficacy (numerical)
    - H A/B: Hill coefficient; describes the steepness of the drug dose-response curve.  indicates a sharp switch like response,  a very slow one (numerical)
    - Synergy score: a measure of interaction, postive values mean the drugs enhance each other (synergy), zero is additivity and negative is antagonism (numerical)
    - GDSC tissue descriptor 2: organ / tissue origin of the cancer; tags from the Genomics of Drug Sensitivity in Cancer database (categorical)
    - MSI: microsatielite instability status, indicates if DNA repair is broken; 'high' status often increases drug sensitivty (categorical)
    - Growth properties: how cells grow in lab; shape and tendency to stick to their neighbors can affect drug efficacy (categorical)
    - Putative target A / B: drug target (categorical)
    - Function A/B: functional annotation of the drug, what it does to the target (categorical)
    - Pathway A/B: drug biological pathway (categorical)
- Size / format: tabular (3475, 21)
- Preprocessing steps: we integrate 3 datasets: the drug synergy dataset (main dataset details on the combinatorial experiments), and the cell lines and drug portfolio datasets (extra information on the cancer cells and drugs for the study), then we preprocess according to [the original publication](https://doi.org/10.1093/biomethods/bpaf033). The exploratory analysis and training are our own.
---

## Methods

### Modeling approaches
- Supervised regression to predict synergy scores

### Algorithms used
- Linear models: Linear Regression, Ridge, Lasso
- Tree-based models: Decision Tree, Random Forest
- Boosting methods: Gradient Boosting, XGBoost, CatBoost, AdaBoost
- Instance-based: K-Nearest Neighbors

### Evaluation metric
- **Weighted Pearson Correlation (WPC)**, computed per drug combination across cell lines

### Validation strategy
- Train/test split using **group-based splitting by drug combination** to avoid data leakage
- Hyperparameter tuning with GridSearchCV (3-fold cross-validation)

---

## Status
- Data pipeline: ✅
- Model training: ✅
- Evaluation: ✅
- Deployment: ⏳ (planned)

---

## Project Structure

```text
drugsynergy/
│
├── artifacts/ #saved models, preprocessor, train/test csv
│
├── data/
│   ├── cell_lines.csv
│   ├── drug_portfolio.csv
│   ├── drug_synergy.csv
│
├── notebooks/
│   ├── EDA.ipynb
│   ├── modeling.ipynb
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_transform.py
│   │   ├── model_trainer.py
│   │
│   ├── pipeline/
│   │   ├── train_pipeline.py
│   │   ├── predict_pipeline.py
│   │
│   ├── utils.py
│   ├── logger.py
│   ├── exception.py
│
├── README.md
├── requirements.txt
├── setup.py
└── .gitignore
