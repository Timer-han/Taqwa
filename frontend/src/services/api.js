export const getSuggests = async () => {
    const uri = "api/questions/suggests";
    console.log("uri: ", uri);

    const response = await fetch(uri);
    if (!response.ok) {
        throw new Error("Ошибка загрузки вопросов")
    }
    const data = await response.json();
    console.log("data: ", data)
    return data.suggests;
};