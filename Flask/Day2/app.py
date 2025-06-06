from flask import Flask
from flask_smorest import Api
from api import blp as books_blueprint

def create_app():
    app = Flask(__name__)
    
    # API 설정
    app.config["API_TITLE"] = "책 관리 API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    api = Api(app)
    
    # 책 관리 블루프린트 등록
    api.register_blueprint(books_blueprint)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)