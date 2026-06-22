import pandas as pd
import numpy as np
import os
import urllib.request
from app import app
from models import db, Passenger

def download_real_titanic():
    os.makedirs('data', exist_ok=True)
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
    file_path = 'data/titanic_real.csv'
    
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"✅ Файл скачан: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        return None

def load_titanic_data():
    if not os.path.exists('data/titanic_real.csv'):
        download_real_titanic()
    
    df = pd.read_csv('data/titanic_real.csv')
    
    print("=" * 60)
    print("📊 РЕАЛЬНЫЕ ДАННЫЕ ТИТАНИКА")
    print("=" * 60)
    print(f"📋 Всего пассажиров: {len(df)}")
    print(f"📋 Выжило: {df['Survived'].sum()} ({df['Survived'].mean()*100:.1f}%)")
    print(f"📋 Погибло: {len(df) - df['Survived'].sum()} ({(1 - df['Survived'].mean())*100:.1f}%)")
    
    with app.app_context():
        db.session.query(Passenger).delete()
        
        count = 0
        for _, row in df.iterrows():
            passenger = Passenger(
                PassengerId=int(row['PassengerId']),
                Pclass=int(row['Pclass']),
                Sex=row['Sex'],
                Age=float(row['Age']) if pd.notna(row['Age']) else None,
                SibSp=int(row['SibSp']) if pd.notna(row['SibSp']) else 0,
                Parch=int(row['Parch']) if pd.notna(row['Parch']) else 0,
                Fare=float(row['Fare']) if pd.notna(row['Fare']) else 0,
                Embarked=row['Embarked'] if pd.notna(row['Embarked']) else 'S',
                Survived=int(row['Survived'])
            )
            db.session.add(passenger)
            count += 1
        
        db.session.commit()
        print(f"\n✅ Загружено {count} пассажиров в базу данных")
    
    df.to_csv('data/titanic.csv', index=False)
    print("✅ Данные сохранены в data/titanic.csv")
    return df

if __name__ == '__main__':
    load_titanic_data()