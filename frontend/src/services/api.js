const url = "http://localhost:4000/"

export const addQuestion = async (question, answers, correctAnswer, description) => {
    const token = getAuthToken();
    if (!token) {
      throw new Error("Ты не авторизован, пожалуйста перейди по ссылке бота");
    }

    const uri = url + "question/suggest";
    console.log("uri: ", uri)

    if (answers.length > 5 || answers.length < 2) {
        throw new Error("Количество ответов должно быть от 2 до 5")
    }

    const payload = {
        question,
        answers,
        correctAnswer,
        description,
    };

    try {
        const response = await fetch(uri, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        });
  
        if (!response.ok) {
            throw new Error("Ошибка при добавлении вопрсоа");
        }
    } catch (error) {
        throw new Error("Ошибка запроса:", error)
    }
}

export const getSuggests = async () => {
    const token = getAuthToken();
    if (!token) {
      throw new Error("Ты не авторизован, пожалуйста перейди по ссылке бота");
    }
    
    const uri = url + "question/suggests";
    console.log("uri: ", uri);

    const response = await fetch(uri, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    console.log("response: ", response);
    if (!response.ok) {
        throw new Error("Ошибка загрузки вопросов");
    }

    try {
        const data = await response.json();
        console.log("data: ", data);
        return data.suggests;
    } catch (err) {
        throw new Error("Ошибка форматирования");
    }
};

export const getSuggest = async (uuid) => {
    const token = getAuthToken();
    if (!token) {
      throw new Error("Ты не авторизован, пожалуйста перейди по ссылке бота");
    }

    const uri = url + "question/suggest?uuid=" + uuid;
    console.log("uri: ", uri);

    const response = await fetch(uri, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    console.log("response: ", response);
    if (!response.ok) {
        throw new Error("Ошибка загрузки вопросов");
    }

    try {
        const data = await response.json();
        console.log("data: ", data);
        return data.suggest;
    } catch (err) {
        throw new Error("Ошибка форматирования");
    }
}

export const sendFeedback = async (type, uuid, comment) => {
    const token = getAuthToken();
    if (!token) {
      throw new Error("Ты не авторизован, пожалуйста перейди по ссылке бота");
    }

    const uri = url + "question/suggest/review/?uuid=" + uuid;
    console.log("uri: ", uri);

    if ((type === "bad" || type === "improve") && (!comment.trim())) {
        throw new Error("Введи комментарий пожалуйста");
    }

    const payload = {
        type,
        comment,
    };

    try {
        const response = await fetch(uri, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(payload),
        })
        console.log("response: ", response)

        if (!response.ok) {
            throw new Error("Ошибка отправки отзыва");
        }
    } catch (error) {
        throw new Error("Ошибка запроса:", error)
    }
}

const getAuthToken = () => {
    const cookies = document.cookie.split("; ");
    const tokenCookie = cookies.find((cookie) => cookie.startsWith("auth_token="));
    if (tokenCookie) {
      return decodeURIComponent(tokenCookie.split("=")[1]); // Декодируем токен
    } else {
      return null;
    }
  };