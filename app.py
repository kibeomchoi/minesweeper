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
# 화면 스타일
# =====================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background-color: #111111;
    }

    /* 일반 Markdown 글씨 */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown li {
        color: #FFFFFF !important;
    }

    /* 제목 */
    .stMarkdown h1 {
        color: #FFFFFF !important;
        font-weight: 900 !important;
    }

    /* 입력창 라벨 */
    label {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* 숫자 입력창 */
    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 800 !important;
        border: 2px solid #FFFFFF !important;
    }

    /* 숫자 입력창 +/- 버튼 */
    [data-testid="stNumberInput"] button {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* 모든 일반 버튼 */
    .stButton button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        min-height: 55px !important;
        font-size: 18px !important;
        font-weight: 900 !important;
    }

    .stButton button:hover {
        background-color: #EEEEEE !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 비활성 버튼 */
    .stButton button:disabled {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }

    /* 경고 / 에러 */
    [data-testid="stAlert"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    [data-testid="stAlert"] * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 구분선 */
    hr {
        border-color: #FFFFFF !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Session State 초기화
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

if "last_bet" not in st.session_state:
    st.session_state.last_bet = 0


# =====================================================
# 함수
# =====================================================

def reset_user():
    """다음 사용자를 위해 게임을 완전히 초기화"""

    st.session_state.screen = "start"
    st.session_state.balance = 0
    st.session_state.bet_amount = 0
    st.session_state.game = None
    st.session_state.last_reward = 0
    st.session_state.last_bet = 0


def start_game(bet_amount):
    """새 게임 시작"""

    st.session_state.balance -= bet_amount

    st.session_state.bet_amount = bet_amount
    st.session_state.last_bet = bet_amount
    st.session_state.game = Game()

    st.session_state.screen = "game"


def next_game():
    """다음 게임을 위해 베팅 화면으로 이동"""

    st.session_state.bet_amount = 0
    st.session_state.game = None
    st.session_state.last_reward = 0

    st.session_state.screen = "bet"


# =====================================================
# 상단 제목
# =====================================================

st.title(TITLE)


# =====================================================
# SCREEN 1
# 시작 화면
# =====================================================

if st.session_state.screen == "start":

    st.subheader("💣 Minesweeper")

    st.write("지뢰를 피하면서 안전한 칸을 찾아보세요.")
    st.write("")
    st.write("💎 안전한 칸을 찾을수록 배율이 올라갑니다.")
    st.write("💣 지뢰를 발견하면 해당 게임은 즉시 종료됩니다.")
    st.write(f"💰 안전한 칸 {MIN_CASHOUT}개부터 Cash Out이 가능합니다.")
    st.write(f"🎲 베팅 금액은 {BET_UNIT:,}칩 단위입니다.")
    st.write("")

    st.subheader("💰 시작 잔액")

    initial_balance = st.number_input(
        "사용자의 시작 잔액을 입력하세요.",
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
                f"잔액은 {BALANCE_UNIT:,}칩 단위로 입력해야 합니다."
            )

        else:

            st.session_state.balance = int(initial_balance)

            st.session_state.bet_amount = 0
            st.session_state.game = None
            st.session_state.last_reward = 0

            st.session_state.screen = "bet"

            st.rerun()


# =====================================================
# SCREEN 2
# 베팅 화면
# =====================================================

elif st.session_state.screen == "bet":

    st.subheader(
        f"💰 현재 잔액 : {st.session_state.balance:,}칩"
    )

    st.write("")

    if st.session_state.balance < MIN_BET:

        st.error(
            "현재 잔액이 최소 베팅 금액보다 적습니다."
        )

        st.write(
            f"남은 잔액 : {st.session_state.balance:,}칩"
        )

        if st.button(
            "⏹ 게임 끝내기",
            use_container_width=True,
        ):

            st.session_state.screen = "final"

            st.rerun()

    else:

        st.subheader("🎲 베팅 금액")

        bet_amount = st.number_input(
            "이번 게임에 베팅할 금액을 입력하세요.",
            min_value=MIN_BET,
            max_value=int(st.session_state.balance),
            step=BET_UNIT,
            value=min(
                1000,
                int(st.session_state.balance)
            ),
            key="current_bet",
        )

        st.write(
            f"베팅 가능 금액 : {st.session_state.balance:,}칩 이하"
        )

        if st.button(
            "🎲 베팅하고 게임 시작",
            use_container_width=True,
        ):

            bet_amount = int(bet_amount)

            # 잔액 초과
            if bet_amount > st.session_state.balance:

                st.error(
                    "현재 잔액보다 큰 금액은 베팅할 수 없습니다."
                )

            # 최소 베팅 미만
            elif bet_amount < MIN_BET:

                st.error(
                    f"최소 베팅 금액은 {MIN_BET:,}칩입니다."
                )

            # 단위 확인
            elif bet_amount % BET_UNIT != 0:

                st.error(
                    f"베팅 금액은 {BET_UNIT:,}칩 단위여야 합니다."
                )

            else:

                start_game(bet_amount)

                st.rerun()


# =====================================================
# SCREEN 3
# 게임 화면
# =====================================================

elif st.session_state.screen == "game":

    game = st.session_state.game

    # -------------------------------------------------
    # 잔액
    # -------------------------------------------------

    st.subheader(
        f"💰 현재 잔액 : {st.session_state.balance:,}칩"
    )

    st.write("")

    # -------------------------------------------------
    # 현재 게임 정보
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💎 안전한 칸",
            f"{game.safe_found}개",
        )

    with col2:

        st.metric(
            "📈 현재 배율",
            f"{game.current_multiplier:.1f}x",
        )

    # -------------------------------------------------
    # 다음 배율
    # -------------------------------------------------

    next_count = game.safe_found + 1

    if next_count in PAYOUTS:

        st.info(
            f"다음 안전한 칸 → {PAYOUTS[next_count]:.1f}x"
        )

    else:

        st.write(
            "다음 배율 정보가 없습니다."
        )

    # -------------------------------------------------
    # Cash Out 상태
    # -------------------------------------------------

    if game.can_cash_out():

        possible_reward = int(
            st.session_state.bet_amount
            * game.current_multiplier
        )

        st.success(
            f"💰 Cash Out 가능! 현재 받는 금액 : {possible_reward:,}칩"
        )

    else:

        st.write(
            f"💰 안전한 칸 {MIN_CASHOUT}개부터 Cash Out 가능합니다."
        )

    st.write("")

    # -------------------------------------------------
    # 게임판
    # -------------------------------------------------

    board = game.get_board_state()

    for row in range(ROWS):

        columns = st.columns(COLS)

        for col in range(COLS):

            cell = board[row][col]

            with columns[col]:

                # 이미 열린 칸
                if cell["open"]:

                    if cell["bomb"]:

                        st.button(
                            "💣",
                            key=f"opened_bomb_{row}_{col}",
                            disabled=True,
                            use_container_width=True,
                        )

                    else:

                        st.button(
                            "💎",
                            key=f"opened_safe_{row}_{col}",
                            disabled=True,
                            use_container_width=True,
                        )

                # 닫힌 칸
                else:

                    if st.button(
                        "⬜",
                        key=f"closed_{row}_{col}",
                        use_container_width=True,
                    ):

                        result = game.click_cell(
                            row,
                            col
                        )

                        # 지뢰
                        if result["result"] == "bomb":

                            game.reveal_all()

                            st.session_state.screen = "result_bomb"

                            st.rerun()

                        # 안전
                        elif result["result"] == "safe":

                            st.rerun()

    # -------------------------------------------------
    # Cash Out 버튼
    # -------------------------------------------------

    if game.can_cash_out():

        st.write("")

        if st.button(
            "💰 CASH OUT",
            use_container_width=True,
        ):

            result = game.cash_out(
                st.session_state.bet_amount
            )

            if result["success"]:

                reward = result["reward"]

                # 보상 지급
                st.session_state.balance += reward

                st.session_state.last_reward = reward

                st.session_state.screen = "result_cashout"

                st.rerun()


# =====================================================
# SCREEN 4
# 지뢰 발견 결과
# =====================================================

elif st.session_state.screen == "result_bomb":

    st.title("💥 GAME OVER")

    st.subheader("지뢰를 발견했습니다!")

    st.write("이번 게임은 종료되었습니다.")

    st.divider()

    st.write(
        f"💸 잃은 베팅 금액 : {st.session_state.last_bet:,}칩"
    )

    st.write(
        f"💰 현재 잔액 : {st.session_state.balance:,}칩"
    )

    st.divider()

    st.subheader("다음 게임을 진행하시겠습니까?")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ 계속하기",
            use_container_width=True,
        ):

            next_game()

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

    st.title("🎉 CASH OUT 성공!")

    st.subheader("게임을 성공적으로 종료했습니다.")

    st.divider()

    st.write(
        f"💰 획득 금액 : {st.session_state.last_reward:,}칩"
    )

    st.write(
        f"💰 현재 잔액 : {st.session_state.balance:,}칩"
    )

    st.divider()

    st.subheader("다음 게임을 진행하시겠습니까?")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ 계속하기",
            use_container_width=True,
        ):

            next_game()

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

    st.title("🎰 게임 종료")

    st.subheader("게임을 종료합니다.")

    st.divider()

    st.write("")

    st.metric(
        "💰 최종 잔액",
        f"{st.session_state.balance:,}칩",
    )

    st.write("")

    st.write(
        "다음 사용자가 게임을 시작할 수 있습니다."
    )

    st.write("")

    if st.button(
        "🎰 다음 사용자 시작",
        use_container_width=True,
    ):

        reset_user()

        st.rerun()
