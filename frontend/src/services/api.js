import axios from "axios"

const API_BASE_URL = 'http://127.0.0.1:8000'

export const getNews = async () => {
    const response = await axios.get(`${API_BASE_URL}/news`)
    return response.data
}

export const getNewsDetail = async (id) => {
    const response = await axios.get(`${API_BASE_URL}/news/${id}`)
    return response.data
}