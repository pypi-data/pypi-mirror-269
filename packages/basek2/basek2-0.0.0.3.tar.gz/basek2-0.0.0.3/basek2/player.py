import pymysql

def player_info(player_name, year, position):
    try:
        # MySQL 연결 설정
        conn = pymysql.connect(
            host='222.111.68.160', 
            user='root',
            password='1233', 
            database='baseball_stat',
            charset='utf8'
        )

        # 커서 생성
        cursor = conn.cursor()

        # 테이블 이름 생성
        table_name = f"regular_{year}_{position}"

        if position == "hitter":
            po = "ht"
        elif position == "pitcher":
            po = "pt"
        elif position == "defender":
            po = "df"
        elif position == "runner":
            po = "run"
        else:
            print("Invalid position")

        # 선수 정보 검색 쿼리 실행
        cursor.execute(f"SELECT * FROM {table_name} WHERE {po}_Playername=%s", (player_name,))
        player_info = cursor.fetchone()

        # 결과를 딕셔너리 형태로 반환
        if player_info:
            if po == "ht":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '평균 타율': player_info[2],
                    '경기': player_info[3],
                    '타석': player_info[4],
                    '타수': player_info[5],
                    '득점': player_info[6],
                    '안타': player_info[7],
                    '2루타': player_info[8],
                    '3루타': player_info[9],
                    '홈런': player_info[10],
                    '루타': player_info[11],
                    '타점': player_info[12],
                    '희생번트': player_info[13],
                    '희생플라이': player_info[14]
                }
            elif po == "pt":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '평균 자책점': player_info[2],
                    '경기': player_info[3],
                    '완투': player_info[4],
                    '완봉': player_info[5],
                    '승리': player_info[6],
                    '패배': player_info[7],
                    '세이브': player_info[8],
                    '홀드': player_info[9],
                    '승률': player_info[10],
                    '타자수': player_info[11],
                    '이닝': player_info[12],
                    '피안타': player_info[13],
                    '홈런': player_info[14],
                    '볼넷': player_info[15],
                    '사구': player_info[16],
                    '삼진': player_info[17],
                    '실점': player_info[18],
                    '자책점': player_info[19]
                }
            elif po == "df":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '포지션': player_info[2],
                    '경기': player_info[3],
                    '선발경기': player_info[4],
                    '수비이닝': player_info[5],
                    '실책': player_info[6],
                    '견제사': player_info[7],
                    '풋아웃': player_info[8],
                    '어시스트': player_info[9],
                    '병살': player_info[10],
                    '수비율': player_info[11],
                    '포일': player_info[12],
                    '도루허용': player_info[13],
                    '도루실패': player_info[14],
                    '도루저지율': player_info[15]
                }
            elif po == "run":
                return {
                    '선수 이름': player_info[0],
                    '팀': player_info[1],
                    '경기': player_info[2],
                    '도루시도': player_info[3],
                    '도루허용': player_info[4],
                    '도루실패': player_info[5],
                    '도루성공률': player_info[6],
                    '주루사': player_info[7],
                    '견제사': player_info[8]
                }
        else:
            print("해당 선수 정보를 찾을 수 없습니다.")
            return None

    except pymysql.Error as err:
        print(f"MySQL 오류: {err}")
        return None
    
def homerun_rank(year, limit=50):
    conn = pymysql.connect(
        host='222.111.68.160', 
        user='root',
        password='1233', 
        database='baseball_stat',
        charset='utf8'
    )
    
    cursor = conn.cursor()
    
    # 테이블명 생성
    table_name = f"regular_{year}_hitter"
    
    # 쿼리 실행
    query = f"""
    SELECT ht_Playername, ht_Teamname, ht_HR
    FROM {table_name}
    ORDER BY ht_HR DESC
    LIMIT {limit}
    """
    cursor.execute(query)
    
    # 결과 가져오기
    results = cursor.fetchall()
    
    # 결과를 문자열로 생성
    result_str = "{:^10s} {:^17s} {:^10s} {:^10s}\n".format("Rank", "Player", "Team", "Homerun")
    for rank, (player, team, homerun) in enumerate(results, start=1):
        result_str += "{:^10d} {:^13s} {:^10s} {:^10d}\n".format(rank, player, team, homerun)
    
    # 연결 종료
    conn.close()

    return result_str
