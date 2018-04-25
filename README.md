This is the project directory for my final project in IST 736 - Text Mining. For this project, I performed topic modeling 
on a self-collected dataset of all 4,032 ETDs (electronic theses and dissertations) from the Syracuse University institutional
repository, [SURFACE](http://surface.syr.edu/etd). Topic modeling was performed using two algorithms: [Latent Dirichlet Allocation
(LDA)](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) and 
[Non-negative Matrix Factorization (NMF)](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization) via 
[scikit-learn](http://scikit-learn.org/stable/), a Python library for Machine Learning.

#### Running the code

Download the project, install the requirements (`python -m pip install -r requirements.txt`), and run the topic_modeling.py script
(`python topic_modeling.py` or in an IDE).

#### Resources Directory

The K topics created by the topic models are located in `topics.txt`. 

The `ETD_metadata` directory is an *annotated* collection containing the title, department, keywords, and abstract for each ETD.
It is collected by running the `main()` function from the `scraper.py` script, which downloads the information using GET requests
from [http://surface.syr.edu/etd/](http://surface.syr.edu/etd/).

The `keystracts` directory is an *unannotated* collection of the keywords and abstracts for each ETD. This acts as the 
primary dataset of documents for topic modeling analysis. It is created by running the `write_keystracts()` function in the 
`deannotator.py` script.

#### Excel Directory

The Excel directory contains data and visuals (from said data) used in the final project report, including the 
topic diversity graph, raw frequency of ETDs by department, and top topics (by document count). 
