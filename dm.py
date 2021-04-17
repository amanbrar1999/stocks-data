import pandas as pd # for data manipulation
import numpy as np # for data manipulation

from sklearn.model_selection import train_test_split # for splitting the data into train and test samples
from sklearn.metrics import classification_report # for model evaluation metrics
from sklearn import tree # for decision tree models

import plotly.express as px  # for data visualization
import plotly.graph_objects as go # for data visualization
import graphviz # for plotting decision tree graphs

import pymysql

import os.path
from os import path





"""
------------------------------ Helper Functions ------------------------------
"""

def fitting(X, y, criterion, splitter, mdepth, clweight, minleaf):

    # Create training and testing samples
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Fit the model
    model = tree.DecisionTreeClassifier(criterion=criterion, 
                                        splitter=splitter, 
                                        max_depth=mdepth,
                                        class_weight=clweight,
                                        min_samples_leaf=minleaf, 
                                        random_state=0, 
                                  )
    clf = model.fit(X_train, y_train)

    # Predict class labels on training data
    pred_labels_tr = model.predict(X_train)
    # Predict class labels on a test data
    pred_labels_te = model.predict(X_test)

    # Tree summary and model evaluation metrics
    print('*************** Tree Summary ***************')
    print('Classes: ', clf.classes_)
    print('Tree Depth: ', clf.tree_.max_depth)
    print('No. of leaves: ', clf.tree_.n_leaves)
    print('No. of features: ', clf.n_features_)
    print('--------------------------------------------------------')
    print("")
    
    print('*************** Evaluation on Test Data ***************')
    score_te = model.score(X_test, y_test)
    print('Accuracy Score: ', score_te)
    # Look at classification report to evaluate the model
    print(classification_report(y_test, pred_labels_te))
    print('--------------------------------------------------------')
    print("")
    
    print('*************** Evaluation on Training Data ***************')
    score_tr = model.score(X_train, y_train)
    print('Accuracy Score: ', score_tr)
    # Look at classification report to evaluate the model
    print(classification_report(y_train, pred_labels_tr))
    print('--------------------------------------------------------')
    
    # Use graphviz to plot the tree
    dot_data = tree.export_graphviz(clf, out_file=None, 
                                feature_names=X.columns, 
                                class_names=[str(list(clf.classes_)[0]), str(list(clf.classes_)[1])],
                                filled=True, 
                                rounded=True, 
                                #rotate=True,
                               ) 
    graph = graphviz.Source(dot_data)
    
    # Return relevant data for chart plotting
    return X_train, X_test, y_train, y_test, clf, graph, model.feature_importances_


def Plot_3D(X, X_test, y_test, clf, x1, x2, mesh_size, margin):
            
    # Specify a size of the mesh to be used
    mesh_size=mesh_size
    margin=margin

    # Create a mesh grid on which we will run our model
    x_min, x_max = X.iloc[:, 0].fillna(X.mean()).min() - margin, X.iloc[:, 0].fillna(X.mean()).max() + margin
    y_min, y_max = X.iloc[:, 1].fillna(X.mean()).min() - margin, X.iloc[:, 1].fillna(X.mean()).max() + margin
    xrange = np.arange(x_min, x_max, mesh_size)
    yrange = np.arange(y_min, y_max, mesh_size)
    xx, yy = np.meshgrid(xrange, yrange)
            
    # Calculate predictions on grid
    Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    Z = Z.reshape(xx.shape)

    # Create a 3D scatter plot with predictions
    fig = px.scatter_3d(x=X_test[x1], y=X_test[x2], z=y_test,
                     opacity=0.8, color_discrete_sequence=['black'])

    # Set figure title and colors
    fig.update_layout(#title_text="Scatter 3D Plot with CART Prediction Surface",
                      paper_bgcolor = 'white',
                      scene = dict(xaxis=dict(title=x1,
                                              backgroundcolor='white',
                                              color='black',
                                              gridcolor='#f0f0f0'),
                                   yaxis=dict(title=x2,
                                              backgroundcolor='white',
                                              color='black',
                                              gridcolor='#f0f0f0'
                                              ),
                                   zaxis=dict(title='Probability of Rain Tomorrow',
                                              backgroundcolor='lightgrey',
                                              color='black', 
                                              gridcolor='#f0f0f0', 
                                              )))
    
    # Update marker size
    fig.update_traces(marker=dict(size=1))

    # Add prediction plane
    fig.add_traces(go.Surface(x=xrange, y=yrange, z=Z, name='CART Prediction',
                              colorscale='Jet',
                              reversescale=True,
                              showscale=False, 
                              contours = {"z": {"show": True, "start": 0.5, "end": 0.9, "size": 0.5}}))
    # fig.show()
    fig.savefig("decision_tree.png")
    return fig




print("------------- Running SQL queries to grab data from MySQL -------------")

"""
------------------------------ Data Preprocessing ------------------------------
"""

if not path.exists("output.csv"):
    conn = pymysql.connect(host='0.0.0.0', port=3307, user='root', passwd='root', db='test_db')
    # query = """
    # select
    # volume,
    # close>open as factor,
    # high/open>open/low as random_metrics,
    # volume>(select AVG(volume) from trade_histories) as volume_metrics,
    # high>(select AVG(high) from trade_histories) as high_metrics,
    # low>(select AVG(low) from trade_histories) as low_metrics
    # from trade_histories
    # """

    query = """
    select ticker, volume, open, high, low, close, close>open as factor from trade_histories
    """

    results = pd.read_sql_query(query, conn)
    results.to_csv("output.csv", index=False)

print("------------- Finished grabbing data from MySQL -------------")

# Set Pandas options to display more columns
pd.options.display.max_columns=50

# For other columns with missing values, fill them in with column mean
# df=df.fillna(df.mean())

print("------------- Starting the data preprocessing -------------")

if not path.exists("stage1_preprocessed_data.csv"):
    df=pd.read_csv('output.csv', encoding='utf-8')

    df['5_day_moving_volume_average'] = df.groupby('ticker', as_index=False)['volume'].transform(lambda x: x.rolling(5, 1).mean())
    df['5_day_moving_high_average'] = df.groupby('ticker', as_index=False)['high'].transform(lambda x: x.rolling(5, 1).mean())
    df['5_day_moving_low_average'] = df.groupby('ticker', as_index=False)['low'].transform(lambda x: x.rolling(5, 1).mean())
    df['5_day_moving_open_average'] = df.groupby('ticker', as_index=False)['open'].transform(lambda x: x.rolling(5, 1).mean())

    df['50_day_moving_volume_average'] = df.groupby('ticker', as_index=False)['volume'].transform(lambda x: x.rolling(50, 1).mean())
    df['50_day_moving_high_average'] = df.groupby('ticker', as_index=False)['high'].transform(lambda x: x.rolling(50, 1).mean())
    df['50_day_moving_low_average'] = df.groupby('ticker', as_index=False)['low'].transform(lambda x: x.rolling(50, 1).mean())
    df['50_day_moving_open_average'] = df.groupby('ticker', as_index=False)['open'].transform(lambda x: x.rolling(50, 1).mean())

    stage1_preprocessed_data = df[['ticker', 'volume', 'high', 'low', 'open', 'close', 'factor',
        '5_day_moving_volume_average', '5_day_moving_high_average', '5_day_moving_low_average', '5_day_moving_open_average', 
        '50_day_moving_volume_average', '50_day_moving_high_average', '50_day_moving_low_average', '50_day_moving_open_average']]
    stage1_preprocessed_data.to_csv("stage1_preprocessed_data.csv", index=False)

print("------------- Completed stage 1 preprocessing -------------")


if not path.exists("stage2_preprocessed_data.csv"):
    df=pd.read_csv('stage1_preprocessed_data.csv', encoding='utf-8')

    df['5_day_moving_volume_metric'] = (df['volume'] >= df['5_day_moving_volume_average']).astype(int)
    df['5_day_moving_high_metric'] = (df['high'] >= df['5_day_moving_high_average']).astype(int)
    df['5_day_moving_low_metric'] = (df['low'] >= df['5_day_moving_low_average']).astype(int)
    df['5_day_moving_open_metric'] = (df['open'] >= df['5_day_moving_open_average']).astype(int)

    df['50_day_moving_volume_metric'] = (df['5_day_moving_volume_average'] >= df['50_day_moving_volume_average']).astype(int)
    df['50_day_moving_high_metric'] = (df['5_day_moving_high_average'] >= df['50_day_moving_high_average']).astype(int)
    df['50_day_moving_low_metric'] = (df['5_day_moving_low_average'] >= df['50_day_moving_low_average']).astype(int)
    # 200day crossover with 50day: 50d>200d -> bullish | 50d<200d -> bearish
    df['50_day_moving_open_metric'] = (df['5_day_moving_open_average'] >= df['50_day_moving_open_average']).astype(int)

    stage2_preprocessed_data = df[['factor', '5_day_moving_volume_metric', '5_day_moving_high_metric', '5_day_moving_low_metric', '5_day_moving_open_metric',
                                    '50_day_moving_volume_metric', '50_day_moving_high_metric', '50_day_moving_low_metric', '50_day_moving_open_metric']]
    stage2_preprocessed_data.to_csv("stage2_preprocessed_data.csv", index=False)

print("------------- Completed stage 2 preprocessing -------------")






"""
------------------------------ Model Builder ------------------------------
"""

print("------------- Starting the Model Builder -------------")

df=pd.read_csv('stage2_preprocessed_data.csv', encoding='utf-8')
# Select data for modeling
X=df[['5_day_moving_volume_metric', '5_day_moving_high_metric', '5_day_moving_low_metric', '5_day_moving_open_metric',
    '50_day_moving_volume_metric', '50_day_moving_high_metric', '50_day_moving_low_metric', '50_day_moving_open_metric']]
y=df['factor'].values

# Fit the model and display results
X_train, X_test, y_train, y_test, clf, graph, importance = fitting(X, y, 'gini', 'best', 
                                                       mdepth=5, 
                                                       clweight=None,
                                                       minleaf=1000)

print("------------- Model Builder has finished -------------")

# Plot the tree graph
# graph

print("------------- Generating the Decision Tree -------------")

# Save tree graph to a PDF
graph.render('Decision_Tree_all_vars_gini')

print("------------- Generating Feature Importance Metrics -------------")

X = list(X.columns)

for i,v in enumerate(importance):
	# print('Feature: %0d, Score: %.5f' % (i,v))
    print("Feature: " + X[i])
    print('Score: %.5f' % (v))


# fig = Plot_3D(X, X_test, y_test, clf, x1='high', x2='volume', mesh_size=1, margin=1)