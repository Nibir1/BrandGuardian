import { useState } from 'react';
import axios from 'axios';
import { ShieldCheck, Loader2, Image as ImageIcon, FileText, AlertCircle } from 'lucide-react';

// Types matching Backend Pydantic models
interface BrandResponse {
    content: string;
    brand_score: number;
    reasoning: string;
    used_references: string[];
}

interface ImageResponse {
    is_compliant: boolean;
    dominant_colors: string[];
    violation_reason?: string;
}

const API_URL = "http://localhost:8000/api/v1";

function App() {
    const [activeTab, setActiveTab] = useState<'text' | 'image'>('text');
    const [loading, setLoading] = useState(false);

    // Text State
    const [topic, setTopic] = useState('');
    const [contentType, setContentType] = useState('LinkedIn Post');
    const [tone, setTone] = useState('Professional');
    const [textResult, setTextResult] = useState<BrandResponse | null>(null);

    // Image State
    const [imgUrl, setImgUrl] = useState('');
    const [imgResult, setImgResult] = useState<ImageResponse | null>(null);

    const handleGenerate = async () => {
        setLoading(true);
        setTextResult(null);
        try {
            const res = await axios.post(`${API_URL}/generate`, {
                topic,
                content_type: contentType,
                tone_modifier: tone
            });
            setTextResult(res.data);
        } catch (err) {
            alert("Error generating content");
        } finally {
            setLoading(false);
        }
    };

    const handleValidateImage = async () => {
        setLoading(true);
        setImgResult(null);
        try {
            const res = await axios.post(`${API_URL}/validate-image`, {
                image_url: imgUrl
            });
            setImgResult(res.data);
        } catch (err) {
            alert("Error validating image");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 font-sans">
            {/* Header */}
            <header className="bg-white border-b border-gray-200">
                <div className="max-w-5xl mx-auto px-6 h-16 flex items-center gap-3">
                    <div className="w-8 h-8 bg-[#00A3E0] rounded-md flex items-center justify-center">
                        <ShieldCheck className="text-white w-5 h-5" />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight text-gray-900">BrandGuardian</h1>
                    <span className="text-xs font-mono bg-gray-100 px-2 py-1 rounded text-gray-500">BETA</span>
                </div>
            </header>

            <main className="max-w-5xl mx-auto px-6 py-8">
                {/* Tabs */}
                <div className="flex gap-4 mb-8 border-b border-gray-200">
                    <button
                        onClick={() => setActiveTab('text')}
                        className={`pb-3 flex items-center gap-2 text-sm font-medium transition-colors ${activeTab === 'text' ? 'border-b-2 border-[#00A3E0] text-[#00A3E0]' : 'text-gray-500 hover:text-gray-700'}`}
                    >
                        <FileText className="w-4 h-4" /> Content Generator
                    </button>
                    <button
                        onClick={() => setActiveTab('image')}
                        className={`pb-3 flex items-center gap-2 text-sm font-medium transition-colors ${activeTab === 'image' ? 'border-b-2 border-[#00A3E0] text-[#00A3E0]' : 'text-gray-500 hover:text-gray-700'}`}
                    >
                        <ImageIcon className="w-4 h-4" /> Visual Validator
                    </button>
                </div>

                {/* CONTENT GENERATOR UI */}
                {activeTab === 'text' && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Input Column */}
                        <div className="space-y-6">
                            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                                <h2 className="text-lg font-semibold mb-4">Briefing</h2>

                                <label className="block text-sm font-medium text-gray-700 mb-1">Content Type</label>
                                <select
                                    value={contentType}
                                    onChange={(e) => setContentType(e.target.value)}
                                    className="w-full mb-4 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#00A3E0] focus:outline-none"
                                >
                                    <option>LinkedIn Post</option>
                                    <option>Email</option>
                                    <option>Press Release</option>
                                    <option>Internal Memo</option>
                                </select>

                                <label className="block text-sm font-medium text-gray-700 mb-1">Topic</label>
                                <textarea
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    className="w-full h-32 mb-4 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#00A3E0] focus:outline-none"
                                    placeholder="e.g. Launch of new humidity sensor for Mars rover..."
                                />

                                <label className="block text-sm font-medium text-gray-700 mb-1">Tone Modifier</label>
                                <input
                                    type="text"
                                    value={tone}
                                    onChange={(e) => setTone(e.target.value)}
                                    className="w-full mb-6 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#00A3E0] focus:outline-none"
                                />

                                <button
                                    onClick={handleGenerate}
                                    disabled={loading || !topic}
                                    className="w-full bg-[#00A3E0] hover:bg-[#0089bd] text-white font-semibold py-2 px-4 rounded-md transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
                                >
                                    {loading ? <Loader2 className="animate-spin w-4 h-4" /> : "Generate Draft"}
                                </button>
                            </div>
                        </div>

                        {/* Output Column */}
                        <div className="space-y-6">
                            {textResult ? (
                                <div className="space-y-4">
                                    {/* Score Card */}
                                    <div className={`p-4 rounded-lg border flex items-start gap-3 ${textResult.brand_score >= 80 ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'}`}>
                                        <div className={`text-2xl font-bold ${textResult.brand_score >= 80 ? 'text-green-700' : 'text-yellow-700'}`}>
                                            {textResult.brand_score}
                                        </div>
                                        <div>
                                            <h3 className={`font-semibold ${textResult.brand_score >= 80 ? 'text-green-800' : 'text-yellow-800'}`}>Brand Compliance Score</h3>
                                            <p className={`text-sm ${textResult.brand_score >= 80 ? 'text-green-700' : 'text-yellow-700'}`}>{textResult.reasoning}</p>
                                        </div>
                                    </div>

                                    {/* Content */}
                                    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                                        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Generated Draft</h3>
                                        <div className="prose prose-sm max-w-none text-gray-800 whitespace-pre-wrap">
                                            {textResult.content}
                                        </div>
                                    </div>

                                    {/* RAG References */}
                                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                                        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 flex items-center gap-2">
                                            Based on Approved Copy
                                        </h3>
                                        <div className="space-y-2">
                                            {textResult.used_references.map((ref, idx) => (
                                                <div key={idx} className="text-xs text-gray-500 italic border-l-2 border-gray-300 pl-2">
                                                    "{ref}"
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="h-full flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 rounded-lg p-12">
                                    <ShieldCheck className="w-12 h-12 mb-2 opacity-20" />
                                    <p>Enter a topic to generate brand-compliant copy.</p>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* IMAGE VALIDATOR UI */}
                {activeTab === 'image' && (
                    <div className="max-w-2xl mx-auto">
                        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm space-y-6">
                            <h2 className="text-lg font-semibold">Visual Compliance Check</h2>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={imgUrl}
                                    onChange={(e) => setImgUrl(e.target.value)}
                                    placeholder="https://example.com/image.jpg"
                                    className="flex-1 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#00A3E0] focus:outline-none"
                                />
                                <button
                                    onClick={handleValidateImage}
                                    disabled={loading || !imgUrl}
                                    className="bg-gray-900 text-white px-4 rounded-md hover:bg-gray-800 disabled:opacity-50"
                                >
                                    {loading ? <Loader2 className="animate-spin w-4 h-4" /> : "Check"}
                                </button>
                            </div>

                            {imgResult && (
                                <div className={`mt-4 p-4 rounded-lg border ${imgResult.is_compliant ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                                    <div className="flex items-center gap-2 mb-2">
                                        {imgResult.is_compliant
                                            ? <ShieldCheck className="text-green-600 w-5 h-5" />
                                            : <AlertCircle className="text-red-600 w-5 h-5" />
                                        }
                                        <h3 className={`font-bold ${imgResult.is_compliant ? 'text-green-800' : 'text-red-800'}`}>
                                            {imgResult.is_compliant ? "Asset Approved" : "Brand Violation Detected"}
                                        </h3>
                                    </div>
                                    <p className={`text-sm mb-4 ${imgResult.is_compliant ? 'text-green-700' : 'text-red-700'}`}>
                                        {imgResult.violation_reason}
                                    </p>

                                    <div className="flex gap-2 items-center">
                                        <span className="text-xs font-bold text-gray-500 uppercase">Detected Palette:</span>
                                        {imgResult.dominant_colors.map((color, idx) => (
                                            <div key={idx} className="w-6 h-6 rounded-full border border-gray-200 shadow-sm" style={{ backgroundColor: color }} title={color}></div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;