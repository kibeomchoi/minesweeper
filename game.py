"""
=====================================================
Casino Mines - Game Logic Part 1

게임의 핵심 로직을 담당하는 파일입니다.

구성:
- Cell 클래스 : 보드의 한 칸 관리
- Game 클래스 : 전체 게임 관리

=====================================================
"""

import random

from config import (
    ROWS,
    COLS,
    GEM_COUNT,
    BOMB_COUNT,
    FIRST_CLICK_SAFE,
    MIN_CASHOUT,
    PAYOUTS,
)


# =====================================================
# Cell 클래스
# =====================================================

class Cell:
    """
    게임판의 하나의 칸을 관리하는 클래스

    한 칸은:
    - 폭탄인지
    - 열렸는지
    - 보석인지

    정보를 가지고 있음.
    """

    def __init__(self):
        # 폭탄 여부
        self.is_bomb = False

        # 플레이어가 클릭했는지 여부
        self.is_open = False

        # 보석 여부
        self.is_gem = False

    def open(self):
        """
        칸을 열기
        """

        self.is_open = True


# =====================================================
# Game 클래스
# =====================================================

class Game:
    """
    Casino Mines 전체 게임 관리 클래스
    """

    def __init__(self):
        """
        새로운 게임 시작
        """

        # 게임판 생성
        self.board = self.create_board()

        # 첫 클릭 여부
        self.first_click = True

        # 현재 찾은 보석 개수
        self.gems_found = 0

        # 게임 종료 여부
        self.game_over = False

        # Cash Out 여부
        self.cashed_out = False

        # 현재 배율
        self.current_multiplier = 1.0


    # =================================================
    # 보드 생성
    # =================================================

    def create_board(self):
        """
        5x5 게임판 생성

        처음에는 모든 칸이 빈 칸.
        폭탄은 첫 클릭 이후 배치.
        """

        board = []

        for _ in range(ROWS):
            row = []

            for _ in range(COLS):
                row.append(Cell())

            board.append(row)

        return board


    # =================================================
    # 폭탄 배치
    # =================================================

    def place_bombs(self, safe_position):
        """
        첫 클릭 이후 폭탄 배치

        safe_position:
        플레이어가 처음 클릭한 위치

        첫 클릭 위치에는 폭탄이 절대 생성되지 않음.
        """

        possible_positions = []

        for row in range(ROWS):
            for col in range(COLS):

                # 첫 클릭 위치 제외
                if (row, col) != safe_position:
                    possible_positions.append((row, col))


        # 폭탄 위치 랜덤 선택
        bomb_positions = random.sample(
            possible_positions,
            BOMB_COUNT
        )


        # 폭탄 배치
        for row, col in bomb_positions:
            self.board[row][col].is_bomb = True


        # 나머지는 보석 처리
        for row in range(ROWS):
            for col in range(COLS):

                cell = self.board[row][col]

                if not cell.is_bomb:
                    cell.is_gem = True
    # =================================================
    # 칸 클릭 처리
    # =================================================

    def click_cell(self, row, col):
        """
        플레이어가 특정 칸을 클릭했을 때 실행

        반환값:
        {
            "result": 결과,
            "message": 메시지
        }
        """

        # 이미 끝난 게임이면 클릭 불가
        if self.game_over:
            return {
                "result": "error",
                "message": "이미 종료된 게임입니다."
            }


        # 잘못된 좌표 방지
        if not (0 <= row < ROWS and 0 <= col < COLS):
            return {
                "result": "error",
                "message": "잘못된 위치입니다."
            }


        cell = self.board[row][col]


        # 이미 연 칸이면 무시
        if cell.is_open:
            return {
                "result": "error",
                "message": "이미 선택한 칸입니다."
            }


        # =============================================
        # 첫 클릭 처리
        # =============================================

        if self.first_click:

            if FIRST_CLICK_SAFE:
                self.place_bombs((row, col))

            self.first_click = False



        # 칸 열기
        cell.open()



        # =============================================
        # 폭탄 발견
        # =============================================

        if cell.is_bomb:

            self.game_over = True

            return {
                "result": "bomb",
                "message": "💥 BOOM! 폭탄을 밟았습니다."
            }



        # =============================================
        # 보석 발견
        # =============================================

        if cell.is_gem:

            self.gems_found += 1

            self.update_multiplier()


            return {
                "result": "gem",
                "message": "💎 보석 발견!"
            }


        return {
            "result": "unknown",
            "message": "알 수 없는 결과"
        }



    # =================================================
    # 배율 업데이트
    # =================================================

    def update_multiplier(self):
        """
        현재 보석 개수에 따른 배율 계산
        """

        if self.gems_found in PAYOUTS:
            self.current_multiplier = PAYOUTS[self.gems_found]

        else:
            # 아직 Cash Out 가능 구간이 아니거나
            # 설정되지 않은 구간

            self.current_multiplier = 1.0



    # =================================================
    # 현재 상태 반환
    # =================================================

    def get_status(self):
        """
        현재 게임 상태 반환

        Streamlit 화면에서 사용 예정
        """

        return {
            "gems_found": self.gems_found,
            "multiplier": self.current_multiplier,
            "game_over": self.game_over,
            "cashed_out": self.cashed_out
        }
    # =================================================
    # Cash Out
    # =================================================

    def can_cash_out(self):
        """
        현재 Cash Out 가능 여부 확인
        """

        return (
            self.gems_found >= MIN_CASHOUT
            and not self.game_over
            and not self.cashed_out
        )


    def cash_out(self, chips):
        """
        현재 배율 기준으로 칩 획득

        chips:
        플레이어가 건 칩

        반환:
        획득한 칩
        """

        if not self.can_cash_out():
            return {
                "success": False,
                "reward": 0,
                "message": "아직 Cash Out 할 수 없습니다."
            }


        reward = int(
            chips * self.current_multiplier
        )


        self.cashed_out = True
        self.game_over = True


        return {
            "success": True,
            "reward": reward,
            "message": f"💰 {reward}칩 획득!"
        }



    # =================================================
    # 폭탄 전체 공개
    # =================================================

    def reveal_all(self):
        """
        게임 종료 후 모든 칸 공개

        UI에서 사용
        """

        for row in self.board:

            for cell in row:

                cell.open()



    # =================================================
    # 보드 상태 반환
    # =================================================

    def get_board_state(self):
        """
        Streamlit에서 화면 출력용

        반환 예시:

        [
            [
                {"bomb":False, "open":True, "gem":True},
                ...
            ]
        ]

        """

        board_state = []


        for row in self.board:

            row_state = []


            for cell in row:

                row_state.append(
                    {
                        "bomb": cell.is_bomb,
                        "gem": cell.is_gem,
                        "open": cell.is_open
                    }
                )


            board_state.append(row_state)


        return board_state



    # =================================================
    # 게임 초기화
    # =================================================

    def reset(self):
        """
        새로운 게임 시작
        """

        self.board = self.create_board()

        self.first_click = True

        self.gems_found = 0

        self.game_over = False

        self.cashed_out = False

        self.current_multiplier = 1.0
