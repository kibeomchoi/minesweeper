"""
=====================================================
Minesweeper - Streamlit App
=====================================================

화면 흐름

1. 시작 화면
2. 초기 잔액 입력
3. 베팅 금액 입력
4. 게임 진행
5. 지뢰 발견 결과
6. Cash Out 결과
7. 계속하기 / 게임 종료
8. 최종 잔액
9. 다음 사용자

팝업을 사용하지 않습니다.
모든 결과는 화면 자체를 변경하여 표시합니다.
=====================================================
"""

import streamlit as st

from config import (
    ROWS,
    COLS,
    MIN_CASHOUT,
    PAYOUTS,
    TITLE,
    PAGE_TITLE,
    PAGE_ICON,
    MIN_BALANCE,
    BALANCE_UNIT,
    MIN_BET,
    BET_UNIT,
)

from game import Game


# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered",
)


# =====================================================
# CSS
# =====================================================

st.markdown(
    """
    <style>

    /* =================================================
       전체 배경
       ================================================= */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {

        background-color: #111111 !important;
        color: #FFFFFF !important;

    }


    /* =================================================
       기본 글씨
       ================================================= */

    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] label,
    [data-testid="stMain"] div {

        color: #FFFFFF;

    }


    /* =================================================
       제목
       ================================================= */

    .main-title {

        background-color: #FFFFFF;

        color: #000000 !important;

        font-size: 42px;

        font-weight: 900;

        text-align: center;

        padding: 18px;

        border-radius: 14px;

        margin-bottom: 25px;

    }


    /* =================================================
       일반 안내 문구
       ================================================= */

    .text-white {

        color: #FFFFFF !important;

        font-size: 20px;

        font-weight: 800;

        text-align: center;

        margin: 15px 0;

    }


    /* =================================================
       잔액 박스
       ================================================= */

    .balance-box {

        background-color: #FFFFFF;

        color: #000000 !important;

        font-size: 28px;

        font-weight: 900;

        text-align: center;

        padding: 15px;

        border-radius: 12px;

        margin: 15px 0 25px 0;

    }


    /* =================================================
       정보 박스
       ================================================= */

    .info-box {

        background-color: #222222;

        border: 2px solid #FFFFFF;

        border-radius: 12px;

        padding: 18px;

        margin: 15px 0;

        text-align: center;

    }


    .info-label {

        color: #FFFFFF !important;

        font-size: 17px;

        font-weight: 800;

    }


    .info-value {

        color: #FFFFFF !important;

        font-size: 30px;

        font-weight: 900;

        margin-top: 6px;

    }


    /* =================================================
       게임판
       ================================================= */

    .cell-open {

        background-color: #FFFFFF;

        color: #000000 !important;

        font-size: 30px;

        font-weight: 900;

        text-align: center;

        border-radius: 8px;

        padding: 12px;

    }


    /* =================================================
       결과 화면
       ================================================= */

    .result-screen {

        background-color: #FFFFFF;

        border-radius: 15px;

        padding: 30px 20px;

        margin: 20px 0;

        text-align: center;

    }


    .result-title {

        color: #000000 !important;

        font-size: 38px;

        font-weight: 900;

        margin-bottom: 20px;

    }


    .result-text {

        color: #000000 !important;

        font-size: 21px;

        font-weight: 800;

        margin: 10px 0;

    }


    .result-number {

        color: #000000 !important;

        font-size: 34px;

        font-weight: 900;

        margin: 15px 0;

    }


    /* =================================================
       버튼
       ================================================= */

    [data-testid="stButton"] button {

        background-color: #FFFFFF !important;

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        border: 2px solid #FFFFFF !important;

        border-radius: 10px !important;

        min-height: 58px !important;

        font-size: 19px !important;

        font-weight: 900 !important;

        opacity: 1 !important;

    }


    [data-testid="stButton"] button * {

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        font-weight: 900 !important;

        opacity: 1 !important;

    }


    /* =================================================
       숫자 입력창
       ================================================= */

    [data-testid="stNumberInput"] {

        margin-bottom: 10px;

    }


    [data-testid="stNumberInput"] label {

        color: #FFFFFF !important;

        font-size: 18px !important;

        font-weight: 900 !important;

    }


    [data-testid="stNumberInput"] input {

        background-color: #FFFFFF !important;

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        font-size: 22px !important;

        font-weight: 900 !important;

        border: 3px solid #FFFFFF !important;

        border-radius: 8px !important;

        opacity: 1 !important;

    }


    /* =================================================
       에러 / 경고 / 성공 메시지
       ================================================= */

    [data-testid="stAlert"] {

        background-color: #FFFFFF !important;

        border: 2px solid #000000 !important;

    }


    [data-testid="stAlert"] * {

        color: #000000 !important;

        -webkit-text-fill-color: #000000 !important;

        font-weight: 800 !important;

        opacity: 1 !important;

    }


    /* =================================================
       구분선
       ================================================= */

    hr {

        border-color: #FFFFFF !important;

    }


    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Session State
# =====================================================

if "screen" not in st.session_state:
    st.session_state.screen = "start"

if "balance" not in st.session_state:
    st.session_state.balance = 0

if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 0

if "game" not in st.session_state:
    st.session_state.game = None

if "last_reward" not in st.session_state:
    st.session_state.last_reward = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# =====================================================
# 함수
# =====================================================

def show_title():
    """
    게임 제목
    """

    st.markdown(
        f"""
        <div class="main-title">
            {TITLE}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_balance():
    """
    현재 잔액
    """

    st.markdown(
        f"""
        <div class="balance-box">
            💰 현재 잔액 : {st.session_state.balance:,}칩
        </div>
        """,
        unsafe_allow_html=True,
    )


def new_game():
    """
    새로운 게임 객체 생성
    """

    st.session_state.game = Game()

    st.session_state.last_reward = 0

    st.session_state.last_result = None


def reset_user():
    """
    다음 사용자를 위해 모든 상태 초기화
    """

    st.session_state.screen = "start"

    st.session_state.balance = 0

    st.session_state.bet_amount = 0

    st.session_state.game = None

    st.session_state.last_reward = 0

    st.session_state.last_result = None


def go_to_bet_screen():
    """
    다음 게임 베팅 화면
    """

    st.session_state.bet_amount = 0

    st.session_state.game = None

    st.session_state.last_reward = 0

    st.session_state.last_result = None

    st.session_state.screen = "bet"


# =====================================================
# 제목
# =====================================================

show_title()


# =====================================================
# SCREEN 1
# 시작 화면
# =====================================================

if st.session_state.screen == "start":

    st.markdown(
        """
        <div class="text-white">
            💣 지뢰를 피하고 안전한 칸을 찾아보세요!
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="info-box">

            <div class="info-label">
                게임 방법
            </div>

            <div style="
                color:#FFFFFF !important;
                font-size:18px;
                font-weight:800;
                line-height:1.9;
                margin-top:12px;
            ">
                💎 안전한 칸을 찾으면 배율이 올라갑니다.<br>
                💣 지뢰를 찾으면 베팅 금액을 잃습니다.<br>
                💰 안전한 칸 5개부터 Cash Out이 가능합니다.<br>
                🎲 베팅 금액은 100칩 단위입니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="text-white">
            먼저 사용자의 시작 잔액을 입력하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )


    initial_balance = st.number_input(
        "시작 잔액",
        min_value=MIN_BALANCE,
        step=BALANCE_UNIT,
        value=10000,
        key="initial_balance",
    )


    if st.button(
        "🎰 게임 시작",
        use_container_width=True,
    ):

        if initial_balance < MIN_BALANCE:

            st.error(
                f"최소 잔액은 {MIN_BALANCE:,}칩입니다."
            )

        elif initial_balance % BALANCE_UNIT != 0:

            st.error(
                f"잔액은 {BALANCE_UNIT}칩 단위로 입력해야 합니다."
            )

        else:

            st.session_state.balance = int(
                initial_balance
            )

            st.session_state.bet_amount = 0

            st.session_state.game = None

            st.session_state.screen = "bet"

            st.rerun()


# =====================================================
# SCREEN 2
# 베팅 화면
# =====================================================

elif st.session_state.screen == "bet":

    show_balance()


    st.markdown(
        """
        <div class="text-white">
            🎲 이번 게임의 베팅 금액을 입력하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.session_state.balance < MIN_BET:

        st.markdown(
            """
            <div class="result-screen">

                <div class="result-title">
                    게임을 더 진행할 수 없습니다.
                </div>

                <div class="result-text">
                    남은 잔액이 최소 베팅 금액보다 적습니다.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        if st.button(
            "⏹ 게임 종료",
            use_container_width=True,
        ):

            st.session_state.screen = "final"

            st.rerun()


    else:

        bet_amount = st.number_input(
            "베팅 금액",
            min_value=MIN_BET,
            max_value=int(
                st.session_state.balance
            ),
            step=BET_UNIT,
            value=min(
                1000,
                int(st.session_state.balance)
            ),
            key="bet_amount_input",
        )


        if st.button(
            "🎲 베팅하고 시작",
            use_container_width=True,
        ):

            bet_amount = int(bet_amount)


            # 잔액 초과 검사
            if bet_amount > st.session_state.balance:

                st.error(
                    "현재 잔액보다 큰 금액은 베팅할 수 없습니다."
                )


            # 최소 금액 검사
            elif bet_amount < MIN_BET:

                st.error(
                    f"최소 베팅 금액은 {MIN_BET:,}칩입니다."
                )


            # 100 단위 검사
            elif bet_amount % BET_UNIT != 0:

                st.error(
                    f"베팅 금액은 {BET_UNIT}칩 단위여야 합니다."
                )


            else:

                # 베팅 금액 차감
                st.session_state.balance -= bet_amount

                st.session_state.bet_amount = bet_amount

                new_game()

                st.session_state.screen = "game"

                st.rerun()


# =====================================================
# SCREEN 3
# 게임 화면
# =====================================================

elif st.session_state.screen == "game":

    game = st.session_state.game


    show_balance()


    # =================================================
    # 현재 게임 정보
    # =================================================

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            f"""
            <div class="info-box">

                <div class="info-label">
                    💎 안전한 칸
                </div>

                <div class="info-value">
                    {game.safe_found}개
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        st.markdown(
            f"""
            <div class="info-box">

                <div class="info-label">
                    📈 현재 배율
                </div>

                <div class="info-value">
                    {game.current_multiplier:.1f}x
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # =================================================
    # 다음 배율
    # =================================================

    next_count = game.safe_found + 1

    next_multiplier = PAYOUTS.get(
        next_count
    )


    if next_multiplier is not None:

        st.markdown(
            f"""
            <div class="text-white">
                다음 안전 칸 : {next_multiplier:.1f}x
            </div>
            """,
            unsafe_allow_html=True,
        )


    # =================================================
    # Cash Out 가능 알림
    # =================================================

    if game.can_cash_out():

        reward_preview = int(
            st.session_state.bet_amount
            * game.current_multiplier
        )


        st.markdown(
            f"""
            <div style="
                background:#FFFFFF;
                color:#000000 !important;
                border-radius:12px;
                padding:15px;
                margin:15px 0;
                text-align:center;
                font-size:20px;
                font-weight:900;
            ">
                💰 CASH OUT 가능!<br>
                지금 받으면 {reward_preview:,}칩
            </div>
            """,
            unsafe_allow_html=True,
        )


    else:

        st.markdown(
            f"""
            <div class="text-white">
                💰 Cash Out은 안전한 칸 {MIN_CASHOUT}개부터 가능합니다.
            </div>
            """,
            unsafe_allow_html=True,
        )


    # =================================================
    # 게임판
    # =================================================

    board = game.get_board_state()


    for row in range(ROWS):

        cols = st.columns(COLS)


        for col in range(COLS):

            cell = board[row][col]


            with cols[col]:

                # -------------------------------------
                # 이미 열린 칸
                # -------------------------------------

                if cell["open"]:

                    if cell["bomb"]:

                        symbol = "💣"

                    elif cell["safe"]:

                        symbol = "💎"

                    else:

                        symbol = "?"


                    st.button(
                        symbol,
                        key=f"opened_{row}_{col}",
                        disabled=True,
                        use_container_width=True,
                    )


                # -------------------------------------
                # 닫힌 칸
                # -------------------------------------

                else:

                    if st.button(
                        "⬜",
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                    ):

                        result = game.click_cell(
                            row,
                            col
                        )


                        # ---------------------------------
                        # 지뢰
                        # ---------------------------------

                        if result["result"] == "bomb":

                            game.reveal_all()

                            st.session_state.last_result = "bomb"

                            st.session_state.last_reward = 0

                            st.session_state.screen = "result_bomb"

                            st.rerun()


                        # ---------------------------------
                        # 안전한 칸
                        # ---------------------------------

                        elif result["result"] == "safe":

                            st.rerun()


    # =================================================
    # Cash Out 버튼
    # =================================================

    if game.can_cash_out():

        st.markdown("---")


        if st.button(
            "💰 CASH OUT",
            use_container_width=True,
        ):

            result = game.cash_out(
                st.session_state.bet_amount
            )


            if result["success"]:

                reward = result["reward"]


                # Cash Out 보상 지급
                st.session_state.balance += reward


                st.session_state.last_reward = reward

                st.session_state.last_result = "cashout"

                st.session_state.screen = "result_cashout"

                st.rerun()


# =====================================================
# SCREEN 4
# 지뢰 결과
# =====================================================

elif st.session_state.screen == "result_bomb":

    st.markdown(
        """
        <div class="result-screen">

            <div class="result-title">
                💥 GAME OVER
            </div>

            <div class="result-text">
                지뢰를 발견했습니다!
            </div>

            <div class="result-text">
                이번 게임의 베팅 금액을 잃었습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="result-screen">

            <div class="result-text">
                잃은 금액
            </div>

            <div class="result-number">
                -{st.session_state.bet_amount:,}칩
            </div>

            <div class="result-text">
                현재 잔액
            </div>

            <div class="result-number">
                {st.session_state.balance:,}칩
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="text-white">
            다음 게임을 어떻게 하시겠습니까?
        </div>
        """,
        unsafe_allow_html=True,
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "▶ 계속하기",
            use_container_width=True,
        ):

            go_to_bet_screen()

            st.rerun()


    with col2:

        if st.button(
            "⏹ 게임 끝내기",
            use_container_width=True,
        ):

            st.session_state.screen = "final"

            st.rerun()


# =====================================================
# SCREEN 5
# Cash Out 결과
# =====================================================

elif st.session_state.screen == "result_cashout":

    st.markdown(
        """
        <div class="result-screen">

            <div class="result-title">
                🎉 CASH OUT 성공!
            </div>

            <div class="result-text">
                게임을 성공적으로 종료했습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="result-screen">

            <div class="result-text">
                획득 금액
            </div>

            <div class="result-number">
                +{st.session_state.last_reward:,}칩
            </div>

            <div class="result-text">
                현재 잔액
            </div>

            <div class="result-number">
                {st.session_state.balance:,}칩
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="text-white">
            다음 게임을 어떻게 하시겠습니까?
        </div>
        """,
        unsafe_allow_html=True,
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "▶ 계속하기",
            use_container_width=True,
        ):

            go_to_bet_screen()

            st.rerun()


    with col2:

        if st.button(
            "⏹ 게임 끝내기",
            use_container_width=True,
        ):

            st.session_state.screen = "final"

            st.rerun()


# =====================================================
# SCREEN 6
# 최종 결과
# =====================================================

elif st.session_state.screen == "final":

    st.markdown(
        """
        <div class="result-screen">

            <div class="result-title">
                🎰 게임 종료
            </div>

            <div class="result-text">
                이용해 주셔서 감사합니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="result-screen">

            <div class="result-text">
                최종 잔액
            </div>

            <div class="result-number">
                {st.session_state.balance:,}칩
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="text-white">
            다음 사용자가 게임을 시작할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.button(
        "🎰 다음 사용자 시작",
        use_container_width=True,
    ):

        reset_user()

        st.rerun()
