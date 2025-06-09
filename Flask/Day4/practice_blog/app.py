import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_smorest import Api
import yaml
from posts_routes import create_posts_blueprint

def load_config():
    """데이터베이스 설정을 로드합니다."""
    config_path = os.path.join(os.path.dirname(__file__), 'db.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 파일 파싱 오류: {e}")

def create_app():
    """Flask 애플리케이션을 생성하고 설정합니다."""
    app = Flask(__name__)
    
    # CORS 설정
    CORS(app)
    
    # 데이터베이스 설정
    db_config = load_config()
    app.config.update({
        'MYSQL_HOST': db_config['mysql_host'],
        'MYSQL_USER': db_config['mysql_user'],
        'MYSQL_PASSWORD': db_config['mysql_password'],
        'MYSQL_DB': db_config['mysql_db'],
        # API 문서 설정
        'API_TITLE': 'Blog API',
        'API_VERSION': 'v1',
        'OPENAPI_VERSION': '3.1.3',
        'OPENAPI_URL_PREFIX': '/',
        'OPENAPI_SWAGGER_UI_PATH': '/swagger-ui',
        'OPENAPI_SWAGGER_UI_URL': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/',
    })
    
    # MySQL 초기화
    mysql = MySQL(app)
    
    # API 및 Blueprint 설정
    api = Api(app)
    posts_blueprint = create_posts_blueprint(mysql)
    api.register_blueprint(posts_blueprint)
    
    # 라우트 설정
    @app.route('/blogs/')
    def manage_blogs():
        """블로그 관리 페이지를 렌더링합니다."""
        return render_template("posts.html")
    
    return app

def main():
    """애플리케이션을 실행합니다."""
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()