const url = "http://" + process.env.REACT_APP_API_URL + "/api/"

export const addQuestion = async (question, answers, correctAnswer, description) => {
    const token = getAuthToken();
    if (!token) {
      throw new Error("Ты не авторизован, пожалуйста перейди по ссылке бота");
    }

    const uri = url + "suggest";
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

    const uri = url + "suggest/all";
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

export const getNonReviewedSuggests = async () => {
    const token = getAuthToken();
    if (!token) {
      throw new Error("Ты не авторизован, пожалуйста перейди по ссылке бота");
    }

    const uri = url + "suggest/review";
    console.log("uri: ", uri);

    const response = await fetch(uri, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    console.log("response: ", response);
    
    if (!response.ok) {
        const errorData = await response.json();
        throw errorData;
    }

    try {
        const data = await response.json();
        console.log("data: ", data);

        if (data.status === "error") {
            throw new Error(data.message)
        }

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

    const uri = url + "suggest?uuid=" + uuid;
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

    const uri = "".concat(url, "suggest/make-review?uuid=", uuid.uuid);
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

export const parseAuthToken = () => {
    try {
        const token = getAuthToken()

      const decoded = atob(token.replace(/_/g, "/").replace(/-/g, "+")); // Преобразуем URL-safe Base64 в обычный Base64
  
      // Разделение токена на telegram_id и signature
      const [telegram_id, signature] = decoded.split(".");
  
      // Проверяем, что в токене есть telegram_id и signature
      if (!telegram_id || !signature) {
        throw new Error("Invalid token format");
      }
  
      return telegram_id;
    } catch (error) {
      console.error("Failed to parse token:", error.message);
      return null;
    }
  };