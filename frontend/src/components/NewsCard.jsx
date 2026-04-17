function NewsCard({data}) {
    return (
        <div className="bg-gray-100 text-gray-700 rounded-xl shadow-sm hover:shadow-md transition p-6 border border-slate-200">
            <h2 className="text-xl font-bold mb-3">{data.title}</h2>
            <div className="text-sm text-slate-600 whitespace-pre-line mb-4">
                {data.summary}
            </div>

            <div className="flex justify-between items-center mt-auto">
                <span className="text-sm text-slate-400">
                    {new Date(data.published_at).toLocaleString('th-TH')}
                </span>
                <a href={data.url} target="_blank" className="text-blue-600 hover:underline text-sm font-medium">
                    อ่านฉบับเต็ม
                </a>
            </div>
        </div>
    )
}

export default NewsCard