# Diversified, miniaturized and ancestral parts for mammalian genome engineering and molecular recording

Troy A. McDiarmid1,2,†,*, Megan L. Taylor1,2,†, Wei Chen1,2, Florence M. Chardon1,2, Junhong Choi1,2,3, Hanna Liao1,2, Xiaoyi Li1,2, Haedong Kim1,2, Jean-Benoît Lalanne1 , Tony Li1, Jenny F. Nathans1,2, Beth K. Martin1,2, Jordan Knuth2, Alessandro L.V. Coradini2, Jesse M. Gray2, Sudarshan Pinglay1,2,4, and Jay Shendure1,2,4,5,6*

Affiliations:
1. Department of Genome Sciences, University of Washington, Seattle, WA, USA
2. Seattle Hub for Synthetic Biology, Seattle, WA, USA
3. Developmental Biology Program, Memorial Sloan Kettering Cancer Center, New York, NY, USA
4. Brotman Baty Institute for Precision Medicine, Seattle, WA, USA
5. Howard Hughes Medical Institute, Seattle, WA, USA
6. Allen Discovery Center for Cell Lineage Tracing, Seattle, WA, USA

† These authors contributed equally to this work

* Correspondence to T.A.M. (troym13@uw.edu) or J.S. (shendure@uw.edu)

Abstract
As the synthetic biology and genome engineering fields mature and converge, there is a clear need for a “parts list” of components that are diversified with respect to both functional activity (to facilitate design) and sequence (to facilitate assembly). Here we designed libraries composed of extant, ancestral, mutagenized or miniaturized variants of Pol III promoters or guide RNA (gRNA) scaffolds and quantified their ability to mediate precise edits to the mammalian genome via multiplex prime editing. We identified thousands of parts that reproducibly drive a range of editing activities in human and mouse stem cells and cancer cell lines, including hundreds exhibiting similar or greater activity than the sequences used in conventional genome engineering constructs. We further conducted saturation mutagenesis screens of canonical Pol III promoters (U6p, 7SKp, H1p) and the prime editing guide RNA (pegRNA) scaffold, which identified tolerated variants that can be superimposed on baseline parts to further enhance sequence diversity. While characterizing thousands of orthologous promoters from hundreds of extant or ancestral genomes, we incidentally mapped related species with Pol III promoters that are highly active in human cells. Finally, to showcase the usefulness of these parts, we designed a “ten key” molecular recording array that lacks repetitive subsequences in order to facilitate its one-step assembly in yeast. Upon delivering this 15.8 kb tandem array of promoters and guides to mammalian cells, individual pegRNAs exhibited balanced activities as predicted by the activity of component parts, despite their relocation to a single locus. Looking forward, we anticipate that the diversified parts and variant effect maps reported here can be leveraged for the design, assembly and deployment of synthetic loci encoding arrays of gRNAs exhibiting predictable, differentiated levels of activity, which will be useful for multiplex perturbation, advanced biological recorders and complex genetic circuits.




This repository contains processed data, analysis code, and visualization code for "Diversified, miniaturized and ancestral parts for mammalian genome engineering and molecular recording". 

An example script used to extract sequence barcode counts from raw data (FASTQ files) is provided. Raw sequencing data have been uploaded on Sequencing Read Archive (SRA) with associated BioProject ID PRJNA1161643 (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1161643). 

The resulting .txt files of sequence barcode counts are then used to generate the processed data tables of edit scores and transcription scores. Edit scores = insertion barcode frequency / plasmid barcode frequency. Transcription scores = RNA barcode frequency / plasmid barcode frequency. These raw edit scores are then further normalized to account effects of specific barcode sequences on prime editing insertion efficiency (i.e. barcode normalized edit score = ((insertion barcode frequency / plasmid barcode frequency) / normalized_barcode_edit_score). See the manuscript for further details. 

The visualization scripts labeled "Fig1_Viz.Rmd", "Fig2_Viz.Rmd" etc. can then be used to recreate all visualizations in the manuscript. All processed edit score data and associated metadata required to recreate visualizations are provided in the final figure data set folders labeled "Fig1_Final_Figure_Datasets", "Fig2_Final_Figure_Datasets" etc. More formal edit score tables including relevant test sequences for all experiments are also availale in Tables S1-S12 in the manuscript. 

Note that we provide these mostly as a guide to see how we performed the analyses and to serve as an example for your own analyses. Most will require the installation of several tools that these scripts depend on and minor edits (e.g., adjusting local paths, folder structure).

We have also provided example sequence files for constructs used in this project (Pol III promoter and gRNA scaffold oligo sequences, amplicons for next-generation sequencing, etc.) in the "Construct_Sequences" folder of this repository. We also provide some example scripts used to design diversified part libraries and append sequences required for synthesis and cloning. 


