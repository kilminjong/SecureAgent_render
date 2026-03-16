from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cache(db.Model):
    __tablename__ = 'cache'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False, unique=True)
    chat_html = db.Column(db.Text, nullable=False)
    session_data = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False, unique=True)
    memo = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SampleData(db.Model):
    __tablename__ = 'sample_data'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), nullable=False, unique=True)
    raw_data = db.Column(db.Text, nullable=False)

SAMPLE_DATA = {
    "자금현황": "자금현황\n회사명 계좌구분 은행명 통화코드 총잔고\n20260313 (주)쿠콘글로벌지점 수시 경남은행 EUR 1.11\n20260313 (주)쿠콘글로벌지점 수시 광주은행 KRW 34,070\n20260313 (주)쿠콘글로벌지점 수시 국민은행 USD 61.72\n20260313 (주)쿠콘글로벌지점 수시 기업은행 KRW 38,490\n20260313 (주)쿠콘글로벌지점 예적금 기업은행 KRW 121,000\n20260313 AI 테스용사업장 대출 농협은행 KRW 8,000,000,000\n20260313 AI 테스용사업장 예적금 농협은행 KRW 127,540,000\n20260313 씨앤에스 대출 농협은행 KRW 2,750,000,000\n20260313 씨앤에스 수시 광주은행 KRW 52,688\n20260313 씨앤에스 수시 농협은행 KRW 18,424\n20260313 씨앤에스 예적금 경남은행 KRW 1,058,903,714\n20260313 씨앤에스 예적금 기업은행 KRW 1,054,476,923\n20260313 씨앤에스 예적금 우리은행 KRW 1,000,000,000\n20260313 웹케시테스트 예적금 농협은행 KRW 0",
    "수시입출계좌 잔액": "수시입출계좌 잔액 EUR 8.46 JPY 473.00 USD 210.26 KRW 157,827\n회사명 계좌구분 은행명 계좌번호 통화코드 총잔고\n(주)쿠콘글로벌지점 수시 경남은행 2810002267104 EUR 1.11\n(주)쿠콘글로벌지점 수시 경남은행 2810002267104 JPY 103.00\n(주)쿠콘글로벌지점 수시 경남은행 2810002267104 USD 11.39\n(주)쿠콘글로벌지점 수시 광주은행 1107020736263 KRW 34,070\n(주)쿠콘글로벌지점 수시 국민은행 75266811010050 USD 61.72\n씨앤에스 수시 농협은행 134401000445 KRW 11,262\n씨앤에스 수시 농협은행 134401000458 KRW 1,615\n씨앤에스 수시 하나은행 14091001922404 KRW 4,073",
    "이번 달 수시입출 거래내역": "이번 달 거래내역 입금 15건 출금 38건\n회사명 계좌구분 은행명 계좌번호 거래일자 거래시간 입금금액 출금금액 잔액 비고\n(주)쿠콘글로벌지점 수시 농협은행 301024282204 20260309 05:56:18 1 0 102,384 IN_0556\n(주)쿠콘글로벌지점 수시 농협은행 301024282204 20260309 05:40:37 0 501 102,383 주식회사 쿠콘\n씨앤에스 수시 농협은행 134401000445 20260311 15:56:37 10 0 11,262\n씨앤에스 수시 농협은행 134401000445 20260310 09:02:39 0 10 11,261 경리나라스크래핑이체\n씨앤에스 수시 농협은행 134401000458 20260311 15:56:37 0 10 1,615 보안자등록",
    "대출 잔액": "대출 잔액 11,000,000,000원\n회사명 계좌구분 은행명 계좌번호 통화코드 총잔고\nAI 테스용사업장 대출 기업은행 03**04**93200033 KRW 0\nAI 테스용사업장 대출 농협은행 01**20**23901 KRW 8,000,000,000\nAI 테스용사업장 대출 농협은행 01**20**64481 KRW 250,000,000\n법케시사업장 대출 농협은행 9912351233246234 KRW 0\n씨앤에스 대출 농협은행 4726614401201 KRW 700,000,000\n씨앤에스 대출 농협은행 7777777 KRW 2,050,000,000",
    "최근 환율": "최근 환율\n환율등록일 통화코드 통화명 평균기준환율 전신환매도율 전신환매입율\n20260309 USD 미국 1,474.50 1,460.20 1,488.80\n20260309 EUR 유로통화 1,700.84 1,683.84 1,717.84\n20260309 JPY 일본 931.61 922.49 940.73\n20260309 CNY 중국 213.29 211.18 215.40\n20260308 USD 미국 1,464.30 1,450.10 1,478.50",
    "달러 잔액 조회": "달러 잔액 USD 210.26\n회사명 계좌구분 은행명 계좌번호 통화코드 총잔고\n(주)쿠콘글로벌지점 수시 경남은행 2810002267104 USD 11.39\n(주)쿠콘글로벌지점 수시 국민은행 75266811010050 USD 61.72\n(주)쿠콘글로벌지점 수시 농협은행 4520016999431 USD 4.06\n(주)쿠콘글로벌지점 수시 신한은행 180008634281 USD 50.86",
    "증권계좌 잔액": "증권계좌 잔액 USD 25.04\n회사명 계좌구분 은행명 계좌번호 통화코드 총잔고\nAI 테스용사업장 증권 농협은행 4580000006621 USD 25.04",
    "신탁계좌 만기일": "신탁계좌 만기일\n회사명 계좌구분 은행명 계좌번호 통화코드 총잔고 만기일자\n(주)쿠콘글로벌지점 신탁 농협은행 0900155151515 KRW 0\n씨앤에스 신탁 농협은행 03201052355522 KRW 0 20251209\n씨앤에스 신탁 농협은행 11122233444568 KRW 0 2025-12-22",
    "3달간 카드 승인내역": "3달간 카드 승인내역 5,542건\n회사명 카드사명 카드번호 내역구분 사용일자 사용시간 승인번호 총승인금액 가맹점명\n씨앤에스 NH카드 5531710494453518 승인 20260127 23:31 84664911 55,000 주식회사 카카오모빌리티\n씨앤에스 NH카드 5531710494453518 승인 20260127 22:59 82364901 2,000 GS25논산은솔점\n씨앤에스 NH카드 5531710494453518 승인 20260127 21:43 84990656 20,000 어해도횟집",
    "월간 자금 흐름": "월간 자금 흐름\n기준일자 회사명 통화코드 입출금구분 잔액\n20260228 (주)쿠콘글로벌지점 KRW 수시 1,541,248\n20260131 (주)쿠콘글로벌지점 KRW 수시 2,038,164\n20260228 AI 테스용사업장 KRW 대출 8,250,000,000\n20260228 씨앤에스 KRW 대출 2,750,000,000\n20260228 씨앤에스 KRW 수시 85,159\n20260228 씨앤에스 KRW 예적금 3,123,408,637",
}

def init_db(app):
    db.create_all()
    # 샘플 데이터 초기 적재 (없을 때만)
    if SampleData.query.count() == 0:
        for label, raw in SAMPLE_DATA.items():
            db.session.add(SampleData(label=label, raw_data=raw))
        db.session.commit()
        print(f"샘플 데이터 {len(SAMPLE_DATA)}건 적재 완료")
