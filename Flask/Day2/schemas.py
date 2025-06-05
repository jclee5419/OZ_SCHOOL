from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    """책 정보를 위한 스키마"""
    id = fields.Int(dump_only=True, description="책 ID")
    title = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200),
        description="책 제목"
    )
    author = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        description="저자"
    )
    publication_year = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1000, max=2025),
        description="출판 연도"
    )
    isbn = fields.Str(
        allow_none=True,
        validate=validate.Length(max=20),
        description="ISBN"
    )

class BookUpdateSchema(Schema):
    """책 정보 업데이트를 위한 스키마 (모든 필드 선택적)"""
    title = fields.Str(
        validate=validate.Length(min=1, max=200),
        description="책 제목"
    )
    author = fields.Str(
        validate=validate.Length(min=1, max=100),
        description="저자"
    )
    publication_year = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1000, max=2025),
        description="출판 연도"
    )
    isbn = fields.Str(
        allow_none=True,
        validate=validate.Length(max=20),
        description="ISBN"
    )