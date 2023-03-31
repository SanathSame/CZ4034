# CZ4034-Information-Retrieval

## Project Overview

Using the wrong skincare products can cause significant harm to the skin. It is crucial to use products that cater to specific skin types and concerns, such as dryness, acne, and sensitivity, to avoid damaging the skin. Therefore, it is essential to develop a proper search engine for skincare products that take into account the user's specific skin type and concerns.

According to a study conducted by the American Academy of Dermatology, 34% of respondents reported having sensitive skin, and 44% reported having acne-prone skin. Using the wrong skincare product for these skin types can lead to adverse effects such as skin irritation, inflammation, and acne flare-ups. Another study by the University of Miami found that 85% of individuals who used skincare products without checking the ingredients first experienced skin irritation.

Furthermore, not all skincare products are suitable for all age groups. For instance, some anti-aging products contain retinoids, which are not recommended for individuals under the age of 25. Using such products can lead to skin damage and worsen the skin's condition.

Having a proper search engine for skincare products that caters to specific skin types and concerns can help users avoid such adverse effects. With advanced features such as filtering, recommendations, and ingredient analysis, users can make informed decisions about the products they choose to use.

In conclusion, developing a proper search engine for skincare products is essential to help users find the right products that cater to their specific skin type and concerns. The adverse effects of using the wrong skincare products, such as skin irritation, inflammation, and acne flare-ups, highlight the importance of using products that cater to specific skin types and concerns. With the help of a proper search engine for skincare products, users can avoid these adverse effects and maintain healthy skin.

## Project objectives

The objective of this project is to build an information retrieval system, specifically a search engine, for skincare products that caters to the user's specific skin type and age. The project aims to assist users in finding the right skincare product, as using the wrong product can have drastic effects on their skin.

Demo: https://youtu.be/3MM8Nxhb4WQ

## Technical details

### Tech stack

- Product Information/Review Retrival: Beautiful Soup, Python
- Frontend: ReactJS, HTML, CSS
- Backend: Flask (Python), Solr (Database - Indexing and querying tweets)
- Deep Learning modelling: Tensorflow, PyTorch, scikit-learn

### Frontend

For screenshot demo of the UI, refer to the Assignment Report

```
cd frontend/my-app/
npm install .
npm start
```

### Backend

1. Create virtual environment under backend folder and install libs:

```
python -m venv venv
venv/Scripts/activate - for window
pip install -r requirements.txt
```

2. Start the solr with "bin\solr.cmd start" command on Windows
3. Start Flask:

```
flask run
```

4. Unzip the weights.zip for model in folder backend/models/roberta

5. Other model weights can be found here:
   https://drive.google.com/drive/folders/10kl7DZ4wr5qKvBDq1dzzEfFfbJiuGdbB?usp=sharing

6. Run Solr under backend/Solr-8.11.1:
   `bin\solr.cmd start `

## Note:

1. Run all backends before starting frontend.
2. Run multiple ports in local will need to allow cross-origin. Please google how to fix this.
3. Create folder for classifiers under backend folder
