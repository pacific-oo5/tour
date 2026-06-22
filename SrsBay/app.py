from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
import pickle
import hashlib
from functools import wraps
from datetime import datetime

from models import db, User, Passenger, PredictionLog, MLModel

app = Flask(__name__)
app.secret_key = 'super_secret_key_titanic_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///titanic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    user = None
    if 'logged_in' in session and session['logged_in']:
        user = {
            'username': session.get('username'),
            'user_id': session.get('user_id'),
            'full_name': session.get('full_name')
        }
    return dict(current_user=user)

def load_and_prepare_data():
    if os.path.exists('data/titanic.csv'):
        df = pd.read_csv('data/titanic.csv')
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
    
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
    df['Embarked'] = df['Embarked'].fillna('S')
    
    df_vis = df.copy()
    df_vis['Survived'] = df_vis['Survived'].map({0: 'Погиб', 1: 'Выжил'})
    return df, df_vis

def generate_plots(df, df_vis):
    plots = {}
    
    # 1. Круговая диаграмма
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    df_vis['Survived'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#ff6b6b', '#51cf66'], ax=ax1, explode=[0.05, 0.05], shadow=True)
    ax1.set_title('Распределение выживших пассажиров')
    ax1.set_ylabel('')
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', bbox_inches='tight', dpi=100)
    buf1.seek(0)
    plots['pie_survived'] = base64.b64encode(buf1.read()).decode('utf-8')
    plt.close()
    
    # 2. Выживаемость по классам
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    class_surv = df.groupby('Pclass')['Survived'].mean() * 100
    class_surv.plot(kind='bar', color=['#4dabf7', '#ffd43b', '#ff6b6b'], ax=ax2)
    ax2.set_title('Выживаемость по классам (%)')
    ax2.set_ylim(0, 100)
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', bbox_inches='tight', dpi=100)
    buf2.seek(0)
    plots['bar_pclass'] = base64.b64encode(buf2.read()).decode('utf-8')
    plt.close()

    # 3. Выживаемость по полу
    fig3, ax3 = plt.subplots(figsize=(6, 5))
    sex_surv = df.groupby('Sex')['Survived'].mean() * 100
    sex_surv.plot(kind='bar', color=['#339af0', '#f06595'], ax=ax3)
    ax3.set_title('Выживаемость по полу (%)')
    ax3.set_ylim(0, 100)
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png', bbox_inches='tight', dpi=100)
    buf3.seek(0)
    plots['bar_sex'] = base64.b64encode(buf3.read()).decode('utf-8')
    plt.close()

    # 4. Распределение возраста
    fig4, ax4 = plt.subplots(figsize=(6, 5))
    ax4.hist(df[df['Survived'] == 0]['Age'], bins=20, alpha=0.6, label='Погиб', color='#ff6b6b')
    ax4.hist(df[df['Survived'] == 1]['Age'], bins=20, alpha=0.6, label='Выжил', color='#51cf66')
    ax4.set_title('Распределение возраста')
    ax4.legend()
    buf4 = io.BytesIO()
    plt.savefig(buf4, format='png', bbox_inches='tight', dpi=100)
    buf4.seek(0)
    plots['hist_age'] = base64.b64encode(buf4.read()).decode('utf-8')
    plt.close()

    # 5. Распределение цены билета
    fig5, ax5 = plt.subplots(figsize=(6, 5))
    ax5.hist(df[df['Survived'] == 0]['Fare'], bins=30, alpha=0.6, label='Погиб', color='#ff6b6b')
    ax5.hist(df[df['Survived'] == 1]['Fare'], bins=30, alpha=0.6, label='Выжил', color='#51cf66')
    ax5.set_title('Распределение цены билета')
    ax5.set_xlim(0, 200)
    ax5.legend()
    buf5 = io.BytesIO()
    plt.savefig(buf5, format='png', bbox_inches='tight', dpi=100)
    buf5.seek(0)
    plots['hist_fare'] = base64.b64encode(buf5.read()).decode('utf-8')
    plt.close()

    # 6. Scatter plot
    fig6, ax6 = plt.subplots(figsize=(6, 5))
    colors6 = ['#ff6b6b' if s == 0 else '#51cf66' for s in df['Survived']]
    ax6.scatter(df['Age'], df['Fare'], c=colors6, alpha=0.6)
    ax6.set_title('Возраст vs Цена билета')
    ax6.set_xlim(0, 80)
    ax6.set_ylim(0, 200)
    buf6 = io.BytesIO()
    plt.savefig(buf6, format='png', bbox_inches='tight', dpi=100)
    buf6.seek(0)
    plots['scatter_age_fare'] = base64.b64encode(buf6.read()).decode('utf-8')
    plt.close()

    # 7. Heatmap
    fig7, ax7 = plt.subplots(figsize=(6, 5))
    sns.heatmap(df[['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Survived']].corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax7)
    ax7.set_title('Матрица корреляций')
    buf7 = io.BytesIO()
    plt.savefig(buf7, format='png', bbox_inches='tight', dpi=100)
    buf7.seek(0)
    plots['heatmap'] = base64.b64encode(buf7.read()).decode('utf-8')
    plt.close()

    # 8. Выживаемость по портам
    fig8, ax8 = plt.subplots(figsize=(6, 5))
    df.groupby('Embarked')['Survived'].mean().plot(kind='bar', color=['#4dabf7', '#ffd43b', '#ff6b6b'], ax=ax8)
    ax8.set_title('Выживаемость по портам (%)')
    buf8 = io.BytesIO()
    plt.savefig(buf8, format='png', bbox_inches='tight', dpi=100)
    buf8.seek(0)
    plots['bar_embarked'] = base64.b64encode(buf8.read()).decode('utf-8')
    plt.close()

    # 9. Линейный по возрасту
    fig9, ax9 = plt.subplots(figsize=(6, 5))
    df.groupby(pd.cut(df['Age'], bins=range(0, 85, 10)))['Survived'].mean().plot(kind='line', marker='o', ax=ax9)
    ax9.set_title('Выживаемость по возрастам')
    buf9 = io.BytesIO()
    plt.savefig(buf9, format='png', bbox_inches='tight', dpi=100)
    buf9.seek(0)
    plots['line_age'] = base64.b64encode(buf9.read()).decode('utf-8')
    plt.close()

    # 10. Количество по классам
    fig10, ax10 = plt.subplots(figsize=(6, 5))
    df['Pclass'].value_counts().sort_index().plot(kind='bar', color=['#4dabf7', '#ffd43b', '#ff6b6b'], ax=ax10)
    ax10.set_title('Количество пассажиров по классам')
    buf10 = io.BytesIO()
    plt.savefig(buf10, format='png', bbox_inches='tight', dpi=100)
    buf10.seek(0)
    plots['bar_pclass_count'] = base64.b64encode(buf10.read()).decode('utf-8')
    plt.close()

    return plots

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        
        if not username or not password:
            flash('Все поля обязательны!', 'danger')
            return render_template('register.html')
            
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким логином уже существует!', 'danger')
            return render_template('register.html')
            
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(username=username, password_hash=password_hash, full_name=full_name or username)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна! Войдите.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')  # Синхронизировано с name="login" в HTML
        password = request.form.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = User.query.filter_by(username=username, password_hash=password_hash).first()
        if user:
            session['logged_in'] = True
            session['username'] = user.username
            session['user_id'] = user.id
            session['full_name'] = user.full_name
            flash(f'Добро пожаловать, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный логин или пароль!', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    df, df_vis = load_and_prepare_data()
    total = len(df)
    survived = int(df['Survived'].sum())
    not_survived = total - survived
    survival_rate = (survived / total * 100)
    plots = generate_plots(df, df_vis)
    return render_template('dashboard.html', total=total, survived=survived, not_survived=not_survived, survival_rate=survival_rate, plots=plots)

@app.route('/eda')
@login_required
def eda():
    df, df_vis = load_and_prepare_data()
    plots = generate_plots(df, df_vis)
    return render_template('eda.html', plots=plots)

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
            # Безопасное получение числовых данных с защитой от пустых строк ''
            pclass_raw = request.form.get('pclass')
            pclass = int(pclass_raw) if pclass_raw and pclass_raw.strip() else 2
            
            gender_text = request.form.get('sex', 'male')
            embarked_text = request.form.get('embarked', 'S')
            
            age_raw = request.form.get('age')
            age = float(age_raw) if age_raw and age_raw.strip() else 29.7
            
            sibsp_raw = request.form.get('siblings')
            sibsp = int(sibsp_raw) if sibsp_raw and sibsp_raw.strip() else 0
            
            parch_raw = request.form.get('parents')
            parch = int(parch_raw) if parch_raw and parch_raw.strip() else 0
            
            fare_raw = request.form.get('fare')
            fare = float(fare_raw) if fare_raw and fare_raw.strip() else 32.20
            
            with open('model/model.pkl', 'rb') as f:
                model_data = pickle.load(f)
                
            model = model_data['model']
            le_sex = model_data['le_sex']
            le_embarked = model_data['le_embarked']
            
            encoded_sex = le_sex.transform([gender_text])[0]
            encoded_embarked = le_embarked.transform([embarked_text])[0]
            
            input_df = pd.DataFrame([{
                'Pclass': pclass, 'Sex': encoded_sex, 'Age': age,
                'SibSp': sibsp, 'Parch': parch, 'Fare': fare, 'Embarked': encoded_embarked
            }])
            
            probabilities = model.predict_proba(input_df)[0]
            prob_surv = float(probabilities[1])
            prob_death = float(probabilities[0])
            predicted_outcome = int(model.predict(input_df)[0])
            
            log = PredictionLog(
                UserID=session['user_id'], Pclass=pclass, Sex=gender_text, Age=age,
                SibSp=sibsp, Parch=parch, Fare=fare, Embarked=embarked_text,
                Predicted=predicted_outcome, Probability=prob_surv
            )
            db.session.add(log)
            db.session.commit()
            
            result_obj = {
                'survived': bool(predicted_outcome),
                'probability': prob_surv,
                'probability_death': prob_death
            }
            
            return render_template('result.html', 
                                   result=result_obj, pclass=pclass, sex=gender_text, 
                                   age=age, fare=fare, embarked=embarked_text,
                                   spouse=1 if sibsp > 0 else 0, siblings=sibsp, 
                                   parents=parch, children=0, sibsp=sibsp, parch=parch)
                                   
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка вычислений: {str(e)}', 'danger')
            return render_template('predict.html')
            
    return render_template('predict.html')

@app.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    pagination = PredictionLog.query.filter_by(UserID=session['user_id'])\
        .order_by(PredictionLog.PredictionDate.desc())\
        .paginate(page=page, per_page=10, error_out=False)
        
    logs = pagination.items
    predictions = []
    for l in logs:
        predictions.append((
            l.LogID, l.Pclass, l.Sex, l.Age, l.SibSp, l.Parch, l.Fare, l.Embarked, l.Predicted, l.Probability, l.PredictionDate.strftime('%d.%m.%Y %H:%M')
        ))
    return render_template('history.html', predictions=predictions, pagination=pagination)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=session.get('username'), full_name=session.get('full_name'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)