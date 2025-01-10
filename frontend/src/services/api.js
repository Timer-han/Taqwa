export const getSuggests = async () => {
    const uri = "http://localhost:4000/question/suggests";
    console.log("uri: ", uri);

    const response = await fetch(uri);
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