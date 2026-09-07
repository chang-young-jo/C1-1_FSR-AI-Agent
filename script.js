const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const answerBox = document.getElementById("answerBox");
const conversationList = document.getElementById("conversationList");

async function sendQuestion() {
    const question = questionInput.value.trim();

    if (!question) {
        answerBox.textContent = "질문을 입력해주세요.";
        return;
    }

    answerBox.textContent = "AI가 분석 중입니다...";
    sendButton.disabled = true;

    try {
        const response = await fetch("https://c1-1fsr-ai-agent.onrender.com", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: question
            })
        });

        if (!response.ok) {
            throw new Error("서버 응답 오류");
        }

        const data = await response.json();

        answerBox.textContent = data.answer;
        loadConversations();
    } catch (error) {
        console.error(error);

        answerBox.textContent =
            "AI 서버와 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인해주세요.";
    } finally {
        sendButton.disabled = false;
    }
}

async function loadConversations() {
    try {
        const response = await fetch(
            "https://c1-1fsr-ai-agent.onrender.com/api/conversations"
        );

        if (!response.ok) {
            throw new Error("대화 이력 조회 실패");
        }

        const data = await response.json();

        if (data.conversations.length === 0) {
            conversationList.textContent = "저장된 대화가 없습니다.";
            return;
        }

        conversationList.innerHTML = "";

        data.conversations.forEach(function(conversation) {
            const item = document.createElement("div");
            item.className = "conversation-item";

            const title = document.createElement("div");
            title.className = "conversation-title";
            title.textContent = conversation.title;

            const time = document.createElement("div");
            time.className = "conversation-time";

            if (conversation.created_at) {
                const date = new Date(conversation.created_at);

                time.textContent = date.toLocaleString("ko-KR", {
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit"
                });
            } else {
                time.textContent = "저장 시간 없음";
            }

            item.appendChild(title);
            item.appendChild(time);

            // 삭제 버튼
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "삭제";
            deleteButton.className = "delete-button";

            deleteButton.addEventListener(
                "click",
                async function(event) {
                    event.stopPropagation();

                    try {
                        const response = await fetch(
                            `https://c1-1fsr-ai-agent.onrender.com/api/conversations/${conversation.id}`,
                            {
                                method: "DELETE"
                            }
                        );

                        if (!response.ok) {
                            throw new Error("대화 삭제 실패");
                        }

                        loadConversations();

                    } catch (error) {
                        console.error(error);
                        alert("대화를 삭제할 수 없습니다.");
                    }
                }
            );

            item.appendChild(deleteButton);

            // 대화 클릭 시 상세 내용 불러오기
            item.addEventListener(
                "click",
                async function() {
                    try {
                        const response = await fetch(
                            `https://c1-1fsr-ai-agent.onrender.com/api/conversations/${conversation.id}`
                        );

                        if (!response.ok) {
                            throw new Error("대화 상세 조회 실패");
                        }

                        const detail = await response.json();

                        questionInput.value = detail.user_message;
                        answerBox.textContent =
                            detail.assistant_message;

                    } catch (error) {
                        console.error(error);
                        answerBox.textContent =
                            "대화 내용을 불러올 수 없습니다.";
                    }
                }
            );

            conversationList.appendChild(item);
        });

    } catch (error) {
        console.error(error);
        conversationList.textContent =
            "대화 이력을 불러올 수 없습니다.";
    }
}


sendButton.addEventListener(
    "click",
    sendQuestion
);

questionInput.addEventListener(
    "keydown",
    function(event) {
        if (event.key === "Enter") {
            sendQuestion();
        }
    }
);

loadConversations();