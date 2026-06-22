import pickle
import pandas as pd
import numpy as np

class TitanicPredictor:
    def __init__(self):
        self.model = None
        self.le_sex = None
        self.le_embarked = None
        self.features = None
        self.load_model()
    
    def load_model(self):
        try:
            with open('model/model.pkl', 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.le_sex = data['le_sex']
                self.le_embarked = data['le_embarked']
                self.features = data['features']
            return True
        except Exception as e:
            print(f"❌ Ошибка загрузки модели: {e}")
            return False
    
    def predict(self, pclass, sex, age, sibsp, parch, fare, embarked):
        # Подготовка данных
        data = pd.DataFrame({
            'Pclass': [pclass],
            'Sex': [sex],
            'Age': [age],
            'SibSp': [sibsp],
            'Parch': [parch],
            'Fare': [fare],
            'Embarked': [embarked]
        })
        
        # Кодирование
        data['Sex'] = self.le_sex.transform(data['Sex'])
        data['Embarked'] = self.le_embarked.transform(data['Embarked'])
        
        # Заполнение пропусков
        data['Age'] = data['Age'].fillna(data['Age'].median())
        data['Fare'] = data['Fare'].fillna(data['Fare'].median())
        
        # Предсказание
        probability = self.model.predict_proba(data)[0]
        prediction = self.model.predict(data)[0]
        
        return {
            'survived': bool(prediction),
            'probability': float(probability[1]),
            'probability_death': float(probability[0])
        }