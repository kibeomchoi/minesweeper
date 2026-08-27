"""
=====================================================
Minesweeper - Game Logic
=====================================================

게임의 실제 진행을 담당하는 파일입니다.

구성:
- Cell : 게임판의 한 칸
- Game : 게임 전체 로직
=====================================================
"""

import random

from config import (
    ROWS,
    COLS,
    BOMB_COUNT,
    FIRST_CLICK_SAFE,
    MIN_CASHOUT,
    PAYOUTS,
)


# =====================================================
# Cell 클래스
# =====================================================

class Cell:

    def __init__(self):
        # 지뢰인지
        self.is_bomb = False

        # 안전한 칸인지
        self.is_safe = False

        # 플레이어가 선택했는지
        self.is_open = False


    def open(self):
        """칸을 공개합니다."""

        self.is_open = True


# =====================================================
# Game 클래스
# =====================================================

class Game:

    def __init__(self):
        """새로운 게임을 생성합니다."""

        self.reset()


    # =================================================
    # 게임 초기화
    # =================================================

    def reset(self):
        """게임 상태를 처음으로 되돌립니다."""

        # 새로운 게임판
        self.board = self.create_board()

        # 첫 클릭 여부
        self.first_click = True

        # 발견한 안전 칸 수
        self.safe_found = 0

        # 현재 배율
        self.current_multiplier = 1.0

        # 게임 종료 여부
        self.game_over = False

        # Cash Out 여부
        self.cashed_out = False

        # 게임 결과
        self.result = None


    # =================================================
    # 게임판 생성
    # =================================================

    def create_board(self):
        """
        모든 칸을 빈 상태로 만든 뒤 반환합니다.

        첫 클릭 전까지 지뢰는 배치하지 않습니다.
        """

        board = []

        for _ in range(ROWS):

            row = []

            for _ in range(COLS):

                row.append(Cell())

            board.append(row)

        return board


    # =================================================
    # 지뢰 배치
    # =================================================

    def place_bombs(self, safe_position):
        """
        첫 클릭 이후 지뢰를 배치합니다.

        첫 클릭한 위치에는 지뢰가 생기지 않습니다.
        """

        possible_positions = []

        for row in range(ROWS):

            for col in range(COLS):

                position = (row, col)

                if position != safe_position:

                    possible_positions.append(position)


        # 지뢰 위치 랜덤 선택
        bomb_positions = random.sample(
            possible_positions,
            BOMB_COUNT
        )


        # 지뢰 배치
        for row, col in bomb_positions:

            self.board[row][col].is_bomb = True


        # 나머지 칸은 안전한 칸
        for row in range(ROWS):

            for col in range(COLS):

                cell = self.board[row][col]

                if not cell.is_bomb:

                    cell.is_safe = True


    # =================================================
    # 칸 선택
    # =================================================

    def click_cell(self, row, col):
        """
        플레이어가 칸을 선택했을 때 실행됩니다.

        반환값:

        {
            "result": "safe",
            "message": "안전한 칸입니다!"
        }

        또는

        {
            "result": "bomb",
            "message": "지뢰를 발견했습니다!"
        }
        """

        # 이미 게임이 끝났다면 선택 불가
        if self.game_over:

            return {
                "result": "error",
                "message": "이미 종료된 게임입니다."
            }


        # 좌표 검사
        if not (
            0 <= row < ROWS
            and
            0 <= col < COLS
        ):

            return {
                "result": "error",
                "message": "잘못된 위치입니다."
            }


        cell = self.board[row][col]


        # 이미 선택한 칸
        if cell.is_open:

            return {
                "result": "error",
                "message": "이미 선택한 칸입니다."
            }


        # =================================================
        # 첫 클릭
        # =================================================

        if self.first_click:

            if FIRST_CLICK_SAFE:

                self.place_bombs(
                    (row, col)
                )

            self.first_click = False


        # 칸 공개
        cell.open()


        # =================================================
        # 지뢰
        # =================================================

        if cell.is_bomb:

            self.game_over = True

            self.result = "bomb"

            return {
                "result": "bomb",
                "message": "💣 지뢰를 발견했습니다!"
            }


        # =================================================
        # 안전한 칸
        # =================================================

        if cell.is_safe:

            self.safe_found += 1

            self.update_multiplier()


            return {
                "result": "safe",
                "message": "💎 안전한 칸입니다!"
            }


        # 예상하지 못한 상태
        return {
            "result": "error",
            "message": "칸 상태를 확인할 수 없습니다."
        }


    # =================================================
    # 배율 업데이트
    # =================================================

    def update_multiplier(self):
        """찾은 안전 칸에 따라 배율을 업데이트합니다."""

        if self.safe_found in PAYOUTS:

            self.current_multiplier = PAYOUTS[
                self.safe_found
            ]

        else:

            self.current_multiplier = 1.0


    # =================================================
    # Cash Out 가능 여부
    # =================================================

    def can_cash_out(self):
        """
        현재 Cash Out이 가능한지 확인합니다.
        """

        return (
            self.safe_found >= MIN_CASHOUT
            and not self.game_over
            and not self.cashed_out
        )


    # =================================================
    # Cash Out
    # =================================================

    def cash_out(self, bet_amount):
        """
        현재 배율에 따라 Cash Out 금액을 계산합니다.

        bet_amount:
            이번 게임에 베팅한 금액

        반환:
            성공 여부
            지급 금액
            메시지
        """

        # Cash Out 불가능
        if not self.can_cash_out():

            return {
                "success": False,
                "reward": 0,
                "message": (
                    f"안전한 칸을 {MIN_CASHOUT}개 이상 "
                    "찾아야 Cash Out할 수 있습니다."
                )
            }


        # 지급 금액 계산
        reward = int(
            bet_amount * self.current_multiplier
        )


        # 게임 종료
        self.cashed_out = True

        self.game_over = True

        self.result = "cashout"


        return {
            "success": True,
            "reward": reward,
            "message": "🎉 Cash Out 성공!"
        }


    # =================================================
    # 모든 칸 공개
    # =================================================

    def reveal_all(self):
        """게임 종료 후 모든 칸을 공개합니다."""

        for row in self.board:

            for cell in row:

                cell.open()


    # =================================================
    # 게임판 상태 반환
    # =================================================

    def get_board_state(self):
        """
        Streamlit에서 사용할 게임판 상태를 반환합니다.
        """

        board_state = []

        for row in self.board:

            row_state = []

            for cell in row:

                row_state.append(
                    {
                        "bomb": cell.is_bomb,
                        "safe": cell.is_safe,
                        "open": cell.is_open,
                    }
                )

            board_state.append(row_state)

        return board_state


    # =================================================
    # 게임 상태 반환
    # =================================================

    def get_status(self):
        """현재 게임 상태를 반환합니다."""

        return {
            "safe_found": self.safe_found,
            "multiplier": self.current_multiplier,
            "game_over": self.game_over,
            "cashed_out": self.cashed_out,
            "result": self.result,
        }
