# Medical Corpus Semantic Similarity Evaluation
Evaluating the similarity of two medical texts semantically.

```
from EntityExtractorv2 import medical_term
from SimMetric import sim_metric

Reference_entities = medical_term(Reference_Text)
Candidate_entities = medical_term(Candidate_Text)

semantic_score = sim_metric(Reference_entities, Candidate_entities)
```
