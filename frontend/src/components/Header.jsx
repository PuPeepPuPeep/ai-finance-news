import { useState, useEffect, useRef } from "react"
import { FaBars, FaGithub } from "react-icons/fa"
import { AiOutlineClose } from "react-icons/ai"
import { BsThreeDotsVertical } from "react-icons/bs"
import API_BASE_URL from "../services/api"

function Header({ activeTopic, onSelectTopic }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false)
    const [topics, setTopics] = useState(["Latest"])
    const [isDropdownOpen, setIsDropdownOpen] = useState(false)

    const [visibleTopics, setVisibleTopics] = useState(["Latest"])
    const [hiddenTopics, setHiddenTopics] = useState([])

    const containerRef = useRef(null)
    const dropdownRef = useRef(null)

    useEffect(() => {
        fetch(`${API_BASE_URL}/topics`)
        .then((res) => res.json())
        .then((data) => setTopics(["Latest", ...data]))
        .catch((err) => console.error("Error feching topics:", err))
    }, [])

    useEffect(() => {
        const handleResize = () => {
            if (!containerRef.current) return

            const containerWidth = containerRef.current.offsetWidth
            let currentWidth = 0
            const newVisible = []
            const newHidden = []

            topics.forEach((topic) => {
                const itemWidth = 100
                if (currentWidth + itemWidth + 50 < containerWidth) {
                    newVisible.push(topic)
                    currentWidth += itemWidth
                } else {
                    newHidden.push(topic)
                }
            })

            setVisibleTopics(newVisible)
            setHiddenTopics(newHidden)
        }

        const observer = new ResizeObserver(handleResize)
        if (containerRef.current) observer.observe(containerRef.current)

        return () => observer.disconnect()
    }, [topics])

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsDropdownOpen(false)
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => document.removeEventListener("mousedown", handleClickOutside)
    }, [])

    return (
        <header className="sticky top-0 z-50 bg-gray-800 border-b border-slate-200">
            <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <button
                        className="md:hidden p-2 text-slate-600 hover:bg-slate-100 rounded"
                        onClick={() => setIsMenuOpen(true)}
                    >
                        <FaBars className="w-6 h-6" />
                    </button>
                    <span className="text-xl font-bold text-blue-600">AI News</span>
                </div>
                <a
                    href="https://github.com/PuPeepPuPeep/ai-finance-news"
                    target="_blank"
                    rel="noreferrer"
                    className="text-white hover:text-slate-600 transition-colors"
                >
                    <FaGithub className="w-8 h-8" />
                </a>
            </div>

            {/* Mobile */}
            <div
                className={`fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300 ${isMenuOpen ? 'opacity-50' : 'opacity-0 pointer-events-none'}`}
                onClick={() => setIsMenuOpen(false)}
            >
            </div>

            <div className={`fixed top-0 left-0 h-full w-64 bg-white z-50 flex flex-col transform transition-transform duration-300 ease-in-out ${isMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                <div className="p-4 border-b flex justify-between items-center shrink-0">
                    <span className="font-bold text-lg">Topics</span>
                    <button onClick={() => setIsMenuOpen(false)} className="p-2 text-slate-600">
                        <AiOutlineClose className="w-6 h-6" />
                    </button>
                </div>
                <nav className="p-4 flex flex-col gap-2 flex-1 overflow-y-auto">
                    {topics.map((topic) => (
                        <button
                            key={topic}
                            onClick={() => { onSelectTopic(topic); setIsMenuOpen(false); }}
                            className={`px-4 py-3 rounded-md text-left font-medium transition-colors
                                ${activeTopic === topic
                                    ? 'bg-blue-600'
                                    : 'hover:bg-slate-100'
                                }`}
                        >
                            {topic}
                        </button>
                    ))}
                </nav>
            </div>

            {/* Desktop */}
            <nav className="hidden md:block bg-white border-t border-slate-100">
                <div ref={containerRef} className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-2 relative">
                    
                    {visibleTopics.map((topic) => (
                        <button
                            key={topic}
                            onClick={() => onSelectTopic(topic)}
                            className={`px-3 py-3 rounded-md text-sm font-medium transition-colors whitespace-nowrap ${
                                activeTopic === topic ? 'bg-blue-600 text-white' : 'text-slate-600 hover:bg-slate-100'
                            }`}
                        >
                            {topic}
                        </button>
                    ))}

                    {/* Dropdown Menu */}
                    {hiddenTopics.length > 0 && (
                        <div className="relative" ref={dropdownRef}>
                            <button
                                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                                className="p-2 text-slate-600 hover:bg-slate-100 rounded-md"
                            >
                                <BsThreeDotsVertical />
                            </button>

                            {isDropdownOpen && (
                                <div className="absolute right-0 top-full mt-2 w-48 bg-white 
                                                border border-slate-200 shadow-lg rounded-lg py-2 z-50
                                                max-h-60 overflow-y-auto scrollbar-hide">
                                    {hiddenTopics.map((topic) => (
                                        <button
                                            key={topic}
                                            onClick={() => { onSelectTopic(topic); setIsDropdownOpen(false) }}
                                            className="block w-full text-left px-4 py-2 hover:bg-slate-100 text-sm"
                                        >
                                            {topic}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </nav>
        </header>
    )
}

export default Header