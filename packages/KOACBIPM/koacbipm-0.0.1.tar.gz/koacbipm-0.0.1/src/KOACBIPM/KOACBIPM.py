#model

def read_data_file():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'data.txt')
    data = pd.read_csv(data_path, delimiter = "\t")	
    return data

def predict_proba_rf(input_data,data=data):
    X = data.drop('OA', axis=1)
    y1 = data['OA']
    lab = preprocessing.LabelEncoder()
    y = lab.fit_transform(y1)
    pca = PCA(n_components=28, random_state=666)
    X_train = pca.fit_transform(X)
    model=HistGradientBoostingClassifier(class_weight='balanced',min_samples_leaf=10max_iter=130, max_depth=3, learning_rate=0.4387179487179487, l2_regularization=0.001,random_state=666)
    hg_model=model.fit(X_train,y)
    X_test = pca.fit_transform(input_data)
    predicted_proba = model.predict_proba(X_test)
    return predicted_proba
    
    
