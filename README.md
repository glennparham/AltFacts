## AltFacts

This is a project from ScaleAI's Generative AI Hackathon on July 15, 2023.

Contributors: Glenn Parham, Josh Marks, Parul Singh, Jim Salsman

### How To Run

1. Initialize up your python virutal env:

   `python3 -m venv myenv`

2. Activate your virtual env:

   `source myenv/bin/activate`

3. Install the requirements:

   `pip install -r requirements.txt`

4. Run main.py

   `python3 main.py`

## Process

1. Pass to AltFacts the text you'd like to be verified.
2. AltFacts uses paperQA to identify relevant citations (if applicable).
3. We transpose these citations into a pandas dataframe.
4. We run meta-analysis of these citations to determine (source credibility, bias, etc.)

## Sample PDFs

- [Trump's Indictment](https://www.justice.gov/storage/US_v_Trump-Nauta_23-80101.pdf)
