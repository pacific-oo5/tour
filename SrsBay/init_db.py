from app import app, db
from models import User, MLModel
import hashlib
from datetime import datetime

def init_database():
    with app.app_context():
        db.create_all()
        print("✅ Структура таблиц успешно создана в файле titanic.db")
        
        if not User.query.filter_by(username='admin').first():
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            admin = User(username='admin', password_hash=password_hash, full_name='Администратор')
            db.session.add(admin)
            print("✅ Дефолтный пользователь добавлен (admin / admin123)")
            
        if not MLModel.query.first():
            model = MLModel(
                ModelVersion='v1.0', ModelName='Random Forest', Algorithm='RandomForestClassifier',
                TrainingDate=datetime.now().date(), AccuracyScore=0.82, AUC_ROC=0.86, F1_Score=0.78,
                IsActive=1, Description='Базовая модель Titanic'
            )
            db.session.add(model)
            print("✅ Запись о ML-модели добавлена в логи")
            
        db.session.commit()
        print("🎉 База данных полностью готова к работе!")

if __name__ == '__main__':
    init_database()