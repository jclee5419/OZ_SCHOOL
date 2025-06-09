from flask import request, jsonify
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 스키마 정의
class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    content = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)

class PostUpdateSchema(Schema):
    title = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    content = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)

def create_posts_blueprint(mysql):
    """게시글 관련 Blueprint를 생성합니다."""
    posts_blp = Blueprint(
        "posts",
        __name__,
        description="게시글 관리 API",
        url_prefix="/api/posts",
    )
    
    def get_cursor():
        """데이터베이스 커서를 반환합니다."""
        return mysql.connection.cursor()
    
    def execute_query(cursor, query, params=None, fetch_type='all'):
        """
        쿼리를 실행하고 결과를 반환합니다.
        
        Args:
            cursor: 데이터베이스 커서
            query: 실행할 SQL 쿼리
            params: 쿼리 파라미터
            fetch_type: 'all', 'one', 'none' 중 하나
        """
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_type == 'all':
                return cursor.fetchall()
            elif fetch_type == 'one':
                return cursor.fetchone()
            else:
                return None
        except Exception as e:
            logger.error(f"데이터베이스 쿼리 실행 오류: {e}")
            mysql.connection.rollback()
            raise
    
    def format_post(post_tuple):
        """게시글 튜플을 딕셔너리로 변환합니다."""
        if not post_tuple:
            return None
        return {
            "id": post_tuple[0],
            "title": post_tuple[1],
            "content": post_tuple[2],
        }
    
    def validate_post_exists(cursor, post_id):
        """게시글 존재 여부를 확인합니다."""
        query = "SELECT id FROM posts WHERE id = %s"
        result = execute_query(cursor, query, (post_id,), 'one')
        if not result:
            abort(404, message="해당 게시글을 찾을 수 없습니다.")
        return result

    # GET 요청 (게시글 목록 조회)
    @posts_blp.route("/", methods=["GET"])
    @posts_blp.response(200, PostSchema(many=True))
    def get_posts():
        """게시글 목록 조회"""
        cursor = get_cursor()
        
        try:
            query = "SELECT id, title, content FROM posts ORDER BY id DESC"
            posts_data = execute_query(cursor, query)
            
            post_list = [format_post(post) for post in posts_data]
            return jsonify(post_list)
                
        except Exception as e:
            logger.error(f"게시글 조회 중 오류 발생: {e}")
            abort(500, message="서버 내부 오류가 발생했습니다.")
        finally:
            cursor.close()

    # POST 요청 (새 게시글 생성)
    @posts_blp.route("/", methods=["POST"])
    @posts_blp.arguments(PostSchema, location='json', as_kwargs=True)
    @posts_blp.response(201, PostSchema)
    def create_post(**kwargs):
        """새 게시글 생성"""
        cursor = get_cursor()
        
        try:
            title = kwargs.get('title', '').strip()
            content = kwargs.get('content', '').strip()
            
            if not title or not content:
                abort(400, message="제목과 내용은 필수 입력 항목입니다.")
            
            query = "INSERT INTO posts (title, content) VALUES (%s, %s)"
            execute_query(cursor, query, (title, content), 'none')
            mysql.connection.commit()
            
            logger.info(f"새 게시글 생성 완료: {title}")
            return jsonify({"message": "게시글이 성공적으로 생성되었습니다."}), 201
                
        except Exception as e:
            logger.error(f"게시글 생성 중 오류 발생: {e}")
            abort(500, message="서버 내부 오류가 발생했습니다.")
        finally:
            cursor.close()

    @posts_blp.route("/<int:post_id>", methods=["GET", "PUT", "DELETE"])
    def post_detail(post_id, **kwargs):
        """게시글 상세 조회, 수정, 삭제"""
        cursor = get_cursor()
        
        try:
            if request.method == "GET":
                query = "SELECT id, title, content FROM posts WHERE id = %s"
                post_data = execute_query(cursor, query, (post_id,), 'one')
                
                if not post_data:
                    abort(404, message="해당 게시글을 찾을 수 없습니다.")
                
                return jsonify(format_post(post_data))
            
            elif request.method == "PUT":
                # JSON 데이터 직접 파싱
                data = request.get_json() or {}
                title = data.get('title', '').strip()
                content = data.get('content', '').strip()
                
                if not title or not content:
                    abort(400, message="제목과 내용은 필수 입력 항목입니다.")
                
                # 게시글 존재 확인
                validate_post_exists(cursor, post_id)
                
                query = "UPDATE posts SET title = %s, content = %s WHERE id = %s"
                execute_query(cursor, query, (title, content, post_id), 'none')
                mysql.connection.commit()
                
                logger.info(f"게시글 수정 완료: ID {post_id}")
                return jsonify({"message": "게시글이 성공적으로 수정되었습니다."})
            
            elif request.method == "DELETE":
                # 게시글 존재 확인
                validate_post_exists(cursor, post_id)
                
                query = "DELETE FROM posts WHERE id = %s"
                execute_query(cursor, query, (post_id,), 'none')
                mysql.connection.commit()
                
                logger.info(f"게시글 삭제 완료: ID {post_id}")
                return jsonify({"message": "게시글이 성공적으로 삭제되었습니다."})
                
        except Exception as e:
            logger.error(f"게시글 상세 처리 중 오류 발생: {e}")
            if "해당 게시글을 찾을 수 없습니다" in str(e):
                raise
            abort(500, message="서버 내부 오류가 발생했습니다.")
        finally:
            cursor.close()

    return posts_blp