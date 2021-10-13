# PoC Nutrition

Table of index: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[🔍 | Queries notebook](https://github.com/theoprovost/poc_nutrition/blob/Th%C3%A9o/notebooks/queries.ipynb) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[🛠 | Data handling notebook](https://github.com/theoprovost/poc_nutrition/blob/Th%C3%A9o/notebooks/data_processing.ipynb) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📊 | EDA notebook](https://github.com/theoprovost/poc_nutrition/blob/Th%C3%A9o/notebooks/EDA.ipynb) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📖 | Methodological notes - Get started](#get_started) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[🔁 | Automate data collection](#auto) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[📺 | Presentation slides](https://slides.com/theoprvt/poc-nutrition/fullscreen) <br>

----
### 📖 | Methodological notes - Get started <a name='get_started'></a>

> 💡 The app needs Node.js. Make sure you have the LTS version.

#### Installation of MVP :
```shell
git clone <project-url>
cd <project_path>/app/backend

npm i
```
#### Start the app :
```shell
node|nodemon index
```

#### App endpoints :
The base URL is : `https://localhost:8443/`
|Endpoint|Description|
|:--:|:--|
|/|Main page, scan products and get results|
|/charts|Charts index|
|/charts/:id|Chart of id|

----
#### Features 📦
- [x] Search a product by it's barcode (via a camera)
- [x] Choose from a selection of nutrition habits/recommendations/food intolerance to check if the product is compliant
- [x] Retrieve data from reworked [Open food Facts data](https://fr.openfoodfacts.org/)

#### Considered features for V.1.*
- [ ] Define custom limitations
- [ ] Store history and provide custom stats and charts about habits
- [ ] Collect user data to do meta-analyze

----
#### 🔁 | Automate data collection <a name='auto'></a>

As asked, the data could be updated on a regular basis without further manipulation. This feature could be enable via a cron task.

> ***Nota Bene*** <br>
> For now, everytime the `handle_data.py` script is executed, it truncates the table, process the data then insert a fresh new copy. For performance concerns and data integrity, this may be changed in a near future.

```shell
# Written for Macintosh
# Everyday, at 6AM, download csv, store it
0 6 * * * curl https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv -o <path-to-folder-with-filename> && python <path-to-script>

# For instance
curl https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv -o /Users/theoprovost/Desktop/P11/data/en.openfoodfacts.org.products.csv  && python /Users/theoprovost/Desktop/P11/scripts/handle_data.py
```

-----
#### 📍 Deliverables reminder
- [x] Queries notebook
- [x] Data processing notebook
- [x] EDA notebook
- [ ] Methodological note
- [ ] Live presentation
