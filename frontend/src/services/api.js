import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const getTopics = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/topics`)
        return response.data
    } catch (error) {
        console.error("Error fetching topics:", error)
        return []
    }
}

export const getNews = async (topic) => {
    try {
        const config = {
            params: (topic && topic !== 'All') ? { topic: topic } : {}
        }
        const response = await axios.get(`${API_BASE_URL}/news`, config)
        return response.data
    } catch (error) {
        console.error("Error fetching news:", error)
        return []
    }
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

export default API_BASE_URL