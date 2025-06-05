from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema, BookUpdateSchema

# 메모리 내 데이터 저장소
books_db = [
    {
        "id": 1,
        "title": "파이썬 완벽 가이드",
        "author": "김파이썬",
        "publication_year": 2023,
        "isbn": "978-1234567890"
    },
    {
        "id": 2,
        "title": "웹 개발의 모든 것",
        "author": "이웹개발",
        "publication_year": 2022,
        "isbn": "978-0987654321"
    }
]

# 다음 ID를 위한 카운터
next_id = 3

blp = Blueprint(
    "books",
    __name__,
    url_prefix="/api/books",
    description="책 관리 API"
)

@blp.route("/")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        """모든 책의 목록을 조회합니다."""
        return books_db
    
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, book_data):
        """새로운 책을 추가합니다."""
        global next_id
        
        # 제목과 저자 중복 확인
        for book in books_db:
            if (book["title"].lower() == book_data["title"].lower() and 
                book["author"].lower() == book_data["author"].lower()):
                abort(400, message="같은 제목과 저자의 책이 이미 존재합니다.")
        
        # 새 책 생성
        new_book = {
            "id": next_id,
            **book_data
        }
        
        books_db.append(new_book)
        next_id += 1
        
        return new_book

@blp.route("/<int:book_id>")
class BookDetail(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        """특정 책의 정보를 조회합니다."""
        book = self._find_book(book_id)
        return book
    
    @blp.arguments(BookUpdateSchema)
    @blp.response(200, BookSchema)
    def put(self, book_data, book_id):
        """특정 책의 정보를 업데이트합니다."""
        book = self._find_book(book_id)
        
        # 제목과 저자가 모두 변경되는 경우 중복 확인
        if "title" in book_data and "author" in book_data:
            for existing_book in books_db:
                if (existing_book["id"] != book_id and
                    existing_book["title"].lower() == book_data["title"].lower() and 
                    existing_book["author"].lower() == book_data["author"].lower()):
                    abort(400, message="같은 제목과 저자의 책이 이미 존재합니다.")
        
        # 책 정보 업데이트
        for key, value in book_data.items():
            book[key] = value
        
        return book
    
    @blp.response(204)
    def delete(self, book_id):
        """특정 책을 삭제합니다."""
        book = self._find_book(book_id)
        books_db.remove(book)
        return ""
    
    def _find_book(self, book_id):
        """ID로 책을 찾습니다."""
        for book in books_db:
            if book["id"] == book_id:
                return book
        abort(404, message="책을 찾을 수 없습니다.")

@blp.route("/search")
class BookSearch(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        """제목이나 저자로 책을 검색합니다."""
        title_query = request.args.get("title", "").lower()
        author_query = request.args.get("author", "").lower()
        
        if not title_query and not author_query:
            abort(400, message="검색어(title 또는 author)를 입력해주세요.")
        
        results = []
        for book in books_db:
            match = True
            
            if title_query and title_query not in book["title"].lower():
                match = False
            
            if author_query and author_query not in book["author"].lower():
                match = False
            
            if match:
                results.append(book)
        
        return results