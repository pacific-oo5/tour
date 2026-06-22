import pandas as pd
import numpy as np
from app import app, db
from models import Passenger

def load_titanic_data():
    """Загрузка данных Titanic в базу данных"""
    
    # Создаем данные если файла нет
    try:
        df = pd.read_csv('data/titanic.csv')
    except:
        # Генерируем данные
        np.random.seed(42)
        n = 891
        
        data = {
            'PassengerId': np.arange(1, n+1),
            'Pclass': np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
            'Sex': np.random.choice(['male', 'female'], n, p=[0.65, 0.35]),
            'Age': np.random.normal(30, 14, n),
            'SibSp': np.random.choice([0, 1, 2, 3, 4, 5], n, p=[0.68, 0.23, 0.03, 0.03, 0.02, 0.01]),
            'Parch': np.random.choice([0, 1, 2, 3, 4, 5], n, p=[0.76, 0.13, 0.09, 0.01, 0.005, 0.005]),
            'Fare': np.random.exponential(30, n),
            'Embarked': np.random.choice(['C', 'Q', 'S'], n, p=[0.19, 0.09, 0.72])
        }
        
        df = pd.DataFrame(data)
        
        def get_survival(row):
            survival_chance = 0.38
            if row['Pclass'] == 1:
                survival_chance += 0.25
            elif row['Pclass'] == 2:
                survival_chance += 0.10
            else:
                survival_chance -= 0.15
            if row['Sex'] == 'female':
                survival_chance += 0.30
            else:
                survival_chance -= 0.20
            if row['Age'] < 10:
                survival_chance += 0.15
            elif row['Age'] > 60:
                survival_chance -= 0.10
            if row['SibSp'] + row['Parch'] > 3:
                survival_chance -= 0.10
            elif row['SibSp'] + row['Parch'] == 0:
                survival_chance -= 0.05
            if row['Embarked'] == 'C':
                survival_chance += 0.05
            elif row['Embarked'] == 'S':
                survival_chance -= 0.05
            survival_chance += np.random.normal(0, 0.05)
            return 1 if np.random.random() < survival_chance else 0
        
        df['Survived'] = df.apply(get_survival, axis=1)
        df['Age'] = df['Age'].clip(0.5, 80).round(1)
        df['Fare'] = df['Fare'].clip(0, 300).round(2)
        
        # Сохраняем CSV
        import os
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/titanic.csv', index=False)
        print(f"✅ Создан файл data/titanic.csv ({len(df)} записей)")
    
    with app.app_context():
        # Очищаем таблицу
        db.session.query(Passenger).delete()
        
        # Загружаем данные
        count = 0
        for _, row in df.iterrows():
            passenger = Passenger(
                PassengerId=int(row['PassengerId']),
                Pclass=int(row['Pclass']),
                Sex=row['Sex'],
                Age=float(row['Age']) if pd.notna(row['Age']) else None,
                SibSp=int(row['SibSp']),
                Parch=int(row['Parch']),
                Fare=float(row['Fare']) if pd.notna(row['Fare']) else 0,
                Embarked=row['Embarked'] if pd.notna(row['Embarked']) else 'S',
                Survived=int(row['Survived'])
            )
            db.session.add(passenger)
            count += 1
        
        db.session.commit()
        print(f"✅ Загружено {count} пассажиров в базу данных")
        
        # Статистика
        survived = db.session.query(Passenger).filter_by(Survived=1).count()
        print(f"   Выжило: {survived} ({survived/count*100:.1f}%)")
        print(f"   Погибло: {count - survived} ({(count - survived)/count*100:.1f}%)")

if __name__ == '__main__':
    load_titanic_data()