## What is the `dataidea` package?

This is a package we are currently developing to help new and old data analysists (especially DATAIDEA students) walk around some repetitive and sometimes disturbing tasks that a data analyst does day to day

This library currently extends and depends on majorly numpy, pandas as sklearn and these, among a few others will be installed once you install dataidea

## Installing `dataidea`

- To install dataidea, you must have python installed on your machine
- It's advised that you install it in a virtual environment
- You can install `dataidea` using the command below

```
pip install dataidea
```

## Learning `dataidea`

The best way to get started with dataidea (and data analysis) is to complete the free course.

To see what’s possible with dataidea, take a look at the Quick Start

Read through the Tutorials to learn how to load datasets, train your own models on your own datasets. Use the navigation to look through the dataidea documentation. Every class, function, and method is documented here.

## Quickstart

```python
from dataidea.tabular import *
```

`dataidea`'s applications all use the same basic steps and code:

- Create appropriate DataLoaders
- Create a Trainer
- Call a fit method
- Make predictions or view results.

In this quick start, we’ll show these steps for classification and regression. As you’ll see, the code in each case is extremely similar, despite the very different models and data being used.

## Loading datasets

`dataidea` library makes loading the most common used dataset in the course easy, but also allows for loading personal dataset with one or 2 tweeks.

In the line of code below, we load the simple music dataset which inbuilt into dataidea for learning purposes

```python
music_data = loadDataset(name='music')
```

We can see some values inside by using our usual `pandas` dataframe methods like `sample()`, `head()`, `tail()` etc

```python
music_data.sample(n=5)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>gender</th>
      <th>genre</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3</th>
      <td>26</td>
      <td>1</td>
      <td>Jazz</td>
    </tr>
    <tr>
      <th>2</th>
      <td>25</td>
      <td>1</td>
      <td>HipHop</td>
    </tr>
    <tr>
      <th>14</th>
      <td>30</td>
      <td>0</td>
      <td>Acoustic</td>
    </tr>
    <tr>
      <th>1</th>
      <td>23</td>
      <td>1</td>
      <td>HipHop</td>
    </tr>
    <tr>
      <th>19</th>
      <td>35</td>
      <td>1</td>
      <td>Classical</td>
    </tr>
  </tbody>
</table>
</div>

We can then create `TabularDataLoader` that allows for easy data manipulation like feature scaling, imputation and splitting for training etc, we use this to quickly prepare and load the data to a machine learning model

```python
music_data_loader = TabularDataLoader(data=music_data,
                                numeric_features=['  age '],
                                categorical_features=['gender'],
                                outcome='genre'
                               )
```

We can (optionally) process the data, however this step is gonna be done for you once you decide to train a machine learning model

```python
transformed_data, transformer = music_data_loader.transform()
```

```python
transformed_data[0].head()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>num__  age</th>
      <th>cat__gender_0</th>
      <th>cat__gender_1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.637262</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.204658</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-0.818631</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-0.613973</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1.227947</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>

Now we can fit a machine learning model, behind the scenes, the `Trainer` has some code to work with the `TabularDataLoader` to process your data quite thorouly, standardizing and imputing and the resulting model is actually a pipeline of these steps.

```python
trainer = Trainer(data_loader=music_data_loader, model=RandomForestClassifier())
```

To train our model, we just call the `train()` method on the trainer object

```python
model = trainer.train()
```

We can obtain the accuracy real fast, this is obtained from a test set which is automatically picked from you data by the `TabularDataLoader`

```python
accuracy = trainer.evaluate()
```

Some times accuracy isn't the best measure for model performance, we can also use a classification report for classification problems

```python
classification_report = trainer.report()
```

```python
classification_report
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>precision</th>
      <th>recall</th>
      <th>f1-score</th>
      <th>support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Acoustic</th>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>Classical</th>
      <td>1.000000</td>
      <td>0.500000</td>
      <td>0.666667</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>HipHop</th>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>accuracy</th>
      <td>0.750000</td>
      <td>0.750000</td>
      <td>0.750000</td>
      <td>0.75</td>
    </tr>
    <tr>
      <th>macro avg</th>
      <td>0.666667</td>
      <td>0.833333</td>
      <td>0.555556</td>
      <td>4.00</td>
    </tr>
    <tr>
      <th>weighted avg</th>
      <td>1.000000</td>
      <td>0.750000</td>
      <td>0.833333</td>
      <td>4.00</td>
    </tr>
  </tbody>
</table>
</div>

It's easy to save a model for future use, you can use the `save()` method on the traner

```python
trainer.save(path='music_model.di')
```

Now (in future) we can load our saved model for prediction

```python
loaded_model = loadModel(filename='music_model.di')
```

Now let's make some predictions on some data

```python
data_to_predict = pd.DataFrame(
    data={
        '  age ': [20, 35],
        'gender': [1, 0]
    })

data_to_predict
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>gender</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>35</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

```python
predicted = loaded_model.predict(X=data_to_predict)
```

```python
data_to_predict['predicted'] = predicted
```

```python
data_to_predict
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>gender</th>
      <th>predicted</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20</td>
      <td>1</td>
      <td>HipHop</td>
    </tr>
    <tr>
      <th>1</th>
      <td>35</td>
      <td>0</td>
      <td>Classical</td>
    </tr>
  </tbody>
</table>
</div>

```python

```
