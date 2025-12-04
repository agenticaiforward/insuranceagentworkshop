import React from 'react';
import { Check, ShieldCheck, RefreshCw } from 'lucide-react';

const QuoteResult = ({ quote, onReset }) => {
    return (
        <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
                <div className="bg-primary px-6 py-8 sm:p-10 text-center">
                    <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-accent/20 mb-4">
                        <ShieldCheck className="h-10 w-10 text-accent" />
                    </div>
                    <h3 className="text-3xl font-bold text-white">
                        Quote Ready!
                    </h3>
                    <p className="mt-2 text-slate-300">
                        Reference ID: {quote.quote_id}
                    </p>
                </div>

                <div className="px-6 py-8 sm:p-10">
                    <div className="text-center mb-8">
                        <p className="text-sm font-medium text-secondary uppercase tracking-wide">Estimated Monthly Premium</p>
                        <div className="mt-2 flex items-baseline justify-center text-5xl font-extrabold text-primary">
                            ${quote.monthly_premium}
                            <span className="ml-1 text-2xl font-medium text-secondary">/mo</span>
                        </div>
                        <p className="mt-4 text-sm text-green-600 font-medium flex items-center justify-center">
                            <Check className="h-4 w-4 mr-1" /> Price guaranteed for 30 days
                        </p>
                    </div>

                    <div className="border-t border-slate-100 pt-8">
                        <h4 className="text-sm font-medium text-secondary mb-4">Your Coverage Includes:</h4>
                        <ul className="space-y-4">
                            <li className="flex items-start">
                                <div className="flex-shrink-0">
                                    <Check className="h-5 w-5 text-green-500" />
                                </div>
                                <p className="ml-3 text-sm text-secondary">
                                    <span className="font-medium text-primary">${quote.coverage_amount.toLocaleString()}</span> Death Benefit
                                </p>
                            </li>
                            <li className="flex items-start">
                                <div className="flex-shrink-0">
                                    <Check className="h-5 w-5 text-green-500" />
                                </div>
                                <p className="ml-3 text-sm text-secondary">
                                    Accelerated Death Benefit Rider
                                </p>
                            </li>
                            <li className="flex items-start">
                                <div className="flex-shrink-0">
                                    <Check className="h-5 w-5 text-green-500" />
                                </div>
                                <p className="ml-3 text-sm text-secondary">
                                    Terminal Illness Coverage
                                </p>
                            </li>
                        </ul>
                    </div>

                    <div className="mt-8">
                        <button
                            onClick={() => alert('Application flow would start here!')}
                            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-accent hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent transition-colors"
                        >
                            Proceed to Application
                        </button>
                        <button
                            onClick={onReset}
                            className="mt-4 w-full flex justify-center items-center py-2 px-4 border border-slate-300 rounded-md shadow-sm text-sm font-medium text-secondary bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
                        >
                            <RefreshCw className="mr-2 h-4 w-4" /> Start Over
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QuoteResult;
