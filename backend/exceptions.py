class ApiException(Exception):
    def __init__(self, code, message, extra=None):
        self.extra = extra
        self.code = code
        self.message = message


# 에러메세지
OK = "SUCCESS"  # GET 성공 : 200 Ok

CREATED = "성공적으로 등록되었습니다"  # POST 성공 : 201 Created

DELETED = "삭제되었습니다"  # DELETE (soft_delete) 성공 : 200 Ok

INVALID_USER = "유효하지 않은 유저입니다"  # 잘못된 token : 400 Bad request

INVALID_EMAIL = "형식에 맞는 이메일을 입력해 주세요"  # 이메일 validation 미충족 : 400 Bad request

INVALID_INPUT = "필수 정보가 입력되지 않았습니다"  # 필수정보가 입력되지 않았을 시 : 400 Bad request

USER_NOT_FOUND = "존재하지 않는 유저입니다"  # 로그인 시 존재하지 않는 email 입력 시 : 400 Bad request

# 로그인시 이메일은 존재하지만 비밀번호가 일치하지 않을 경우 : 400 Bad request
PASSWORD_MISMATCH = "비밀번호를 확인해 주세요"

PRODUCT_MISSING = "상품을 담아주세요"  # 결제/장바구니 진행 시 물건을 선택하지 않았을 때

# 중복을 허용하지 않는데 확인한 값이 이미 존재할 경우 : 400 Bad request ex) 회원가입 시 이메일, 셀러명, 브랜드명 등
DUPLICATED_INPUT = "이미 존재하는 값입니다"

LOGIN_REQUIRED = "로그인이 필요합니다"  # token이 필요한 기능에 token이 없을 시 : 401 Unauthorized

# master 전용 기능에 user나 seller의 토큰 혹은 seller의 전용 기능에 user의 token으로 접속할 시 : 403 Forbidden
ACCESS_DENIED = "접근 권한이 없습니다"

PAGE_NOT_FOUND = "존재하지 않는 페이지입니다"  # 잘못된 path parameter로 접근 시 : 404 Not Found

INTERNAL_SERVER_ERROR = "서버 요청 실패"  # backend 로직 에러 : 500 Internal Server Error
