import streamlit as st

from game import Game

from config import (
    TITLE,
    ROWS,
    COLS,
    PAYOUTS,
    MIN_CASHOUT,
)


# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="Casino Mines",
    page_icon="🎰",
    layout="centered"
)


# =====================================================
# 기본 CSS
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b0b0b;
    }


    /* 일반 글씨 */
    .stMarkdown,
    .stText,
    label {
        color: white !important;
    }


    /* 버튼 글씨 */
    div.stButton > button {
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        min-height: 60px;
    }


    /* 비활성 게임판 버튼의 이모지 흐림 방지 */
    div.stButton > button:disabled {
        opacity: 1 !important;
        color: white !important;
    }


    div.stButton > button:disabled p {
        opacity: 1 !important;
        color: white !important;
    }


    /* 베팅 입력창 */
    div[data-testid="stNumberInput"] input {
        color: white !important;
        background-color: #222222 !important;
        font-size: 22px !important;
        font-weight: bold !important;
    }


    div[data-testid="stNumberInput"] label {
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# Session State 초기화
# =====================================================

if "balance" not in st.session_state:
    st.session_state.balance = None


if "game" not in st.session_state:
    st.session_state.game = None


if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 0


if "round_active" not in st.session_state:
    st.session_state.round_active = False


if "show_game_over" not in st.session_state:
    st.session_state.show_game_over = False


if "show_cashout" not in st.session_state:
    st.session_state.show_cashout = False


if "cashout_reward" not in st.session_state:
    st.session_state.cashout_reward = 0


if "game_finished" not in st.session_state:
    st.session_state.game_finished = False


# =====================================================
# 현재 게임 가져오기
# =====================================================

game = st.session_state.game


# =====================================================
# 결과 팝업
# =====================================================

@st.dialog("💥 GAME OVER")
def game_over_popup():

    st.error("💥 폭탄을 발견했습니다!")

    st.markdown(
        f"현재 잔액 : **{st.session_state.balance}칩**"
    )

    st.write("다음 게임을 진행하시겠습니까?")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "계속하기",
            use_container_width=True
        ):

            st.session_state.show_game_over = False

            if st.session_state.balance > 0:

                st.session_state.round_active = False

            else:

                st.session_state.game_finished = True

            st.rerun()


    with col2:

        if st.button(
            "게임 끝내기",
            use_container_width=True
        ):

            st.session_state.show_game_over = False

            st.session_state.game_finished = True

            st.rerun()



@st.dialog("🎉 CASH OUT")
def cashout_popup(reward):

    st.success("🎉 Cash Out 성공!")

    st.markdown(
        f"획득 칩 : **{reward}칩**"
    )

    st.markdown(
        f"현재 잔액 : **{st.session_state.balance}칩**"
    )

    st.write("다음 게임을 진행하시겠습니까?")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "계속하기",
            use_container_width=True
        ):

            st.session_state.show_cashout = False

            if st.session_state.balance > 0:

                st.session_state.round_active = False

            else:

                st.session_state.game_finished = True

            st.rerun()


    with col2:

        if st.button(
            "게임 끝내기",
            use_container_width=True
        ):

            st.session_state.show_cashout = False

            st.session_state.game_finished = True

            st.rerun()


# =====================================================
# 제목
# =====================================================

st.title(TITLE)


# =====================================================
# 게임 종료 화면
# =====================================================

if st.session_state.game_finished:

    st.divider()

    st.subheader("🎰 GAME END")

    st.success(
        f"최종 잔액 : {st.session_state.balance}칩"
    )

    st.write("게임이 종료되었습니다.")

    st.stop()

# =====================================================
# 처음 잔액 설정
# =====================================================

if st.session_state.balance is None:

    st.subheader("💰 게임 시작")

    st.write(
        "게임에 사용할 총 칩을 입력해주세요."
    )

    initial_balance = st.number_input(
        "보유 칩",
        min_value=100,
        step=100,
        value=1000,
        key="initial_balance_input"
    )

    if st.button(
        "🎰 게임 시작",
        use_container_width=True
    ):

        st.session_state.balance = int(initial_balance)

        st.session_state.game = None

        st.session_state.bet_amount = 0

        st.session_state.round_active = False

        st.rerun()

    st.stop()


# =====================================================
# 현재 잔액 표시
# =====================================================

st.subheader(
    f"💰 현재 잔액 : {st.session_state.balance}칩"
)


# =====================================================
# 새로운 게임 베팅
# =====================================================

if (
    not st.session_state.round_active
    and not st.session_state.show_game_over
    and not st.session_state.show_cashout
    and not st.session_state.game_finished
):

    if st.session_state.balance <= 0:

        st.session_state.game_finished = True

        st.rerun()


    st.divider()

    st.subheader("🎲 이번 게임 베팅")

    st.write(
        f"현재 사용할 수 있는 칩 : "
        f"{st.session_state.balance}칩"
    )


    bet_amount = st.number_input(
        "베팅 금액",
        min_value=100,
        max_value=st.session_state.balance,
        step=100,
        value=min(
            100,
            st.session_state.balance
        ),
        key="bet_input"
    )


    # =================================================
    # 베팅 시작
    # =================================================

    if st.button(
        "🎲 베팅하고 게임 시작",
        use_container_width=True
    ):

        bet_amount = int(bet_amount)


        # ---------------------------------------------
        # 100칩 단위 확인
        # ---------------------------------------------

        if bet_amount % 100 != 0:

            st.error(
                "베팅은 100칩 단위로만 가능합니다."
            )

            st.stop()


        # ---------------------------------------------
        # 잔액보다 많이 베팅했는지 확인
        # ---------------------------------------------

        if bet_amount > st.session_state.balance:

            st.error(
                "보유한 칩보다 많이 베팅할 수 없습니다."
            )

            st.stop()


        # ---------------------------------------------
        # 베팅 금액 차감
        # ---------------------------------------------

        st.session_state.balance -= bet_amount

        st.session_state.bet_amount = bet_amount


        # ---------------------------------------------
        # 새 게임 생성
        # ---------------------------------------------

        st.session_state.game = Game()

        st.session_state.round_active = True

        st.session_state.show_game_over = False

        st.session_state.show_cashout = False

        st.rerun()


# =====================================================
# 게임 시작
# =====================================================

if (
    st.session_state.round_active
    and st.session_state.game is not None
):

    game = st.session_state.game

    status = game.get_status()


    # =================================================
    # 게임 진행 정보
    # =================================================

    st.divider()

    st.write(
        f"💎 발견한 보석 : "
        f"{status['gems_found']}개"
    )

    st.write(
        f"🔥 현재 배율 : "
        f"{status['multiplier']}x"
    )


    # =================================================
    # Cash Out 가능 알림
    # =================================================

    if game.can_cash_out():

        st.success(
            "🎉 보석 5개 이상 발견! "
            "Cash Out 가능합니다."
        )


    # =================================================
    # 다음 배율
    # =================================================

    next_gem = status["gems_found"] + 1

    if next_gem in PAYOUTS:

        st.info(
            f"💎 {next_gem}개 성공 시 "
            f"→ {PAYOUTS[next_gem]}x"
        )


    # =================================================
    # 게임판
    # =================================================

    st.subheader("💎 Mines")

    board = game.get_board_state()


    for row in range(ROWS):

        cols = st.columns(COLS)


        for col in range(COLS):

            cell = board[row][col]


            # -----------------------------------------
            # 기본 닫힌 칸
            # -----------------------------------------

            symbol = "⬜"


            # -----------------------------------------
            # 열린 칸
            # -----------------------------------------

            if cell["open"]:

                if cell["bomb"]:

                    symbol = "💣"

                elif cell["gem"]:

                    symbol = "🔷"


            # -----------------------------------------
            # 닫힌 칸
            # -----------------------------------------

            if not cell["open"]:

                if cols[col].button(
                    "⬜",
                    key=f"cell_{row}_{col}",
                    use_container_width=True
                ):

                    result = game.click_cell(
                        row,
                        col
                    )


                    # -----------------------------
                    # 폭탄
                    # -----------------------------

                    if result["result"] == "bomb":

                        game.reveal_all()

                        st.session_state.round_active = False

                        st.session_state.show_game_over = True


                    st.rerun()


            # -----------------------------------------
            # 열린 칸
            # -----------------------------------------

            else:

                cols[col].button(
                    symbol,
                    key=f"open_{row}_{col}",
                    disabled=True,
                    use_container_width=True
                )


    # =================================================
    # 현재 Cash Out 금액
    # =================================================

    current_reward = int(
        st.session_state.bet_amount
        * status["multiplier"]
    )


    st.divider()

    st.write(
        f"💰 현재 Cash Out 금액 : "
        f"**{current_reward}칩**"
    )


    # =================================================
    # Cash Out 버튼
    # =================================================

    if st.button(
        "💰 Cash Out",
        use_container_width=True
    ):

        if game.can_cash_out():

            result = game.cash_out(
                st.session_state.bet_amount
            )


            if result["success"]:

                reward = result["reward"]


                # -----------------------------
                # 획득 금액 지급
                # -----------------------------

                st.session_state.balance += reward

                st.session_state.cashout_reward = reward

                st.session_state.round_active = False

                st.session_state.show_cashout = True

                st.rerun()


        else:

            st.warning(
                "💎 보석 5개 이상 발견해야 "
                "Cash Out 할 수 있습니다."
            )

# =====================================================
# 결과 팝업 실행
# =====================================================

if st.session_state.show_game_over:

    game_over_popup()


if st.session_state.show_cashout:

    cashout_popup(
        st.session_state.cashout_reward
    )
