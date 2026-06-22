import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

# ============================================
# ОБУЧЕНИЕ МОДЕЛИ НА РЕАЛЬНЫХ ДАННЫХ
# ============================================

def train_model():
    """Обучение модели Random Forest на данных Titanic"""
    
    # Проверяем наличие файла
    if not os.path.exists('data/titanic.csv'):
        print("❌ Файл data/titanic.csv не найден!")
        print("📝 Запустите сначала: python load_real_titanic.py")
        return None
    
    # Загружаем данные
    try:
        df = pd.read_csv('data/titanic.csv')
        print(f"✅ Загружено {len(df)} записей")
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return None
    
    # ============================================
    # ПОДГОТОВКА ДАННЫХ
    # ============================================
    
    # Выбираем признаки
    X = df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']].copy()
    y = df['Survived']
    
    # Заполняем пропуски
    X['Age'] = X['Age'].fillna(X['Age'].median())
    X['Fare'] = X['Fare'].fillna(X['Fare'].median())
    X['Embarked'] = X['Embarked'].fillna('S')
    
    # Кодируем категориальные признаки
    le_sex = LabelEncoder()
    le_embarked = LabelEncoder()
    
    X['Sex'] = le_sex.fit_transform(X['Sex'])  # male=0, female=1
    X['Embarked'] = le_embarked.fit_transform(X['Embarked'])  # C=0, Q=1, S=2
    
    # Разделяем на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\n📊 Размер обучающей выборки: {len(X_train)}")
    print(f"📊 Размер тестовой выборки: {len(X_test)}")
    
    # ============================================
    # ОБУЧЕНИЕ МОДЕЛИ
    # ============================================
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # ============================================
    # ОЦЕНКА МОДЕЛИ
    # ============================================
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "=" * 50)
    print("📊 Titanic Survival Model Training")
    print("=" * 50)
    print(f"✅ Точность (Accuracy): {accuracy*100:.2f}%")
    
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\n📋 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # ============================================
    # СОХРАНЕНИЕ МОДЕЛИ
    # ============================================
    
    os.makedirs('model', exist_ok=True)
    
    model_data = {
        'model': model,
        'le_sex': le_sex,
        'le_embarked': le_embarked,
        'features': X.columns.tolist(),
        'accuracy': accuracy
    }
    
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✅ Модель сохранена в model/model.pkl")
    
    # ============================================
    # ТЕСТ НА ПРИМЕРАХ
    # ============================================
    
    print("\n📋 Тест на конкретных примерах:")
    test_cases = [
        (1, 'female', 25, 0, 0, 100, 'C', 'Богатая женщина 1-го класса'),
        (3, 'male', 25, 0, 0, 10, 'S', 'Бедный мужчина 3-го класса'),
        (2, 'female', 30, 1, 2, 50, 'Q', 'Женщина 2-го класса с семьей'),
        (1, 'male', 60, 0, 0, 80, 'C', 'Пожилой мужчина 1-го класса'),
        (3, 'female', 5, 1, 1, 20, 'S', 'Девочка 3-го класса с семьей'),
    ]
    
    for pclass, sex, age, sibsp, parch, fare, embarked, desc in test_cases:
        # Создаем DataFrame для теста
        test_df = pd.DataFrame({
            'Pclass': [pclass],
            'Sex': [sex],
            'Age': [age],
            'SibSp': [sibsp],
            'Parch': [parch],
            'Fare': [fare],
            'Embarked': [embarked]
        })
        
        # Кодируем
        test_df['Sex'] = le_sex.transform(test_df['Sex'])
        test_df['Embarked'] = le_embarked.transform(test_df['Embarked'])
        
        # Предсказываем
        pred = model.predict(test_df)[0]
        proba = model.predict_proba(test_df)[0][1]
        
        result = '✅ ВЫЖИВЕТ' if pred == 1 else '❌ НЕ ВЫЖИВЕТ'
        print(f"  {desc}: {result} (вероятность: {proba*100:.1f}%)")
    
    print("\n" + "=" * 50)
    print("🎉 ОБУЧЕНИЕ ЗАВЕРШЕНО!")
    print("=" * 50)
    
    return model, accuracy

# ============================================
# ЗАПУСК
# ============================================

if __name__ == '__main__':
    train_model()