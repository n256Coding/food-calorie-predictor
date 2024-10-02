# Data Analysis and Dashboard
This is a data dashboard which is built on Python using streamlit package.

## Prerequisits
These are the prerequisites that that should meet before runnnig this application and notebook.
* Python 3.11 or later
* Jupyter notebook along with jupyter kernel
* Anaconda

## Steps to Start
* Create a new anaconda environment.
  ```bash
  conda create --name com725_project python=3.11
  conda activate com725_project
  ```

* Install required libraries for dashboard.
  ```bash
  pip install pandas seaborn matplotlib squarify numpy scikit-learn
  ```

* Install required libraries for jupyter notebook file.
  ```bash
  pip install streamlit plotly
  ```

* Run the dashboard.
  ```bash
  streamlit run data_dashboard.py
  ```


## Dataset Files
* `nutrition dataset.csv` is the original dataset which was downloded from the (data.world)[https://data.world/craigkelly/usda-national-nutrient-db]
* `preprocessed_nutrition_dataset.csv` is the preprocessed dataset out of the original dataset. this is used in dashboard.
