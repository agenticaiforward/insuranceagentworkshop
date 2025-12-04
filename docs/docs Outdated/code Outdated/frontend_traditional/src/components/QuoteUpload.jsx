import React, { useState } from 'react';
import { UploadCloud, File, X, ArrowRight, CheckCircle } from 'lucide-react';

const QuoteUpload = ({ onSubmit, isLoading }) => {
    const [file, setFile] = useState(null);
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (file) {
            onSubmit(file);
        }
    };

    return (
        <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
                <div className="px-6 py-8 sm:p-10 bg-slate-50 border-b border-slate-100">
                    <h3 className="text-2xl font-bold text-primary text-center">
                        Upload Your Current Quote
                    </h3>
                    <p className="mt-2 text-secondary text-center">
                        We'll analyze your document and find you a better deal.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="px-6 py-8 sm:p-10 space-y-6">
                    <div
                        className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-colors ${dragActive ? "border-accent bg-blue-50" : "border-slate-300 hover:border-accent"
                            }`}
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                    >
                        <input
                            type="file"
                            id="file-upload"
                            className="hidden"
                            onChange={handleChange}
                            accept=".pdf,.png,.jpg,.jpeg"
                        />

                        {!file ? (
                            <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                                <UploadCloud className="h-12 w-12 text-slate-400 mb-4" />
                                <span className="text-lg font-medium text-primary">
                                    Drag and drop your file here
                                </span>
                                <span className="text-sm text-secondary mt-1">
                                    or click to browse (PDF, PNG, JPG)
                                </span>
                            </label>
                        ) : (
                            <div className="flex flex-col items-center">
                                <File className="h-12 w-12 text-accent mb-4" />
                                <span className="text-lg font-medium text-primary break-all">
                                    {file.name}
                                </span>
                                <button
                                    type="button"
                                    onClick={() => setFile(null)}
                                    className="mt-4 text-sm text-red-500 hover:text-red-700 font-medium flex items-center"
                                >
                                    <X className="h-4 w-4 mr-1" /> Remove file
                                </button>
                            </div>
                        )}
                    </div>

                    <div className="pt-4">
                        <button
                            type="submit"
                            disabled={!file || isLoading}
                            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            {isLoading ? (
                                <span className="flex items-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Analyzing Document...
                                </span>
                            ) : (
                                <>
                                    Analyze Quote <ArrowRight className="ml-2 h-4 w-4" />
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default QuoteUpload;
