function TimeSummary({ summary }) {
    if (!summary) return null

    return (
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-6 mb-8 shadow-sm">
            <div className="flex items-center mb-3">
                <span className="flex h-2 w-2 rounded-full bg-blue-500 mr-2 animate-pulse"></span>
                <h3 className="text-blue-800 font-bold uppercase tracking-wider text-sm">
                    Market Pulse (Last 6 Hours)
                </h3>
            </div>
            <p className="text-slate-700 leading-relaxed italic">
                "{summary}"
            </p>
        </div>
    )
}

export default TimeSummary