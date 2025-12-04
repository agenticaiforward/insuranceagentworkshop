import React from 'react';
import { Shield, ArrowRight, CheckCircle } from 'lucide-react';

const HeroSection = ({ onGetQuote }) => {
    return (
        <div className="relative overflow-hidden bg-slate-50 pt-16 pb-32 lg:pt-24 lg:pb-40">
            <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="lg:grid lg:grid-cols-12 lg:gap-8">
                    <div className="sm:text-center md:mx-auto md:max-w-2xl lg:col-span-6 lg:text-left">
                        <h1>
                            <span className="block text-base font-semibold uppercase tracking-wide text-accent">
                                AI-Powered Protection
                            </span>
                            <span className="mt-1 block text-4xl font-extrabold tracking-tight text-primary sm:text-5xl xl:text-6xl">
                                <span className="block">Insurance made</span>
                                <span className="block text-accent">intelligent</span>
                            </span>
                        </h1>
                        <p className="mt-3 text-base text-secondary sm:mt-5 sm:text-xl lg:text-lg xl:text-xl">
                            Experience the future of insurance with our Agentic AI. Get a personalized quote in seconds, backed by data-driven precision and premium support.
                        </p>
                        <div className="mt-8 sm:mx-auto sm:max-w-lg sm:text-center lg:mx-0 lg:text-left">
                            <button
                                onClick={onGetQuote}
                                className="inline-flex items-center justify-center rounded-full border border-transparent bg-primary px-8 py-3 text-base font-medium text-white shadow-lg hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 transition-all duration-200"
                            >
                                Get Your Quote
                                <ArrowRight className="ml-2 -mr-1 h-5 w-5" />
                            </button>
                            <p className="mt-3 text-sm text-secondary">
                                No credit card required · Instant approval
                            </p>
                        </div>
                    </div>
                    <div className="relative mt-12 sm:mx-auto sm:max-w-lg lg:col-span-6 lg:mx-0 lg:mt-0 lg:flex lg:max-w-none lg:items-center">
                        <div className="relative mx-auto w-full rounded-lg shadow-lg lg:max-w-md">
                            <div className="relative block w-full overflow-hidden rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2">
                                <img
                                    className="w-full"
                                    src="https://images.unsplash.com/photo-1556742049-0cfed4f7a07d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
                                    alt="Team working on insurance"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-primary/60 to-transparent mix-blend-multiply" />
                                <div className="absolute bottom-0 left-0 p-6">
                                    <div className="flex items-center space-x-2 text-white">
                                        <Shield className="h-6 w-6 text-accent" />
                                        <span className="font-semibold">Enterprise Grade Security</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HeroSection;
