function TimeSummary({ data }) {
    if (!data.summary) return null

    return (
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-6 mb-8 shadow-sm">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-bold text-blue-900 flex items-center gap-2">
                    <span className="flex h-2 w-2 rounded-full bg-blue-600 animate-pulse"></span>
                    สรุปภาพรวมตลาด (6 ชั่วโมงล่าสุด)
                </h2>
                <span className="text-[10px] font-medium text-blue-400 bg-white px-2 py-1 rounded-md border border-blue-50 shadow-sm">
                    AI Agent: {data.model_used}
                </span>
            </div>
            
            <div className="text-slate-700 text-sm leading-relaxed whitespace-pre-line">
                {data.summary}
            </div>

            <div className="mt-4 pt-4 border-t border-blue-100/50 flex justify-end">
                <span className="text-[11px] text-slate-400">
                    อัปเดตล่าสุดเมื่อ: {new Date(data.created_at).toLocaleString('th-TH', {
                        hour: '2-digit',
                        minute: '2-digit',
                        day: 'numeric',
                        month: 'short',
                        timeZone: 'Asia/Bangkok'
                    })}
                </span>
            </div>
        </div>
    )
}

export default TimeSummary