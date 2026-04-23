import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const getNews = async (topic) => {
    const config = {
        params: (topic && topic !== 'All') ? { topic: topic } : {}
    }
    
    const response = await axios.get(`${API_BASE_URL}/news`, config)
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

export default API_BASE_URL