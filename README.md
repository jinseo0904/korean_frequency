# KoFREN: Comprehensive Korean Word Frequency Norms Derived from Large Scale Free Speech Corpora

## What is KoFREN?
Word frequencies are integral in linguistic studies, showing strong correlations with speakers’ cognitive abilities
and other important linguistic parameters including the Age of Acquisition (AoA). However, the formulation of
credible Korean word frequency norms has been obstructed by the lack of expansive speech data and a reliable
part-of-speech (POS) tagger. In this study, we unveil Korean word frequency norms (KoFREN), derived from
large-scale spontaneous speech corpora (41 million words) that include a balanced representation of gender and
age. We employed a machine learning-powered POS tagger, showcasing accuracy on par with human annotators. Our frequency norms exhibit a significant correlation with lexical decision time (LDT) and AoA measures from external studies. KoFREN also aligns with English counterparts sourced from SUBTLEXUS - an English word frequency measure that has been frequently used in the literature. KoFREN is poised to facilitate research
in spontaneous Contemporary Korean and can be utilized in many fields, including clinical studies of Korean patients.

## How we calculated the frequency norms
We combined three corpora of spontaneous free speech from children, young adults, and elderly adults. The corpora are available for download at [AiHub](https://aihub.or.kr) (Korean nationals only). Transcripts of participants’ everyday conversations on topics such as food and travel are included in each corpus. We then used the [Bareun Tokenizer](https://bareun.ai) to tokenize the transcribed texts to count their lemma frequencies.


|           | FS_child | FS_young | FS_old   |
|-----------|----------|----------|----------|
| Speakers  | 1000     | 2000     | 1000     |
| Age Range | 3-10     | 11-59    | 60+      |
| Audio     | 3000 hrs | 4000 hrs | 3000 hrs |
| Words     | 11.2M    | 17.9M    | 11.8M    |
| Syllables | 28.9M    | 48.5M    | 31.0M    |

## How to use the frequency measures
The repository consists of four different files. `adult_frequency_counts_final.csv`, `elderly_frequency_counts_final.csv`, and `elderly_frequency_counts_final.csv` consist of word frequencies derived exclusively from each (children, young adults, elderly adults) corpus. `all_speakers_frequency_counts_final.csv` includes the word frequencies derived from the aggregations of all three corpora.

Each csv file contains the following columns. **WORD** and **POS_TAG** represents each word and its corresponding part-of-speech (POS) tag, automatically tagged by the [Bareun tokenizer](https://bareun.ai/docs). **COUNT** represents the raw word count within the Korean Free Speech corpus. **COUNT_ADJUST** is the scaled raw frequency count that aligns with the size of SUBTLEX_US, the gold-standard English word frequency norms (see our paper). **LOG10** contains the log10 values of these adjusted frequency counts.

## Citing the KoFREN Paper
If you used our work, please cite our paper, accepted to the [LREC-COLING 2024 Conference](https://lrec-coling-2024.org):
```
@inproceedings{kofren,
  title        = {KoFREN: Comprehensive Korean Word Frequency Norms Derived from Large Scale Free Speech Corpora},
  author       = {Jin-seo Kim, Anna Seo Gyeong Choi, and Sunghye Cho},
  year         = 2024,
  month        = {May},
  booktitle    = {Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING)},
  publisher    = {ACM Press},
}
```
