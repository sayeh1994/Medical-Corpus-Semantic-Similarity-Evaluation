# Medical Corpus Semantic Similarity Evaluation

Medical language processing and deep learning techniques have emerged as critical tools for improving healthcare, particularly in the analysis of medical imaging and medical text data. These multimodal data fusion techniques help to improve the interpretation of medical imaging and lead to increased diagnostic accuracy, informed clinical decisions, and improved patient outcomes. The success of these models relies on the ability to extract and consolidate semantic information from clinical text. This paper addresses the need for more robust methods to evaluate the semantic content of medical reports. Conventional natural language processing approaches and metrics are initially designed for considering the semantic context in the natural language domain and machine translation, often failing to capture the complex semantic meanings inherent in medical content. In this study, we introduce a novel approach designed specifically for assessing the semantic similarity between generated medical reports and the ground truth. Our approach is validated, demonstrating its efficiency in assessing domain-specific semantic similarity within medical contexts. By applying our metric to state-of-the-art Chest X-ray report generation models, we obtain results that not only align with conventional metrics but also provide more contextually meaningful scores in the considered medical domain.

# How to use

Create the environment:
```
conda env create -f environment.yml
```
You may need to install the dictionaries from Spacy and [Scispacy](https://allenai.github.io/scispacy/).

> To install the dictionaries of [Scispacy](https://allenai.github.io/scispacy/):

```
pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_md-0.5.3.tar.gz # en_core_sci_md
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_ner_bionlp13cg_md-0.5.3.tar.gz # en_ner_bionlp13cg_md
```
> To install ``en_core_web_sm" dictionary from [Spacy](https://spacy.io/usage):

```
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
```

To evaluate the semantic similarity between "Reference_Text" and "Candidate_Text" try the following commands:
```
from EntityExtractorv2 import medical_term
from SimMetric import sim_metric

Reference_entities = medical_term(Reference_Text)
Candidate_entities = medical_term(Candidate_Text)

semantic_score = sim_metric(Reference_entities, Candidate_entities)
```
If you find this repository useful to your project please consider citing our paper in your future publication:
```
@conference{bioinformatics24,
author={Sayeh Gholipour Picha and Dawood Al Chanti and Alice Caplier},
title={Semantic Textual Similarity Assessment in Chest X-ray Reports Using a Domain-Specific Cosine-Based Metric},
booktitle={Proceedings of the 17th International Joint Conference on Biomedical Engineering Systems and Technologies - Volume 1: BIOINFORMATICS},
year={2024},
pages={487-494},
publisher={SciTePress},
organization={INSTICC},
doi={10.5220/0012429600003657},
isbn={978-989-758-688-0},
}
```
