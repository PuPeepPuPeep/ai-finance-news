import axios from "axios"

const API_BASE_URL = 'http://127.0.0.1:8000'

export const getNews = async (topic) => {
    const url = (topic && topic !== 'All')
    ? `${API_BASE_URL}/news?topic=${topic}`
    : `${API_BASE_URL}/news`

    const response = await axios.get(url)
    return response.data
}

export const getNewsDetail = async (id) => {
    const response = await axios.get(`${API_BASE_URL}/news/${id}`)
    return response.data
}

export const getTimeSummary = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/news/summary-6h`)
        return response.data
    } catch (error) {
        console.error("Error fetching time summary:", error)
        return null
    }
}