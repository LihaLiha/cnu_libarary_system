import pymysql

from config.config_db import connection_db
from service.MemberService import member_match

# 도서목록 조회



def get_books():


    # 1. MariaDB와 Connection 성공하면
    conn = connection_db()  # Connection -> MariaDB

    try:

        curs = conn.cursor()             # 2. cursor() 객체를 사용해서 작업(노동자)
        sql = "SELECT * FROM tbl_book;"  # 3. MariaDB 실행 SQL문(실행 X)
        curs.execute(sql)                # 4. cursor() 객체를 통해서 SQL문 실행(실행 O)

        # fetchall()  -> 모든 row 반환
        # fetchone()  -> 1개 row 반환
        # fetchmany() -> n개 row 반환
        rows = curs.fetchall()           # 5. 실행 결과 받기
    finally:
        conn.close()                     # 6. MariaDB Connection 끊기기


    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ISBN\tTITLE\tWRITER\tPUBLISHER\tPRICE\tDATE')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f':: {row.values()}')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# 도서 검색
def search_books():
    print(':: 검색하고 싶은 키워드를 입력하세요.')
    keyword = input('>> 검색 키워드: ')

    conn = connection_db()
    try:
        curs = conn.cursor()
        # keword = "파이썬"
        # SELECT문 (DB로부터 데이터를 GET)
        # 3:     SELECT *                           # 데이터의 어떤 Column을 가져올지
        # 1:     FROM tbl_book                      # table 설정
        # 2:     WHERE book-name LIKE '%{keyword}%' # 필터: book_name에 kewword가 포함!

        sql = f'''
                SELECT *
                FROM tbl_book
                WHERE book_name LIKE '%{keyword}%'
                      OR book_writer LIKE '%{keyword}%'
              '''
        curs.execute(sql)
        rows = curs.fetchall()
    finally:
        conn.close()

    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    print(':: ISBN\tTITLE\tWRITER\tPUBLISHER\tPRICE\tDATE')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    for row in rows:
        print(f':: {row.values()}')
    print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::')


# 도서 대출
def rental_books():
    # 1 회원 조회(tbl_member)
    print(':: 회원번호를 입력하세요')
    member_num = input('>> 회원 번호: ')

    # result = 1(회원), 0(비회원)
    result = member_match(member_num)


    # 2 도서 대출! => 대출 정보 저장(tbl_rental)
    if result == 1:
        # 2-1 대출 가능한 책인지 판단!
        print(':: 대출하고싶은 도서 ISBN을 입력하세요.')
        book_isbn = input('>> ISBN: ')
        print(book_isbn, 'y')   # 도서 대출 가능 확인


    else:
        # 경고 메세지 출력 후 메인화면 전환
        print('#Warning: 회원이 아닙니다. 회원 등록을 먼저 해주세요.')
        return

    # 3 도서 보유 정보 수정 => 대출한 책 Count -1(tbl_book)