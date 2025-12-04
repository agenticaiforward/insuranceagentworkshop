import React, { useState } from 'react';
import { ArrowRight, DollarSign, MapPin, User } from 'lucide-react';

const QuoteForm = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState({
        age: '',
        zip_code: '',
        coverage_amount: 100000,
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
                <div className="px-6 py-8 sm:p-10 bg-slate-50 border-b border-slate-100">
                    <h3 className="text-2xl font-bold text-primary text-center">
                        Get Your Personalized Quote
                    </h3>
                    <p className="mt-2 text-secondary text-center">
                        Tell us a bit about yourself to get started.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="px-6 py-8 sm:p-10 space-y-6">
                    <div>
                        <label htmlFor="age" className="block text-sm font-medium text-secondary mb-1">
                            Age
                        </label>
                        <div className="relative rounded-md shadow-sm">
                            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                <User className="h-5 w-5 text-slate-400" />
                            </div>
                            <input
                                type="number"
                                name="age"
                                id="age"
                                required
                                min="18"
                                max="100"
                                className="block w-full rounded-md border-slate-300 pl-10 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                placeholder="e.g. 30"
                                value={formData.age}
                                onChange={handleChange}
                            />
                        </div>
                    </div>

                    <div>
                        <label htmlFor="zip_code" className="block text-sm font-medium text-secondary mb-1">
                            Zip Code
                        </label>
                        <div className="relative rounded-md shadow-sm">
                            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                <MapPin className="h-5 w-5 text-slate-400" />
                            </div>
                            <input
                                type="text"
                                name="zip_code"
                                id="zip_code"
                                required
                                pattern="[0-9]{5}"
                                className="block w-full rounded-md border-slate-300 pl-10 focus:border-accent focus:ring-accent sm:text-sm py-3 border"
                                placeholder="e.g. 10001"
                                value={formData.zip_code}
                                onChange={handleChange}
                            />
                        </div>
                    </div>

                    <div>
                        <label htmlFor="coverage_amount" className="block text-sm font-medium text-secondary mb-1">
                            Desired Coverage Amount
                        </label>
                        <div className="relative rounded-md shadow-sm">
                            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                <DollarSign className="h-5 w-5 text-slate-400" />
                            </div>
                            <select
                                name="coverage_amount"
                                id="coverage_amount"
                                className="block w-full rounded-md border-slate-300 pl-10 focus:border-accent focus:ring-accent sm:text-sm py-3 border bg-white"
                                value={formData.coverage_amount}
                                onChange={handleChange}
                            >
                                <option value="50000">$50,000</option>
                                <option value="100000">$100,000</option>
                                <option value="250000">$250,000</option>
                                <option value="500000">$500,000</option>
                                <option value="1000000">$1,000,000</option>
                            </select>
                        </div>
                    </div>

                    <div className="pt-4">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            {isLoading ? (
                                <span className="flex items-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Calculating...
                                </span>
                            ) : (
                                <>
                                    Calculate Premium <ArrowRight className="ml-2 h-4 w-4" />
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default QuoteForm;
