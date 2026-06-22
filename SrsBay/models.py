from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Passenger(db.Model):
    __tablename__ = 'passengers'
    PassengerId = db.Column(db.Integer, primary_key=True)
    Pclass = db.Column(db.Integer)
    Sex = db.Column(db.String(10))
    Age = db.Column(db.Float)
    SibSp = db.Column(db.Integer)
    Parch = db.Column(db.Integer)
    Fare = db.Column(db.Float)
    Embarked = db.Column(db.String(1))
    Survived = db.Column(db.Integer)

class PredictionLog(db.Model):
    __tablename__ = 'prediction_logs'
    LogID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'))
    Pclass = db.Column(db.Integer)
    Sex = db.Column(db.String(10))
    Age = db.Column(db.Float)
    SibSp = db.Column(db.Integer)
    Parch = db.Column(db.Integer)
    Fare = db.Column(db.Float)
    Embarked = db.Column(db.String(1))
    Predicted = db.Column(db.Integer)
    Probability = db.Column(db.Float)
    PredictionDate = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200))
    
    predictions = db.relationship('PredictionLog', backref='user', lazy=True)

class MLModel(db.Model):
    __tablename__ = 'ml_models'
    ModelID = db.Column(db.Integer, primary_key=True)
    ModelVersion = db.Column(db.String(20))
    ModelName = db.Column(db.String(100))
    Algorithm = db.Column(db.String(100))
    TrainingDate = db.Column(db.Date)
    AccuracyScore = db.Column(db.Float)
    AUC_ROC = db.Column(db.Float)
    F1_Score = db.Column(db.Float)
    IsActive = db.Column(db.Integer, default=0)
    Description = db.Column(db.String(500))